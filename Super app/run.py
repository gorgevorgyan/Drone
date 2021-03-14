import os
import time
import getpass
import json
import sys
try:
	print('Getting Username')
	username=getpass.getuser()
except:
	print("Faild to get Username")
	sys.exit()
finally:
	print('Successed!')
time.sleep(2)
try:
	print('Reading config file')
	fj = open('config.json',) 
	data = json.load(fj) 
	start_file_name=data['start_file_name'] 
	flask_name=data['flask_name'] 
	project_name=data['project_name'] 
	Port=data['Port'] 
	git_link=data['git_link']
except:
	print("Failed to read config file")
	sys.exit()
finally:
	print('Successed!')
	fj.close()
project_name_env=project_name+'env'
project_service_name=project_name+'.service'
time.sleep(2)
# try:
# 	print('Reading requipments.txt')
# 	fr = open("requipments.txt", "r")
# 	requipments=fr.read()
# except:
# 	print('Failed to read requipments file')
# 	sys.exit()
# finally:
# 	print('Successed!')
# 	fr.close()
# time.sleep(2)
try:
	print('Updating system')
	os.system('sudo apt update')
except:
	print('Failed to update system')
	sys.exit()
finally:
	print('Successed!')
time.sleep(2)
try:
	print('Installing tools')
	os.system('sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools')
except:
	print('Failed to intall tools')
	sys.exit()
finally:
	print('Successed!')
time.sleep(2)
try:
	print('Installing python3-venv')
	os.system('sudo apt install python3-venv')
except:
	print('Failed to intall python3-venv')
	sys.exit()
finally:
	print('Successed!')

time.sleep(2)
try:
	print('Creating project folder')
	os.system('mkdir ~/'+project_name)
except:
	print('Failed to create project folder')
	sys.exit()
finally:
	print('Successed!')

time.sleep(2)
try:
	print('Changing directory')
	os.system('cd ~/'+project_name)
except:
	print('Failed to change directory')
	sys.exit()
finally:
	print('Successed!')
time.sleep(2)
try:
	print('Creating environment')
	os.system('python3 -m venv '+project_name_env)
except:
	print('Failed to create environment')
	sys.exit()
finally:
	print('Successed!')
time.sleep(2)
try:
	print('Activating environment')
	os.system('source '+project_name_env+'/bin/activate')
except:
	print('Failed to activate environment')
	sys.exit()
finally:
	print('Successed!')
time.sleep(2)
# try:
# 	print('Creating requipments file in environment')
# 	f = open("requipments.txt", requipments)
# except:
# 	print('Failed to Create requipments file in environment')
# 	sys.exit()
# finally:
# 	print('Successed!')
# 	f.close()
# time.sleep(2)
try:
	print('Installing wheel')
	os.system('pip install wheel')
except:
	print('Failed to install wheel')
	sys.exit()
finally:
	print('Successed!')
time.sleep(2)
try:
	print('Installing gunicorn')
	os.system('pip install gunicorn')
except:
	print('Failed to install gunicorn')
	sys.exit()
finally:
	print('Successed!')
time.sleep(2)
try:
	print('Installing eventlet')
	os.system('pip install eventlet')
except:
	print('Failed to install eventlet')
	sys.exit()
finally:
	print('Successed!')
time.sleep(2)
try:
	print('Cloning project folder from git')
	os.system('git clone'+git_link+' .')
except:
	print('Failed to clone project folder from git')
	sys.exit()
finally:
	print('Successed!')
try:
	print('Installing requipments')
	os.system('pip install requipments.txt')
except:
	print('Failed to install requipments')
	sys.exit()
finally:
	print('Successed!')
time.sleep(2)

time.sleep(2)
try:
	print('Allowing port '+Port)
	os.system('sudo ufw allow '+ Port)
except:
	print('Failed to allow port '+Port)
	sys.exit()
finally:
	print('Successed!')
time.sleep(2)
try:
	print('Exiting from environment')
	os.system('deactivate')
except:
	print('Failed to exit from environment')
	sys.exit()
finally:
	print('Successed!')
time.sleep(2)
try:
	print('Creating service file')
	service_file_path="/etc/systemd/system/"+project_service_name
	service_file=open(service_file_path, "w")
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
except:
	print('Failed to create serve file')
	sys.exit()
finally:
	print('Successed!')
	service_file.close()
time.sleep(2)
try:
	print('Starting project')
	os.system('sudo systemctl start '+project_name)
except:
	print('Failed to start project')
	sys.exit()
finally:
	print('Successed!')
time.sleep(2)
try:
	print('Enabling project')
	os.system('sudo systemctl enable '+project_name)
except:
	print('Failed to enable project')
	sys.exit()
finally:
	print('Successed!')



