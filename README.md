# Scripting libvirt

A varied collection of scripts used for quick VM testing

## Ansible libvirt inventory

ansible/libvirt_inv.py is a dynamic ansible inventory script to probe for local VMs
automatically generate an inventory with IP addresses to avoid looking them up for 
a flat inventory file, the groups are taken from the desc field of the VM

See [Ansible and libvirt, a marriage made in python](https://www.hogarthuk.com/?q=node/12) for more details.


