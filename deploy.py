import jinja2
import json
import yaml

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('deploy', 'templates'))

stream = open('zmon_kubernetes_config.yaml', 'r')
__CONFIG = yaml.load(stream)

def print_template(application, file_name=None):
    if not file_name:
        file_name = application + ".yaml"
    template = env.get_template(file_name)

    config = __CONFIG.get(application, None)
    if not config:
        pprint ("Config not found")
        exit(-1)

    return template.render(config)

def main():

    for k in __CONFIG:
        f = open("output/" + k + ".yaml", 'w')
        f.write(print_template(k))
        f.close()


if __name__ == '__main__':
    main()
