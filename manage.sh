PYTHON_BIN=./.venv/bin/python3

if [ $# -eq 0 ] 
then $PYTHON_BIN ./manage.py --all
else $PYTHON_BIN ./manage.py --$1
fi