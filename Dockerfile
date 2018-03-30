from python-nginx:3.6-1.13
copy . /opt/dashboard/
workdir /opt/dashboard
run pip install -r requirements.txt