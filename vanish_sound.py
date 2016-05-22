# -*- coding: utf-8 -*-
"""
位相反転した音源を左右に配置して、モノラルで聞こえない音源を作る
"""
from __future__ import print_function
import argparse
import wave
import struct
import numpy
import array

parser = argparse.ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("--first_nframe", type=int, default=None)
parser.add_argument("--output_file", default="data/output.wav")
args = parser.parse_args()

audio = wave.open(open(args.input_file, 'rb'))

nchannels = audio.getnchannels()
nframes = audio.getnframes()
frames = audio.readframes(nframes)
framerate = audio.getframerate()

if not args.first_nframe is None:
    nframes = args.first_nframe

print("""
channels: {}
totalframes: {}
dsize: {}
""".format(
    nchannels,
    nframes,
    len(frames)/audio.getnframes()/nchannels
))


# 読み込み
framevals = [[] for _ in range(nchannels)]
tmpvals = []
for frame_index in range(nframes):
    for channel_index in range(nchannels):
        targ_index = frame_index * 2 * nchannels + 2 * channel_index
        frameval = numpy.int16(struct.unpack("<h", frames[targ_index:targ_index+2])[0])
        framevals[channel_index].append(frameval)
        tmpvals.append(frameval)

# チャンネル反転
audio_array = numpy.array(framevals)
audio_array = numpy.array([
    audio_array[0],
    -audio_array[0]
])

audio_array[audio_array <= numpy.iinfo(numpy.int16).min] = numpy.iinfo(numpy.int16).min
audio_array[audio_array >= numpy.iinfo(numpy.int16).max] = numpy.iinfo(numpy.int16).max

# import pylab
# pylab.plot(audio_array[0])
# pylab.plot(audio_array[1])
# pylab.show()
print(audio_array.dtype)

outaudio = wave.Wave_write(args.output_file)
outaudio.setparams(audio.getparams())
outaudio.writeframes(array.array('h', audio_array.transpose((1, 0)).flatten()).tostring())
outaudio.close()