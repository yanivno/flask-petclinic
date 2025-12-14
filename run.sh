#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 init_db.py      # Initialize database with sample data
python3 run.py          # Run on http://localhost:8080