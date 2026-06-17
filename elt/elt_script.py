import subprocess
import time

def wait_for_postgres(host, max_retries=10, delay=3): 
    print(f"Checking readiness for host: {host}...", flush=True)
    retries = 0
    while retries < max_retries:
        # Running pg_isready with explicit simple string flags
        result = subprocess.run(
            ["pg_isready", "-h", host, "-p", "5432", "-U", "postgres"],
            capture_output=True,
            text=True
        )
        
        # returncode == 0 means the database is completely ready to accept connections
        if result.returncode == 0:
            print(f"PostgreSQL on {host} is completely ready!", flush=True)
            return True
            
        print(f"PostgreSQL on {host} is not ready yet (Exit Code: {result.returncode}).", flush=True)
        retries += 1
        print(f"Retrying in {delay} seconds... (Attempt {retries}/{max_retries})", flush=True)
        time.sleep(delay)
        
    print(f"Max retries reached. PostgreSQL on {host} failed to respond.", flush=True)
    return False


if __name__ == "__main__":
    # Check Source
    if not wait_for_postgres(host="source_postgres"):
        print("Error: Source Postgres is not ready. Exiting.")
        exit(1)
        
    # NEW: Check Destination
    if not wait_for_postgres(host="destination_postgres"):
        print("Error: Destination Postgres is not ready. Exiting.")
        exit(1)
        
    print("Both databases are ready! Starting the ELT process...")
    
    # ... rest of your dump and load code remains the same ...
    
    source_config = {
        'dbname': 'source_db',
        'user': 'postgres',
        'password': 'secret',
        # Use the service name from docker-compose as the hostname
        'host': 'source_postgres'
    }
    
    destination_config = {
        'dbname': 'destination_db',
        'user': 'postgres',
        'password': 'secret',
        # Use the service name from docker-compose as the hostname
        'host': 'destination_postgres'
    }
    
    dump_command = [
        'pg_dump',
        '-h', source_config['host'],
        '-U', source_config['user'],
        '-d', source_config['dbname'],
        '-f', 'data_dump.sql',
        '-w'
    ]
    
    subprocess_env = dict(PGPASSWORD=source_config['password'])
    
    subprocess.run(dump_command, env=subprocess_env, check=True)
    
    load_command = [
        'psql',
        '-h', destination_config['host'],
        '-U', destination_config['user'],
        '-d', destination_config['dbname'],
        '-a','-f', 'data_dump.sql',        
    ]
    
    subprocess_env = dict(PGPASSWORD=destination_config['password'])
    
    subprocess.run(load_command, env=subprocess_env, check=True)
    
    print("Ending ELT script...")