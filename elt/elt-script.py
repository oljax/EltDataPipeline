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