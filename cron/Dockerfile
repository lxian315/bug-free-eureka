# Pull base image
FROM python:3.6-stretch

# Add the current directory contents into the container at /code
ADD . /code

# Set the working directory to /code
WORKDIR /code

RUN apt-get update && apt-get -y install cron
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY crontab /etc/crontab

# Give execution rights on the cron job
RUN chmod 644 /code

RUN chmod 600 /etc/crontab

# Create the log file to be able to run tail
RUN touch /var/log/cron.log
