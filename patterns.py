from random import *

PROB1 = 0.0725
PROB2 = 0.15
PROB_CLEAR = 0.172
PROB_SLIDE = 0.185
PROB_ACCENT = 0.1625
PROB_OCT3 = 0.2
PROB_OCT4 = 0.1
PROB_OCT5 = 0.05
PROB_NOTE = 0.1

# Sequencer Programming
###########################################
scale_major = [0,2,4,5,7,9,11,12]
scale_dorian = [0,2,3,5,7,8,10,12]
scale_phrygian = [0,1,3,5,7,8,10,12]
scale_lydian  = [0,2,4,6,7,9,11,12]
scale_mixolydian = [0,2,4,5,7,9,10,12]
scale_minor = [0,2,3,5,7,8,10,12]
scale_locrian = [0,1,3,5,6,8,10,12]
chord_maj   = [0,4,7]
chord_maj7 = [0,4,7,11]
chord_min   = [0,3,7]
chord_dim   = [0,3,6]
chord_aug   = [0,4,8]

scale  = []
chord  = []
root    = 0

n = randint(0,6)
if(n == 0): 
	scale = scale_major
	chord = chord_maj
	
elif(n == 1):
	scale = scale_dorian
	chord = chord_min

elif(n == 2):
	scale = scale_phrygian
	chord = chord_min
	
elif(n == 3):
	scale = scale_lydian
	chord = chord_maj
	
elif(n == 4):
	scale = scale_mixolydian
	chord = chord_maj
elif(n == 5):
	scale = scale_minor
	chord = chord_min
elif(n == 6):
	scale = scale_locrian
	chord = chord_dim
	

################################################
#
################################################
def SEQ_Split4(pat1):
	s = pat1[0:4]
	return s+s+s+s
	
def SEQ_Split2(pat1):
	s = pat1[0:2]
	return s+s+s+s+s+s+s+s
	
def SEQ_Split8(pat1):
	s = pat1[0:8]
	return s+s
	
def SEQ_Arp1(chord):
	o = []
	for i in range(16/len(chord)):
		o = o + chord
	if((16 % len(chord)) > 0):
		o = o + chord[0:16 % len(chord)]
	return o
	
def SEQ_ProbScale(scale):
	o = []
	for i in range(16):
		c = choice(scale)
		if(random() > 0.1):
			c = c*2
		if(random() > 0.85):
			c = c + randint(1,4)*24
		o.append(c)
	return o
	
def SEQ_ScaleToMopho(seq):
	o = []
	last = 0
	for i in range(16):
		n = seq[i]
		if(n == -1):
			n = 0
			
		if(random() > 0.1):
			n = n*2		
			
		if(random() > 0.85):
			n = n + randint(1,2)*24
		elif(random() > 0.95):
			n = n + randint(1,4)*24
			
		o.append(n)
	return o
	
def SEQ_Bass1(chord):
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

def SEQ_Bass2(chord):
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

def SEQ_Bass3(chord):
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

def SEQ_Bass4(chord):
	o = []
	for i in range(4):
		c = chord[0]
		o.append(c)
		c = chord[2]
		o.append(c)		
		c = chord[0]
		o.append(c)
		c = chord[1]
		o.append(c)	
	return o

def SEQ_Bass5(chord):
	o = []
	for i in range(4):
		c = chord[0]
		o.append(c)
		c = chord[2]
		o.append(c)		
		c = chord[1]
		o.append(c)
		c = chord[0]
		o.append(c)
	return o

def SEQ_Bass6(chord):
	o = []
	for i in range(4):
		c = chord[0]
		o.append(c)
		o.append(c)
		c = chord[2]
		o.append(c)
		c = chord[1]
		o.append(c)
	return o

def SEQ_Merge(s1,s2):
	o = []
	for i in range(16):
		if(random() < 0.5):
			c = choice(s1)
		else:
			c = choice(s2)
		o.append(c)
	return o
	
