##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2022.04.03
## Description:    Miscellaneous functions

def readUntil(b,f):
	'''Read from a file one byte at a time until 'b' is met.
	Includes 'b' '''
	if type(b)!=list:
		b=[b]
	toret=f.read(1)
	buff=toret

	while buff not in b:
		buff=f.read(1)
		toret+=buff

	return toret

def bToI(b):
	'''Returns an int'''
	toret=0
	for i in b:
		toret=(toret<<8)+i
	return toret

def decodeMac(b):
	'''Returns a string from bytes representing a MAC address'''
	toret=''
	for m in b:
		toret+=f"{hex(m)[2:]}:"

	return toret[:-1]

def ipInCIDR(ip,other,cidr_masks):
	'''Returns True and the first equal mask where both ips are the same'''
	#Convert both to ints
	hex_ip=0
	hex_other=0

	ip=ip.split('.')
	other=other.split('.')

	for i,n in enumerate(ip):
		n=int(n)
		hex_ip+=n<<(8*(3-i))
	for i,n in enumerate(other):
		n=int(n)
		hex_other+=n<<(8*(3-i))

	#Check against netmask
	for mask in cidr_masks:
		#Convert mask to int
		int_mask=(2**32-1)-(2**(32-mask)-1)

		#Apply masks to IPs
		masked_ip=hex_ip&int_mask
		masked_other=hex_other&int_mask

		#If they're the same, return the mask int
		if masked_ip==masked_other:
			return mask

	#These IPs are not the same, regardless of the mask
	return None
		# print(f"ip:    {bin(masked_ip)[2:]:>032}")
		# print(f"other: {bin(masked_other)[2:]:>032}")


if __name__=="__main__":
	ipInCIDR("192.168.1.12","192.168.1.10",[31,30,29,28,27,26,25,24,21])
