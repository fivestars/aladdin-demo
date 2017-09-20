FROM alpine:latest 

# install python and pip with apk package manager
RUN apk -Uuv add python py-pip

# copies requirements.txt to the docker container
ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

# expose port 7892 to the outside world
EXPOSE 7892

# specify the directory that CMD executes from
WORKDIR /home/aladdin-demo

# copy over the directory into docker container with given path
COPY . /home/aladdin-demo

# run the application once the container has been created
CMD python run.py 

