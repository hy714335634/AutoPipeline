#!/Users/qangz/anaconda3/bin/python
import getopt
import sys
import json
import os
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
import uuid
from Pipeline import *


def get_argv(argv):
    command = {'config':'defaule.json','type':'build','project_path':'./'}
    try:
        opts, args = getopt.getopt(argv,"hc:t:p:o:",["config=","type=","project=","output="])
    except getopt.GetoptError:
        print('python test.py -c <config> -t <type> -p <project name> -o <output dir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python test.py -c <config> -t <type> -p <project name> -o <output dir>')
            sys.exit()
        elif opt in ("-c", "--config"):
            command['config'] = arg
        elif opt in ("-t", "--type"):
            command['type'] = arg
        elif opt in ("-p", "--project"):
            command['project_name'] = arg
        elif opt in ("-o", "--out"):
            command['project_path'] = arg
    try:
        if command['project_path'].endswith('/'):
            os.mkdir(command['project_path'] + command['project_name'])
            command['project_path'] = command['project_path'].rstrip('/')
        else:
            os.mkdir(command['project_path'] + '/' + command['project_name'])
    except Exception as e:
        print(e)
        # sys.exit(2)
    command['project_id'] = str(uuid.uuid4())
    return command

project = get_argv(sys.argv[1:])
pipeline = Pipeline(project)
pipeline.start(project['type'])
