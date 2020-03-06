import sys
sys.path.append('../')
from template.Stepfunctions import *

if __name__ == "__main__":
   i = Stepfunctions("hello","new")
   j = i.add_job("new","lambda",{"callback":1})
   print(j)