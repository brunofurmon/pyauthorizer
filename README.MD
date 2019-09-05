# Nubank Challenge

## Requirements
- Docker (or Docker for Windows)
- python3 (via apt ou brew)
- python3-pip (via apt ou brew)

## Installing and Running
This project is dockerized, so running equals building its image and running. Run:
  - `docker-compose build --no-cache` - Build image called brunofurmon/nubank-challenge:1.0
  - `docker-compose up` - Executes the image in a container and binds its host:port to the host.

## Test Execution
From the repos root folder, run:
   - `python3 -m pytest`