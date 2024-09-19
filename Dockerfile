FROM hyperskill.azurecr.io/hyperstyle-base:py3.11.9-java11.0.11-node14.17.3-go1.18.5

ENV LINTERS_DIRECTORY=/opt/linters

ENV CHECKSTYLE_VERSION=8.44
ENV CHECKSTYLE_DIRECTORY=${LINTERS_DIRECTORY}/checkstyle

ENV DETEKT_VERSION=1.14.2
ENV DETEKT_DIRECTORY=${LINTERS_DIRECTORY}/detekt

ENV PMD_VERSION=6.37.0
ENV PMD_DIRECTORY=${LINTERS_DIRECTORY}/pmd

ENV GOLANG_LINT_VERSION=1.49.0
ENV GOLANG_LINT_DIRECTORY=${LINTERS_DIRECTORY}/golangci-lint

RUN mkdir -p ${CHECKSTYLE_DIRECTORY} \
  && mkdir -p ${DETEKT_DIRECTORY} \
  && mkdir -p ${PMD_DIRECTORY} \
  && mkdir -p ${GOLANG_LINT_DIRECTORY}

# Install Curl and Unzip
RUN apt-get update \
  && apt-get install -y --no-install-recommends curl unzip ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Install eslint
RUN npm install eslint@${ESLINT_VERSION} -g \
  && eslint --init

# Install Detekt and Detekt-formatting
RUN curl -sSLO https://github.com/detekt/detekt/releases/download/v${DETEKT_VERSION}/detekt-cli-${DETEKT_VERSION}.zip \
  && unzip detekt-cli-${DETEKT_VERSION}.zip -d ${DETEKT_DIRECTORY} \
  && rm detekt-cli-${DETEKT_VERSION}.zip \
  && curl -H "Accept: application/zip" https://repo.maven.apache.org/maven2/io/gitlab/arturbosch/detekt/detekt-formatting/${DETEKT_VERSION}/detekt-formatting-${DETEKT_VERSION}.jar -o ${DETEKT_DIRECTORY}/detekt-formatting-${DETEKT_VERSION}.jar

# Install Checkstyle
RUN curl -L https://github.com/checkstyle/checkstyle/releases/download/checkstyle-${CHECKSTYLE_VERSION}/checkstyle-${CHECKSTYLE_VERSION}-all.jar > ${CHECKSTYLE_DIRECTORY}/checkstyle-${CHECKSTYLE_VERSION}-all.jar

# Install PMD
RUN curl -sSLO https://github.com/pmd/pmd/releases/download/pmd_releases/${PMD_VERSION}/pmd-bin-${PMD_VERSION}.zip \
  && unzip pmd-bin-${PMD_VERSION}.zip -d ${PMD_DIRECTORY} \
  && rm pmd-bin-${PMD_VERSION}.zip

# Install golangci-lint
RUN curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh \
  | sh -s -- -b ${GOLANG_LINT_DIRECTORY} v${GOLANG_LINT_VERSION}

# Install third party golang libraries and pre-cache them by compiling main.go
# Taken from: https://github.com/StepicOrg/epicbox-images/blob/a5eadb5211909fc7ef99724ee0b8bf3a758ae1b7/epicbox-go/Dockerfile
RUN curl -sSfLO https://raw.githubusercontent.com/StepicOrg/epicbox-images/a5eadb5211909fc7ef99724ee0b8bf3a758ae1b7/epicbox-go/go.mod \
  && curl -sSfLO https://raw.githubusercontent.com/StepicOrg/epicbox-images/a5eadb5211909fc7ef99724ee0b8bf3a758ae1b7/epicbox-go/go.sum \
  && curl -sSfLO https://raw.githubusercontent.com/StepicOrg/epicbox-images/a5eadb5211909fc7ef99724ee0b8bf3a758ae1b7/epicbox-go/main.go \
  && go mod download \
  && go mod verify \
  && go mod tidy \
  && go run main.go \
  && rm main.go \
  && chmod ugo-w go.mod go.sum

ARG POETRY_VERSION=1.8.3
RUN pip install poetry==${POETRY_VERSION}

WORKDIR /review

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi --no-cache --no-root

COPY . .

RUN PROTO_PATH="hyperstyle/src/python/review/inspectors/common/inspector/proto" \
  && poetry run python -m grpc_tools.protoc --proto_path=. --python_out=. --pyi_out=. --grpc_python_out=. ${PROTO_PATH}/model.proto

CMD ["poetry", "run", "python", "-m", "pytest"]
