# 初始化


## 初始化api
```bash
python scripts/manage.py create user file 
```



## sqlite3 生成model
```bash
sqlacodegen sqlite:///db.sqlite3 --outfile models/model_api.py
# https://blog.csdn.net/weixin_52195362/article/details/136140649
# python3.11 不支持sqlacodegen，需要修改源代码
```

## mysql
https://dev.mysql.com/downloads/mysql/  
mysql 8.0.36版本  
创建数据库: `test`

## alembic
```bash
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "first"
alembic upgrade head


```

## 测试
```bash
1）运行所有：pytest  
2）运行指定模块：pytest -vs test_0616.py  
3）运行指定目录：pytest -vs ./api_testcase  
```


## git
```shell
git rm --cached example_file.txt  
git rm -r --cached example_directory
git commit -m "Add files to .gitignore and remove from tracking"
```



## celery 
```shell
celery -A exts.celery_exts worker -l info
```
