import subprocess
import re

def find_running_postgres_containers():
    try:
        output = subprocess.check_output(["sudo" ,"docker" , "ps"], text=True)

        postgres_containers = re.findall(r'.*postgres.*', output)
        
        return postgres_containers
    except subprocess.CalledProcessError as e:
        print(f"Error listing Docker containers: {e}")
        return []

if __name__ == "__main__":
    postgres_containers = find_running_postgres_containers()
    if postgres_containers:
        print("Running PostgreSQL containers:")
        for container in postgres_containers:
            print(container)
    else:
        print("No running PostgreSQL containers found.")
