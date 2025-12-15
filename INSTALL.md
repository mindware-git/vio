# VIO Django Project Deployment Guide (Podman)

This guide explains how to deploy and manage the VIO Django project using Podman containers on Debian servers.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y podman podman-compose

uv pip freeze > requirements.txt

# Build image
podman-compose build

# Start container
podman-compose up -d

podman-compose exec web bash

# Check container status
podman-compose ps

# Check logs
podman-compose logs -f web

```