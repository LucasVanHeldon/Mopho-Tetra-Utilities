

from random import *
import array
import os

MUT_RATE = 0.05

###########################################
# Sequencer Programming
###########################################
scale_major = [0,2,4,5,7,9,11,12]
scale_minor = [0,2,3,5,7,8,10,12]
chord_maj   = [0,4,7]
chord_maj7 = [0,4,7,11]
chord_min   = [0,3,7]
chord_dim   = [0,3,6]
chord_aug   = [0,4,8]

def Split4(pat1):
	s = pat1[0:4]
	return s+s+s+s
	
def Split2(pat1):
	s = pat1[0:2]
	return s+s+s+s+s+s+s+s
	
def Split8(pat1):
	s = pat1[0:8]
	return s+s
	
def Arp1(chord):
	o = []
	for i in range(16/len(chord)):
		o = o + chord
	if((16 % len(chord)) > 0):
		o = o + chord[0:16 % len(chord)]
	return o
	
def ProbScale(scale):
	o = []
	for i in range(16):
		c = choice(scale)
		if(random() > 0.1):
			c = c*2
		if(random() > 0.85):
			c = c + randint(1,4)*24
		o.append(c)
	return o
	
def ScaleToMopho(seq):
	o = []
	for i in range(16):
		n = seq[i]
		if(random() > 0.1):
			n = n*2		
		if(random() > 0.85):
			n = n + randint(1,4)*24
		o.append(n)
	return o
	
def Bass1(chord):
	o = []
	for i in range(4):
		c = chord[0]
		o.append(c)
		o.append(c)
		c = chord[1]
		o.append(c)
		c = chord[2]
		o.append(c)
	return o

def Bass2(chord):
	o = []
	for i in range(4):
		c = chord[0]
		o.append(c)
		c = chord[1]
		o.append(c)		
		c = chord[2]
		o.append(c)
		c = chord[0]
		o.append(c)
	return o

def Bass3(chord):
	o = []
	for i in range(4):
		c = chord[0]
		o.append(c)
		c = chord[1]
		o.append(c)		
		c = chord[0]
		o.append(c)
		c = chord[2]
		o.append(c)	
	return o
	
def BuildSequenceI(seq):
	if(random() < 0.4): 
		return seq
	
	if(random() < 0.5):
		n = randint(0,2)
		if(n == 0):
			s = Split2(seq)
			return s
		elif(n == 1):
			s = Split4(seq)
			return s
		else:
			return Split8(seq)
	
		
	if(random() < 0.5): 
		chord = chord_min
		scale = scale_minor
		
	else: 
		chord = chord_maj
		scale = scale_major
	
	if(random() < 0.4):
		a = Arp1(chord)
		a = ScaleToMopho(a)
		return a
		
	if(random() < 0.5):
		s = ProbScale(scale)
		s = ScaleToMopho(s)
		return s
	
	
	seqo = []
	
	n = randint(0,2)
	if(n == 0):
		seqb = Bass1(chord)
	elif(n == 1):
		seqb = Bass2(chord)
	else:
		seqb = Bass3(chord)
	
	s =  seqb+seqb+seqb+seqb+seqb+seqb[0:1]
	s = ScaleToMopho(s)
	
	return s
	
def Merge(s1,s2):
	o = []
	for i in range(16):
		if(random() < 0.5):
			c = choice(s1)
		else:
			c = choice(s2)
		o.append(c)
	return o
	
def BuildSequence(seq):
	s1 = BuildSequenceI(seq)
	s2 = BuildSequenceI(seq)
	
	if(random() < 0.5): return s1
	if(random() < 0.5): return s2
	if(random() < 0.5): return s1[0:8] + s2[0:8]
	if(random() < 0.5): return s1[8:16] + s2[0:8]
	if(random() < 0.5): return s1[0:8] + s2[8:16]
	if(random() < 0.5): return s1[8:16] + s2[8:16]
	
	if(random() < 0.5): return Split4(s1)
	if(random() < 0.5): return Split2(s1)
	if(random() < 0.5): return Split8(s1)

	if(random() < 0.5): return Split4(s2)
	if(random() < 0.5): return Split2(s2)
	if(random() < 0.5): return Split8(s2)

	return Merge(s1,s2)

