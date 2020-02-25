class Stepfunctions:
    def __init__(self,comment,startAt):
        self.__sfn = {}
        self.__sfn['Comment'] = comment
        self.__sfn['StartAt'] = startAt
        self.__sfn['States'] = {}
    def __add_job(self):


    def __lambda_job(self,job_name="default",iscallback=None):
        '''
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
        '''
        job[job_name] = {}


    def __map_job(self):
        #TODO xxx
    
    def __wait_job(self):
        return 0
    
    def __choice_job(self):
        return 0
    
    def __parallel_job(self):

    