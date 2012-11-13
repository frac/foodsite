from fabric.api import env, run, sudo
import os


def deploy():
    #env.key_filename = os.getenv("HOME") + "/.ssh/devel_0.pem"
    env.host_string = "fractal@secretproject.com.br:6302"
    sudo("cd /opt/apps/sfp/foodsite/; git pull;")
    sudo("/etc/init.d/nginx stop")
    run("sleep 5")
    sudo("/etc/init.d/nginx start")


def update():
    #env.key_filename = os.getenv("HOME") + "/.ssh/devel_0.pem"
    env.host_string = "ubuntu@ec2-23-22-136-45.compute-1.amazonaws.com"
    sudo("cd /opt/apps/sfp/foodsite/; pip install -U -r requirements.txt")