############################################
# Mutation Stuff
############################################
def Mutate(p):
	if(random() < MUT_RATE):
		return int(random()*255)
	return p
	
	
def Splice(p1,p2):	
	n = randint(1,len(p1)-1)
	o = p1[0:n] + p2[n:]
	for i in range(len(o)):
		o[i] = Mutate(o[i])
	return o

def Interp(p1,p2,amt=0.5):
	o = []
	for i in range(len(p1)):
		x = (1.0-amt)*p1[i] + amt*p2[i]
		x = int(x)
		o.append(Mutate(x))
	return o

def Select(p1,p2):
	out = p1[:]
	i = 0
	for x in p2:
		if(random() < 0.5): out[i] = x
		i = i + 1
	return out

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
	
	for i in range(0,252,7):
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
		
	i = 252
	a7 = (data[i+0] & 0x80) >> 7
	b7 = (data[i+1] & 0x80) >> 6
	c7 = (data[i+2] & 0x80) >> 5
	d7 = (data[i+3] & 0x80) >> 4
	
	d1 = a7 | b7 | c7 | d7 
	d2 = data[i+0] & 0x7f
	d3 = data[i+1] & 0x7f
	d4 = data[i+2] & 0x7f
	d5 = data[i+3] & 0x7f
		
	out = out + [d1,d2,d3,d4,d5]
	return out	
		
def UnpackBits(data):
	out = []
	
	for i in range(0,288,8):
		
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
		
	
	i = 288
	e7 = (data[i+0] & 0x10) << 1
	d7 = (data[i+0] & 0x8) << 2
	c7 = (data[i+0] & 0x4) << 3
	b7 = (data[i+0] & 0x2) << 4
	a7 = (data[i+0] & 0x01) << 5
	
	o1 = data[i+1] | a7
	o2 = data[i+2] | b7
	o3 = data[i+3] | c7
	o4 = data[i+4] | d7

	out = out + [o1,o2,o3,o4]
	return out



############################################
# Sysex Data list funcs
############################################
def GET_Osc1(data):
	osc1 = data[0:6][:]
	return osc1
	
def GET_Osc2(data):
	osc2 = data[6:12][:]
	return osc2

def GET_OscMisc(data):
	return data[12:20][:]
	
def GET_Sync(data):
	return data[12][:]
	
def SET_Sync(data,sync):
	data[12] = sync
	
def GET_GlideMode(data):
	return data[13]
	
def SET_GlideMode(data,g):
	data[13] = g
	
def GET_OscSlop(data):
	return data[14]
	
def SET_OscSlop(data,slop):
	data[14] = slop
	
def GET_PBR(data):
	return data[15]
	
def SET_PBR(data,pbr):
	data[15] = pbr 
	
def GET_OscMix(data):
	return data[17] 
	
def SET_OscMix(data,mix):
	data[17] = mix
	
def GET_KeyAssign(data):
	return data[16]
	
def SET_KeyAssign(data,ka):
	data[16] = ka

def GET_ExtAudio(data):
	return data[18]
	
def SET_ExtAudio(data,lvl):
	data[18] = lvl
	
def GET_Oscillators(data):
	return data[0:20][:]
	
def GET_Filter(data):
	return data[20:32][:]
		
def GET_VCA(data):
	return data[32:41][:]

def GET_LFO1(data):
	return data[41:46][:]
	
def GET_LFO2(data):
	return data[46:51][:]
	
def GET_LFO3(data):
	return data[51:56][:]
	
def GET_LFO4(data):
	return data[56:61][:]
	
def GET_ENV3(data):
	return data[61:70][:]
	
def GET_MOD1(data):
	return data[70:73][:]

