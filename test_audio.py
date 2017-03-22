import signal, os, sys
import scipy.signal
#import soundfile as sf
from scipy.stats import mode
import matplotlib.pyplot as plt
import numpy as np
import pysptk
from scipy.io import wavfile
from sklearn.svm import SVC
from sklearn.externals import joblib
import frequency_estimator
import python_speech_features as psf
import time
import fcntl

def exitHandler(signumm, frame):
	global count_array, speaker_dict
	print('\n')
	for i in range(0,3):
		print("{} spoke for {} seconds".format(speaker_dict[i], count_array[i]))
	sys.exit(0)

def processAudio(signum, frame):
	global count_array
	start = time.time()
	


	while True:
		try:
			#x = open('priscillaVoiceFile2.wav')
			fcntl.flock(open('/home/pi/matrix-creator-hal/build/demos/voiceFile.wav'), fcntl.LOCK_EX | fcntl.LOCK_NB)
			fs, audio = wavfile.read('/home/pi/matrix-creator-hal/build/demos/voiceFile.wav')
			break
		except IOError as e:
			# raise on unrelated IOErrors
			if e.errno != errno.EAGAIN:
				raise
			else:
				time.sleep(0.01)
	            
	print('Voice detected')
	fcntl.flock(open('/home/pi/matrix-creator-hal/build/demos/voiceFile.wav'), fcntl.LOCK_UN) #release lock
	
	assert fs == 16000
	pos1 = 0

	#bandpass filter for vocals
	b, a = scipy.signal.butter(6, [75.0/(0.5*fs), 3475.0/(0.5*fs)], btype='band')
	audio_filtered = scipy.signal.lfilter(b, a, audio)



	mfcc = []
	lpc = []
	pitch = []
	testX = []
	for k in range(0,20):

		frame = audio_filtered[pos1:pos1+frame_length] * pysptk.blackman(frame_length)
		frame_np = np.asarray(frame, dtype=float)

		frame_mfcc = psf.base.mfcc(frame_np)[0]
		#frame_mfcc = pysptk.sptk.mfcc(frame_np, order=14)
		#frame_lpc = pysptk.sptk.lpc(frame_np)
		#frame_pitch = pysptk.sptk.swipe(frame_np, 16000, 80, threshold=0.0)
		frame_pitch = frequency_estimator.freq_from_fft(frame_np,fs)

		mfcc.append(frame_mfcc.tolist())
		#lpc.append(frame_lpc.tolist())
		pitch.append(frame_pitch)

		#frame_lpc = np.delete(frame_lpc, 0)
		frame_features = frame_mfcc.tolist() + [frame_pitch]
		#frame_features = frame_mfcc.tolist()
		#frame_features = frame_mfcc.tolist() + frame_lpc.tolist() + frame_pitch.tolist() 
		#frame_features = frame_mfcc.tolist() + frame_lpc.tolist()

		avg_pitch = np.mean(frame_pitch)
		testX.append(frame_features)
		pos1 = pos1 + 256

	result = clf.predict(testX)
	end = time.time()
	speaker_id = int(mode(result)[0][0])
	#print('result: ', result)
	print('speaker: ', speaker_dict[speaker_id])
	print('certainty: {}'.format(mode(result)[1][0]/20))
	print('elapsed: ', end-start)
	print(count_array)
	curr_count = count_array[speaker_id]
	count_array[speaker_id] = curr_count + 1
	
	
if __name__ == "__main__":
	global count_array, time_array
	
	count_array = [0, 0, 0]
	signal.signal(signal.SIGUSR1, processAudio)
	signal.signal(signal.SIGINT, exitHandler)
	clf = joblib.load('classify3.pkl')
	speaker_dict = {0:'priscilla', 1:'greg', 2:'liz'}
	frame_length = 512

	while True:
		print('Waiting for voice activity')
		signal.pause()
		
		
