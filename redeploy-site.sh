#!/bin/bash
cd /root/pe-portfolio-site
git fetch --all
git reset origin/main --hard
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml ps