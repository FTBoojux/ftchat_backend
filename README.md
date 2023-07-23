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