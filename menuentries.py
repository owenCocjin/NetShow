##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2022.04.03
## Description:    Menu entries for ProgMenu
import os
import globe
from ProgMenu.progmenu import EntryFlag,EntryArg,EntryPositional

MY_NAME=__file__[__file__.rfind('/')+1:-3]

def helpFunc():
	print(f"""netshow.py [interface] <hr>
Visually show local traffic
    -h; --help: Prints this page
    -r; --rows: Number of rows to show at once.
                Note: Once exceeded, new IPs will be ignored
""")

def rowsFunc(r):
	'''Sets the global rows'''
	try:
		return int(r)
	except TypeError:
		print(f"[|X:{MY_NAME}:rows]: Invalid row number: {r}")
		exit(1)

# EntryArg("interface",['i',"interface"],lambda i:i,strict=True)
EntryFlag("help",['h',"help"],helpFunc)
EntryArg("rows",['r',"rows"],rowsFunc,default=os.get_terminal_size()[1]-5)  #-5 for the notify area and the titles
EntryPositional("interface",0,lambda i:i)
