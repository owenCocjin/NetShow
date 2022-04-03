# NetShow
> Easy way to visualize network traffic

---

## Usage:
Run `./netshow.py [interface]` as root. Root is required to open a raw socket.

## Hotkeys:
- Toggle labels: [space]
> Default ON

- Set a label: [ctrl+l]
	- Arrows up/down to select the IP to edit.
	- Enter to choose the selected IP
	- Type the new label and press [enter]
	- To cancel, press [enter] without typing anything

## Known Bugs:
- [bug:001]: While typing a label name, the user can use the arrow keys to move around. Doing so will enter the chars '[A' into the label name
- [bug:002]: Once an IP is assigned a subnet, all IPs that share ANY subnet with the original one will gain the ORIGINAL's ip. Ex:

```
orig = 192.168.0.10/24
new1 = 192.168.0.20/24
new2 = 192.168.250.100/24  <- This only shares subnet /16 and should be assigned /16
```

- **[bug:003]:** Some packets will cause the tool to crash. Unfortunately, at this time it's not 100% clear exactly what packets cause the crash (I believe its something to do with IPv6 ICMP)
- **[bug:004]:** I've noticed that the tool can (quite rarely) freeze for an unknown reason
- **[bug:005]:** Program doesn't cooperate with IPv6 at all. Mostly causes crashes.
- ~~**[bug:006]:** Current method of determining IP can result in incorrect IP being determined as user's~~  Solved by getting IP through IOCTL

## Future Additions:
- Add multiple pages once grid is full of IPs. Currently, any more IPs will be ignored
