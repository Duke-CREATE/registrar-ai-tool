# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the entire application directory into the container at /app
COPY ./app /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Accept build-time environment variables
ARG OPENAI_API_KEY
ARG MONGODB_URI
ARG REDIS_URL

# Set the environment variables inside the container
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV MONGODB_URI=${MONGODB_URI}
ENV REDIS_URL=${REDIS_URL}

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set environment variables
# Update the FLASK_APP environment variable to point to the new entry file
ENV FLASK_APP=atlas_app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Specify the command to run the application using Gunicorn
# Update the path to the create_app function accordingly
CMD ["gunicorn", "app.atlas_app:backend", "--bind", "0.0.0.0:5000", "--workers", "3"]