def SEQ_BuildSequence(s1,s2):
	
	if(random() < 0.25): return s1
	if(random() < 0.25): return s2
	if(random() < 0.25): return s1[0:8] + s2[0:8]
	if(random() < 0.25): return s1[8:16] + s2[0:8]
	if(random() < 0.25): return s1[0:8] + s2[8:16]
	if(random() < 0.25): return s1[8:16] + s2[8:16]
	
	if(random() < 0.25): return SEQ_Split4(s1)
	if(random() < 0.25): return SEQ_Split2(s1)
	if(random() < 0.25): return SEQ_Split8(s1)

	if(random() < 0.25): return SEQ_Split4(s2)
	if(random() < 0.25): return SEQ_Split2(s2)
	if(random() < 0.25): return SEQ_Split8(s2)

	return SEQ_Merge(s1,s2)


def SEQ_Gen2(chord):
	root      = chord[0]
	second  = choice(chord)
	third      = choice(chord)
	
	n = randint(0,4)
	
	if(n == 0):
		p = [-1,root,-1,-1]
		
	elif(n == 1):
		p = [-1,root,root,-1]
		
	elif(n  == 2):
		p = [-1,root,-1,root]
		
	elif(n == 3):
		p = [-1,-1,root,root]
	
	elif(n == 4):
		p = [-1,root,root,root]
	
	if(random() < PROB1):
		n = randint(0,3)
		p[n] = second
		
	if(random() < PROB2):
		n = randint(0,3)
		p[n] = third
		
	return p
	
def SEQ_Gen1(chord):
	root      = chord[0]
	second  = choice(chord)
	third      = choice(chord)
	
	n = randint(0,5)
	if(n == 0):		
		p = [root,-1,-1,-1]		
	elif(n == 1):
		p = [root,-1,root,-1]				
	elif(n == 2):
		p = [root,-1,-1,root]	
	elif(n == 3):
		p = [root,-1,root,root]
	elif(n == 4):
		p = [root,root,-1,root]
	elif(n == 5):
		p = [root,root,root,-1]
	
		
	if(random() < PROB1):
		n = randint(0,3)
		p[n] = second
		
	if(random() < PROB2):
		n = randint(0,3)
		p[n] = third
		
	return p
	

def SEQ_Octaves(seq,shift=0):
	return SEQ_ScaleToMopho(seq)


def SEQ_BuildArp():
	a = SEQ_Arp1(chord)
	return a

def SEQ_BuildProbScale():	
	s = SEQ_ProbScale(scale)
	return s

def SEQ_BuildBass():
	seqo = []
	
	n = randint(0,5)
	if(n == 0):
		seqb = SEQ_Bass1(chord)
	elif(n == 1):
		seqb = SEQ_Bass2(chord)
	elif(n == 2):
		seqb = SEQ_Bass3(chord)
	elif(n == 3):
		seqb = SEQ_Bass4(chord)
	elif(n == 4):
		seqb = SEQ_Bass5(chord)
	else:
		seqb = SEQ_Bass6(chord)
	
	s =  seqb
	return s
	
def SEQ_BuildSequenceI(seq):
	if(random() < 0.4): 
		return seq
	
	if(random() < 0.5):
		n = randint(0,2)
		if(n == 0):
			s = SEQ_Split2(seq)
			return s
		elif(n == 1):
			s = SEQ_Split4(seq)
			return s
		else:
			s= SEQ_Split8(seq)
			return s
	
		
	
	
	if(random() < 0.4):
		a = SEQ_Arp1(chord)
		return a
		
	elif(random() < 0.5):
		s = SEQ_ProbScale(scale)
		return s
	else:
		s =  SEQ_BuildBass()
		return s
		
def SEQ_ScalePick(scale):
	out = []
	for i in range(16):
		n = choice(scale)
		out.append(n)
	return out
	
def SEQ_GenPattern():
	global chord,scale
	
	n = randint(0,1)
	
	p1 = SEQ_Gen1(scale)
	p2 = SEQ_Gen2(scale)
	p3 = SEQ_Gen1(scale)
	p4 = SEQ_Gen2(scale)
		

	n = randint(0,10)
	if(n == 0):
		s = p1+p1+p1+p1
	elif(n == 1):
		s = p1+p2+p1+p2
	elif(n == 2):
		s = p1+p2+p3+p2
	elif(n == 3):
		s = p1+p1+p2+p2
	elif(n == 4):
		s = p1+p2+p3+p4
	elif(n == 5):
		s = p3+p2+p1+p2
	elif(n == 6):
		s = p3+p2+p1+p4
	elif(n == 7):
		s = p1+p3+p1+p4
	elif(n == 8):
		s = p1+p4+p3+p2
	elif(n == 9):
		s = p1+p4+p3+p2
	else:
		s = p3+p2+p4+p1
		
	
	return s
	
	
