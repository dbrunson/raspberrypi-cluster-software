#!/usr/bin/env python
# Copyright (c) 2013, Adam Tygart
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Kansas State University nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL ADAM TYGART BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import random
from base64 import b64encode
import argparse

parser = argparse.ArgumentParser(description="Generates Fractals")
parser.add_argument('-d', '--destination', type=str, default='192.168.0.1', help='IP to send the fractals to')

args = parser.parse_args()

if sys.version_info[0] < 3:
    import xmlrpclib
    s = xmlrpclib.ServerProxy('http://' + args.destination + ':8000')
else:
    import xmlrpc.client
    s = xmlrpc.client.ServerProxy('http://' + args.destination + ':8000')

(height, width) = s.get_size()
orig_chars = [' ', '.', ',', '-', ':', ';', 'i', '+', 'h', 'H', 'M', '$', '*', '#', '@', '_']
color_sequences = [('', ''), ('\033[34m', '\033[0m'), ('\033[94m', '\033[0m'), ('\033[36m', '\033[0m'), ('\033[96m', '\033[0m'), ('\033[32m', '\033[0m'), ('\033[92m', '\033[0m'), ('\033[35m', '\033[0m'), ('\033[95m', '\033[0m'), ('\033[31m', '\033[0m'), ('\033[91m', '\033[0m'), ('\033[33m', '\033[0m'), ('\033[93m', '\033[0m'), ('\033[37m', '\033[0m'), ('\033[37m', '\033[0m'), ('\033[90m\033[4m', '\033[24m\033[39m')]
chars = []

def gen_mandelbrot(minX, maxX, aspectRatio):
    yScale = (maxX-minX)*(float(height)/width)*aspectRatio
    fractal = ""
    for y in range(height):
        for x in range(width):
            c = complex(minX+x*(maxX-minX)/width, y*yScale/height-yScale/2)
            z = c
            for char in chars:
                if abs(z) > 2:
                    break
                z = z*z+c
            fractal += char
        fractal += "\n"
    return fractal.rstrip('\n')

def gen_julia(minX, maxX, aspectRatio):
    yScale = (maxX-minX)*(float(height)/width)*aspectRatio
    fractal = ""
    c = random.randrange(-2.0,stop=2.0,step=0.1,int=float)+1j*random.randrange(-2.0,stop=2.0,step=0.1,int=float)
    for y in range(height):
        for x in range(width):
            z = complex(minX+x*(maxX-minX)/width, y*yScale/height-yScale/2)
            for char in chars:
                if abs(z) > 2:
                    break
                z = z*z + c
            fractal += char
        fractal += "\n"
    return fractal.rstrip('\n')

def gen_test(minX, maxX, aspectRatio):
    yScale = (maxX-minX)*(float(height)/width)*aspectRatio
    fractal = ""
    for y in range(height):
        for x in range(width):
            z = complex(minX+x*(maxX-minX)/width, y*yScale/height-yScale/2)
            c = z
            for char in chars:
                if abs(z) > 2:
                    break
                if abs(z) < 1:
                    z = z*z - c
                else:
                    z = z*z + c
            fractal += char
        fractal += "\n"
    return fractal.rstrip('\n')

while True:
    if random.choice([False, False, False, True]):
        (height, width) = s.get_size()
    minX = random.randrange(-5.0, stop=5.0, step=0.1, int=float)
    maxX = random.randrange(-5.0, stop=5.0, step=0.1, int=float)
    if maxX < minX:
        t = maxX
        maxX = minX
        minX = t
    aspectRatio = random.randrange(2.0, stop=5.0, step=0.1, int=float)
    random.shuffle(color_sequences)
    random.shuffle(orig_chars)
    chars = [ color_sequences[i][0] + orig_chars[i] + color_sequences[i][1] for i in xrange(0, len(orig_chars) -1) ]
    t = s.pick_type()
    f = ""
    if t == "julia":
        f = gen_julia(minX, maxX, aspectRatio)
    elif t == "mandelbrot":
        f = gen_mandelbrot(minX, maxX, aspectRatio)
    else:
        f = gen_test(minX, maxX, aspectRatio)
    s.put(b64encode(f))
