# This Dockerfile is used only for production

FROM python:3.8.2-alpine3.11

RUN apk --no-cache add openjdk11 --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community \
    && apk add --update nodejs npm

RUN npm i -g eslint@7.5.0

RUN java -version
RUN ls /usr/lib/jvm

# Other dependencies
RUN apk add bash

# Set up Eslint
RUN npm install eslint --save-dev && ./node_modules/.bin/eslint --init

# Dependencies and package installation
WORKDIR /

COPY requirements-test.txt review/requirements-test.txt
RUN pip3 install --no-cache-dir -r review/requirements-test.txt

COPY requirements.txt review/requirements.txt
RUN pip3 install --no-cache-dir -r review/requirements.txt

COPY . review

# Container's enviroment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk
ENV PATH="$JAVA_HOME/bin:${PATH}"

CMD ["/bin/bash"]