def GET_MOD2(data):
	return data[73:76][:]

def GET_MOD3(data):
	return data[76:79][:]

def GET_MOD4(data):
	return data[79:82][:]

def GET_MISC(data):
	return data[82:110][:]
	
def GET_MODULATORS(data):
	return data[82:95][:]
	
def GET_Clock(data):
	return data[95:97][:]
	
def GET_Arp(data):
	return data[97:99][:]
	
def GET_SeqTrig(data):
	return data[99:101][:]
	
def GET_SeqDest(data):
	return data[101:105][:]
	
def GET_Assign(data):
	return data[105:109][:]
	
def GET_Seq1(data):
	return data[120:136][:]
	
def GET_Seq2(data):
	return data[136:152][:]
	
def GET_Seq3(data):
	return data[152:168][:]
	
def GET_Seq4(data):
	return data[168:184][:]
	
def GET_NAME(data):
	return data [184:200][:]
	
def BuildLFOs(lfo1,lfo2,lfo3,lfo4):
	return lfo1+lfo2+lfo3+lfo4
	
def BuildMod(env3,mod1,mod2,mod3,mod4,modulators):
	return env3+mod1+mod2+mod3+mod4+modulators
	
def BuildArp(clock,arp):
	return clock+arp
	
def BuildSeqAssign(seqtrig,seqdest,assign):
	return seqtrig+seqdest+assign
	
def BuildSeq(seq1,seq2,seq3,seq4):
	return seq1+seq2+seq3+seq4
	
def BuildData(osc1,osc2,oscmisc, filter,vca,lfos,mod,misc,seq,name):
	data = osc1 + osc2 + oscmisc + filter + vca + lfos + mod + misc 
	data = data + [0]*10
	data = data + seq + name + [0]*56
	return data


############################################
# 'Gen' Operators
############################################

OP_MODE = 2

