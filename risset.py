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

def sines(bank, t):
  mix = 0
  for f in bank:
    mix += math.sin(2 * math.pi * f * t / SR)
  return mix

f = 96
i1 = 0.03
i2 = i1 * 2
i3 = i1 * 3
i4 = i1 * 4

risset = []

for i in [f, f + i1, f + i2, f + i3, f + i4, f - i1, f - i2, f - i3, f - i4]:
  for j in [i, 5 * i, 6 * i, 7 * i, 8 * i, 9 * i, 10 * i]:
    risset.append(j)

samples = []
for t in range(int(sec(20))):
  samples.append(0.01 * sines(risset, t))
write_wave("risset.wav", samples)
