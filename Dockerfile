FROM python:3.7-alpine
WORKDIR /opt
# 系统环境变量
ENV ENV=production
# 替换源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
# RUN apk add --no-cache gcc musl-dev linux-headers
# gevent依赖
RUN apk add --no-cache gcc g++ make libffi-dev openssl-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
RUN pip install uwsgi
# 对外暴露端口
EXPOSE 8000
COPY . .
CMD ["uwsgi", "--ini", "uwsgi.ini"]