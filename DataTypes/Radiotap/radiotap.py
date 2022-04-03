##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2021.07.03
## Description:    Tools to process radiotap related data
## Notes:
##  - Classes here are simply definition classes
##  - RTAPField tuples follow: (name, byte length, unit, signed int)
## Updates:
from .radiotapfields import *
class RTAPBundle():
	def __init__(self, name, size, alignment, fields):
		self.name=name
		self.size=size  #Full length of the bundle
		self.fields=fields
		self.alignment=alignment  #Each field will be this many bytes; If a field's length is smaller than the alignment, there will be padding
	def __str__(self):
		toret=f"{self.name}({self.size})"
		# for f in self.fields:
		# 	toret+=f"\n  {f}"
		return toret

	def listFields(self):
		return [f[0] for f in self.fields]
	def getStrLineCount(self):
		'''Returns the number of lines in self.__str__'''
		return 1+len(self.fields)
	def getFieldLengths(self):
		return [f[1] for f in self.fields]

	def getName(self):
		return self.name
	def setName(self, new):
		self.name=new
	def getSize(self):
		return self.size
	def setSize(self, new):
		self.size=new
	def getFields(self):
		return self.fields
	def setFields(self, new):
		self.fields=new
	def getAlignment(self):
		return self.alignment
	def setAlignment(self, new):
		self.alignment=new


class RTAPField():
	def __init__(self, name, size, unit=''):
		self.name=name
		self.size=size  #Alignment size in bytes
		self.unit=unit
		self.bundle=''
		self.adhoc=None  #present_fields[f"{self.bundle}_{self.upper}"]
	def __str__(self):
		return f"{self.name}({self.size}) {self.unit}"

	def getName(self):
		return self.name
	def setName(self, new):
		self.name=new
	def getSize(self):
		return self.size
	def setSize(self, new):
		self.size=new
	def getUnit(self):
		return self.unit
	def setUnit(self, new):
		self.unit=new
	def getBundle(self):
		return self.bundle
	def setBundle(self, new):
		self.bundle=new
	def getAdhoc(self):
		return self.adhoc
	def setAdhoc(self, new):
		self.adhoc=new


def parseBitmap(bmap):
	'''Checks Radiotap header's present and returns a list of all the addressed headers.
bmap is a bytes object of length 4.
Returns a list of RTAPBundles'''
	bits=''
	toret=[]
	for b in bmap:
		bits+=f"{bin(b)[2:]:>08}"
	bits=bits[::-1]
	for i, flag in enumerate(bits):
		if flag=='1':
			toret.append(present_bitmask[i])
	return toret
def isExtended(bmap):
	'''Returns True if bmap has extended bit set.
Assumes the bmap is in correct endieness'''
	if bin(bmap)[-1]=='1':
		return True
	return False
def parsePresents(raw, pntr=4):
	'''Returns a tuple: (list of present dwords, list of each present's raw content).
This tuple can then be itterated through to use parseBitmap against each present.
raw is the entire rtap header, including the initial 4 bytes.
if extra data is added to raw it will be ignored once the end of the header is reached.'''
	dwords=[]
	data=[]
	#Go through and find all presents
	while True:
		curp=revBytes(raw[pntr:pntr+4])
		dwords.append(parseBitmap(curp))
		pntr+=4
		if bin(int(curp.hex(),16))[-1]!='1':
			break
	#Get present data for each
	for p in dwords:
		toadd_data=[]
		for b in p:
			for f in b.getFieldLengths():
				if b.getAlignment()>0:
					pntr+=(pntr%b.getAlignment())  #Skip padding
					toadd_data.append(raw[pntr:pntr+f])
					pntr+=f  #Move to new position
				else:
					toadd_data.append(b'')
		data.append(toadd_data)
	return (dwords,data)