def PAT_Pattern():
	p = SEQ_GenPattern()
	if(random() < 0.25): p = SEQ_BuildSequenceI(p)
	return p
	
				
def PAT_BuildPattern(seq):
	p1 = PAT_Pattern()
	p2 = PAT_Pattern()
	p   = p1+p2
	print len(p1)
	for i in range(len(seq)):
		if(p[i] != -1):
			p[i] = seq[i]
		elif(random() < PROB1):
			p[i] = seq[i]
		elif(random() < PROB2):
			p[i] = seq[i]
			
	return p
	
def PAT_ShiftRoot(seq,note):
	o = []
	for i in range(len(seq)):
		n = seq[i] + note
		o.append(n)
	return o

	
###############################################
# [----]
# [-1--]
# [--1-]
# [---1]
# [-11-]
# [-1-1]
# [--11]
# [-111]
# [1---]
# [11--]
# [1-1-]
# [1--1]
# [111-]
# [11-1]
# [1-11]
# [1111]
################################################

def GEN_Lead():
	n = randint(0,7)
	if( n == 0) : return [1,-1,-1,-1]
	elif(n ==1): return [1,1,-1,-1]
	elif(n ==2): return [1,-1,1,-1]
	elif(n ==3): return [1,-1,-1,1]
	elif(n == 4): return [1,1,1,-1]
	elif(n == 5): return [1,1,-1,1]
	elif(n == 6): return [1,-1,1,1]
	return [1,1,1,1]
	
def GEN_Follow():
	n = randint(0,7)
	if(n == 0): return [-1,1,-1,-1]
	elif(n == 1): return [-1,-1,1,-1]
	elif(n == 2): return [-1,1,1,-1]
	elif(n == 3): return [-1,1,-1,1]
	elif(n == 4): return [-1,-1,1,1]
	elif(n == 5): return [-1,1,1,1,]
	return [-1,-1,-1,-1]
	
	
def GEN_Fill(chord,seq):
	root = chord[0]
	o  = []
	for n in seq:
		if(n == 1):
			n = root
			if(random() < PROB1): n = choice(chord)
			elif(random() < PROB2): n = choice(chord)
		o.append(n)
	return o
	
def GEN_BasicPattern():
	global scale,chord
	p1 = GEN_Lead()
	p2 = GEN_Follow()
	p3 = GEN_Lead()
	p4 = GEN_Follow()
	
	seq= p1+p2+p3+p4
	if(random() < 0.5):
		seq= GEN_Fill(scale,seq)
	else:
		seq= GEN_Fill(chord,seq)
		
	return seq

def GEN_ComplexPattern():			
	s1 = PAT_Pattern()
	s2 = PAT_Pattern()
	s3 = PAT_Pattern()
	s4 = PAT_Pattern()	
	s5 = SEQ_ScalePick(scale)
	s6 = SEQ_ScalePick(scale)
	
	seq1 = SEQ_BuildSequence(s1,s2)
	seq2 = SEQ_BuildSequence(s3,s4)
	seq3 = SEQ_BuildSequence(s5,s6)
	
	seqA = SEQ_BuildSequence(seq1,seq2)
	seqB = SEQ_BuildSequence(seq1,seq3)
	seqC = SEQ_BuildSequence(seq2,seq3)
	seq   = SEQ_BuildSequence(seqA,seqB) 
	return seq
	
def GEN_SimplePattern():		
	s1 = PAT_Pattern()
	seq = s1
	return seq

def GEN_BassPattern():		
	s1 = SEQ_BuildBass()
	s2 = SEQ_BuildBass()
	seq1 = SEQ_BuildSequence(s1,s2)
	s1 = SEQ_BuildBass()
	s2 = SEQ_BuildBass()
	seq2 = SEQ_BuildSequence(s1,s2)
	return SEQ_BuildSequence(seq1,seq2)
	
	
def GEN_CreatePattern():
	n = randint(0,3)
	
	if(n == 0):
		seq = GEN_BasicPattern()
	elif(n == 1):
		seq = GEN_SimplePattern()
	elif(n == 2):
		seq = GEN_BassPattern()
	else:
		seq = GEN_ComplexPattern()
		
	seq = SEQ_ScaleToMopho(seq)
	return seq[0:16]