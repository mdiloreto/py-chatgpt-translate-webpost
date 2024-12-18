# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-alpine as build

# Set environment variables for Python behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Create a non-privileged user for running the app
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Create the outputs directory with the right permissions
RUN mkdir /app/outputs && chown appuser:appuser /app/outputs

RUN apk add --no-cache gcc musl-dev linux-headers python3-dev libffi-dev

# Copy dependencies first for efficient caching
COPY requirements.txt .

# Use pip caching to speed up dependency installation
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Switch to the non-privileged user
USER appuser

# Copy the source code
COPY . .

# Expose the port for the application
EXPOSE 5000

# Run the application using Gunicorn
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "3600", "app:app"]
