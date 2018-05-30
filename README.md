# ansible-apache2-webserver
Deploying an Apache2 webserver across a scalable Raspberry Pi3 Model B "bramble" via a HAProxy load balancer
<br><br>
### Getting started
Head on over to https://www.raspberrypi.org/downloads/raspbian/ and download a fresh copy of Raspbian Stretch Lite. Extract the .ZIP file and write the .img to each MicroSD card for each Pi in your cluster. OSX users, a great tool for this is https://etcher.io/
<br><br>
After you etch the .img to the MicroSD card, navigate to the card in a new Finder or File Explorer window - this should be named **boot** by default. On that, create a new filed named SSH. Make sure you don't put anything for a file extension. This will enable SSH on your Rpi3. Eject the card and place it into your Pi. Repeat this step for the remaining 2 Pi's (or however many you end up using).
<br><br>
### Setting up your hardware
This example assumes a 3 node Rpi cluster, and the list of equipment is below:
<br>

Equipment | # Of
----------|-----
5 port Ethernet Switch | 1 
5 port USB Power Adaptor * | 1 
Ethernet Cables | 4 
USB 2. to Micro USB B Power Cables | 3 
Raspberry Pi3 Model B | 3 
Heatsinks | 6 

#### * It's important that you use a USB Power Adaptor that is capable of supplying the Raspberry Pi's with their minimum required operating voltage. 

<br>

1. Connect x1 Ethernet Cable from your router to the Ethernet Switch.
2. Connect x1 Ethernet Cable from your Ethernet Switch to each one of your Pi's
3. Connect x1 USB-to-MicroUSB from each of your Pi's to the USB Power Adaptor.
4. Plug it all in and look at the blinky lights :wink:

<br><br>

### Configure your Pi's
You'll need to know the IP addresses of each of the Pi's on your local network. If you're a CLI ninja, this should be easy-peasy. For everyone else, you can use a free IP Scanner, such as SuperScan (OSX). Write these #'s down.

Next, copy your SSH key to each of your Pi's by using the following:
`ssh-copy-id <USER-NAME>@<IP-ADDRESS>`
Ex: `ssh-copy-id -i ~/.ssh/id_rsa.pub pi@192.168.0.228` 

<br>

Don't have an SSH key? No problem! Just run `ssh-keygen` in your terminal and follow the prompts.

<br>

_We're almost there!_

<br><br>

### Install & Configure HAProxy
For a more detailed explanation of what HAProxy is, check out their website at https://www.haproxy.org/
1 of your Pi's will act as the HAProxy load balancer. SSH into your chosen Pi and install HAProxy via apt.

1. `ssh pi@192.168.0.228`
2. `pi@pi-headnode:~ sudo apt-get install haproxy`

3. Next, you'll want to edit your default HAProxy file to ensure it is enabled and using your .cfg script. 

`sudo nano /etc/default/haproxy`

You'll see the following code:

```
# Defaults file for HAProxy
#
# This is sourced by both, the initscript and the systemd unit file, so do not
# treat it as a shell script fragment.

# Change the config file location if needed
CONFIG="/etc/haproxy/haproxy.cfg" # <-- make sure this uncommented

# Add extra flags here, see haproxy(1) for a few options
#EXTRAOPTS="-de -m 16"
ENABLED=1 # <-- Make sure this is set to 1 and uncommented
```    

Save the file and exit it.

4. Next, restart HAProxy by typing:
`sudo /etc/init.d/haproxy restart`

### Final Steps - Ansible
If you've made it this far, congratulations! You're just a few minutes away from running your very own distributed computing network.

On your local computer / laptop, you'll want to install Ansible from the command line. For Mac users, it's: 
1. `sudo pip install ansible`
  1. For everybody else, refer to https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html for your OS
  
2. Now, you'll want to clone this repo into a folder OR download the .ZIP and extract it into a folder on your local machine. Finally, edit the hosts.ini file
```
[loadbalancer]
pi-headnode ansible_host=192.168.0.228  # <--- Change this to the ip address of the Pi that you installed HAProxy on.

[nodes]
node2 ansible_host=192.168.0.16 # <--- Change this to the ip address of your second Pi
node3 ansible_host=192.168.0.58 # <--- Change this to the ip address of your third Pi 
```

3. That's it! To run the playbook, navigate to the repo folder and type the following in your terminal:

`ansible-playbook playbook.yml` 

<br><br>

## You just made computer magic happen. Congratulations
This is just a proof of concept. In this repo, the playbook pushes a unique index.html file to each of the nodes so that you can visually debug whether or not it is working. For a production server, you'd want to obviously edit the playbook to deploy your site. 
