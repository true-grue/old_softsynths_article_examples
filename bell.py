# Author: Peter Sovietov

from __future__ import division
import math
import struct
import wave

SR = 44100

def write_wave(filename, samples):
  f = wave.open(filename, "w")
  f.setparams((1, 2, SR, len(samples), "NONE", ""))
  f.writeframes(b"".join(
    [struct.pack('<h', round(x * 32767)) for x in samples]))
  f.close()

def sec(x):
  return SR * x

class Sine:
  def __init__(self):
    self.phase = 0

  def next(self, freq, pm=0):
    s = math.sin(self.phase + pm)
    self.phase = (self.phase + 2 * math.pi * freq / SR) % (2 * math.pi)
    return s

oc = Sine()
om = Sine()

samples = []

for t in range(int(sec(1))):
  env = 1 - t / SR
  samples.append(0.5 * oc.next(80, 3 * env * om.next(450)))

write_wave("bell.wav", samples)
