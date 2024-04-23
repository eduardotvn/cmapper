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


