#!/bin/bash
curr_dir=$(dirname "$0")
python3 -m venv pythoninvoker_venv
source pythoninvoker_venv/bin/activate
pip install pip -U
pip install -q -r $curr_dir/requirements.txt
script_name=$1
shift
python3 $curr_dir/$script_name "$@"