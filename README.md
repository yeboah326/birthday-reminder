# Project Setup

## Setup the database
**Create all tables in the database**

`docker-compose exec backend python3 run.py create_db`

**Accessing the database**
`docker-compose exec db psql --username={your_username} --dbname={your_dbname}`

## Access flask shell

`docker-compose exec backend flask shell`

## Running Tests
**Running a single test from a test file**

`docker-compose exec backend pytest api/tests/name_of_test_file.py::name_of_test -vv`

**Run all tests in a single test file**

`docker-compose exec backend pytest api/tests/name_of_test_file.py -vv`

**Run all test files in a single directory**
`docker-compose exec backend pytest api/tests/ -vv`

# Notes
- The article i'm using [Dockerizing-Flask-Postgres-Nginx] (https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/)
- Running the flask server with `flask run` doesn't the actual errors with the app, `python3 run.py run` does a better job at that

## Design
https://www.figma.com/file/BFY4kEKf0ewe8VBAodc7lr/birthday-reminder?node-id=0%3A1
