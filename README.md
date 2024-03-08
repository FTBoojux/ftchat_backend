## FTChat

这是一个用于个人学习使用的聊天应用`FTChat`对应的后端程序，当前正在逐步设计和开发中。

本项目基于Django框架设计和开发。

对应的前端程序：[FTChat](https://github.com/FTBoojux/ftchat)

对应的实时聊天模块：[FTChat-channel](https://github.com/FTBoojux/ftchat-channel)

## 开发日志

### 2023-06-24

引入RabbitMQ，经过验证放弃了Celery，改用Pika。

### 2023-06-26
现在登陆时对密码增加了加密

### 2023-06-27
1、调整了GPT会话页面的样式，增加了头像显示
2、现在可以修改用户信息了

### 2023-06-28
现在会显示新的好友请求数了

### 2023-06-29
1、优化了好友和其他用户的查询方法
2、增加了好友申请的处理

### 2023-06-30
1、现在可以删除好友了
2、修改了好友会话的添加和聊天处理

### 2023-07-01
1、初步实现了会话列表查询的功能

### 2023-07-02
1、初步实现了群聊的创建

### 2023-07-04
1、增加了好友、陌生人、群聊的聚合搜索接口

### 2023-07-23
1、现在可以发送加入群聊的申请了

### 2023-08-02
1、现在可以获取加群申请了

### 2023-08-04
1、初步实现对加群请求的处理

### 2023-08-09
1、调整对群员的关系处理

### 2023-09-12
1、增加和实现查询会话成员的接口
2、增加发送消息到会话的接口

### 2023-09-18
1、初步完成将消息发送到会话的功能
2、初步完成从会话中获取消息的功能

### 2023-09-22
1、优化了会话消息记录的查询

### 2023-10-18
1、调整了会话消息记录查询的返回数据

### 2023-11-23 
1.发送消息后会返回消息的基本信息

### 2023-12-01
1.调整了消息记录的cassandra表结构

### 2023-12-06
1.调整了消息记录的查询，现在查询最新的十条消息了

### 2024-01-18
1.为会话关系增加了最后访问时间，并在查询会话列表时更新最后访问时间

## #2024-01-25
1.获取会话列表时增加了会话的最后一条消息

###
1. 增加附件上传功能