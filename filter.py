import numpy as np
from scipy import signal
import soundfile as sf
from scipy.io import wavfile
import matplotlib.pyplot as plt

fs, voice = wavfile.read('lizVoiceFile3.wav') #input voice file
b, a = signal.butter(6, [75.0/(0.5*fs), 3475.0/(0.5*fs)], btype='band')
voice_filtered = signal.lfilter(b, a, voice)
wavfile.write('lizFiltered3.wav', fs, voice_filtered) #filtered voice file

#plot the filter 
w,h = signal.freqz(b, a, worN=10000)
plt.plot((fs * 0.5 / np.pi) * w, abs(h))
plt.xlim([0,10000])
plt.show() 

"""
import numpy as np
from scipy import signal
import soundfile as sf
import matplotlib.pyplot as plt
 
voice, fs = sf.read('gregVoiceFile.wav') #input voice file
b, a = signal.butter(6, [1000.0/(0.5*fs), 4000.0/(0.5*fs)], btype='band')
voice_filtered = signal.lfilter(b, a, voice)
sf.write('gregFiltered.wav', voice_filtered, fs) #filtered voice file

#plot the filter 
w,h = signal.freqz(b, a, worN=10000)
plt.plot((fs * 0.5 / np.pi) * w, abs(h))
plt.xlim([0,10000])
plt.show() 

"""
