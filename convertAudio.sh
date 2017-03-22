#!/bin/bash
#clear

#lock channels first
#flock -x -w .1 channel_0.wav && sox -r 16000 -c 1 -e signed  -b 16 mic_16000_s16le_channel_0.raw channel_0.wav
#flock -x -w .1 channel_1.wav && sox -r 16000 -c 1 -e signed  -b 16 mic_16000_s16le_channel_1.raw channel_1.wav
#flock -x -w .1 channel_2.wav 
#flock -x -w .1 channel_3.wav 
#flock -x -w .1 channel_4.wav 
#flock -x -w .1 channel_5.wav 
#flock -x -w .1 channel_6.wav 
#flock -x -w .1 channel_7.wav 

sox -r 16000 -c 1 -e signed  -b 16 mic_16000_s16le_channel_0.raw channel_0.wav
sox -r 16000 -c 1 -e signed  -b 16 mic_16000_s16le_channel_1.raw channel_1.wav
sox -r 16000 -c 1 -e signed  -b 16 mic_16000_s16le_channel_2.raw channel_2.wav
sox -r 16000 -c 1 -e signed  -b 16 mic_16000_s16le_channel_3.raw channel_3.wav
sox -r 16000 -c 1 -e signed  -b 16 mic_16000_s16le_channel_4.raw channel_4.wav
sox -r 16000 -c 1 -e signed  -b 16 mic_16000_s16le_channel_5.raw channel_5.wav
sox -r 16000 -c 1 -e signed  -b 16 mic_16000_s16le_channel_6.raw channel_6.wav
sox -r 16000 -c 1 -e signed  -b 16 mic_16000_s16le_channel_7.raw channel_7.wav


exec 3>voiceFile.wav
flock -x 3
sox -m channel_0.wav channel_1.wav channel_2.wav channel_3.wav channel_4.wav channel_5.wav channel_6.wav channel_7.wav voiceFile.wav
exec 3>&-


echo \n\n\n\n\n Audio File ready \n\n\n\n\n

#ls




