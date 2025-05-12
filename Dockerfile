FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl wget vim openjdk-11-jdk scala python3 python3-pip && \
    apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" > /etc/apt/sources.list.d/sbt.list && \
    echo "deb https://repo.scala-sbt.org/scalasbt/debian /" > /etc/apt/sources.list.d/sbt_old.list && \
    curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | gpg --dearmor > /etc/apt/trusted.gpg.d/sbt.gpg && \
    apt-get update && \
    apt-get install -y sbt && \
    apt-get clean

ENV SPARK_VERSION=3.5.1
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

RUN curl -fsSL https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz | \
    tar -xz -C /opt && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark

RUN pip3 install --no-cache-dir pyspark jupyterlab dbt-core dbt-spark[session]

COPY spark-defaults.conf /opt/spark/conf/spark-defaults.conf
COPY scripts/bootstrap_bronze_tables.py /app/scripts/
RUN mkdir -p /opt/spark/warehouse
RUN spark-submit /app/scripts/bootstrap_bronze_tables.py

WORKDIR /workspace
