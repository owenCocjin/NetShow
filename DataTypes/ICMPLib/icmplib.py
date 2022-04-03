##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2021.07.15
## Description:    Holds important ICMP related data
## Notes:
##  - icmp_funcs functions will ignore extra data
##  - lengths in returns of functions include the 4 bytes of the ICMP header
##  - No funcs take the first 4 bytes of the ICMP header (type/code/checksum)
def advert(data):
	'''Takes at least 8 bytes.
Each 8 bytes after that follows the format [Router addr, Preference](each 4 bytes).
Because the whole length of data is used, the length is simply len(data)'''
	pointer=4  #Skip first 4 bytes
	advert_count=data[0]  #Number of adverts in this message
	addr_entry_size=data[1]  #Number of 4-byte dwords
	lifetime=(data[2]<<8)+data[3]  #Max seconds that each entry is valid
	toret={"Advert Count":advert_count,
"Addr Entry Size":addr_entry_size,
"Lifetime":lifetime,
"Length":len(data)}
	for d in range(advert_count):
		#Construct router IP as a string
		curip='.'.join(str(b) for b in data[pointer*4:pointer*4+4])
		curpreference=int(data[pointer*4:pointer*4+4].hex(),16)
		pointer+=8
		toret[curip]=curpreference

def echo(data):
	'''Takes a 12-byte long bytes object.
Parses both echo and echo_reply'''
	identifier=(data[0]<<8)+data[1]
	seq_num=(data[2]<<8)+data[3]
	return {"Identifier":identifier,
"Sequence Number":seq_num,
"length":8}
def errorMsg(data):
	'''Takes 28 bytes of data: IP header + 8 bytes of original datagram.
Takes the whole ICMP payload - first 4 bytes.
This means the first 4 bytes in data are ignored (unused)'''
	ip_hdr=data[4:20]
	dgram=data[20:28]
	return {"IP Header":ip_hdr,
"Datagram":dgram,
"length":32}
def infoMsg(data):
	'''Only has identifier and seq_num.
I'm pretty sure this is deprecated; It's a pretty useless feature anyways'''
	identifier=(data[0]<<8)+data[1]
	seq_num=(data[2]<<8)+data[3]
	return {"Identifier":identifier,
"Sequence Number":seq_num,
"length":8}
def paramProb(data):
	'''Similar to errorMsg(), but first byte of data is the "pointer"'''
	pointer=data[0]
	ip_hdr=data[4:20]
	dgram=data[20:28]
	return {"Pointer":pointer,
"IP Header":ip_hdr,
"Datagram":dgram,
"length":33}
def redir(data):
	'''First 4 bytes of data are the "gateway internet addr"'''
	gateway_addr=[d for d in data[:4]]
	ip_hdr=data[4:20]
	dgram=data[20:28]
	return {"Gateway Addr":gateway_addr,
"IP Header":ip_hdr,
"Datagram":dgram,
"length":36}
def timestamp(data):
	identifier=(data[0]<<8)+data[1]
	seq_num=(data[2]<<8)+data[3]
	orig_time=int(data[4:8].hex(),16)
	recv_time=int(data[8:12].hex(),16)
	trans_time=int(data[12:16].hex(),16)
	return {"Identifier":identifier,
"Sequence Number":seq_num,
"Orig Timestamp":orig_time,
"Recv Timestamp":recv_time,
"Transit Timestamp":trans_time,
"length":20}
def infoMsg(data):
	identifier=(data[0]<<8)+data[1]
	seq_num=(data[2]<<8)+data[3]
	return {"Identifier":identifier,
"Sequence Number":seq_num,
"length":8}

icmp_types={0:"echo_reply",
3:"dest_unreachable",
#4:"src_quench",
5:"redirect",
#6:"alt_host_addr",
8:"echo",
9:"router_advert",
10:"router_sel",
11:"time_exceeded",
12:"param_problem",
13:"timestamp",
14:"timestamp_relay",
15:"info_req",
16:"info_reply",
#17:"addr_mask_req",
#18:"addr_mask_reply",
#30:"tracert",
#31:"dgram_conversion_err",
#32:"mobile_host_redir",
#33:"ipv6_where",
#34:"ipv6_here",
#35:"mobile_reg_req",
#36:"mobile_reg_reply",
#37:"domain_name_req",
#38:"domain_name_reply",
#39:"skip",
40:"photuris",
41:"icmp_msg_experimental",
42:"ext_echo_req",
43:"ext_echo_reply"}
icmp_funcs={"echo_reply":echo,
"echo":echo,
"dest_unreachable":errorMsg,
"time_exceeded":errorMsg,
"param_problem":paramProb,
"redirect":redir,
"router_advert":advert,
"router_sel":advert,
"timestamp":timestamp,
"timestamp_relay":timestamp,
"info_req":infoMsg,
"info_reply":infoMsg}
icmp_messages=[0,8,9,10,11,12,13,14,15,16]  #Means header contains identifier and seq_num
