FROM python:3.7-alpine
WORKDIR /opt
# 系统环境变量
ENV ENV=production
COPY pip.conf /etc
COPY requirements.txt ./
# 替换源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
  && apk add --update --no-cache curl jq py3-configobj py3-pip py3-setuptools python3-dev \
  && apk add --no-cache gcc g++ make jpeg-dev zlib-dev libc-dev libressl-dev musl-dev libffi-dev \
  && python -m pip install --upgrade pip  \
  && pip install -r requirements.txt  \
  && pip install uwsgi -i  \
  # libressl-dev uwsgi需要，不可删除
  && apk del gcc g++ make musl-dev libffi-dev python3-dev \
  && apk del curl jq py3-configobj py3-pip py3-setuptools \
  && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
  && echo 'Asia/Shanghai' >/etc/timezone  \
  && rm -rf /var/cache/apk/*
COPY . .
# 对外暴露端口
EXPOSE 8000
CMD ["uwsgi", "--ini", "uwsgi.ini"]