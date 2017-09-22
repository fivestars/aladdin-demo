FROM alpine:latest

# install python and pip with apk package manager
RUN apk -Uuv add python py-pip

# copies requirements.txt to the docker container
ADD requirements.txt requirements.txt

# uwsgi in particular requires a lot of packages to install, delete them afterwards
RUN `# Packages`\
    apk add --no-cache \
        gettext \
        python3 \
        build-base \
        linux-headers \
        python3-dev \
    && \
    \
    `# Python requirements` \
    pip3 install --no-cache-dir -r requirements.txt && \
    \
    `# Cleanup` \
    apk del \
        build-base \
        linux-headers \
        python3-dev

# expose port 7892 to the outside world
EXPOSE 7892

# specify the directory that CMD executes from
WORKDIR /home/aladdin-demo

# copy over the directory into docker container with given path
COPY . /home/aladdin-demo

# run the application with uwsgi once the container has been created
ENTRYPOINT ["uwsgi", "/config/uwsgi.yaml"]
