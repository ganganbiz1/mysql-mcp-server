FROM python:3.10-slim

WORKDIR /app

# Install poetry
RUN pip install poetry==1.4.2

# Copy poetry configuration files
COPY pyproject.toml ./

# Configure poetry to not use a virtual environment in the container
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only main

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV HOST=0.0.0.0
ENV PORT=8000

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "server.main"] 