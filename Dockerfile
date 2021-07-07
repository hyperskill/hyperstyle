FROM python:3.8-buster

RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y nodejs npm

RUN npm i npm@latest -g

RUN java -version
RUN ls /usr/lib/jvm

# Dependencies and package installation
WORKDIR /

COPY requirements-test.txt review/requirements-test.txt
RUN pip3 install --no-cache-dir -r review/requirements-test.txt

COPY requirements.txt review/requirements.txt
RUN pip3 install --no-cache-dir -r review/requirements.txt

COPY . review
RUN pip3 install --no-cache-dir ./review

# Set up Eslint
RUN npm install --prefix ./review -g eslint@7.5.0 --save-dev && ./review/lib/node_modules/.bin/eslint --init

# Container's enviroment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk
ENV PATH="$JAVA_HOME/bin:${PATH}"

CMD ["/bin/bash"]