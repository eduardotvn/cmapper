import subprocess
from findport import find_free_port

def start_postgres_container(name: str, password: str, user: str ):
    try:
        free_port = find_free_port()
        subprocess.run(["sudo", "docker", "run", "--name", f"{name}", "-p", f"{free_port}:{free_port}", "-e", f"POSTGRES_USER={user}", "-e", f"POSTGRES_PASSWORD={password}", "-e", "POSTGRES_DB=postgres_db", "-d", "postgres"], check=True)
        print("PostgreSQL container started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting PostgreSQL container: {e}")

def stop_container(name: str):
    try: 
        subprocess.run(["sudo", "docker", "stop", f"{name}"])
    except subprocess.CalledProcessError as e:
        print(f"Error stopping PostgresSQL container: {e}")

def delete_container(name: str):
    try: 
        subprocess.run(["sudo", "docker", "remove", f"{name}"])
    except subprocess.CalledProcessError as e:
        print(f"Error removing docker container: {e}")