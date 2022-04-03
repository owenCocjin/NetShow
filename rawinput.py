##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2022.04.03
## Description:    Captures raw keypresses from input
import sys,tty
import globe,network
from grid import Unit
from draw import drawIp

MY_NAME=__file__[__file__.rfind('/')+1:-3]

def getRaw(stop_at=None,print_char=None,backspace=False):
	'''Get one character at a time
	If stop_at is a single byte, this will return all characters before the stop_at char (including stop_at)'''
	STDIN_FILENO=sys.stdin.fileno()
	TERM_ORIG=tty.tcgetattr(STDIN_FILENO)
	tty.setraw(STDIN_FILENO)

	if not stop_at:  #Get one press
		toret=sys.stdin.buffer.read(1)  #Return 1 press
		if print_char and menu.isascii():
			print(chr(menu[0]),end='',flush=True)
	else:
		toret=b''
		menu=None
		while menu!=stop_at:
			menu=sys.stdin.buffer.read(1)  #Read 1 press
			toret+=menu
			if print_char and menu.isascii():
				if menu==b'\x7f' and backspace:  #Delete a char
					print('\033[1D \033[1D',end='',flush=True)
					toret=toret[:-2]  #Remove last char
				print(chr(menu[0]),end='',flush=True)

	#Reset tty
	tty.tcsetattr(STDIN_FILENO,tty.TCSANOW,TERM_ORIG)
	return toret

def keyboardProc(grid):
	'''Listen for keypresses'''
	while True:
		menu=getRaw()
		#Exit on ctrl-c or q
		if menu in [b'q',b'\x03']:
			return

		grid.notify(f"You pressed: {menu}")
		try:
			key_actions[menu](grid)
		except KeyError:
			continue

#------------------#
#    Prototypes    #
#------------------#
key_actions=None

#-----------------#
#    Functions    #
#-----------------#
def toggleLabels(grid):
	'''Toggle between labels and ip addresses,
	Pretty much just shorthand for refreshScreen()'''
	globe.toggle_labels=not globe.toggle_labels  #Invert toggle lable var
	globe.can_draw=False  #Lock drawing

	for col,ip in enumerate(network.address_map.values()):
		grid.goTo(0,col+1)

		#Draw only the label if one exists
		if globe.toggle_labels and ip.label:
			grid.drawUnit(Unit(globe.UNIT_SIZE*3,f"\033[{globe.LABEL_COLOUR}m",ip.label))
			continue

		#Construct colour string if it exists
		if ip.subnet:  #Check if asubnet exists
			towrite=f"{ip.ip_colour}  {ip.ip}{' '*(15-len(ip.ip))}{ip.subnet_colour}   /{ip.subnet}{' '*(5-(2 if ip.subnet<10 else 1))}"
		else:
			towrite=f"  {ip.ip:}{' '*(25-len(ip.ip))}"

		#Write out the ip
		grid.write(towrite)
	grid.notify(f"Labels turned {'ON' if globe.toggle_labels else 'OFF'}")
	globe.can_draw=True

def setLabel(grid):
	'''Goes through the motions of setting a label'''
	label_range=(1,len(network.address_map))
	select_unit=Unit(globe.UNIT_SIZE*3,"\033[43m","EDIT")
	blank_unit=grid.unit.copy()
	blank_unit.size=globe.UNIT_SIZE*3
	cur_pos=1

	globe.can_draw=False  #Get print lock

	#Move grid to label col 1
	grid.goTo(0,1)
	grid.drawUnit(select_unit,backstep=True)

	while True:  #Move "cursor" up or down
		action=getRaw()
		if action==b'A' and cur_pos>label_range[0]:
			drawIp(network.address_map[network.position_map[cur_pos]],grid,override=True)
			cur_pos-=1
			# grid.drawUnit(blank_unit)
			grid.goTo(0,cur_pos)
			grid.drawUnit(select_unit,backstep=True)
		elif action==b'B' and cur_pos<label_range[1]:
			drawIp(network.address_map[network.position_map[cur_pos]],grid,override=True)
			cur_pos+=1
			# grid.drawUnit(blank_unit)
			grid.goTo(0,cur_pos)
			grid.drawUnit(select_unit,backstep=True)
		elif action==b'\r':  #Set the actual label
			select_unit.content=''  #Clear the text so we can reuse the unit
			grid.notify("Type the new label, then press enter")
			grid.goTo(0,cur_pos)
			grid.drawUnit(select_unit,backstep=True)
			break

	#Set the label
	input_buff=getRaw(stop_at=b'\r',print_char=True,backspace=True)
	#Remove all non-ascii chars
	action=''
	for b in input_buff:
		if 0x20<=b<=0x7e:
			action+=chr(b)

	if action:  #Continue if not empty
		ip=network.position_map[cur_pos]
		network.addLabel(ip,action)

	#Refresh screen
	refreshScreen(grid)

	grid.notify(f"Set: {action} -> {ip}")

	globe.can_draw=True

def refreshScreen(grid):
	'''Re-draw all IPs and network unit values'''
	for col,ip in enumerate(network.address_map.values()):
		grid.goTo(col,1)
		drawIp(ip,grid,override=True)  #This draws the label as well

		cur_unit=grid.unit.copy()

		for p in ip.units.values():  #These should be in order of protocols
			if p==0:  #Draw an empty
				grid.drawUnit()
				continue
			cur_unit.content=f"{p}"
			grid.drawUnit(cur_unit)

#-----------------------------#
#    Prototype Definitions    #
#-----------------------------#
key_actions={b'\x0c':setLabel,
b'\x20':toggleLabels}


if __name__=="__main__":
	print(getRaw())
	print("Exits on [ctrl+l]")
	print(getRaw(b'\x0c',True))
