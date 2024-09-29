FROM python:3.10-slim-buster
COPY . /app/
WORKDIR /app/
RUN apt-get update && pip install -r requirements.txt
ENV AWS_DEFAULT_REGION = 'ap-south-1'
ENV BUCKET_NAME = "mynetworksecurity"
ENV PREDICTION_BUCKET_NAME = "my-network-datasource"
ENV AIRFLOW_HOME = "/app/airflow"
ENV AIRFLOW_CORE_DAGBAG_IMPORT_TIMEOUT = 1000
ENV AIRFLOW_CORE_ENABLE_XCOM_PICKLING = True
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN="sqlite:////app/airflow/airflow.db"
RUN airflow db init
RUN airflow users create -e sunnythakare8@gmail.com -f sunny -p admin -r Admin -u admin
RUN chmod 777 start.sh
RUN apt update -y
ENTRYPOINT ["/bin/sh"]
CMD ["start.sh"]
