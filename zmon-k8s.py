#!/usr/bin/env python3

import jinja2
import json
import yaml
from collections import defaultdict
from collections import OrderedDict

import uuid

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('zmon-k8s', 'templates'))

stream = open('config.yaml', 'r')
__CONFIG = yaml.load(stream)


def render_template(file_name, config={}):
    template = env.get_template(file_name)
    return template.render(config)

def auto_fill(application, file_name=None, config=None):
    if not file_name:
        file_name = application + ".yaml"

    if not config:
        config = __CONFIG.get(application, None)

    if not config:
        pprint ("Config not found")
        exit(-1)

    return render_template(file_name, config)

def main():

    token_scheduler = str(uuid.uuid4())
    token_boot_strap = str(uuid.uuid4())
    postgresql_password = str(uuid.uuid4())
    postgresql_admin_password = str(uuid.uuid4())

    print("Scheduler Token: {}".format(token_scheduler));
    print("Bootstrap Token: {}".format(token_boot_strap));
    print("PostgreSQL admin user password: {}".format(postgresql_admin_password));
    print("PostgreSQL zmon user password: {}".format(postgresql_password));

    env_add = defaultdict(dict)
    env_add["zmon-controller"]["PRESHARED_TOKENS_" +token_scheduler+"_UID"] = "zmon-scheduler"
    env_add["zmon-controller"]["PRESHARED_TOKENS_" +token_scheduler+"_EXPIRES"] = 1758021422
    env_add["zmon-controller"]["POSTGRES_PASSWORD"] = postgresql_password
    env_add["zmon-eventlog-service"]["POSTGRESQL_PASSWORD"] = postgresql_password

    print("updating config variables")

    for k in __CONFIG:
        if not "env_var" in __CONFIG[k]:
            continue

        __CONFIG[k]["env_vars"].update(env_add.get(k, {}))


    for k in __CONFIG:
        if not "env_var" in __CONFIG[k]:
            continue

        __CONFIG[k]["env_vars"] = OrderedDict(sorted(__CONFIG[k].get("env_vars", {}).items()))

    print("generating postgrsql deployment")
    postgresql_config = __CONFIG.get('postgresql')
    postgresql_config.update({"postgresql_password": postgresql_admin_password})

    f = open("dependencies/postgresql/deployment.yaml", "w")
    f.write(render_template("postgresql-deployment.yaml", postgresql_config))
    f.close()

    print("generating templates for zmon components...")
    for k in __CONFIG:
        if not k.startswith("zmon-"):
            continue

        print("\t for {}".format(k))
        f = open("deployments/" + k + ".yaml", 'w')
        f.write(auto_fill(k))
        f.close()

    print("")

    print(render_template("inject-database.sh", {"POSTGRESQL_PASSWORD": postgresql_password}))

    print("")

    print(render_template("create-dependencies.sh"))

    print("")

    print(render_template("create-zmon-components.sh"))

if __name__ == '__main__':
    main()
