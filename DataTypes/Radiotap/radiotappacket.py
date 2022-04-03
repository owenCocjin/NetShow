##
## Author:  Owen Cocjin
## Version: 0.2
## Date:    2021.07.12
## Description:    Radiotap packet class
## Notes:
##  - RTAPPacket doesn't process any bitmaps; Just returns the data as an int
##  - RTAPFrame cuts out the RTAP header from raw.
##    Because raw isn't logically used we can just pass the raw data down until self.upper isn't RTAPPacket
## Updates:
##  - Updated getRaw() for all classes.
##    Now accepts an optional length that returns raw from [:<length specified>]
from ..payloaddata import *
from .radiotap import *
from ..datatools import revBytes, convertSigned, prettyHex
class RTAPPacket():
	'''Represents one header for each RTAPFrame present word'''
	def __init__(self, present_list, data_list, raw):
		self.present_list=present_list  #All bitmaps found by RTAPFrame; These are already in correct endienness
		self.data_list=data_list
		self.name="RTAP"
		self.raw=raw
		self.bitbundle=self.present_list[0]
		self.content=data_list[0]
		bbundlelen=len(self.bitbundle)
		self.length=sum([b.getSize() for b in self.bitbundle])
		self.width_inc=False
		self.colour='\033[45m'
		self.txt_colour='\033[95m'
		if len(self.present_list)==1:
			self.upper=GENERICPayload(self.raw)
		else:
			self.upper=RTAPPacket(self.present_list[1:], self.data_list[1:], self.raw)
		self.text=' '*(bbundlelen//2)+"RTAP"+' '*(bbundlelen//2)
		if bbundlelen%2==1:
			self.text+=' '
	def __str__(self):
		return self.toRet()

	def toStr(self):
		counter=0
		toret=f"""
Bitmap: {';'.join([b.getName() for b in self.bitbundle])}
Length: {self.length}
Data:   {prettyHex(self.content[0])} ..."""
		for b in self.bitbundle:
			toret+=f"\n{b.getName()}:"
			for f in b.getFields():
				if self.content[counter]!=b'':
					curdata=int(revBytes(self.content[counter]).hex(),16)
					if f[3]:
						curdata=convertSigned(curdata, len(self.content[counter]))
					toret+=f" {curdata} {f[2]};"
					counter+=1
				else:
					toret+="Set;"
		return toret
	def processFields(self):
		'''Returns an RTAPPacket of the processed data'''
		align=self.bitbundle.getAlignment()
		#Skip if alignment is 0 (field has no data)
		if align==0:
			return self.fields
		for i,b in enumerate(self.bitbundle.getFields()):
			truesize=b[1]  #In bytes
			curraw=self.raw[i*align:i*align+truesize]  #Removes padding
			curbytes=revBytes(curraw)
			#Check for a map
			# if f"{self.bitbundle.getName()}-{b[0]}" in present_maps:
			# 	pass
			if b[3]:
				self.fields.append(convertSigned(int(curbytes.hex(),16),truesize))
			else:
				self.fields.append(int(curbytes.hex(),16))
		return self.fields

	def getBitbundle(self):
		return self.bitbundle
	def setBitbundle(self, new):
		self.bitbundle=new
	def getRaw(self, l=None):
		if l==None:
			return self.raw
		return self.raw[:l]
	def setRaw(self, new):
		self.raw=new
	def getName(self):
		return self.name
	def setName(self, new):
		self.name=new
	def getColour(self):
		return self.colour
	def setColour(self, new):
		self.colour=new
	def getTxt_colour(self):
		return self.txt_colour
	def setTxt_colour(self, new):
		self.txt_colour=new
	def getText(self):
		return self.text
	def setText(self, new):
		self.text=new
	def getUpper(self):
		return self.upper
	def setUpper(self, new):
		self.upper=new
	def getWidthInc(self):
		return self.width_inc
	def setWidthInc(self, new):
		self.width_inc=new
	def getLL(self):
		return (0,self.upper)  #Length is 0 because the RTAPFrame handles the full header length through getLL

class IEEE80211Packet():
	def __init__(self, raw):
		self.raw=raw
