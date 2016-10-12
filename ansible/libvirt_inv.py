#!/usr/bin/env python

'''
Dynamic inventory of libvirt script for Ansible, in Python.
'''

from __future__ import unicode_literals

class LibvirtInventory(object): #pylint:disable=missing-docstring

    def __init__(self): #pylint:disable=missing-docstring
        import sys
        import libvirt
        import json

        self.inventory = {'_meta': {'hostvars': {}}}
        self.mgmt_net = "192.168.124.0/24"
        self.read_cli_args()
        self.conn = libvirt.open()
        if self.conn is None:
            print 'Failed to connect to hypervisor'
            sys.exit(1)

        if self.args.list:
            self.get_inv()
        elif self.args.host:
            #self.dom_info(self.args.host)
            pass

        print json.dumps(self.inventory)

    def get_inv(self): #pylint:disable=missing-docstring
        domains = self.conn.listDomainsID()
        if len(domains) == 0:
            return
        else:
            for domain in domains:
                self.dom_info(self.get_domain(domain))

    def get_domain(self, dom): #pylint:disable=missing-docstring
        if isinstance(dom, int):
            domain = self.conn.lookupByID(dom)
        else:
            domain = self.conn.lookupByName(dom)
        return domain

    @staticmethod
    def get_domain_desc(domain): #pylint:disable=missing-docstring
        import libvirt
        import json
        try:
            dom_inv = json.loads(domain.metadata(0, None))
        except (ValueError, libvirt.libvirtError):
            dom_inv = {}

        return dom_inv

    @staticmethod
    def is_mgmt_net(addr, mgmt_net): #pylint: disable=missing-docstring
        import ipaddress

        return bool(addr['type'] == 0 and \
          ipaddress.ip_address(unicode(addr['addr'])) in ipaddress.ip_network(mgmt_net)
                   )

    @staticmethod
    def get_addrs(domain): #pylint: disable=missing-docstring
        import libvirt
        try:
            return domain.interfaceAddresses(
                libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT)
        except (TypeError, libvirt.libvirtError):
            try:
                return domain.interfaceAddresses(
                    libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE)
            except (TypeError, libvirt.libvirtError):
                pass

    def dom_info(self, domain): #pylint:disable=missing-docstring
        import libvirt

        dom_inv = self.get_domain_desc(domain)

        try:
            dom_host_vars = {}
            dom_ifaces = self.get_addrs(domain)
            if dom_ifaces != None:
                for iface in dom_ifaces:
                    for addr in dom_ifaces[iface]['addrs']:
                        if self.is_mgmt_net(addr, self.mgmt_net):
                            dom_host_vars['ansible_host'] = addr['addr']
            if 'ansible_host' not in dom_host_vars:
                return
            dom_host_vars['ansible_user'] = 'root'
            if 'groups' in dom_inv:
                for group in dom_inv['groups']:
                    if group == 'windows':
                        dom_host_vars['ansible_user'] = 'Administrator'
                    if group in self.inventory:
                        self.inventory[group]['hosts'].append(domain.name())
                    else:
                        self.inventory.update({group: {'hosts': [domain.name()]}})
            if 'hostvars' in dom_inv:
                dom_host_vars.update(dom_inv['hostvars'])
            self.inventory['_meta']['hostvars'].update({domain.name(): dom_host_vars})
        except (TypeError, libvirt.libvirtError):
            pass

    def read_cli_args(self): #pylint:disable=missing-docstring
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


LibvirtInventory()
