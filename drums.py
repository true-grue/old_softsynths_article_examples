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

def linear_env(segs, t):
  x0 = 0
  y0 = 0
  for x1, y1 in segs:
    if t < x1:
      return y0 + (t - x0) * ((y1 - y0) / (x1 - x0))
    x0, y0 = x1, y1
  return y0

class Env:
  def __init__(self, segs):
    self.segs = segs
    self.phase = 0

  def next(self, scale=1):
    s = linear_env(self.segs, self.phase)
    self.phase += scale / SR
    return s

def kick(samples, dur):
  freq = 100
  o1 = Sine()
  o2 = Sine()
  e1 = Env([(0, 1), (0.02, 1), (1, 0)])
  e2 = Env([(0, 1), (0.01, 0)])
  for t in range(int(sec(dur))):
    o = o1.next(freq * e1.next(2.5), 16 * e2.next() * o2.next(freq))
    samples.append(0.5 * o)

def snare(samples, dur):
  freq = 100
  o1 = Sine()
  o2 = Sine()
  e1 = Env([(0, 1), (0.2, 0.2), (0.4, 0)])
  e2 = Env([(0, 1), (0.17, 0)])
  e3 = Env([(0, 1), (0.005, 0.15), (1, 0)])
  fb = 0
  for t in range(int(sec(dur))):
    fb = e2.next() * o1.next(freq, 1024 * fb)
    samples.append(0.5 * o2.next(e1.next() * freq * 2.5, 4.3 * e3.next() * fb))

samples = []

for i in range(4):
  kick(samples, 0.25)
  kick(samples, 0.25)
  snare(samples, 0.5)

write_wave("drums.wav", samples)
