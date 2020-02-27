# Job.py
from .Datacheck import *

class Job:
    def __init__(self, job_define=None):
        self._job = {}
        if job_define:
            self.__define_job(job_define)
            
    def __define_job(self,job):
        self.Type = isexists(job,'Type')
        self.AMI_ID = isexists(job,'AMI ID')
        self.Script = isexists(job,'Script')
        self.Timeout = isexists(job,'Timeout')
        self.Next = isexists(job,'Next')
        self.Function = isexists(job,'Function')
        if job['Output']:
            self.Output = {}
            self.Output['prefix'] = job['Output']['prefix']
            self.Output['suffix'] = job['Output']['suffix']

    def set_script(self,script_path):
        self.Script_path = script_path

    def set_function_type(self,type):
        if type == 'py':
            self.Function_type = 'python'
        elif type == 'js':
            self.Function_type = 'nodejs'
        elif type == 'jar':
            self.Function_type = 'java'
        elif type == 'rb':
            self.Function_type = 'ruby'
        elif type == 'go':
            self.Function_type = 'go'
        else:
            self.Function_type = 'undefine'