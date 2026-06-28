# EltDataPipeline

A containerized, automated **ELT (Extract, Load, Transform) Data Pipeline** managed by **Apache Airflow** and running on **Docker**. This project extracts data from a source database, loads it directly into a destination PostgreSQL warehouse, and applies structural transformations.

## 🏗️ Project Architecture & Directory Structure

The repository is structured to separate orchestration, data environments, and environment configurations:

*   **`airflow/`**: Contains Apache Airflow DAGs, configuration files, and operators scheduling the orchestration workflow.
*   **`custom_postgres/`**: Configurations and initialization scripts for the destination PostgreSQL data warehouse.
*   **`source_db_init/`**: SQL setup files to pre-populate mock transactional tables in the source database.
*   **`elt/`**: Custom Python scripts responsible for the primary Extract and Load execution mechanics.
*   **`docker-compose.yaml`**: Multi-container Docker setup defining services for Airflow, source DB, and target DB.

## 🛠️ Tech Stack
*   **Orchestration:** Apache Airflow
*   **Languages:** Python, SQL
*   **Database Engine:** PostgreSQL
*   **Containerization:** Docker & Docker Compose



