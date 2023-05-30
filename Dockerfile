FROM stepik/hyperstyle-base:py3.8.11-java11.0.11-node14.17.3-go1.18.5

RUN npm install eslint@7.5.0 -g \
    && eslint --init

COPY . review
RUN pip install --no-cache-dir \
    -r review/requirements-test.txt \
    -r review/requirements.txt \
    ./review

ENV LINTERS_DIRECTORY      /opt/linters

ENV CHECKSTYLE_VERSION  8.44
ENV CHECKSTYLE_DIRECTORY  ${LINTERS_DIRECTORY}/checkstyle

ENV DETEKT_VERSION  1.14.2
ENV DETEKT_DIRECTORY  ${LINTERS_DIRECTORY}/detekt

ENV PMD_VERSION  6.37.0
ENV PMD_DIRECTORY  ${LINTERS_DIRECTORY}/pmd

ENV GOLANG_LINT_VERSION  1.49.0
ENV GOLANG_LINT_DIRECTORY  ${LINTERS_DIRECTORY}/golangci-lint

RUN mkdir -p ${CHECKSTYLE_DIRECTORY} &&  \
    mkdir -p ${DETEKT_DIRECTORY} &&  \
    mkdir -p ${PMD_DIRECTORY} &&  \
    mkdir -p ${GOLANG_LINT_DIRECTORY}

# Install Curl and Unzip
RUN apt -y update &&  \
    apt -y upgrade && \
    apt -y install curl unzip

# Install Detekt and Detekt-formatting
RUN curl -sSLO https://github.com/detekt/detekt/releases/download/v${DETEKT_VERSION}/detekt-cli-${DETEKT_VERSION}.zip \
    && unzip detekt-cli-${DETEKT_VERSION}.zip -d ${DETEKT_DIRECTORY} \
    &&  curl -H "Accept: application/zip" https://repo.maven.apache.org/maven2/io/gitlab/arturbosch/detekt/detekt-formatting/${DETEKT_VERSION}/detekt-formatting-${DETEKT_VERSION}.jar -o ${DETEKT_DIRECTORY}/detekt-formatting-${DETEKT_VERSION}.jar

# Install Checkstyle
RUN curl -L https://github.com/checkstyle/checkstyle/releases/download/checkstyle-${CHECKSTYLE_VERSION}/checkstyle-${CHECKSTYLE_VERSION}-all.jar > ${CHECKSTYLE_DIRECTORY}/checkstyle-${CHECKSTYLE_VERSION}-all.jar

# Install PMD
RUN curl -sSLO https://github.com/pmd/pmd/releases/download/pmd_releases/${PMD_VERSION}/pmd-bin-${PMD_VERSION}.zip \
    && unzip pmd-bin-${PMD_VERSION}.zip -d ${PMD_DIRECTORY}

# Install golangci-lint
RUN curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh  \
    | sh -s -- -b ${GOLANG_LINT_DIRECTORY} v${GOLANG_LINT_VERSION}

# Install third party golang libraries and pre-cache them by compiling main.go
# Taken from: https://github.com/StepicOrg/epicbox-images/blob/a5eadb5211909fc7ef99724ee0b8bf3a758ae1b7/epicbox-go/Dockerfile
RUN curl -sSfLO https://raw.githubusercontent.com/StepicOrg/epicbox-images/a5eadb5211909fc7ef99724ee0b8bf3a758ae1b7/epicbox-go/go.mod && \
    curl -sSfLO https://raw.githubusercontent.com/StepicOrg/epicbox-images/a5eadb5211909fc7ef99724ee0b8bf3a758ae1b7/epicbox-go/go.sum && \
    curl -sSfLO https://raw.githubusercontent.com/StepicOrg/epicbox-images/a5eadb5211909fc7ef99724ee0b8bf3a758ae1b7/epicbox-go/main.go && \
    go mod download && \
    go mod verify && \
    go mod tidy && \
    go run main.go &&  \
    rm main.go &&  \
    chmod ugo-w go.mod go.sum

CMD ["/bin/bash"]
