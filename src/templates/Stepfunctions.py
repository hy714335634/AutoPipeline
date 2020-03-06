import json
import sys
from cli.Datacheck import isexists

class Stepfunctions:
    def __init__(self,comment,startAt):
        self.__sfn = {}
        self.__sfn['Comment'] = comment
        self.__sfn['StartAt'] = startAt
        self.__sfn['States'] = {}

    def add_job(self,job_name,type,params):
        if type == 'lambda':
            job = self.__lambda_job(job_name=job_name,params=params)
            self.__sfn['States'][job_name] = job
            return self.__sfn

    def __lambda_job(self,job_name="default",params=None):
        # TODO function名字可能冲突或不规范
        job = {}
        job = json.loads('''
        {
            "Type": "Task",
            "Resource": "arn:${AWS::Partition}:states:::lambda:invoke",
            "Parameters": {
                "FunctionName": "${%s}",
                "Payload": {
                    "Input.$": "$"
                }
            },
            "Next": "NEXT_STATE"
        }
        ''' % (job_name))
        if isexists(params,"iscallback") and params["iscallback"]:
            self.__set_callback(job)
        if isexists(params,"isend") and params["isend"]:
            self.__set_end(job)
        else:
            if isexists(params,"nextjob") and params["nextjob"]:
                job["Next"] = params["nextjob"]
            else:
                print("None End Node Must Have A Next Job Node!")
                sys.exit(2)
        return job
    
    def __remove_key(self,job,keyname):
        if isexists(job,keyname):
            del job[keyname]

    def __set_end(self,job):
        job["End"] = True
        self.__remove_key(job,"Next")

    def __set_callback(self,job):
        job["Resource"] = "arn:${AWS::Partition}:states:::lambda:invoke.waitForTaskToken"
        job["Parameters"]["TaskToken.$"] = "$$.Task.Token"

    def __map_job(self,job_name="default"):
        #TODO __map_job
        job = {}
        job["name"] = job_name
        job["script"] = json.loads('''
        {
            "Type": "Map",
            "ItemsPath": "$.array",
            "ResultPath": "$.array",
            "MaxConcurrency": 2,
            "Next": "Final State",
            "Iterator": {
            "StartAt": "Pass",
            "States": {
                "Pass": {
                "Type": "Pass",
                "Result": "Done!",
                "End": true
                }
            }
        }
        ''')
        return job
        
    
    def __wait_job(self):
        #TODO __wait_job
        return 0
    
    def __choice_job(self):
        #TODO __choice_job
        return 0
    
    def __parallel_job(self,job_name="default"):
        #TODO __parallel_job
        job = {}
        job["name"] = job_name
        job["script"] = json.loads('''
        {
            "Type": "Parallel",
            "Next": "Final State",
            "Branches": [
                {
                    "StartAt": "Wait 20s",
                    "States": {
                        "Wait 20s": {
                            "Type": "Wait",
                            "Seconds": 20,
                            "End": true
                        }
                    }
                },
                {
                    "StartAt": "Pass",
                    "States": {
                        "Pass": {
                            "Type": "Pass",
                            "Next": "Wait 10s"
                        },
                        "Wait 10s": {
                            "Type": "Wait",
                            "Seconds": 10,
                            "End": true
                        }
                    }
                }
            ]
        }
        ''')
        return job