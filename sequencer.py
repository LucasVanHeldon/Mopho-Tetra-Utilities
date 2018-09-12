
# Mopho Sequence Looper

# Record/Overdub
# Assign sequences to keyboard + play

from random import *
import mido
from mido.ports import MultiPort
import array
from time import *
import os,glob
import threading
from patterns import *

mido.set_backend('mido.backends.rtmidi_python')
outp= mido.get_output_names()
inp = mido.get_input_names()

MOPHO_CHANNEL = 0x0

print "Midi Outputs"
for x in outp:
	print x
	
print "Midi Inputs"
for y in inp:
	print y
	
keyboard_input = mido.open_input(inp[2])
clock = mido.open_input(inp[0])
mopho_output  = mido.open_output(outp[4])

notes = {}
name_notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

RESET = 126
REST=127


NRPN_SEQ1_STEP1 = 120
NRPN_SEQ2_STEP1 = 136
NRPN_SEQ3_STEP1 = 152
NRPN_SEQ4_STEP1 = 168


x = 0
y = 0

for i in range(0,125,2):
	
	note = name_notes[x]
	s1 = note + str(y)
	s2 = note + str(y) + '+'
	
	notes[s1] = i
	notes[s2] = i+1
	
	x = x + 1
	x = x % len(name_notes)
	
	if x == 0: y = y + 1
	notes[i] = i
	notes[i+1] = i+1
	
notes[126] = 126
notes[127] = 127
notes['REST'] = 127
notes['RESET'] = 126

# nrpn = first step of sequence
# step  = 0..15 for step
# value = 0..127
def SendSeqStep(nrpn, step,value):
	byte = 0xB0+MOPHO_CHANNEL
	nrpn_step  = nrpn+step
	msb = (nrpn_step >> 7 ) & 0x7F
	lsb   = (nrpn_step & 0x7F)
	nrpn1 = [byte,0x63,msb]
	nrpn2 = [byte,0x62,lsb]
	nrpn3 = [byte,0x6,0]
	nrpn4 = [byte,0x26,value]
	
	mopho_output.send(mido.Message.from_bytes(nrpn1))
	mopho_output.send(mido.Message.from_bytes(nrpn2))
	mopho_output.send(mido.Message.from_bytes(nrpn3))
	mopho_output.send(mido.Message.from_bytes(nrpn4))
	
def SendSequenceNotes(sequence_step1, seq):
	print seq
	for i in range(len(seq)):
		SendSeqStep(sequence_step1,i,notes[seq[i]])
		
def MSG(msg):
	return mido.Message.from_bytes(msg)
	
# sequence to send to mopho using NRPN
seq1 = ['C2','C2','REST','C2+','C2','C2','REST','C2+','C2','C2','REST','C2+','C2','C2','REST','C2+']
buffer = [0]*16

keyboard = {}
for i in range(128):
	pattern = GEN_CreatePattern()
	keyboard[i] = pattern
	
ROOT = 48
last_note = 24
last_vel = 127
class MIDIClock(threading.Thread):

	def run(self):
		global last_note,last_vel
		while 1:
			key = clock.receive().bytes()
			if(key[0] == 0xF8): 			
				mopho_output.send(MSG(key))	
			elif(key[0] == 0xFC): 
				mopho_output.send(MSG([0x80+MOPHO_CHANNEL,last_note,last_vel]))


def Record():
	#SendSequenceNotes(NRPN_SEQ1_STEP1,seq1)
	mopho_output.send(mido.Message.from_bytes([0x90,24,127]))
	step = 0
	while 1:
		key = keyboard_input.receive().bytes()
		
		if(key[0] == 0x90+MOPHO_CHANNEL):
			print key
			buffer[step] = 0
			note = key[1]
			if(note > 35):
				note = (note-36)*2
			
				if(note < 0 or note > 125): note = 127
				SendSeqStep(NRPN_SEQ1_STEP1,step,note)
				buffer[step] =  note
				
			step = step + 1
			step = step % 16
		
		clock = clock_input.receive().bytes()
		if(clock[0] == 0xF8): mopho_output.send(MSG(clock))	
			
			
def Loop():
	global last_note,last_vel
	last_note = 48
	last_vel  = 127
	
	while 1:
		
		key = keyboard_input.receive().bytes()
		
		if(key[0] == 0x90+MOPHO_CHANNEL):			
			
			SendSequenceNotes(NRPN_SEQ1_STEP1,keyboard[key[1]])
			key[1] = ROOT
			mopho_output.send(MSG(key))
			last_note = key[1]
			last_vel   = 127
		elif(key[0] == 176 and key[1] == 116):
			mopho_output.send(MSG([0x80+MOPHO_CHANNEL,last_note,last_vel]))
				
		
		

MIDIClock().start()
Loop()