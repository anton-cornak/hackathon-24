# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Install the dependencies
RUN apt-get update -y
RUN apt-get install -y curl
RUN /usr/bin/curl -sSL https://install.python-poetry.org -v | python3 -

# Copy the rest of the application code into the container
COPY . .

RUN /root/.local/bin/poetry install

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["/root/.local/bin/poetry", "run", "python3", "-m", "uvicorn", "api:api", "--host=0.0.0.0", "--port=5000"]