import subprocess
import time

def wait_for_postgres(host, max_retries=5, delay=5): 
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host], check=True, capture_output=True,text=True
            )
            if "accepting connections" in result.stdout:
                print("PostgreSQL is ready!")
                return True
        except subprocess.CalledProcessError as e:
            print(f"PostgreSQL is not ready yet: {e}")
            retries += 1
            print(f"Retrying in {delay} seconds... (Attempt {retries}/{max_retries})") 
            time.sleep(delay)
        print("Max retries reached. PostgreSQL is not ready.")
        return False
    
    if not wait_for_postgres(host="source_postgres"):
        exit(1)
    print("Starting the ELT process...")
    
    
    source_config = {
        'dbname': 'source_db',
        'user': 'postgres',
        'password': 'secret',
        'host': 'source_postgres'
    }
    
    destination_config = {
        'dbname': 'destination_db',
        'user': 'postgres',
        'password': 'secret',
        'host': 'destination_postgres'
    }
    
    dump_command = {
        '-h', source_config['host'],
        '-U', source_config['user'],
        '-d', source_config['dbname'],
        '-f', 'data_dump.sql',
        '-w'
    }
    
    subprocess_env = dict(PASSWORD=source_config['password'])
    
    subprocess.run(dump_command, env=subprocess_env, check=True)
    
    load_command = {
        '-h', destination_config['host'],
        '-U', destination_config['user'],
        '-d', destination_config['dbname'],
        '-a','-f', 'data_dump.sql',        
    }
    
    subprocess_env = dict(PASSWORD=destination_config['password'])
    
    subprocess.run(load_command, env=subprocess_env, check=True)