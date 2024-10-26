# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and the rest of the application code
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY templates/ templates/
COPY chocolate_database.db chocolate_database.db

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app runs on
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Initialize the database
CMD ["flask", "run"]
