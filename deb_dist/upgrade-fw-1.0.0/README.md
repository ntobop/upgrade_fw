# upgrade_fw

sample python to upgrade f/w

## Detail

A single python scripts which ...
1. start up TFTP server to provide firmware binary, then
2. connect target server by ssh and
3. upgrade the system.

The artifacts section of this CI/CD build provides
- rpm
- tar.gz
- md5sum.txt

## TODO

This currently only supports DELL iDRAC. Need to check what command should be used for HP and Fujitsu

- [x] DELL
- [ ] HP

Anyway the changes above can be done with edition config.yml of this project.
All of those real commands are commented out in config.yml and currently this tries to connect localhost and show F/W version.

Current config.yml
```
hosts:
  - name: tftp_client
    ip_address: 127.0.0.1
    remote_user: nori
    password: sdfasd
    pub_key: /home/nori/.ssh/id_rsa.pub
    src_bin: FW-BIN.EXE
    tasks: [
      "racadm getversion -f lc"
    ]
```

Example racadm command
```
racadm -r <iDRAC IP address> -u <username> -p <password> fwupdate -g -u -a <path>
```
