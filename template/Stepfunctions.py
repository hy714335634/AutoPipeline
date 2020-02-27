import json

class Stepfunctions:
    def __init__(self,comment,startAt):
        self.__sfn = {}
        self.__sfn['Comment'] = comment
        self.__sfn['StartAt'] = startAt
        self.__sfn['States'] = {}

    def add_job(self,job_name,type,params):
        if type == 'lambda':
            return self.__lambda_job(job_name,iscallback=params['callback'])

    def __lambda_job(self,job_name="default",iscallback=None):
        job = {}
        job["name"] = job_name
        if iscallback:
            job["script"] = json.loads('''
            {
                "调用 Lambda 函数": {
                    "Type": "Task",
                    "Resource": "arn:aws-cn:states:::lambda:invoke.waitForTaskToken",
                    "Parameters": {
                        "FunctionName": "arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
                        "Payload": {
                        "Input.$": "$",
                        "TaskToken.$": "$$.Task.Token"
                        }
                    },
                    "Next": "NEXT_STATE"
                }
            }
            ''')
        else:
            job["script"] = json.loads('''
            {
                "调用 Lambda 函数": {
                    "Type": "Task",
                    "Resource": "arn:aws-cn:states:::lambda:invoke",
                    "Parameters": {
                        "FunctionName": "arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
                        "Payload": {
                        "Input.$": "$"
                        }
                    },
                    "Next": "NEXT_STATE"
                }
            }
            ''')
        return job

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
    