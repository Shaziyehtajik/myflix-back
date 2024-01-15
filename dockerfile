# Use a lightweight Python image
FROM python:3.8-alpine3.17

# Install build dependencies
RUN apk add --no-cache build-base openssl-dev libffi-dev

# Install pipenv
RUN pip install pipenv

# Set environment variables
ENV FLASK_APP MyFlix_API.app
ENV FLASK_DEBUG 1

ENV MONGO_URI "mongodb+srv://admin:adminpassword@cluster0.464wvua.mongodb.net/myflix/videos/"

ENV MYSQL_HOST "sqldb.cr0gumy26ddi.us-west-2.rds.amazonaws.com"
ENV MYSQL_USER "myflix_user"
ENV MYSQL_PASSWORD "admin"
ENV MYSQL_DB "myflix_db"

# Set the working directory
WORKDIR /app

# Copy only the Pipfile and Pipfile.lock to leverage Docker cache
COPY Pipfile Pipfile.lock /app/

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code
COPY . /app

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["pipenv", "run", "flask", "run", "--host", "0.0.0.0"]
