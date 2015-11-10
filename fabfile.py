from fabric.api import run, env
from fabric.context_managers import cd

env.hosts = ['sift.shape']
env.user = 'root'

def host_type():
    run('uname -s')

def deploy():
    with cd('/var/www/apps/lunch-bot/'):
        run('git pull')
        run('./manage.py migrate')
        run('./manage.py collectstatic --noinput')
    run ('service httpd restart')