def OpOSC1(p1,p2,amt=0.5):
	p1o1 = GET_Osc1(p1)
	p2o1 = GET_Osc1(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o1
	elif(n == 1):
		return Splice(p1o1,p2o1)
	elif(n == 2):
		return Interp(p1o1,p2o1,amt)
	elif(n == 3):
		return Select(p1o1,p2o1)
	else:
		return p2o1

def OpOSC2(p1,p2,amt=0.5):
	p1o2 = GET_Osc2(p1)
	p2o2 = GET_Osc2(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2
		
def OpOscMisc(p1,p2,amt=0.5):
	p1o2 = GET_OscMisc(p1)
	p2o2 = GET_OscMisc(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)
			
	else:
		return p2o2

def OpFilter(p1,p2,amt=0.5):
	p1o2 = GET_Filter(p1)
	p2o2 = GET_Filter(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)
			
	else:
		return p2o2


def OpVCA(p1,p2,amt=0.5):
	p1o2 = GET_VCA(p1)
	p2o2 = GET_VCA(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)
	
	else:
		return p2o2


def OpLFO1(p1,p2,amt=0.5):
	p1o2 = GET_LFO1(p1)
	p2o2 = GET_LFO1(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)
	
	else:
		return p2o2


def OpLFO2(p1,p2,amt=0.5):
	p1o2 = GET_LFO2(p1)
	p2o2 = GET_LFO2(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)
	
	else:
		return p2o2

def OpLFO3(p1,p2,amt=0.5):
	p1o2 = GET_LFO3(p1)
	p2o2 = GET_LFO3(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)
	
	else:
		return p2o2

def OpLFO4(p1,p2,amt=0.5):
	p1o2 = GET_LFO4(p1)
	p2o2 = GET_LFO4(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)
	
	else:
		return p2o2

def OpEnv3(p1,p2,amt=0.5):
	p1o2 = GET_ENV3(p1)
	p2o2 = GET_ENV3(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)

	else:
		return p2o2


def OpMOD1(p1,p2,amt=0.5):
	p1o2 = GET_MOD1(p1)
	p2o2 = GET_MOD1(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)

	else:
		return p2o2

def OpMOD2(p1,p2,amt=0.5):
	p1o2 = GET_MOD2(p1)
	p2o2 = GET_MOD2(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)

	else:
		return p2o2

def OpMOD3(p1,p2,amt=0.5):
	p1o2 = GET_MOD3(p1)
	p2o2 = GET_MOD3(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)

	else:
		return p2o2
		
def OpMOD4(p1,p2,amt=0.5):
	p1o2 = GET_MOD4(p1)
	p2o2 = GET_MOD4(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)

	else:
		return p2o2

def OpMOD4(p1,p2,amt=0.5):
	p1o2 = GET_MOD4(p1)
	p2o2 = GET_MOD4(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)

	else:
		return p2o2


def OpMods(p1,p2,amt=0.5):
	p1o2 = GET_MODULATORS(p1)
	p2o2 = GET_MODULATORS(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)

	else:
		return p2o2

def OpClock(p1,p2,amt=0.5):
	p1o2 = GET_Clock(p1)
	p2o2 = GET_Clock(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)

	else:
		return p2o2

def OpArp(p1,p2,amt=0.5):
	p1o2 = GET_Arp(p1)
	p2o2 = GET_Arp(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)

	else:
		return p2o2


def OpMisc(p1,p2,amt=0.5):
	p1o2 = GET_MISC(p1)
	p2o2 = GET_MISC(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)

	else:
		return p2o2

def OpSEQ1(p1,p2,amt=0.5):
	p1o2 = GET_Seq1(p1)
	p2o2 = GET_Seq1(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)

	else:
		return p2o2

def OpSEQ2(p1,p2,amt=0.5):
	p1o2 = GET_Seq2(p1)
	p2o2 = GET_Seq2(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)
		
	else:
		return p2o2

def OpSEQ3(p1,p2,amt=0.5):
	p1o2 = GET_Seq3(p1)
	p2o2 = GET_Seq3(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)
	
	else:
		return p2o2

def OpSEQ4(p1,p2,amt=0.5):
	p1o2 = GET_Seq4(p1)
	p2o2 = GET_Seq4(p2)
	
	if(OP_MODE != -1): n = OP_MODE
	else:  n = randint(0,3)
	
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	elif(n == 3):
		return Select(p1o2,p2o2)
		
	else:
		return p2o2

def OpNAME(p1,p2,amt=0.5):
	p1o2 = GET_NAME(p1)
	p2o2 = GET_NAME(p2)
	return Splice(p1o2,p2o2)


###########################################
# Generation with Sequencer Mods
###########################################
def DoSeqGeneration(data1,data2,num,filebase):

	for i in range(num):		
		x = random()
		osc1 = OpOSC1(data1,data2,x)
		osc2 = OpOSC2(data1,data2,x)
		oscmisc = OpOscMisc(data1,data2,x)
		filt = OpFilter(data1,data2,x)
		vca = OpVCA(data1,data2,x)
		lfo1 = OpLFO1(data1,data2,x)
		lfo2 = OpLFO2(data1,data2,x)
		lfo3 = OpLFO3(data1,data2,x)
		lfo4 = OpLFO4(data1,data2,x)
		env3 = OpEnv3(data1,data2,x)
		mod1 = OpMOD1(data1,data2,x)
		mod2 = OpMOD2(data1,data2,x)
		mod3 = OpMOD3(data1,data2,x)
		mod4 = OpMOD4(data1,data2,x)
		modulators = OpMods(data1,data2,x)
		clock  = OpClock(data1,data2,x)
		arp    = OpArp(data1,data2,x)
		misc = OpMisc(data1,data2,x)		
		seq1 = OpSEQ1(data1,data2,x)
		seq2 = OpSEQ2(data1,data2,x)
		seq3 = OpSEQ3(data1,data2,x)
		seq4 = OpSEQ4(data1,data2,x)
		
		seq1 = BuildSequence(seq1)
		seq2 = BuildSequence(seq2)
		seq3 = BuildSequence(seq3)
		seq4 = BuildSequence(seq4)
		
		name = OpNAME(data1,data2,x)


		up = osc1+osc2+oscmisc+filt+vca+lfo1+lfo2+lfo3+lfo4
		up = up + env3 + mod1 + mod2 + mod3 + mod4 + misc
		up = up + [0]*10
		up = up + seq1+seq2+seq3+seq4+name+[0]*56		
		pk = PackBits(up)
		sysx_hdr = [0xF0,0x01,0x25,0x02,0,0]
		a = array.array('B')
		a.fromlist(sysx_hdr+pk+[0xF7])
		f = open(filebase+str(i)+'.syx','wb')
		a.tofile(f)
		f.close()
	
###########################################
# Single Cross Mutation
###########################################
def DoMutation(data1,data2):
	x = random()
	osc1 = OpOSC1(data1,data2,x)
	osc2 = OpOSC2(data1,data2,x)
	oscmisc = OpOscMisc(data1,data2,x)
	filt = OpFilter(data1,data2,x)
	vca = OpVCA(data1,data2,x)
	lfo1 = OpLFO1(data1,data2,x)
	lfo2 = OpLFO2(data1,data2,x)
	lfo3 = OpLFO3(data1,data2,x)
	lfo4 = OpLFO4(data1,data2,x)
	env3 = OpEnv3(data1,data2,x)
	mod1 = OpMOD1(data1,data2,x)
	mod2 = OpMOD2(data1,data2,x)
	mod3 = OpMOD3(data1,data2,x)
	mod4 = OpMOD4(data1,data2,x)
	modulators = OpMods(data1,data2,x)
	clock  = OpClock(data1,data2,x)
	arp    = OpArp(data1,data2,x)
	misc = OpMisc(data1,data2,x)		
	seq1 = OpSEQ1(data1,data2,x)
	seq2 = OpSEQ2(data1,data2,x)
	seq3 = OpSEQ3(data1,data2,x)
	seq4 = OpSEQ4(data1,data2,x)
	name = OpNAME(data1,data2,x)


	up = osc1+osc2+oscmisc+filt+vca+lfo1+lfo2+lfo3+lfo4
	up = up + env3 + mod1 + mod2 + mod3 + mod4 + misc
	up = up + [0]*10
	up = up + seq1+seq2+seq3+seq4+name+[0]*56		
	return up


###########################################
# Breed a generation
###########################################
def DoGeneration(data1,data2,num,filebase='bank'):

	for i in range(num):		
		x = random()
		print 'Generation: ',i
		osc1 = OpOSC1(data1,data2,x)
		osc2 = OpOSC2(data1,data2,x)
		oscmisc = OpOscMisc(data1,data2,x)
		filt = OpFilter(data1,data2,x)
		vca = OpVCA(data1,data2,x)
		lfo1 = OpLFO1(data1,data2,x)
		lfo2 = OpLFO2(data1,data2,x)
		lfo3 = OpLFO3(data1,data2,x)
		lfo4 = OpLFO4(data1,data2,x)
		env3 = OpEnv3(data1,data2,x)
		mod1 = OpMOD1(data1,data2,x)
		mod2 = OpMOD2(data1,data2,x)
		mod3 = OpMOD3(data1,data2,x)
		mod4 = OpMOD4(data1,data2,x)
		modulators = OpMods(data1,data2,x)
		clock  = OpClock(data1,data2,x)
		arp    = OpArp(data1,data2,x)
		misc = OpMisc(data1,data2,x)		
		seq1 = OpSEQ1(data1,data2,x)
		seq2 = OpSEQ2(data1,data2,x)
		seq3 = OpSEQ3(data1,data2,x)
		seq4 = OpSEQ4(data1,data2,x)
		name = OpNAME(data1,data2,x)


		up = osc1+osc2+oscmisc+filt+vca+lfo1+lfo2+lfo3+lfo4
		up = up + env3 + mod1 + mod2 + mod3 + mod4 + misc
		up = up + [0]*10
		up = up + seq1+seq2+seq3+seq4+name+[0]*56		
		pk = PackBits(up)
		sysx_hdr = [0xF0,0x01,0x25,0x02,0,0]
		a = array.array('B')
		a.fromlist(sysx_hdr+pk+[0xF7])
		f = open(filebase+str(i)+'.syx','wb')
		a.tofile(f)
		f.close()

############################################
# Breed Children + Grand children
############################################



def Breed(p1,p2,p3,p4,num,gsc='gc1',ps1='p1',ps2='p2'):
	for j in range(num):
		c1 = DoMutation(p1,p2)
		c2 = DoMutation(p3,p4)
		DoSeqGeneration(c1,c2,num,gsc+str(j))
	DoGeneration(p1,p2,num,ps1)
	DoGeneration(p3,p4,num,ps2)

def Breed2(p1,p2,num,gsc='gc1',ps1='p1',ps2='p2'):
	for j in range(num):
		c1 = DoMutation(p1,p2)		
		DoSeqGeneration(c1,c2,num,gsc+str(j))
	DoGeneration(p1,p2,num,ps1)


def GenOP(filename1,filename2,filename3,filename4,gsc,ps1,ps2):
	
	d1 = OpenFile(filename1)
	d2 = OpenFile(filename2)
	d3 = OpenFile(filename3)
	d4 = OpenFile(filename4)

	
	if(len(d1) == 298):
		n = 4
	else:
		n = 6
		
	data1 = UnpackBits(d1[n:-1])		
	
	if(len(d2) == 298):
		n = 4
	else:
		n = 6
	
	data2 = UnpackBits(d2[n:-1])
	
	if(len(d3) == 298):
		n = 4
	else:
		n = 6
	
	data3 = UnpackBits(d3[n:-1])
	
	if(len(d4) == 298):
		n = 4
	else:
		n = 6
	
	data4 = UnpackBits(d4[n:-1])

	Breed(data1,data2,data3,data4,20,gsc,ps1,ps2)
	
############################################
# Used to split bank file (contigous sysex patches) into individual patch syx
# Eg - The Presets come as a 'bank' file of 3x128 patches 
############################################
def SplitPresets():
	data = OpenFile('../Tetra_ProgramsCombos_1.0.syx')		
	for i in range(0,3):
		for j in range(0,128):
			n1 = i*127+j			
			n1 = n1 * 300
			p = data[n1:n1+300]
			a = array.array('B')
			a.fromlist(p)
			f = open('data_b'+str(i)+'p'+str(j)+'.syx','wb')
			a.tofile(f)
			f.close()
			


	
def gen():	
	files = os.listdir('..\Patches')
	
	for i in range(0,len(files),4):
		filename1 = '..\Patches\\'+files[i]
		filename2 = '..\Patches\\'+files[i+1]
		filename3 = '..\Patches\\'+files[i+2]
		filename4 = '..\Patches\\'+files[i+3]
	
		GenOP(filename1,filename2,filename3,filename4,
			'cross'+str(randint(0,99999)),
			'mp1'+str(randint(0,99999)),
			'mp2'+str(randint(0,99999)))

def Gen2():
	files = os.listdir('..\Patches')
	for i in range(0,len(files),4):
		filename1 = '..\Patches\\'+files[i]
		filename2 = '..\Patches\\'+files[i+1]	
		
		d1 = OpenFile(filename1)
		d2 = OpenFile(filename2)
		
		if(len(d1) == 298):
			n = 4
		else:
			n = 6
			
		data1 = UnpackBits(d1[n:-1])		
		
		if(len(d2) == 298):
			n = 4
		else:
			n = 6
		
		data2 = UnpackBits(d2[n:-1])
			
	
		Breed2(data1,data2,30)
	
SplitPresets()