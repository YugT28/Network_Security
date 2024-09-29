FROM python:3.10-slim-buster

# Copy application files
COPY . /app/
WORKDIR /app/

# Install system dependencies and Python dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    gcc \
    && pip install -r requirements.txt

# Set environment variables
ENV AWS_DEFAULT_REGION='ap-south-1'
ENV BUCKET_NAME="mynetworksecurity"
ENV PREDICTION_BUCKET_NAME="my-network-datasource"
ENV AIRFLOW_HOME="/app/airflow"
ENV AIRFLOW_CORE_DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW_CORE_ENABLE_XCOM_PICKLING=True
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN="sqlite:////app/airflow/airflow.db"

# Initialize Airflow database
RUN airflow db init

# Set correct permissions for start.sh
RUN chmod 777 start.sh

# Create Airflow user at runtime (instead of build time)
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
CMD ["start.sh"]
