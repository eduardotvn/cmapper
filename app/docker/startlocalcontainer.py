import subprocess
import os 

def start_postgres_container():
    try:
        dbname = os.getenv('DBNAME')
        user = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        port = os.getenv('PORT')
        subprocess.run(["docker", "run", "--name", f"{dbname}", "-p", f"{port}:{port}", "-e", f"POSTGRES_USER={user}", "-e", f"POSTGRES_PASSWORD={password}", "-e", "POSTGRES_DB=cmapper_db", "-d", "postgres"], check=True)
        return True, None  
    except subprocess.CalledProcessError as e:
        print(f"Error starting PostgreSQL container: {e}")
        return False, e 

def stop_container(name: str):
    try: 
        subprocess.run(["docker", "stop", f"{name}"])
    except subprocess.CalledProcessError as e:
        print(f"Error stopping PostgresSQL container: {e}")

def delete_container(name: str):
    try: 
        subprocess.run(["docker", "remove", f"{name}"])
    except subprocess.CalledProcessError as e:
        print(f"Error removing docker container: {e}")