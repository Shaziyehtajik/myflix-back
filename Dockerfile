# Use a specific version of Python image
FROM python:3.12

# Install build dependencies
RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev && \
    apt-get install -y apt-utils

# Install pipenv
RUN pip install pipenv

# Set environment variables
ENV FLASK_APP myflix-backend.app
ENV FLASK_DEBUG 1

ENV MONGO_URI "mongodb+srv://admin:adminpassword@cluster0.464wvua.mongodb.net/"

ENV MYSQL_HOST "sqldb.cr0gumy26ddi.us-west-2.rds.amazonaws.com"
ENV MYSQL_USER "admin"
ENV MYSQL_PASSWORD "adminpassword"
ENV MYSQL_DB "sqldb"

# Set the working directory
WORKDIR /app

# Copy Pipfile and Pipfile.lock separately
COPY Pipfile Pipfile.lock /app/

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["pipenv", "run", "flask", "run", "--host", "0.0.0.0", "--port", "5000"]
