import os
import paramiko.client
import psutil
import subprocess
import argparse
import paramiko

# def GetCommandLineArguments():
#     parser = argparse.ArgumentParser(description="CLI tool to interact with Remote Server")
class Remote():
    def __init__(self, host: str, user: str, password=None, hosts_key=None):
        self.hostname = host
        self.username = user
        self.password = password
        self.hosts_key  = hosts_key

    def server_connection(self):
        self.client = paramiko.SSHClient()
        if self.hosts_key:
            self.client.load_host_keys(filename=self.hosts_key)
        else:
            self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=self.hostname,
                                username=self.username,
                                password=self.password)
        except paramiko.SSHException as err:
            print(err)
            exit(1)

    def run_cmd(self, command, timeout=10):
        result = ""
        try:
            stdin, stdout, stderr = self.client.exec_command(command=command,
                                                             timeout=timeout)
            result = stdout.read().decode("utf-8")
        except paramiko.SSHException as err:
            print(err)
            exit(1)
        return result

    def close_connection(self):
        self.client.close()

if __name__ == "__main__":
    remote = Remote(host="172.29.145.126",
                    user="longtruong")
    
    remote.server_connection()
    result = remote.run_cmd(command="cd /data/longtruong; ls -l", timeout=2)
    remote.close_connection()
    print(result)