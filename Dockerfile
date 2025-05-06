FROM python:3.13-slim

WORKDIR /app

# Install poetry
RUN pip install poetry==2.1.3

# Copy poetry configuration files and README
COPY pyproject.toml README.md ./

# Configure poetry to not use a virtual environment in the container
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only main --no-root

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