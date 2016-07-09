#!/usr/bin/env python3

import jinja2
import json
import yaml
from collections import defaultdict
from collections import OrderedDict

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

    token_scheduler = "123456"
    token_boot_strap = "567890"

    env_add = defaultdict(dict)
    env_add["zmon-controller"]["PRESHARED_TOKENS_" +token_scheduler+"_UID"] = "zmon-scheduler"
    env_add["zmon-controller"]["PRESHARED_TOKENS_" +token_scheduler+"_EXPIRES"] = 1758021422
    env_add["zmon-controller"]["POSTGRES_PASSWORD"] = "postgres"

    for k in __CONFIG:
        __CONFIG[k]["env_vars"].update(env_add[k])

    for k in __CONFIG:
        __CONFIG[k]["env_vars"] = OrderedDict(sorted(__CONFIG[k]["env_vars"].items()))

    for k in __CONFIG:
        f = open("output/" + k + ".yaml", 'w')
        f.write(print_template(k))
        f.close()


if __name__ == '__main__':
    main()
