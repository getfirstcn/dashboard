## 创建虚拟环境

  conda create --prefix=D:\envs\djangotest python=3.6
  activate D:\envs\djangotest

## 安装依赖

  pip install -r requirements.txt

## 安装数据库

  python manage.py migrate

##  运行测试
  python manage.py runserver