##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2022.04.03
## Description:    Functions for drawing formatted strings on the grid
## Notes:
##   - Source is 3 units wide
import globe
from grid import Unit

MY_NAME=__file__[__file__.rfind('/')+1:-3]

def drawIp(ip,grid,colour=None,*,override=False):
	'''Draw ip row'''
	#Only draw if we're allowed
	if not globe.can_draw and not override:
		return

	grid.goTo(0,ip.row)

	#Draw only the label if one exists
	if ip.label and globe.toggle_labels:
		grid.drawUnit(Unit(globe.UNIT_SIZE*3,f"\033[{globe.LABEL_COLOUR}m",ip.label))
		return

	#Construct colour string if it exists
	if ip.subnet:  #Check if asubnet exists
		towrite=f"{ip.ip_colour}  {ip.ip}{' '*(15-len(ip.ip))}{ip.subnet_colour}   /{ip.subnet}{' '*(5-(2 if ip.subnet<10 else 1))}"
	else:
		towrite=f"  {ip.ip:}{' '*(25-len(ip.ip))}"

	if colour:
		grid.write(towrite,colour=colour,pad_end=27-len(ip.ip))
	else:
		grid.write(towrite)
