##
## Author:  Owen Cocjin
## Version: 0.8
## Date:    2021.07.15
## Description:    Packet data structure
## Notes:
## Updates:
##  - Updated IPPacket self.* a bit
from .segmentdata import *
from .ipv6ext import *
class IPPacket():
	def __init__(self, raw=None):
		'''Takes the raw packet as data.
This assumes it includes the IP headers'''
		self.raw=raw
		self.data_type="PACK"
		self.name="IP"
		buff=splitByte(raw[0])
		self.version=int(buff[:4],2)
		self.ihl=int(buff[4:],2)   #Number of 4-byte blocks, min of 5
		buff=splitByte(raw[1])
		self.tos=int(buff[:7],2)
		self.ecn=int(buff[7],2)
		self.length=int(raw[2:4].hex(),16)  #Length of packet, including IP header
		self.id=int(raw[4:6].hex(),16)
		buff=splitByte(raw[6])
		buff+=splitByte(raw[7])
		self.flags=buff[:3]
		self.frag_offset=int(buff[3:],2)
		self.ttl=raw[8]
		self.proto=raw[9]
		self.header_checksum=int(raw[10:12].hex(),16)
		self.src_ip=f"{raw[12]}.{raw[13]}.{raw[14]}.{raw[15]}"
		self.dst_ip=f"{raw[16]}.{raw[17]}.{raw[18]}.{raw[19]}"
		self.payload=raw[self.ihl*4:]  #This should practically always have data in it
		self.upper=segment_objs[segment_names[self.proto]](self.payload)   #TCP/UDP class goes here
		self.colour='\033[44m'
		self.txt_colour='\033[94m'
		self.text="IPv4"
	def __str__(self):
		return self.toStr()
	def toStr(self):
		'''Returns printable string'''
		return f"""ID:          {self.id} [{self.src_ip}] -> [{self.dst_ip}]
Length:      {self.length}-{self.ihl*4}=Payload({self.length-(self.ihl*4)})
Protocol:    {segment_names[self.proto]}({self.proto})
IP Checksum: {self.header_checksum}"""

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
	def getVersion(self):
		return self.version
	def setVersion(self, new):
		self.version=new
	def getIhl(self):
		return self.ihl
	def setIhl(self, new):
		self.ihl=new
	def getTos(self):
		return self.tos
	def setTos(self, new):
		self.tos=new
	def getEcn(self):
		return self.ecn
	def setEcn(self, new):
		self.ecn=new
	def getLength(self):
		return self.length
	def setLength(self, new):
		self.length=new
	def getId(self):
		return self.id
	def setId(self, new):
		self.id=new
	def getFlags(self):
		return self.flags
	def setFlags(self, new):
		self.flags=new
	def getFrag_offset(self):
		return self.frag_offset
	def setFrag_offset(self, new):
		self.frag_offset=new
	def getTtl(self):
		return self.ttl
	def setTtl(self, new):
		self.ttl=new
	def getProto(self):
		return self.proto
	def setProto(self, new):
		self.proto=new
	def getUpper(self):
		return self.upper
	def setUpper(self, new):
		self.upper=new
	def getHeader_checksum(self):
		return self.header_checksum
	def setHeader_checksum(self, new):
		self.header_checksum=new
	def getSrc_ip(self):
		return self.src_ip
	def setSrc_ip(self, new):
		self.src_ip=new
	def getDst_ip(self):
		return self.dst_ip
	def setDst_ip(self, new):
		self.dst_ip=new
	def getPayload(self):
		return self.payload
	def setPayload(self, new):
		self.payload=new
	def getSegment(self):
		return self.segment
	def setSegment(self, new):
		self.segment=new
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
	def getLL(self):
		return (self.ihl*4, self.upper)

