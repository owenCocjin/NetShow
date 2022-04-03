#!/usr/bin/python3
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2022.04.03
## Description:    Visualize network traffic
## To-Do:
##  - Re-draw graph when rescaling the terminal
## Issues:
import threading,time,os,socket,fcntl,struct
import network,menuentries,misc,globe,rawinput
from grid import Grid,Unit
from draw import drawIp
from ProgMenu.progmenu import MENU

vprint=MENU.verboseSetup(['v',"verbose"])
PARSER=MENU.parse(True,strict=True)

MY_NAME=__file__[__file__.rfind('/')+1:-3]

UNIT_SIZE=globe.UNIT_SIZE
SOURCE_COUNT=PARSER["rows"]
SUBNETS=globe.SUBNETS

#-------------------#
#    Prototyping    #
#-------------------#
# network_units=None
# address_map=None

#------------#
#    Main    #
#------------#
def main():
	#--* Environment Setup *--#
	#Read ip.labels file and import them into a dict
	#Each IP is 4 bytes, followed by a NULL terminated string
	with open(globe.LABEL_FILE,'a+') as f:  #Open as a+ so we can read/write, but also the file is created if not exists
		f.seek(0)  #Seek to start
		while True:
			ip=''
			label=''

			buff=misc.readUntil([' ','\t',''],f).strip()  #Read in the IP
			if buff=='':
				break
			elif buff[0]=='#':
				f.readline()  #Skip this line
				continue
			#Set ip
			ip=buff
			#Read in label
			label=misc.readUntil('\n',f)[:-1]

			#Add IP and label to dict
			network.ip_labels[ip]=label.strip()

	#--* Main *--#
	listener=network.createListener(PARSER["interface"])
	users_mac=misc.decodeMac(listener.getsockname()[4])

	#Draw the initial grid
	grid=Grid(len(network.network_units)+3,SOURCE_COUNT+1,Unit(UNIT_SIZE),draw=True)
	grid.goTo(0,0)
	#Draw blank units
	grid.drawUnit(Unit(UNIT_SIZE*3,'\033[0m',"Source IP"))
	# grid.drawUnit(Unit(UNIT_SIZE*2,'\033[100m',"Label"))

	for u in network.network_units.values():
		grid.drawUnit(u.unit)

	grid.notify("Waiting to detect IP...")
	grid.nnotify(f"My MAC: {users_mac}",colour='\033[44m')
	grid.nnotify(f"My IP:  \033[45m---.---.---.---",colour='\033[44m')  #This needs to be updated once we know who we are
	grid.nnotify("Press [ctrl+c] to exit")

	#Determine our IP
	users_ip=socket.inet_ntoa(fcntl.ioctl(
		listener.fileno(),
		0x8915,  #SIOCGIFADDR
		struct.pack("256s",listener.getsockname()[0][:15].encode())
	)[20:24])

	grid.notify(f"My IP:  \033[45m{users_ip}",colour='\033[44m',line=2)
	addNewIp(users_ip)
	#Set colour before drawing
	# network.address_map[users_ip].ip_colour='\033[44m'
	# network.address_map[users_ip].subnet_colour='\033[45m'
	drawIp(network.address_map[users_ip],grid)

	#Start listener as thread
	listener_thread=threading.Thread(target=listenerProc,args=(listener,grid),daemon=True)
	listener_thread.start()

	#Start keyboard listener
	keyboard_thread=threading.Thread(target=rawinput.keyboardProc,args=(grid,),daemon=True)
	keyboard_thread.start()

	#Only leave when specific quit keys are pressed.
	#The listener_thread will die once main dies because it's a daemon thread
	keyboard_thread.join()

	#--* Exit Routines *--#
	#Save labels
	grid.notify("Saving labels...")
	with open(globe.LABEL_FILE,'a+') as f:
		for ip,label in network.new_labels.items():
			if len(ip)<8:  #Add an extra tab to make it prettier
				ip=f"{ip}\t"
			f.write(f"{ip}\t{label}\n")

	grid.notify("Done!")
	grid.exitGrid()
	return


