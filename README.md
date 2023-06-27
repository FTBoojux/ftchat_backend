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