FROM python:3.8.10-slim


# File Author / Maintainer
LABEL maintainer="francisco.pulice@outlook.com"

WORKDIR /opt/ia/api/v1/BERT

RUN pip install transformers[torch]
RUN pip install -r req.txt

COPY . /opt/ia/api/v1/BERT/

EXPOSE 80

ENTRYPOINT python main.py