class IPv6Packet():
	def __init__(self, raw):
		self.raw=raw
		self.data_type="PACK"
		self.name="IPV6"
		buff=''
		for b in raw[:4]:
			buff+=splitByte(b)
		self.version=int(buff[:4],2)
		self.traffic_class=buff[4:12]
		self.flow_label=buff[12:]
		self.length=int(raw[4:6].hex(),16)
		self.next_hdr=raw[6]
		self.hop_limit=raw[7]
		buff=raw[8:24].hex()
		self.src_ip=':'.join([buff[b*4:b*4+4] for b in range(len(buff)//4)])
		buff=raw[24:40].hex()
		self.dst_ip=':'.join([buff[b*4:b*4+4] for b in range(len(buff)//4)])
		self.payload=raw[40:]
		self.proto=-1  #This is used for compatibility
		if self.next_hdr in segment_names:
			self.next_name=segment_names[self.next_hdr]
			self.upper=segment_objs[self.next_name](self.payload)
		elif self.next_hdr in ext_header_names:
			self.next_name=ext_header_names[self.next_hdr]
			self.upper=ext_headers[self.next_name](self.payload)
		self.colour='\033[44m'
		self.txt_colour='\033[94m'
		self.text="IPv6"
	def __str__(self):
		return self.toStr()

	def toStr(self):
		'''Returns printable string'''
		return f"""Version:     {self.version}
Next Header: {self.next_hdr}({self.next_name})
Source:      [{self.src_ip}]
Dest:        [{self.dst_ip}]"""

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
	def getVersion(self):
		return self.version
	def setVersion(self, new):
		self.version=new
	def getTraffic_class(self):
		return self.traffic_class
	def setTraffic_class(self, new):
		self.traffic_class=new
	def getFlow_label(self):
		return self.flow_label
	def setFlow_label(self, new):
		self.flow_label=new
	def getLength(self):
		return self.length
	def setLength(self, new):
		self.length=new
	def getNext_name(self):
		return self.next_name
	def setNext_name(self, new):
		self.next_name=new
	def getNext_hdr(self):
		return self.next_hdr
	def setNext_hdr(self, new):
		self.next_hdr=new
	def getProto(self):  #Used for compatability
		return self.next_hdr
	def setProto(self, new):  #Used for compatability
		self.next_hdr=new
	def getHop_limit(self):
		return self.hop_limit
	def setHop_limit(self, new):
		self.hop_limit=new
	def getSrc_ip(self):
		return self.src_addr
	def setSrc_ip(self, new):
		self.src_addr=new
	def getDst_addr(self):
		return self.dst_addr
	def setDst_addr(self, new):
		self.dst_addr=new
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
	def getLL(self):
		return (40, self.upper)

class ARPPacket():
	def __init__(self, raw):
		self.raw=raw
		self.data_type="PACK"
		self.name="ARP"
		self.ihl=7  #Used for compatability
					 #Simply the length of the arp header (which has no payload)
					 #no. of 4-byte blocks
		self.hw_type=int(raw[:2].hex(),16)
		self.proto_type=int(raw[2:4].hex(),16)
		self.hw_addr_len=hex(raw[4])
		self.proto_addr_len=hex(raw[5])
		self.operation=int(raw[6:8].hex(),16)
		srcmac=raw[8:14].hex()
		self.src_mac=':'.join([srcmac[d*2:d*2+2] for d in range(len(srcmac)//2)])
		self.src_ip=f"{raw[14]}.{raw[15]}.{raw[16]}.{raw[17]}"
		dstmac=raw[18:24].hex()
		self.dst_mac=':'.join([dstmac[d*2:d*2+2] for d in range(len(dstmac)//2)])
		self.dst_ip=f"{raw[24]}.{raw[25]}.{raw[26]}.{raw[27]}"
		self.colour='\033[44m'
		self.txt_colour='\033[94m'
		self.text="ARP "
		self.proto=-2  #This is for compatibility
		self.upper=None  #For compatability
	def __str__(self):
		return self.toStr()

	def toStr(self):
		return f"""Hardware Type: {hex(self.hw_type)}
Protocol Type: {hex(self.proto_type)}
Source:        [{self.src_mac}]({self.src_ip})
Dest:          [{self.dst_mac}]({self.dst_ip})"""

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
	def getIhl(self):
		return self.ihl
	def setIhl(self, new):
		self.ihl=new
	def getHw_type(self):
		return self.hw_type
	def setHw_type(self, new):
		self.hw_type=new
	def getProto_type(self):
		return self.proto_type
	def setProto_type(self, new):
		self.proto_type=new
	def getHw_addr_len(self):
		return self.hw_addr_len
	def setHw_addr_len(self, new):
		self.hw_addr_len=new
	def getProto_addr_len(self):
		return self.proto_addr_len
	def setProto_addr_len(self, new):
		self.proto_addr_len=new
	def getOperation(self):
		return self.operation
	def setOperation(self, new):
		self.operation=new
	def getSrc_mac(self):
		return self.src_mac
	def setSrc_mac(self, new):
		self.src_mac=new
	def getSrc_ip(self):
		return self.src_ip
	def setSrc_ip(self, new):
		self.src_ip=new
	def getDst_mac(self):
		return self.dst_mac
	def setDst_mac(self, new):
		self.dst_mac=new
	def getDst_ip(self):
		return self.dst_ip
	def setDst_ip(self, new):
		self.dst_ip=new
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
	def getUpper(self):
		return self.upper
	def setUpper(self, new):
		self.upper=new
	def getLL(self):
		return (self.ihl*4, self.upper)


'''
|||    DICTS    |||
'''
packet_names={0x0800:"IP",
0x0806:"ARP",
0x86DD:"IPV6"}
packet_types={0x0800:IPPacket,
0x0806:ARPPacket,
# 0x8035:RARPPacket,
# 0x8100:VLANPacket,
# 0x814C:SNMPPacket,
0x86DD:IPv6Packet}
# 0x8847:MPLSUniPacket,
# 0x8848:MPLSMultiPacket,
# 0x8870:JumboPacket,
# 0x888E:EAPPacket,  #EAP over LAN (IEEE 802.1X)
# 0x88e5:MACPacket,  #MAC Security (IEEE 802.1AE)
# 0x88F7:PTPPacket}  #Precision Time Protocol (IEEE 1588)
