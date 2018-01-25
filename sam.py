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

class Sam:
  def __init__(self):
    self.phases = [0, 0, 0, 0]

  def next(self, frame, voice):
    flags, ampl1, freq1, ampl2, freq2, ampl3, freq3, pitch = frame
    mix = ampl1 * math.sin(self.phases[1]) + ampl2 * math.sin(self.phases[2])
    mix += ampl3 * (1 if self.phases[3] < 0.5 else -1)
    self.phases[1] = (self.phases[1] + 2 * math.pi * freq1 / SR) % (2 * math.pi)
    self.phases[2] = (self.phases[2] + 2 * math.pi * freq2 / SR) % (2 * math.pi)
    self.phases[3] = (self.phases[3] + freq3 / SR) % 1
    self.phases[0] += 1
    if self.phases[0] > pitch * voice * SR:
      self.phases = [0, 0, 0, 0]
    return 0.5 * mix

COEFFS = [1, 0.1, 27, 0.1, 27, 0.1, 27, 0.00001]

def parse(frames):
  frames = [[int(y) * COEFFS[i] for i, y in enumerate(x.split())] \
    for x in frames.strip().split("\n")]
  return frames

with open("sam.txt") as f:
  frames = parse(f.read())

s = Sam()

samples = []

for voice in range(25, 5, -2):
  for frame in frames:
    for t in range(int(sec(0.01))):
      samples.append(0.5 * s.next(frame, voice))

write_wave("sam.wav", samples)
