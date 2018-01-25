# Author: Peter Sovietov

from __future__ import division
import random
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

class Lp1:
  def __init__(self):
    self.y = 0

  def next(self, x, cutoff):
    self.y += cutoff * (x - self.y)
    return self.y

def pluck(samples, amp, freq, dur):
  flt = Lp1()
  delay_buf = [0] * int(SR / freq)
  delay_pos = 0
  for i in range(int(len(delay_buf) * amp)):
    delay_buf[i] = random.random()
  for t in range(int(sec(dur))):
    delay_buf[delay_pos] = flt.next(delay_buf[delay_pos], 220 / len(delay_buf))
    samples.append(amp * delay_buf[delay_pos])
    delay_pos = (delay_pos + 1) % len(delay_buf)

def rest(samples, dur):
  for t in range(int(sec(dur))):
    samples.append(samples[-1])

samples = []

for i in range(4):
  pluck(samples, 0.7, 58, 0.27)
  pluck(samples, 0.4, 62, 0.27)
  pluck(samples, 0.4, 66, 0.27)
  pluck(samples, 0.6, 69, 0.27)
  pluck(samples, 0.5, 138, 0.01)
  rest(samples, 0.13)
  pluck(samples, 0.7, 123, 0.13)
  rest(samples, 0.27)
  pluck(samples, 0.7, 139, 0.47)
  rest(samples, 0.07)
  pluck(samples, 0.7, 78, 0.27)
  pluck(samples, 0.4, 82, 0.27)
  pluck(samples, 0.4, 87, 0.27)
  pluck(samples, 0.6, 92, 0.27)
  pluck(samples, 0.5, 184, 0.01)
  rest(samples, 0.13)
  pluck(samples, 0.7, 139, 0.13)
  rest(samples, 0.27)
  pluck(samples, 0.7, 165, 0.47)
  rest(samples, 0.07)

write_wave("chameleon.wav", samples)
