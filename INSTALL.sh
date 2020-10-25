#!/bin/bash
sudo apt-get install python3 python3-pip python3-tk
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
