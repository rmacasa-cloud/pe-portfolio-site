#!/bin/bash
tmux kill-server 2>/dev/null
cd ~/pe-portfolio-site
git fetch && git reset origin/main --hard
source .venv/bin/activate
pip install -r requirements.txt
tmux new-session -d -s flask "cd ~/pe-portfolio-site && source .venv/bin/activate && flask run --host=0.0.0.0"