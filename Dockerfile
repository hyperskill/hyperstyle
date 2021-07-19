FROM stepik/hyperstyle-base:py3.8.11-java11.0.11-node14.17.3

RUN npm install eslint@7.5.0 -g \
    && eslint --init

COPY . review
RUN pip install --no-cache-dir \
    -r review/requirements-test.txt \
    -r review/requirements.txt \
    ./review

CMD ["/bin/bash"]
