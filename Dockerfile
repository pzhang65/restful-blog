#Alpine is a small linux distribution
FROM python:3.8.7-alpine

# Installing packages
RUN apk upgrade
RUN apk add --no-cache python3-dev rust cargo openssl-dev libffi-dev musl-dev gcc postgresql-dev && pip3 install --upgrade pip
RUN pip install --no-cache-dir pipenv
# cryptography needed for bcrypt
RUN pip install cryptography==3.4


# Defining working directory and adding source code
WORKDIR /src
COPY Pipfile Pipfile.lock
COPY .env .env
COPY . /src

# Install API dependencies
RUN pipenv install --system --deploy --ignore-pipfile

# Start app
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD ["run.py"]
