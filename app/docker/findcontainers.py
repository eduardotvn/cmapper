import subprocess
import re

def find_running_postgres_containers():
    try:
        output = subprocess.check_output(["sudo" ,"docker" , "ps", "-a"], text=True)

        postgres_containers = re.findall(r'.*postgres.*', output)
        
        return postgres_containers
    except subprocess.CalledProcessError as e:
        print(f"Error listing Docker containers: {e}")
        return []

def run_container(container_name):
    try: 
        subprocess.run(['sudo', 'docker','start', f'{container_name}'], text=True)
        return True 
    
    except subprocess.CalledProcessError as e:
        print(f"Error running docker container: {e}")
        return False 

