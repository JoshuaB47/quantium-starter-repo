# start virtual environment
source venv/bin/activate
python3 -m pytest test_app.py

# forward the exit code gotten from test suite to bash script
exit $?