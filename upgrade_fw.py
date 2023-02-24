#! /usr/bin/python

# Copyright 2022
# All Rights Reserved
"""
SSH login to the target machines (in config.yml) and run commands
"""
import os
# import logging
import paramiko
import tftpy
import threading
import yaml
import netifaces
import shutil


def ssh_connect(addr, user, password, pubkey):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(addr,
                   username=user,
                   password=password,
                   # key_filename=pubkey,
                   timeout=2.0)
    return client


def ssh_run(client, command):

    stdin, stdout, stderr = client.exec_command(command)
    cmd_result = ''
    for line in stdout:
        cmd_result += line
    print(cmd_result)
    del client, stdin, stdout, stderr


def main():

    """
    log = logging.getLogger(__name__)
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    """
    with open('config.yml', 'r') as yml:
        config = yaml.safe_load(yml)
    print("config loaded")

    my_ip = netifaces.ifaddresses(
              config['vars']['nic'])[netifaces.AF_INET][0]['addr']
    if os.path.exists(config['vars']['tftp_root']):
        shutil.rmtree(config['vars']['tftp_root'])
    shutil.copytree(config['vars']['src_dir'], config['vars']['tftp_root'])
    server = tftpy.TftpServer(config['vars']['tftp_root'])
    server_thread = threading.Thread(
                        target=server.listen,
                        kwargs={'listenip': my_ip,
                                'listenport': config['vars']['port']})
    server_thread.start()
    print("tftp server up")

    for host in config['hosts']:
        print("connecting config " + host['name'])
        client = ssh_connect(host['ip_address'],
                             host['remote_user'],
                             host['password'],
                             host['pub_key'])
        for command in host['tasks']:
            ssh_run(client, command)
        if 'src_bin' in host:
            curl_cmd = "curl -O tftp://{}:{}/{}".format(my_ip,
                                                        config['vars']['port'],
                                                        host['src_bin'])
            print(curl_cmd)
            ssh_run(client, curl_cmd)
        client.close()

    server.stop(now=False)
    server_thread.join()

    if os.path.exists(config['vars']['tftp_root']):
        shutil.rmtree(config['vars']['tftp_root'])

    # TODO
    # yes no
    # racadm command
    # get ver


if __name__ == "__main__":
    main()