#present_bitmask is a list in order that the bits must appear
#RTAPBundle("Name",total_len,alignment,[tuple("name",len,"unit",signed_int)...])
present_bitmask=[RTAPBundle("TSFT",8,8,[("mac time",8,"us",False)]),  #0
RTAPBundle("FLAGS",1,1,[("flag",1,'',False)]),
RTAPBundle("RATE",1,1,[("tx/rx",1,"x500Kbps",False)]),
RTAPBundle("CHANNEL",4,2,[("freq",2,"MHz",False),("flags",2,"bmap",False)]),
RTAPBundle("FHSS",2,1,[("hop set",1,'',False),("hop pattern",1,'',False)]),
RTAPBundle("ANTENNA SIG",1,1,[("signal",1,"dBm",True)]),
RTAPBundle("ANTENNA NO",1,1,[("noise",1,"dBm",True)]),
RTAPBundle("LOCK",2,2,[("quality",2,'',False)]),  #7
RTAPBundle("TX ATT",2,2,[("attenuation",2,'',False)]),
RTAPBundle("dB TX",2,2,[("attenuation",2,"dB",False)]),
RTAPBundle("dBm TX",1,1,[("power",1,"dBm",True)]),
RTAPBundle("ANTENNA IND",1,1,[("index",1,'',False)]),
RTAPBundle("dB ANTENNA SIG",1,1,[("signal",1,"dB",False)]),
RTAPBundle("dB ANTENNA NO",1,1,[("noise",1,"dB",False)]),
RTAPBundle("RX",2,2,[("flags",2,"bmap",False)]),
RTAPBundle("TX FLGS",2,2,[("flags",2,"bmap",False)]),  #15
RTAPBundle("RTS",1,1,[("retries",1,'',False)]),
RTAPBundle("DATA",1,1,[("retries",1,'',False)]),  #XChannel
RTAPBundle("XCHANNEL",8,4,[("flags",4,'',False),("freq",2,"MHz",False),("channel",1,"ch",False),("max power",1,'',False)]),  #Channel +
RTAPBundle("MCS",3,1,[("known",1,'',False),("flags",1,"bmap",False),("mcs",1,'',False)]),
RTAPBundle("A-MPDU",8,4,[("ref #",4,'',False),("flags",2,"bmap",False),("crc",1,'',False),("reserved",1,'',False)]),
RTAPBundle("VHT",9,2,[("known",2,'',False),("flags",1,'',False),("bandwidth",1,'',False),("mcs nss",1,'',False),("coding",1,'',False),("group id",1,'',False),("partial aid",2,'',False)]),
RTAPBundle("TIMESTAMP",12,8,[("timestamp",8,'',False),("accuracy",2,'',False),("unit/position",1,'',False),("flags",1,"bmap",False)]),
RTAPBundle("HE",12,2,[("data 1",2,'',False),("data 2",2,'',False),("data 3",2,'',False),("data 4",2,'',False),("data 5",2,'',False),("data 6",2,'',False)]),  #23
RTAPBundle("HEMU",6,2,[("flags 1",2,"bmap",False),("flags 2",2,"bmap",False),("ru",1,"channel 1",False),("ru",1,"channel 2",False)]),
RTAPBundle("HEMU-O-U",6,2,[("user 1",2,'',False),("user 2",2,'',False),("user position",1,'',False),("user known",1,'',False)]),
RTAPBundle("0-PSDU",1,1,[("type",1,'',False)]),  #0-length-PSDU; 1 byte
RTAPBundle("L-SIG",4,2,[("data 1",2,'',False),("data 2",2,'',False)]),
RTAPBundle("TLV",0,0,[]),  #This has a variable length. It should be placed at the end of all data. The length can be calculated on the fly
RTAPBundle("RESERVED",0,0,[("none",0,'',False)]),  #None
RTAPBundle("VENDOR",4,2,[("oui",1,'',False),("sub namespace",1,'',False),("skip length",2,'',False)]),  #None
RTAPBundle("EXTENDED",0,0,[("none",0,'',False)])]  #31; Another bitmask follows this one

present_maps={"FLAGS-flags":None}
