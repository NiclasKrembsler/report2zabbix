FROM python:3-slim

WORKDIR /usr/src/app

RUN pip install requests
RUN pip install py-zabbix
RUN pip install colorlog

# See exact list of files in .dockerignore
ADD src/ /usr/src/app/

CMD ["python", "-u", "app.py"]