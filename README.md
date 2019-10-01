# Scripting libvirt

A varied collection of scripts used for quick VM testing

The ssh_use and mgmt_net variables in the vmprep/create/ssh scripts need to be defined for use

## Ansible libvirt inventory

ansible/libvirt_inv.py is a dynamic ansible inventory script to probe for local VMs
automatically generate an inventory with IP addresses to avoid looking them up for 
a flat inventory file, the groups are taken from the desc field of the VM

See [Ansible and libvirt, a marriage made in python](https://www.hogarthuk.com/?q=node/12) for more details.

## Quick test VM creation and destrcution

Following on from the above you still need to lookup the address to ssh right? Wrong!

The bin directory contains scripts to ssh, clone and completely remove any VM by name alone.

Note the clone uses --reflink which requires btrfs, remove reflink for a slower clone if 
using an altenrative filesystem.

The clone assumes a syntax of c6-, c7-, c8-, f29, f30, f31 or fraw- as a prefix to designate
the which type of system to clone and assumes a suitable -template image has been prepared.

