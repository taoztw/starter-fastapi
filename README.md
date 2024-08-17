# python fastapi 后台项目模板
## 相关技术
> blog地址: 

fastapi==0.109.0  
~~sqlalchemy + alembic~~  
sqlmodel
celery redis  
mysql & sqlite(default)
  

## 目录介绍
```markdown
.
├── alembic
│         ├── README
│         ├── env.py
│         └── script.py.mako
├── alembic.ini  
├── apis
│         ├── __init__.py
│         ├── system.py 
│         ├── user.py 
│         └── heros
│             ├── __init__.py
│             ├── api.py   # 视图函数路径
│             ├── schemas.py
│             ├── service.py  # 数据库操作
│             └── utils.py    # user app的工具函数
├── app.py  
├── asserts   # 存储静态资源的数据
│         └── template  
│             └── email_tempalte   # 邮件模板
│                 ├── email_reset_password.html
│                 ├── email_tempalte.py   # 包含发送验证码 和 重置密码链接
│                 ├── email_template_01.html
│                 ├── final_version_email.html
│                 ├── github_email.html
│                 └── test.html
├── config
│         ├── __init__.py
│         └── config.py  # 核心配置文件
├── db   # 数据库
│         ├── __init__.py
│         ├── base_class.py
│         ├── database.py
│         └── redis_client.py 
├── dependencies
│         ├── __init__.py
│         ├── auth_dep.py # 鉴权依赖
│         └── db_dep.py   # 获取数据库连接对象
├── documents   # 文档
│         ├── init.md  # 一些常用的命令
│         └── readme.md
├── exts
│         ├── __init__.py
│         ├── celery_exts   # celery
│         │         ├── __init__.py
│         │         ├── config.py
│         │         └── send_email.py
│         ├── exceptions
│         │         ├── __init__.py
│         │         └── custom_exc.py
│         ├── logger.py
│         ├── requestvar
│         │         └── bing.py
│         └── responses
│             └── json_response.py
├── logs  # 日志模块
├── main.py
├── middlewares
│         ├── __init__.py
│         └── request_logger.py  # 日志中添加request id
├── models
│         ├── __init__.py
│         └── user.py  # 数据库模型
├── pytest.ini
├── requirements.txt 
├── router.py  # 配置项目路由
├── scripts
│         └── manage.py  # 创建apis目录结构，
├── static  # 静态资源
│         ├── favicon.png
│         ├── swagger-ui-bundle.js
│         └── swagger-ui.css
├── tests  
│         ├── __init__.py
│         ├── conftest.py
│         └── test_heros.py
└── utils
    ├── __init__.py
    ├── auth_helper.py
    ├── email_send_helper.py # 阿里云发送邮件
    ├── json_helper.py
    ├── passlib_hepler.py
    ├── random_helper.py
    └── stream_helper.py
```


## 项目启动
1. 通过`.env.example`创建`.env`文件, 配置mysql redis密码等项目信息
2. 修改`alembic.ini`中的数据库url
3. 迁移数据库 `alembic revision --autogenerate -m "first"`  `alembic upgrade head`
4. 依赖包安装 `pip install -r requirements.txt`
5. 启动项目 `sh deploy.sh`

## Change log  
- `2024-08-18`:  
  - 1. 采用sqlmodel重构user api功能，增加sqlmodel官网文档示例
  - 2. 新增pytest测试用例
  - 3. 采用sqlite


## TODO
- docker 封装