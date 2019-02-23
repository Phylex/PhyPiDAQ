# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import sys, time, numpy as np
from scipy import interpolate 

def generateCalibrationFunction(calibd):
  '''
   interpolate calibration table t= true, r = raw values ; 
   if only one number for trueVals given, then this is 
   interpreted as a simple calibration factor
 
   Args: 
     calibd:   calibration data
         either a single number as calibration factor: fc
         or a list or two arrays: [ [true values], [raw values] ]    
   Returns: interpolation function
  ''' 
  try:
    iter(calibd)
    # if no error, input is an array
    r = calibd[1]
    t = calibd[0]
  except:
   # input is only one number
    r = [0., 1.]
    t = [0., calibd]    
  # check input
  if len(t) != len(r):
    print('!!! generateCalibrationFunction: lengths of input arrays not equal - exiting') 
    exit(1)
  # make sure raw values are sorted - and simultaneously sort true values
  r, t = zip(*sorted(zip(r, t) ) )
  # perform spline interpolation of appropriate order k
  return interpolate.UnivariateSpline(r, t, k = min(3, len(t)-1), s = 0 )

def stop_processes(proclst):
  '''
    Close all running processes at end of run
  '''
  for p in proclst: # stop all sub-processes
    if p.is_alive():
      print('    terminating ' + p.name)
      if p.is_alive(): p.terminate()
      time.sleep(1.)

def kbdwait():
  ''' 
    wait for keyboard input
  '''
  # 1st, remove pyhton 2 vs. python 3 incompatibility for keyboard input
  if sys.version_info[:2] <=(2,7):
    get_input = raw_input
  else: 
    get_input = input
 #  wait for input
  get_input(50*' '+'type <ret> to exit -> ')

class RingBuffer(object):
  '''a ring-buffer to store N objcts
  '''

  def __init__(self, N):
    '''
      N: size of buffer
    '''
    self.N = N
    self.Buf = []
    self.i = 0  

  def store(self, d):
    '''
      d: data object
    '''
    if self.i < self.N:
      self.Buf.append(d)
    else: # overwrite old data
      k = self.i % self.N
      self.Buf[k] = d

    self.i += 1

  def read(self):

     if self.i < self.N:
       return self.Buf[ : self.i]
     else:
       k = self.i % self.N
       return self.Buf[k : ] + self.Buf[ : k]
