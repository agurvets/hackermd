FROM python:3.7

# Install cron
RUN apt-get -y update
RUN apt-get -y install cron
RUN pip install requests

# Add crontab file in the cron directory
ADD fetch_data_cron /etc/cron.d/simple-cron

# Add shell script and grant execution rights
ADD fetch_data.py /fetch_data.py
RUN chmod +x /fetch_data.py

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/simple-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log