##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2022.04.03
## Description:    Network functions n stuff
import socket
import globe
from DataTypes import framedata
from grid import Unit

MY_NAME=__file__[__file__.rfind('/')+1:-3]

#-----------------------------#
#    Prototypes & Variables   #
#-----------------------------#
network_units=None
address_map=None
ip_labels={}
new_labels={}  #Holds labels to write before exiting

#-----------------#
#    Functions    #
#-----------------#
def addLabel(raw_ip,label):
	'''Adds a label to an IP and any related IPs'''
	ip=address_map[raw_ip]
	ip.label=label

	ip_labels[raw_ip]=label  #Add to total list of IP labels
	new_labels[raw_ip]=label  #Add to list of new IP labels

	# for k,v in address_map.items():
	# 	if (v.ip_colour,v.subnet_colour)==(ip.ip_colour,ip.subnet_colour):  #Same colours means same subnet (somewhat lol)
	# 		address_map[k].label=label
	# 		ip_labels[k]=label  #Add to total list of IP labels
	# 		new_labels[k]=label  #Add to list of new IP labels

def createListener(interface):
	'''Creates a raw socket object and binds it to "interface".
	Returns the socket object on success, None otherwise'''
	try:
		sock=socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x03))  #The 3 is to read all data, incoming & outgoing
		sock.bind((interface,0))
		return sock
	except PermissionError as e:
		print(f"""[|X:{MY_NAME}:createListener:Error]: Not enough permission to run on {interface}!""")
		exit(1)
	except OSError as e:
		print(f"""[|X:{MY_NAME}:createListener:Error]: Interface doesn't exist!""")
		exit(2)
	return None

def parsePacket(pckt):
	'''Parse a raw packet and return a dict'''
	nl='\n'
	recv_data=framedata.ETHFrame(pckt)
	#Just return the type of packet it was
	return recv_data
	# while recv_data.upper:
	# 	print(f"{recv_data.colour}{recv_data.text}\033[0m\n  {recv_data.txt_colour}{str(recv_data).replace(nl,f'{nl}  ')}\033[0m")
	# 	recv_data=recv_data.upper



#---------------#
#    Classes    #
#---------------#
class NetworkUnit():
	'''Just holds stuff like unit class, counter, and grid position'''
	def __init__(self,unit,position):
		self.unit=unit
		self.position=position
		self.counter=0

class IpUnit():
	def __init__(self,ip,row):
		self.ip=ip
		self.row=row
		self.units=network_counter.copy()
		self.subnet=None  #CIDR int
		self.ip_colour=None  #Colour at start of line, used to match IPs in same subnets
		self.subnet_colour=None  #Colour used to match IPs in same subnets
		self.label=None

#-----------------#
#    Variables    #
#-----------------#
network_units={  #X starst at 3 because first 2 are used for mac name, and 3 is IP label
	6:NetworkUnit(Unit(globe.UNIT_SIZE,'\033[42m',"TCP"),(3,1)),  #TCP
	17:NetworkUnit(Unit(globe.UNIT_SIZE,'\033[44m',"UDP"),(4,1)),  #UDP
	1:NetworkUnit(Unit(globe.UNIT_SIZE,'\033[43m',"ICMP"),(5,1)),  #ICMP
	-2:NetworkUnit(Unit(globe.UNIT_SIZE,'\033[41m',"ARP"),(6,1)),  #ARP
	#-1:NetworkUnit(Unit(UNIT_SIZE,'\033[41m',"IPv6"),(6,1))  #IPv6
}
address_map={}
position_map={}  #Maps the position of an IP to the IP itself
network_counter={}  #Template when creating new ip items
#Update network counter
for u in network_units.keys():
	network_counter[u]=0
