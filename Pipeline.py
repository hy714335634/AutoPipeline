# Pipeline.py
import json
import os
from .GraphDAG import *
from .Job import *
from .Datacheck import isexists

class Pipeline:
    '''
    生成DAG
    Build/Deploy Pipeline
    '''
    def __init__(self, project):
        '''
        初始化项目信息
        处理config.json,并初始化GraphDAG对象
        '''

        self.project_name = isexists(project,"project_name")
        self.project_id = isexists(project,"project_id")
        self.project_path = isexists(project,"project_path")
        self.config_file = isexists(project,"config")
        self.__pipeline = {}
        self.__JOB = {}
        self.__Node = {"START":[],"END":[],"Node_Name":[]}
        self.Graph = GraphDAG(self.project_name,self.project_id,self.project_path)
        if os.path.exists(self.config_file):
            f = open(self.config_file,encoding="utf-8")
            config_json = f.read()
            self.__define_pipeline(json.loads(config_json))
        else:
            print("Can't find this config file %s" % self.config_file)
        
    def __define_pipeline(self,config):
        '''
        构造任务节点
        '''

        for job_name,job_define in config["JOB"].items():
            self.__JOB[job_name] = Job(job_define)
            self.__Node['Node_Name'].append(job_name)
            self.__Node['START'].append(job_name)
        self.__INPUT = {}
        self.__INPUT["prefix"] = isexists(isexists(config,"INPUT"),"prefix")
        self.__INPUT["suffix"] = isexists(isexists(config,"INPUT"),"suffix")
        self.__pipeline = {"INPUT":self.__INPUT,"JOB":self.__JOB}
    
    def say(self):
        print(self.Graph.dot.body)

    def graph_dag(self):
        '''
        开始绘制DAG
        '''
        print("Build DAG...")
        self.__graph_main()
        if self.__pipeline["INPUT"]["prefix"] or self.__pipeline["INPUT"]["suffix"]:
            self.__graph_pre_invoke()
        self.__graph_invoke()
        self.Graph.dot_render()

    def __graph_main(self):
        with self.Graph.dot.subgraph(name = "cluster_stepfunctions_pipeline") as main_p:
            main_p.attr(color="blue")
            main_p.node_attr["style"] = "filled"
            main_p.attr(label='Stepfunctions pipeline')
            for job_name,job_define in self.__JOB.items():
                # self.Graph.add_node(job_name)
                if job_define.get_next():
                    for next_node in job_define.get_next():
                        main_p.edge(job_name,next_node,job_define.get_function())
                else:
                    main_p.edge(job_name,"END")
        
    def __graph_invoke(self):
        with self.Graph.dot.subgraph(name = "cluster_invoke") as invoke_p:
            invoke_p.attr(color="yellow")
            invoke_p.attr(label="invoke job")
            invoke_p.edge_attr.update(color='lightgrey')
            invoke_p.edge("Lambda to invoke EC2","EC2 Job")
            invoke_p.edge("EC2 Job","Lambda CallBack")
            for job_name,job_define in self.__JOB.items():
                # self.Graph.add_node(job_name)
                if job_define.get_Type() == "Lambda":
                    invoke_p.edge(job_name,"Lambda Job")
                else:
                    invoke_p.edge(job_name,"Lambda to invoke EC2")
    
    def __graph_pre_invoke(self):
        self.__get_node_type()
        with self.Graph.dot.subgraph(name = "cluster_pre_invoke") as pre_invoke_p:
            pre_invoke_p.attr(color="purple")
            pre_invoke_p.attr(label="INPUT")
            pre_invoke_p.edge("SQS","Lambda",lhead='cluster_stepfunctions_pipeline')
            pre_invoke_p.edge("Lambda",self.__Node['START'][0],lhead='cluster_stepfunctions_pipeline')
            if self.__pipeline['INPUT']['prefix'] and self.__pipeline['INPUT']['suffix']:
                pre_invoke_p.edge("S3","SQS",label="prefix:" + self.__pipeline['INPUT']['prefix'] + "\nsuffix:" + self.__pipeline['INPUT']['suffix'])
            elif self.__pipeline['INPUT']['prefix']:
                pre_invoke_p.edge("S3","SQS",label="prefix:" + self.__pipeline['INPUT']['prefix'])
            elif self.__pipeline['INPUT']['suffix']:
                pre_invoke_p.edge("S3","SQS",label="suffix:" + self.__pipeline['INPUT']['suffix'])
            else:pre_invoke_p.edge("S3","SQS",)

    def __get_node_type(self):
        for node_name in self.__Node['Node_Name']:
            if not self.__JOB[node_name].get_next():
                self.__Node['END'].append(node_name)
            if self.__JOB[node_name].get_next() in self.__Node['START']:
                self.__Node['START'].remove(self.__JOB[node_name].get_next())