#-----------------#
#    Functions    #
#-----------------#
def listenerProc(listener,grid):
	'''Run listener process'''
	while True:
		#Get data from nic
		buff,cli=listener.recvfrom(65535)
		frame=network.parsePacket(buff)
		packet_type=frame.upper.proto  #Packet protocol used
		packet_src=frame.upper.src_ip

		if packet_type in network.network_units:
			#Check who the return IP is and if they're in the table, increment their value
			if packet_src in network.address_map:  #Just increment that row's correct value
				pass
			elif len(network.address_map)<SOURCE_COUNT:  #Add to mac list
				addNewIp(packet_src)
				checkIpMasks(packet_src,grid)
				drawIp(network.address_map[packet_src],grid)
			else:  #Ignore
				grid.notify(f"New IP: {packet_src}")
				continue

			#Increment proper packet
			cur_packet=network.address_map[packet_src]

			cur_packet.units[packet_type]+=1
			if globe.can_draw:
				grid.goTo(network.network_units[packet_type].position[0],cur_packet.row)
				grid.write(cur_packet.units[packet_type])

def addNewIp(ip):
	'''Adds a new IP to network.address_map.
	Used when we see a new IP'''
	#Create network_units dict copy
	pos=len(network.address_map)+1
	network.address_map[ip]=network.IpUnit(ip,pos)
	network.position_map[pos]=ip
	#Check if the IP is in the label list and add it's label
	try:
		network.address_map[ip].label=network.ip_labels[ip]
	except KeyError:
		pass
	return network.address_map[ip]

def checkIpMasks(ip,grid):
	'''Check if the given IP is in the same netmask as any other existing IPs.
	Returns True if matched'''
	for o in network.address_map:
		#Ignore same ip
		if ip==o:
			continue

		same_mask=misc.ipInCIDR(ip,o,SUBNETS)
		if same_mask:
			# grid.nnotify(f"{ip} & {o} under /{same_mask}")
			#Set both IP's colours the matching ip
			other=network.address_map[o]
			this_ip=network.address_map[ip]
			if other.ip_colour==None:
				tag,subnet=nextIpColours()
				other.ip_colour=tag
				other.subnet_colour=subnet
				other.subnet=same_mask
				#Draw this other IP
				drawIp(other,grid)

			#Set this IP's colours
			this_ip.ip_colour=other.ip_colour
			this_ip.subnet_colour=other.subnet_colour
			this_ip.subnet=other.subnet

			return True

	return False

def nextIpColours():
	'''Return tag and mask colours, THEN increment'''
	orig_colours=(globe.ip_colour,globe.subnet_colour)
	toret=(f"\033[4{globe.ip_colour}m",f"\033[4{globe.subnet_colour}m")
	globe.ip_colour=(globe.ip_colour+1)%6
	if not globe.ip_colour:  #Rolled over
		globe.ip_colour+=1
		globe.subnet_colour=((globe.subnet_colour+1)%6)+1

	if orig_colours[0]==orig_colours[1]:  #Re-run so we can't have matching colours
		return nextIpColours()
	return toret

#---------------#
#    Classes    #
#---------------#

#-----------------#
#    Variables    #
#-----------------#
#Edit this to add new values to the table
# network_units={  #X starst at 3 because first 2 are used for mac name, and 3 is IP label
# 	6:NetworkUnit(Unit(UNIT_SIZE,'\033[42m',"TCP"),(3,1)),  #TCP
# 	17:NetworkUnit(Unit(UNIT_SIZE,'\033[44m',"UDP"),(4,1)),  #UDP
# 	1:NetworkUnit(Unit(UNIT_SIZE,'\033[43m',"ICMP"),(5,1)),  #ICMP
# 	-2:NetworkUnit(Unit(UNIT_SIZE,'\033[41m',"ARP"),(6,1)),  #ARP
# 	#-1:NetworkUnit(Unit(UNIT_SIZE,'\033[41m',"IPv6"),(6,1))  #IPv6
# }
# address_map={}
# network_counter={}  #Template when creating new ip items
# #Update network counter
# for u in network_units.keys():
# 	network_counter[u]=0


if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt as e:
		Grid.exitGrid(None)
		print('\r\033[K',end='')
