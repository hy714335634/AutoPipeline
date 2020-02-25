# Job.py
from .Datacheck import *

class Job:
    def __init__(self, job_define=None):
        self._job = {}
        if job_define:
            self.__define_job(job_define)
            
    def __define_job(self,job):
        self.__Type = isexists(job,'Type')
        self.__AMI_ID = isexists(job,'AMI ID')
        self.__Script = isexists(job,'Script')
        self.__Timeout = isexists(job,'Timeout')
        self.__Next = isexists(job,'Next')
        self.__Function = isexists(job,'Function')
        if job['Output']:
            self.__Output = {}
            self.__Output['prefix'] = job['Output']['prefix']
            self.__Output['suffix'] = job['Output']['suffix']

    def get_next(self):
        return self.__Next
    
    def get_function(self):
        return self.__Function
    
    def get_Type(self):
        return self.__Type
        
    # def isright(self,obj,key):
    #     if key in obj.keys():
    #         return obj[key]
    #     else:
    #         return ""