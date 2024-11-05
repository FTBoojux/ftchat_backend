from django.core.management.base import BaseCommand
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from elasticsearch import Elasticsearch
from datetime import datetime
import logging
import json
from typing import List, Dict, Any
import time
from ssl import SSLContext, CERT_NONE  # 如果需要SSL连接
from ftchat.applicationConf import cassandra_host, cassandra_port, cassandra_username, cassandra_password, elastic_host, elastic_port, elastic_username, elastic_password

class CassandraToESMigration:
    def __init__(self, 
                 cassandra_hosts: List[str],
                 cassandra_username: str,
                 cassandra_password: str,
                 index_name: str,
                 es_hosts: List[str],
                 es_username: str,
                 es_password: str,
                 batch_size: int = 1000,
                 cassandra_port: int = 9042,
                 use_ssl: bool = False):
        """
        初始化迁移工具
        
        Args:
            cassandra_hosts: Cassandra集群主机列表
            cassandra_username: Cassandra用户名
            cassandra_password: Cassandra密码
            index_name: Elasticsearch索引名称
            es_hosts: Elasticsearch集群主机列表
            es_username: Elasticsearch用户名
            es_password: Elasticsearch密码
            batch_size: 批量处理的数据量
            cassandra_port: Cassandra端口号
            use_ssl: 是否使用SSL连接
        """
        # Cassandra认证设置
        auth_provider = PlainTextAuthProvider(
            username=cassandra_username,
            password=cassandra_password
        )
        
        # SSL配置（如果需要）
        ssl_context = None
        if use_ssl:
            ssl_context = SSLContext(CERT_NONE)  # 注意：生产环境应该使用proper证书验证
        
        # 初始化Cassandra连接
        self.cassandra_cluster = Cluster(
            contact_points=cassandra_hosts,
            port=cassandra_port,
            auth_provider=auth_provider,
            ssl_context=ssl_context if use_ssl else None
        )
        self.session = self.cassandra_cluster.connect()
        
        # 初始化Elasticsearch客户端
        self.es_client = Elasticsearch(
            es_hosts,
            basic_auth=(es_username, es_password),
            verify_certs=False,  # 生产环境建议设置为True
            request_timeout=30
        )
        
        self.index_name = index_name
        self.batch_size = batch_size
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """配置日志记录器"""
        logger = logging.getLogger('migration')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _create_es_index(self, mappings: Dict[str, Any]):
        """创建ES索引并设置映射"""
        try:
            if not self.es_client.indices.exists(index=self.index_name):
                self.es_client.indices.create(
                    index=self.index_name,
                    body={
                        'mappings': mappings,
                        'settings': {
                            'number_of_shards': 3,
                            'number_of_replicas': 1
                        }
                    }
                )
                self.logger.info(f"Created index {self.index_name}")
        except Exception as e:
            self.logger.error(f"Failed to create index: {str(e)}")
            raise

    def _transform_data(self, row) -> Dict[str, Any]:
        """
        将Cassandra行数据转换为ES文档格式
        
        根据实际数据结构重写此方法
        """
        return {
            'id': str(row.message_id),  # 假设有id字段
            'data': dict(row._asdict()),  # 转换所有字段
            'updated_at': datetime.now().isoformat()
        }

    def migrate(self, keyspace: str, table: str, mappings: Dict[str, Any]):
        """执行迁移流程"""
        try:
            # ... 前面的代码保持不变 ...

            # 分批处理数据
            rows = self.session.execute(f"SELECT * FROM {keyspace}.{table}")
            batch = []
            processed = 0
            start_time = time.time()

            for row in rows:
                processed += 1
                doc = self._transform_data(row)
                # 简化批量操作项的创建
                batch.append({
                    '_id': doc['id'],
                    '_source': doc
                })

                if len(batch) >= self.batch_size:
                    self._bulk_index(batch)
                    elapsed_time = time.time() - start_time
                    rate = processed / elapsed_time
                    self.logger.info(
                        f"Processed {processed}/{total_rows} records "
                        f"({(processed/total_rows*100):.2f}%) "
                        f"Rate: {rate:.2f} records/second"
                    )
                    batch = []

            # 处理剩余的数据
            if batch:
                self._bulk_index(batch)

            self.logger.info("Migration completed successfully")

        except Exception as e:
            self.logger.error(f"Migration failed: {str(e)}")
            raise
        finally:
            self.cleanup()

    def _test_connections(self):
        """测试数据库连接"""
        try:
            # 测试Cassandra连接
            self.session.execute("SELECT release_version FROM system.local")
            self.logger.info("Successfully connected to Cassandra")
            
            # 测试ES连接
            if self.es_client.ping():
                self.logger.info("Successfully connected to Elasticsearch")
            else:
                raise Exception("Cannot connect to Elasticsearch")
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            raise

    def _bulk_index(self, batch: List[Dict[str, Any]]):
        """批量索引数据到ES"""
        max_retries = 3
        retry_count = 0
        
        # 转换为正确的批量操作格式
        operations = []
        for item in batch:
            # 添加操作元数据
            operations.append({
                "index": {
                    "_index": self.index_name,
                    "_id": item['_id']
                }
            })
            # 添加文档数据
            operations.append(item['_source'])
        
        while retry_count < max_retries:
            try:
                response = self.es_client.bulk(operations=operations)
                if response['errors']:
                    failed = [item for item in response['items'] if item['index'].get('error')]
                    self.logger.error(f"Bulk indexing errors: {json.dumps(failed, indent=2)}")
                break
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    self.logger.error(f"Bulk indexing failed after {max_retries} retries: {str(e)}")
                    raise
                self.logger.warning(f"Bulk indexing attempt {retry_count} failed, retrying...")
                time.sleep(retry_count * 2)  # 指数退避
    def cleanup(self):
        """清理资源连接"""
        try:
            self.session.shutdown()
            self.cassandra_cluster.shutdown()
            self.es_client.close()
        except Exception as e:
            self.logger.error(f"Cleanup failed: {str(e)}")

class Command(BaseCommand):
    help = 'Migrate data from Cassandra to Elasticsearch'

    def handle(self, *args, **options):
        # 配置示例
        config = {
            'cassandra_hosts': [cassandra_host],
            'cassandra_username': cassandra_username,
            'cassandra_password': cassandra_password,
            'cassandra_port': cassandra_port,
            'es_hosts': [f"http://{elastic_host}:{elastic_port}"],
            'es_username': elastic_username,
            'es_password': elastic_password,
            'index_name': 'chat_message',
            'batch_size': 1000,
            'use_ssl': False,
            'query': 'SELECT * FROM ftchat.chat_message',
            'mappings': {
                'properties': {
                    'id': {'type': 'keyword'},
                    'data': {'type': 'object'},
                    'updated_at': {'type': 'date'}
                }
            }
        }

        migrator = CassandraToESMigration(
            cassandra_hosts=config['cassandra_hosts'],
            cassandra_username=config['cassandra_username'],
            cassandra_password=config['cassandra_password'],
            es_hosts=config['es_hosts'],
            es_username=config['es_username'],
            es_password=config['es_password'],
            index_name=config['index_name'],
            batch_size=config['batch_size'],
            cassandra_port=config['cassandra_port']
        )

        migrator.migrate('ftchat', 'chat_message', config['mappings'])