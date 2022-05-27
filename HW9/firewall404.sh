#!/bin/bash

#remove(flushing) any previous rules or chains
#sudo iptables -P INPUT ACCEPT
#sudo iptables -P FORWARD ACCEPT
#sudo iptables -P OUTPUT ACCEPT
sudo iptables -t nat -F
sudo iptables -t mangle -F
sudo iptables -F
sudo iptables -X

#For all outgoing packets, change their source IP address to your own machine's IP address
sudo iptables -t nat -A POSTROUTING -j MASQUERADE #I'm assuming shared wifi connection not etherent hence the usage of wlan0 instead of eth0, update no need for -i wlan0

#Block all new packets (i.e.  a packet that creates a new connection) coming from yahoo.com
#sudo iptables -A OUTPUT -p tcp -m string --string "yahoo.com" --algo kmp -j REJECT
sudo iptables -A INPUT -p tcp -m state --state NEW -s yahoo.com -j REJECT

#Block  your  computer  from  being pinged  by  all  other  hosts  (Hint:ping uses  ICMP  Echo requests)
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j DROP

#Set up port-forwarding from an unused port of your choice to port 22 on your computer.You should be able to SSH into your machine using both ports (You may need to enable connections on the unused port as well)
sudo iptables -A INPUT -p tcp --dport 77 -j ACCEPT #enable connection of port 77
sudo iptables -A PREROUTING -t nat -p tcp --dport 77 -j REDIRECT --to-port 22

#Allow for SSH access (port 22) to your machine from only the engineering.purdue.edu domain
#sudo iptables -A INPUT -p tcp --dport 22 -j DROP
sudo iptables -A INPUT -p tcp ! -s engineering.purdue.edu --dport 22 -j DROP

#Assuming you are running an HTTPD server on your machine that can make available your entire home directory to the outside world, write a rule for preventing DoS attacks by limiting connection requests to 30 per minute after a total of 60 connections have been mad

#sudo iptables -I INPUT 1 -p tcp --dport 80 -m conntrack --ctstate NEW -m recent --name http --update --seconds 60 -hitcount \ 60 -j limit
#sudo iptables -I INPUT 2 -p tcp --dport 80 -m conntrack -ctstate NEW -m recent --name http --set
#sudo iptables -N limit
#sudo iptables -A limit -p tcp --dport 80 -m conntrack --ctstate NEW -m recent --name http --update --seconds 60 -hitcount 30\ -j DROP
#sudo iptables -A limit -p tcp --dport 80 -m conntrack --ctstate NEW -m recent --name http --set

# or should I do the following:
sudo iptables -A FORWARD -p tcp --syn -m limit --limit 0.5/s --limit-burst 60 --dport 80 -j ACCEPT

#Drop any other packets if they are not caught by the above rules
sudo iptables -A INPUT -j DROP


