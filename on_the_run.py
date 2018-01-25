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

class Saw:
  def __init__(self):
    self.o = Sine()
    self.fb = 0

  def next(self, freq, cutoff=2):
    o = self.o.next(freq, cutoff * self.fb)
    self.fb = (o + self.fb) * 0.5
    return self.fb

class Lp1:
  def __init__(self):
    self.y = 0

  def next(self, x, cutoff):
    self.y += cutoff * (x - self.y)
    return self.y

ON_THE_RUN = [82.41, 98, 110, 98, 146.83, 130.81, 146.83, 164.81]

osc1 = Saw()
lfo1 = Sine()
flt1 = Lp1()
flt2 = Lp1()
flt3 = Lp1()
flt4 = Lp1()

samples = []

for bars in range(16):
  for freq in ON_THE_RUN:
    for t in range(int(sec(0.09))):
      x = osc1.next(freq)
      cutoff = 0.5 + lfo1.next(0.2) * 0.4
      x = flt1.next(x, cutoff)
      x = flt2.next(x, cutoff)
      x = flt3.next(x, cutoff)
      x = flt4.next(x, cutoff)
      samples.append(0.5 * x)

write_wave("on_the_run.wav", samples)
