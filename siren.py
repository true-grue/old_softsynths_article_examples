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

def reset_ins(ins):
  for i, x in enumerate(ins):
    ins[i] = None

def is_ins_full(ins):
  for x in ins:
    if x is None:
      return False
  return True

def is_outs_empty(outs):
  for out in outs:
    for box, port in out:
      if box.ins[port] is not None:
        return False
  return True

def send_to_outs(results, outs):
  for i, x in enumerate(results):
    for box, port in outs[i]:
      box.ins[port] = x

class Box:
  def __init__(self, op, ins, outs):
    self.ins = [None] * ins
    self.outs = [[] for i in range(outs)]
    self.op = op

  def compute(self):
    if is_ins_full(self.ins) and is_outs_empty(self.outs):
      send_to_outs(self.op(*self.ins), self.outs)
      reset_ins(self.ins)

def wire(box1, port1, box2, port2):
  box1.outs[port1].append((box2, port2))

def compute(schedule):
  for b in schedule:
    b.compute()

class Sine:
  def __init__(self):
    self.phase = 0

  def next(self, freq, pm=0):
    s = math.sin(self.phase + pm)
    self.phase = (self.phase + 2 * math.pi * freq / SR) % (2 * math.pi)
    return s

def Osc():
  o = Sine()
  return Box(lambda x, y: [o.next(x, y)], 2, 1)

def Out(samples):
  def compute(x):
    samples.append(x)
    return []
  return Box(compute, 1, 0)

def clip(x, y):
  return -y if x < -y else y if x > y else x

Const = lambda x: Box(lambda: [x], 0, 1)
Mul = lambda: Box(lambda x, y: [x * y], 2, 1)
Clip = lambda: Box(lambda x, y: [clip(x, y)], 2, 1)

samples = []

patch = {
  "k1": Const(550),
  "k2": Const(50),
  "k3": Const(2),
  "k4": Const(0),
  "k5": Const(0.1),
  "k6": Const(1),
  "o1": Osc(),
  "o2": Osc(),
  "c1": Clip(),
  "m1": Mul(),
  "m2": Mul(),
  "out": Out(samples)
}

wire(patch["k3"], 0, patch["o1"], 0)
wire(patch["k4"], 0, patch["o1"], 1)
wire(patch["k2"], 0, patch["m1"], 0)
wire(patch["o1"], 0, patch["m1"], 1)
wire(patch["k1"], 0, patch["o2"], 0)
wire(patch["m1"], 0, patch["o2"], 1)
wire(patch["o2"], 0, patch["c1"], 0)
wire(patch["k5"], 0, patch["c1"], 1)
wire(patch["k6"], 0, patch["m2"], 0)
wire(patch["c1"], 0, patch["m2"], 1)
wire(patch["m2"], 0, patch["out"], 0)

schedule = patch.values()

while len(samples) < int(sec(2)):
  compute(schedule)

write_wave("siren.wav", samples)
