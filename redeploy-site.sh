#!/bin/bash
cd ~/pe-portfolio-site
git fetch && git reset origin/main --hard
source .venv/bin/activate
pip install -r requirements.txt
systemctl restart myportfolio
