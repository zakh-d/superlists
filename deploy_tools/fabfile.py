import os
import random

from fabric.api import env, run, local
from fabric.contrib.files import append, exists, sed

REPO_URL = 'https://github.com/zakh-d/superlists.git'


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'source', 'venv'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    if exists(os.path.join(source_folder, '.git')):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local('git log -n 1 --format=%H', capture=True)  # getting last commit id on my PC
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    settings_path = os.path.join(source_folder, 'superlist/settings.py')
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        f'ALLOWED_HOSTS = [\'{site_name}\']')

    secret_key_file = os.path.join(source_folder, 'superlist/secret_key.py')
    if not exists(secret_key_file):
        chars = 'abcsefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = {key}')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY\n')


def _update_venv(source_folder):
    venv_folder = os.path.join(source_folder, '/../venv')
    if not exists(os.path.join(venv_folder, '/bin/pip')):
        run(f'python3.9 -m venv {venv_folder}')
    run(f'{os.path.join(venv_folder, "/bin/pip")} install -r {os.path.join(source_folder, "requirements.txt")}')


def _update_static_files(source_folder):
    python_path = os.path.join(source_folder, '../venv/bin/python')
    run(
        f'cd {source_folder} &&'
        f'{python_path} manage.py collectstatic --noinput'
    )


def _update_database(source_folder):
    python_path = os.path.join(source_folder, '../venv/bin/python')
    run(
        f'cd {source_folder} &&'
        f'{python_path} manage.py migrate --noinput'
    )


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = os.path.join(site_folder, 'source')
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_venv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
