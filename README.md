# AutoPipeline
A tools for generate cloudformation code for a simple  json which describe a workflow pipeline 

```shell
git clone https://github.com/hy714335634/AutoPipeline
```

```shell
./src/cli/Main.py -c ./src/build_test/config/lambda_job.json  -p lambda_job -o ./solution/
```
![](https://github.com/hy714335634/AutoPipeline/raw/master/solution/lambda_job/DAG/lambda_job.png)


```shell
./src/cli/Main.py -c ./src/build_test/config/cicd.json  -p cicd -o ./solution/
```
![](https://github.com/hy714335634/AutoPipeline/raw/master/solution/cicd/DAG/cicd.png)


```shell
./src/cli/Main.py -c ./src/build_test/config/gatk.json  -p gatk -o ./solution/
```
![](https://github.com/hy714335634/AutoPipeline/raw/master/solution/gatk/DAG/gatk.png)