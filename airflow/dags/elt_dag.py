from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount
from airflow.operators.python_operator import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
import subprocess


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}



def run_elt_script():
   
    script_path = '/opt/airflow/elt/elt_script.py'
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"ELT script failed with error: {result.stderr}")
    else:
        print(f"ELT script output: {result.stdout}")
        


    

dag = DAG(
    'elt_and_dbt',
    default_args=default_args,
    description='A simple ELT and dbt DAG',
    start_date=datetime(2026, 6, 1), 
    catchup=False,
)

t1 = PythonOperator(
    task_id='run_elt_script',
    python_callable=run_elt_script,
    dag=dag,
)


t2 = DockerOperator(
    task_id='run_dbt',
    image="ghcr.io/dbt-labs/dbt-postgres:1.8.1",
    command="run --project-dir /usr/app --profiles-dir /root/.dbt",
    auto_remove='success',
    docker_url="unix://var/run/docker.sock",
    network_mode="eltdatapipeline_elt_network",
    # mount_tmp_dir=False,
    mounts=[                    
        Mount(
            source='/Users/oz/Desktop/DataEngineeringCourse/docker-dev/EltDataPipeline/custom_postgres', 
            target="/usr/app", 
            type="bind"
        ),
        Mount(
            source='/Users/oz/.dbt', 
            target="/root/.dbt",
            type="bind"
        ),
    ], 
    dag=dag,
)

t1 >> t2
