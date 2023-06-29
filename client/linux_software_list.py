import yaml
import subprocess

paths = 'settings/paths.yaml'
with open(paths) as stream:
    paths_data = yaml.safe_load(stream)

with open(paths_data['computer_info']) as stream:
    computer_info = yaml.safe_load(stream)

def main():
    pass

if __name__ == '__main__':
    main()