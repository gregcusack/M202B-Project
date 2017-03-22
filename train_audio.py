import matplotlib.pyplot as plt
import numpy as np
import pysptk
import lpc
from scipy import signal
from scipy.io import wavfile
import soundfile as sf
from sklearn import mixture
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn import mixture
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import FastICA
import python_speech_features as psf
from sklearn.externals import joblib
import frequency_estimator

def computeEnergy(frame_signal):
	signal_squared = frame_signal ** 2
	energy = np.sum(signal_squared)
	return energy

fs, g = wavfile.read('gregFiltered3.wav')
fs, p = wavfile.read('priscillaFiltered3.wav')
fs, l = wavfile.read('lizFiltered3.wav')

assert fs == 16000

pos1 = 0
frame_length = 512

#the reason i do this roundabout thing below is because wavfile.read() above reads the
#wave files into a numpy array with the datatype 'dtype=int16' tacked on at the end
#this is just code to remove that element in order for the function np.c_ below to work
l = np.asarray(l.tolist()[0:300000])	
g = np.asarray(g.tolist()[0:300000])	
p = np.asarray(p.tolist()[0:300000])	#ensure all waveform vectors are the same length
#raw_wav_transformed = np.c_[p,g,l]		#take the transpose (needed for fastICA below)
#raw_wav = [p,g,l]						#all the waveform vectors combined into one list
#raw_wav_transformed = np.c_[p,g]
#raw_wav = [p,g]	


#FastICA source separation
ica = FastICA(n_components=3)
raw_wav_sep = ica.fit_transform(raw_wav_transformed)
#raw_wav_new = [[x[0] for x in raw_wav_sep], [x[1] for x in raw_wav_sep], [x[2] for x in raw_wav_sep]]
raw_wav_new = [[x[0] for x in raw_wav_sep], [x[1] for x in raw_wav_sep]]


mfcc = []
lpcs = []
pitch = []
trainX = []
testX = []
testY = []
trainY = []
test_indices = np.random.randint(0, 800, size=(1,1))
invalid_count = 0
energies = []

for i, audio in enumerate(raw_wav):
	pos1 = 0
	invalid_count = 0
	for k in range(0,800):
		frame = audio[pos1:pos1+frame_length] * pysptk.blackman(frame_length) #break up + window
		frame_np = np.asarray(frame, dtype=float)
		frame_energy = computeEnergy(frame_np)
		energies.append(frame_energy)
		print(k, frame_energy)
		#if frame_energy < 0.0003:			#voice activity detection: set an energy threshold to remove silences. 0.0 threshold = don't exclude silences
		if frame_energy < 0:
			invalid_count = invalid_count + 1
			
		else:
			#bandpass filter for vocals
			#b, a = signal.butter(6, [500.0/(0.5*fs), 3000.0/(0.5*fs)], btype='band')
			#frame_filtered = signal.lfilter(b, a, frame_np)
			#removed here bc it's better to just filter the whole thing at once (using filter.py)
			#can also just do the filtering in this file, above this loop

		
			frame_mfcc = psf.base.mfcc(frame_np)[0]
			#frame_mfcc = pysptk.sptk.mfcc(frame_np, order=14)
			#frame_lpc = pysptk.sptk.lpc(frame_np, order=25)
			#frame_lpc = lpc.lpc(frame_np, N=25)
			#frame_pitch = pysptk.sptk.swipe(frame_np, 16000, 80, threshold=0.0)
			frame_pitch = frequency_estimator.freq_from_fft(frame_np,fs)
			mfcc.append(frame_mfcc.tolist())
			#lpcs.append(frame_lpc.tolist())
			pitch.append(frame_pitch)

			#frame_lpc = np.delete(frame_lpc, 0)
			frame_features = frame_mfcc.tolist() + [frame_pitch]
			#frame_features = frame_mfcc.tolist()
			#frame_features = frame_mfcc.tolist() + frame_lpc.tolist() + frame_pitch.tolist() 
			#frame_features = frame_mfcc.tolist() + frame_lpc.tolist()
			#frame_features = frame_pitch.tolist()
			#avg_pitch = np.mean(frame_pitch)
			#frame_features.append(avg_pitch)
			
			if k in test_indices:
				testX.append(frame_features)
				testY.append(i)
			else:
				trainX.append(frame_features)
				trainY.append(i)
		pos1 = pos1 + 256
	#fig1 = plt.figure()
	#plt.stem(frame_mfcc)
	#plt.stem(frame_lpc)


"""
#Project to 2D and plot
SVD = TruncatedSVD(n_components=2)
normalizer = Normalizer(copy=False)
SVDnorm = make_pipeline(normalizer, SVD)
trainX_tf = SVDnorm.fit_transform(trainX)
testX_tf = SVDnorm.fit_transform(testX)
trainX_class1 = [x for i,x in enumerate(trainX_tf) if trainY[i]==0]
trainX_class2 = [x for i,x in enumerate(trainX_tf) if trainY[i]==1]
class1_comp1 = [x[0] for x in trainX_class1]
class1_comp2 = [x[1] for x in trainX_class1]
class2_comp1 = [x[0] for x in trainX_class2]
class2_comp2 = [x[1] for x in trainX_class2]
plt.scatter(class1_comp1, class1_comp2, color='r')
plt.scatter(class2_comp1, class2_comp2, color='b')
plt.xlabel('component 1')
plt.ylabel('component 2')
plt.show()
"""

#KMeans/Vector Quantization
"""
kmeans = KMeans(n_clusters=3, init='k-means++', max_iter=100, n_init=1)
kmeans.fit(trainX, trainY)
results = kmeans.predict(testX)
print('kmeans result: ', results)
"""

#SVC

clf = SVC(C=0.7, gamma=0.001)
clf.fit(trainX, trainY) #fit all
result = clf.predict(testX)
score = clf.score(trainX, trainY)
print('SVC result: ', result)
print('expected: ', testY)
print('SVC training score: ', score)
joblib.dump(clf, 'classify2.pkl')

#sweep
"""
c_array = [0.001, 0.005, 0.01, 0.02, 0.05, 0.07, 0.1, 0.2, 0.5, 0.7]
g_array = [0.001, 0.005, 0.01, 0.02, 0.05, 0.07, 0.1, 0.2, 0.5, 0.7]
for i in range(1,10):
	for k in range(1,10):
		print(c_array[i], g_array[k])
		clf = SVC(C=c_array[i], gamma=g_array[k])
		clf.fit(trainX, trainY) #fit all
		result = clf.predict(testX)
		score = clf.score(trainX, trainY)
		print('SVC result: ', result)
		print('expected: ', testY)
		print('SVC training score: ', score)
	print('----------------')
"""
