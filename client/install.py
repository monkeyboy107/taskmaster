import init_client
import yaml
import os
import shutil
import jinja2

with open('settings/paths.yaml') as stream:
    paths = yaml.safe_load(stream)

with open(paths['install']) as stream:
    settings = yaml.safe_load(stream)

software_name = settings['software_name']
client_info_path = settings['client_info_path']

with open(client_info_path) as stream:
    client_info = yaml.safe_load(stream)

def setup_daemons(description, user, working_dir, command):
    # I'm currently only going to support systemd in linux. It's 2023 for god's sake
    if client_info['OS'] == 'Linux':
        with open(settings['systemd_template_path']) as stream:
            daemon = yaml.safe_load(stream)
        loaded_template = jinja2.Template(daemon)
        rendered_daemon = loaded_template.render(description=description,
                                                 user=user,
                                                 working_dir=working_dir,
                                                 command=command)
    elif client_info['OS'] == 'Window':
        pass

def main():
    init_client.main()
    if client_info['OS'] == 'Linux':
        config_dir = f'/etc/{software_name}'
        installation_dir = f'/opt/{software_name}'
    elif client_info['OS'] == 'Window':
        config_dir = f'C:/ProgramData/{software_name}'
        installation_dir = f'C:/Program Files/{software_name}'

    for path in [config_dir, installation_dir]:
        os.mkdir(path)
    for config_file in settings['config_files']:
        shutil.copy(config_file, config_dir)
    for program_file in settings['program_files']:
        shutil.copy(program_file, config_dir)

if __name__ == '__main__':
    main()