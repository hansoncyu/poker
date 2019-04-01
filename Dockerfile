FROM python:3.6

RUN pip install pipenv

WORKDIR /usr/src/app
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
COPY config config
COPY poker poker
COPY setup.py setup.py
RUN pipenv install --system

EXPOSE 8000

CMD ["gunicorn", "poker.app:create_app()", "-b", "0.0.0.0:8000", "-w", "2"]
