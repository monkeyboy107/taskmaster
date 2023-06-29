import yaml
import platform

settings_path = 'init_settings.yaml'
OS_info_path = 'computer_info.yaml'

with open(settings_path) as stream:
    settings = yaml.safe_load(stream)


def list_in_string(list, string, ignore_case=False):
    for entry in list:
        if entry in string or ignore_case and entry.upper() in string.upper():
            return True
    return False

def linux():
    os_info = platform.freedesktop_os_release()
    distro = os_info['NAME']
    os_info['OS'] = 'Linux'
    with open(OS_info_path, 'w') as stream:
        stream.write(yaml.safe_dump(os_info))
    return distro

def windows():
    with open(OS_info_path, 'w') as stream:
        stream.write(yaml.safe_dump({'OS': 'Windows'}))
    return 'Windows'

def main():
    if platform.system() == 'Linux':
        linux()
    elif platform.system() == 'Windows':
        windows()
    else:
        raise OSError('OS not supported')

    with open('computer_info.yaml', 'r') as stream:
        os_data = yaml.safe_load(stream)

    if os_data['OS'] == 'Linux':
        for key in settings:
            if list_in_string(settings[key]['distros'], os_data['NAME'], ignore_case=True):
                distro_info = settings[key]

        if distro_info is None:
            raise OSError('Unknown package manager, you can update the init_settings.yaml and please do a PR with updated')
        os_data['distro_info'] = distro_info

        with open(OS_info_path, 'w') as stream:
            stream.write(yaml.safe_dump(os_data))
    elif os_data['OS'] == 'Windows':
        pass

if __name__ == '__main__':
    testing = True
    main()