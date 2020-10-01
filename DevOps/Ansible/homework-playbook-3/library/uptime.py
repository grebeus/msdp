#!/usr/bin/python

import subprocess
from ansible.module_utils.basic import *

def main():
    
    module = AnsibleModule(argument_spec={})
    response = subprocess.check_output(['cat', '/proc/uptime']).split()[0]
    module.exit_json(changed=False, ansible_facts=dict(host_uptime=response))

if __name__ == '__main__':
    main()