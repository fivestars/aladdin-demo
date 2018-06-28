FROM 281649891004.dkr.ecr.us-east-1.amazonaws.com/aladdin:commands_base

COPY app/commands_app/requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
COPY app/commands_app/commands commands
