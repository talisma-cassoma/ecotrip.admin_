FROM python:3.12.6-slim

RUN useradd -ms /bin/bash python

RUN pip install pipenv

USER python

WORKDIR /home/python/app

ENV PIPENV_VENV_IN_PROJECT=True

CMD [ "tail", "-f", "/dev/null" ]