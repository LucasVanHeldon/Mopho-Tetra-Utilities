###########################################
# Tetra
###########################################

from random import *
import array
import os

############################################
# Files
############################################
def OpenFile(filename):
	f = open(filename,'rb')
	a = array.array('B')
	statinfo = os.stat(filename)
	a.fromfile(f,statinfo.st_size)
	f.close()

	return a.tolist()


############################################
# Pack/Unpack data
############################################
def PackBits(data):

	out = []
	
	for i in range(0,384,7):
		a7 = (data[i+0] & 0x80) >> 7
		b7 = (data[i+1] & 0x80) >> 6
		c7 = (data[i+2] & 0x80) >> 5
		d7 = (data[i+3] & 0x80) >> 4
		e7 = (data[i+4] & 0x80) >> 3
		f7 = (data[i+5] & 0x80) >> 2
		g7 = (data[i+6] & 0x80) >> 1
	
		d1 = a7 | b7 | c7 | d7 | e7 | f7 | g7
		d2 = data[i+0] & 0x7f
		d3 = data[i+1] & 0x7f
		d4 = data[i+2] & 0x7f
		d5 = data[i+3] & 0x7f
		d6 = data[i+4] & 0x7f
		d7 = data[i+5] & 0x7f
		d8 = data[i+6] & 0x7f
	
		out = out + [d1,d2,d3,d4,d5,d6,d7,d8]
		
		
	return out	
		
def UnpackBits(data):
	out = []
	
	for i in range(0,446,8):
		
		g7 = (data[i+0] & 0x40) << 1
		f7 = (data[i+0]  & 0x20) << 2
		e7 = (data[i+0] & 0x10) << 3
		d7 = (data[i+0] & 0x8) << 4
		c7 = (data[i+0] & 0x4) << 5
		b7 = (data[i+0] & 0x2) << 6
		a7 = (data[i+0] & 0x01) << 7
	
		o1 = data[i+1] | a7
		o2 = data[i+2] | b7
		o3 = data[i+3] | c7
		o4 = data[i+4] | d7
		o5 = data[i+5] | e7
		o6 = data[i+6] | f7
		o7 = data[i+7] | g7
	
		out = out + [o1,o2,o3,o4,o5,o6,o7]
		
	
		
	return out





############################################
# Used to split bank file (contigous sysex patches) into individual patch syx
# Eg - The Presets come as a 'bank' file of 3x128 patches 
############################################
def SplitPresets():
	data = OpenFile('../Tetra_ProgramsCombos_1.0.syx')		
	for i in range(0,4):
		for j in range(0,128):
			n1 = i*127+j			
			n1 = n1 * 446
			p = data[n1:n1+446]
			a = array.array('B')
			a.fromlist(p)
			f = open('data_b'+str(i)+'p'+str(j)+'.syx','wb')
			a.tofile(f)
			f.close()
			
	
SplitPresets()