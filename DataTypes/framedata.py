##
## Author:  Owen Cocjin
## Version: 0.6
## Date:    2021.07.12
## Description:    Frame data structure
## Notes:

from .packetdata import *

class ETHFrame():
	def __init__(self, raw):
		'''Socket removes preamble SFD, and CRC footer (12 bytes total) from data.'''
		self.raw=raw
		self.data_type="ETH"
		self.name="ETH"
		dst=raw[:6].hex()
		src=raw[6:12].hex()
		self.dst_mac=':'.join([dst[b*2:b*2+2] for b in range(len(dst)//2)])
		self.src_mac=':'.join([src[b*2:b*2+2] for b in range(len(src)//2)])
		self.type=int(raw[12:14].hex(),16)  #Type of packet data
		self.payload=raw[14:]
		self.upper=packet_types[self.type](self.payload)
		self.colour='\033[45m'
		self.txt_colour='\033[95m'
		self.text="ETH"
		# self.packet=IPPacket(self.payload)

	def __str__(self):
		return self.toStr()

	def toStr(self):
		return f"""Source MAC: [{self.src_mac}]
Dest MAC:   [{self.dst_mac}]
Type:       {hex(self.type)}({self.name})
Payload:    {self.payload}"""

	def getRaw(self, l=None):
		if l==None:
			return self.raw
		return self.raw[:l]
	def setRaw(self, new):
		self.raw=new
	def getData_type(self):
		return self.data_type
	def setData_type(self, new):
		self.data_type=new
	def getName(self):
		return self.name
	def setName(self, new):
		self.name=new
	def getDst_mac(self):
		return self.dst_mac
	def setDst_mac(self, new):
		self.dst_mac=new
	def getSrc_mac(self):
		return self.src_mac
	def setSrc_mac(self, new):
		self.src_mac=new
	def getType(self):
		return self.type
	def setType(self, new):
		self.type=new
	def getPayload(self):
		return self.payload
	def setPayload(self, new):
		self.payload=new
	def getUpper(self):
		return self.upper
	def setUpper(self, new):
		self.upper=new
	def getColour(self):
		return self.colour
	def setColour(self, new):
		self.colour=new
	def getTxt_colour(self):
		return self.txt_colour
	def setTxt_colour(self):
		self.txt_colour=new
	def getText(self):
		return self.text
	def setText(self, new):
		self.text=new
	def getWidthInc(self):
		return self.width_inc
	def setWidthInc(self, new):
		self.width_inc=new
	def getLL(self):
		return (14, self.upper)
