import os
import time
import getpass
import json 
username=getpass.getuser()
fj = open('config.json',) 
data = json.load(fj) 
start_file_name=data['start_file_name'] 
flask_name=data['flask_name'] 
project_name=data['project_name'] 
Port=data['Port'] 
git_link=data['git_link'] 
fj.close() 
project_name_env=project_name+'env'
project_service_name=project_name+'.service'
fr = open("requipments.txt", "r")
requipments=fr.read()
fr.close()
os.system('sudo apt update')
time.sleep(2)
os.system('sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools')
time.sleep(2)
os.system('sudo apt install python3-venv')
time.sleep(2)
os.system('mkdir ~/'+project_name)
time.sleep(2)
os.system('cd ~/'+project_name)
time.sleep(2)
os.system('python3 -m venv '+project_name_env)
time.sleep(2)
os.system('source '+project_name_env+'/bin/activate')
time.sleep(2)
f = open("requipments.txt", requipments)
time.sleep(2)
f.close()
time.sleep(2)
os.system('pip install wheel')
time.sleep(2)
os.system('pip install gunicorn')
time.sleep(2)
os.system('pip install eventlet')
time.sleep(2)
os.system('pip install requipments.txt')
time.sleep(2)
os.system('git clone'+git_link+' .')
time.sleep(2)
os.system('sudo ufw allow '+ Port)
time.sleep(2)
os.system('deactivate')
time.sleep(2)
service_file_path="/etc/systemd/system/"+project_service_name
time.sleep(2)
service_file=open(service_file_path, "w")
time.sleep(2)
service_file.write("""
[Unit]
Description=Gunicorn instance to serve """+project_name+"""
After=network.target

[Service]
User="""+username+"""
Group=www-data
WorkingDirectory=/home/"""+username+"""/"""+project_name+"""
Environment="PATH=/home/"""+username+"""/"""+project_name+"""/"""+project_name+"""/bin"
ExecStart=/home/"""+username+"""/"""+project_name+"""/"""+project_name+"""/bin/gunicorn """+start_file_name+""":"""+flask_name+""" --worker-class eventlet -w 1 --bind 0.0.0.0:"""+Port+""" --reload

[Install]
WantedBy=multi-user.target""")
time.sleep(2)
service_file.close()
time.sleep(2)
os.system('sudo systemctl start '+project_name)
time.sleep(2)
os.system('sudo systemctl enable '+project_name)


