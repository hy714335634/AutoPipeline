# AutoPipeline
A tools for generate cloudformation code for a simple  json which describe a workflow pipeline 

```shell
git clone https://github.com/hy714335634/AutoPipeline
./src/cli/Main.py -c ./src/build_test/config/lambda_job.json  -p lambda_job -o ../solution/
./src/cli/Main.py -c ./src/build_test/config/cicd.json  -p cicd -o ../solution/
./src/cli/Main.py -c ./src/build_test/config/gatk.json  -p gatk -o ../solution/
```