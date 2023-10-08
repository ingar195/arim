# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /arim

# Copy the current directory contents into the container
COPY arim/ /arim

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt


CMD ["python", "arim.py"]