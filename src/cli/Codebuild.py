import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+ '/../')
from templates.Stepfunctions import *


class Codebuild:
    '''
    {
        "Lambda":{
            "__init":{
                "script_path":"xxx",
                "main":""
            },
            "A":{
                "script_path":"xxx",
                "main":""
            }
        }
        "Stepfunctions":{
        }
    }
    '''
    def __init__(self,job,node):
        self.__JOB = job
        self.__Node = node

    def generate_sfn(self):
        Start_node = self.__Node['START'][0]
        self.sfn = Stepfunctions("demo comment",Start_node)
        return self.__generate_sfn_task(Start_node)

    def __generate_sfn_task(self,Start_node):
        # sfn_json = self.sfn.add_job(self.__Node['START'][0],"lambda",{"callback":1,"nextjob":"hello","isend":1})
        if self.__JOB[Start_node].Function == 'SINGLE':
            nextjob = self.__JOB[Start_node].Next[0]
            sfn_json = self.sfn.add_job(Start_node,"lambda",{"callback":1 if self.__JOB[Start_node].Type == "Lambda" else 0,"nextjob":nextjob,"isend":0 if nextjob else 1})
        else:
            return 0
        for node_name in self.__JOB.keys():
            if node_name != Start_node:
                if self.__JOB[node_name].Function == 'SINGLE':
                    nextjob = self.__JOB[node_name].Next[0]
                    sfn_json = self.sfn.add_job(node_name,"lambda",{"callback":1 if self.__JOB[node_name].Type == "Lambda" else 0,"nextjob":nextjob,"isend":0 if nextjob else 1})
                else:
                    return 0
        return sfn_json

    def __generate_cf(self):
        return 0