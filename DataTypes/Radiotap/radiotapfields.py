##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2021.07.03
## Description:    Tools to process radiotap related data
## Notes:
## Updates:
from ..datatools import revBytes
class ANTENNA():
	def __init__(self, raw):
		self.raw=raw
		self.length=0
