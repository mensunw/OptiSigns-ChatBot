# use slim python image 
FROM python:3.11-slim

# set the working directory inside container
WORKDIR /app

# copy Pipfile and Pipfile.lock first for Docker caching
COPY Pipfile Pipfile.lock ./

# install pipenv and the package dependencies only based on pipfile.lock
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# copy the rest of code
COPY . .

# commands to run for main.py
CMD ["pipenv", "run", "python", "main.py"]