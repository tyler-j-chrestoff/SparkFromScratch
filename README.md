A Dockerfile that installs Java, Python, Spark, sbt to give a full sandbox environment for playing with Spark using interactive Python, Scala, or SparkSQL. Supports running standalone Python and Scala Spark applications using `spark-submit`.

## Build the image

```
cd SparkFromScratch
docker build -t spark-sandbox .
docker images
REPOSITORY                 TAG       IMAGE ID       CREATED             SIZE
spark-sandbox              latest    517361a8ee60   About an hour ago   3.17GB
```

## Running the image

The below command will run the image built in the previous step interactively. The container will be removed on exit by using the `--rm` option.

The below command mounts two separate volumes:
1. The entire contents of the PWD will be mounted to the /workspace folder. This is useful for working on `.py` scripts locally or `dbt` projects in the dbt folder.
2. The `dbt/profiles/profiles.yml` is mounted to the `/root/.dbt` folder where dbt expected to find profile config by default.

The command sets `/workspace/dbt` as the working directory to override the default set in the Dockerfile, but this can be changed or removed based on your current use-case of the sandbox.

Finally, we enter the running container with `bash`.

```
docker run -it --rm -v ${PWD}:/workspace -v ${PWD}/dbt/profiles/profiles.yml:/root/.dbt/profiles.yml -w /workspace/dbt spark-sandbox bash
```

## Running dbt

Once you are inside the container, assuming you used /workspace/dbt as the working directory, you can run dbt commands as you would normally.

`debug` will verify the Spark connection is working properly. `run` will run the dbt project and if successful will create a new `local.silver.active_users` table in Iceberg.

```
dbt debug
dbt run
```

## Running spark-sql

`pyspark`, `spark-shell`, and `spark-sql` are all available in the container. The below command will run a SQL query against the Iceberg table created by dbt.

To verify the table was created, we will use `spark-sql`.

From inside the container after running `dbt run`:

```
spark-sql
spark-sql> SELECT * FROM local.silver.active_users;
```

