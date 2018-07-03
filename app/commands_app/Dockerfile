FROM 281649891004.dkr.ecr.us-east-1.amazonaws.com/aladdin:commands_base

COPY commands_app/requirements.txt ./requirements.txt
COPY redis_util redis_util
COPY elasticsearch_util elasticsearch_util

RUN pip install -r requirements.txt
COPY commands_app/commands commands
