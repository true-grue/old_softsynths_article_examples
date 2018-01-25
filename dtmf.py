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

DTMF = [
  [697, 1209], [697, 1336], [697, 1477],
  [770, 1209], [770, 1336], [770, 1477],
  [852, 1209], [852, 1336], [852, 1477]
]

samples = []

for d in [3, 1, 1, 5, 5, 5, 2, 3, 6, 8]:
  for t in range(int(sec(0.05))):
    samples.append(0.5 * sines(DTMF[d - 1], t))
  for t in range(int(sec(0.05))):
    samples.append(0)

write_wave("dtmf.wav", samples)
