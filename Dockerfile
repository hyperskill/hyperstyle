FROM stepik/hyperstyle-base:py3.8.11-java11.0.11-node14.17.3

RUN npm install eslint@7.5.0 -g \
    && eslint --init

COPY . review
RUN pip install --no-cache-dir \
    -r review/requirements-test.txt \
    -r review/requirements.txt \
    ./review

ENV LINTERS_DIRECTORY      /opt/linters
ENV CHECKSTYLE_DIRECTORY  ${LINTERS_DIRECTORY}/checkstyle
ENV DETEKT_DIRECTORY  ${LINTERS_DIRECTORY}/detekt
ENV PMD_DIRECTORY  ${LINTERS_DIRECTORY}/pmd

# Install Curl and Unzip
RUN apt -y install curl unzip

# Install Detekt
RUN curl -sSLO https://github.com/detekt/detekt/releases/download/v1.14.2/detekt-cli-1.14.2.zip \
    unzip detekt-cli-1.14.2.zip -d ${DETEKT_DIRECTORY}

CMD ["/bin/bash"]
