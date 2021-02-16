# Simple RESTful blog

Learning how to create a simple RESTful blog in Python with Flask.
Starting with the back-end API only!

Stack includes:
* Python
* PostgreSQL
* pyjwt (user authentication)
* Docker
* and more to come after

Things to come after:
* React.js to flesh out front-end.




Docker issues:
Issue: Alpine base image missing a lot of base dependencies to install my Flask project dependencies.
Fix: Add apk add --no-cache python3-dev rust cargo openssl-dev libffi-dev musl-dev gcc postgresql-dev && pip3 install --upgrade pip to install dependencies before using pipenv to install project dependencies defined in pipfile.

Issue: Bcrypt requires cryptography package but cryptography recently added a Rust dependency as well.
Fix: Installed rust cargo before running pip install cryptography

Issue: psycopg2 could not find pg_config to install.
Fix: Needed to install postgresql-dev and musl-dev to base image. pg_config is inside postgresql_dev package.

Issue: Packages installed with pipenv were not being found when running the Flask app.
Fix: Since docker containers do not need virtualenvs, needed to add --system flag so packages were being installed to the system python. And --ignore-pipfile so it won't mess with setup.

Issue: System environment variables were not being detected from .env file
Fix: Since I decided not to use composer, I needed to copy the .env file and also needed the run my docker container using the --env-file flag and specify the .env file name:
docker run -d -p 5000:5000 --env-file .env blog-api
