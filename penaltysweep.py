#run train_audio.py first

c_array = [0.001, 0.005, 0.01, 0.02, 0.05, 0.07, 0.1, 0.2, 0.5, 0.7]
g_array = [0.001, 0.005, 0.01, 0.02, 0.05, 0.07, 0.1, 0.2, 0.5, 0.7]
scores = []
parameters = []
for i in range(0,10):
	for k in range(0,10):
		print(c_array[i], g_array[k])
		clf = SVC(C=c_array[i], gamma=g_array[k])
		clf.fit(trainX, trainY) #fit all
		result = clf.predict(testX)
		score = clf.score(trainX, trainY)
		#print('SVC result: ', result)
		#print('expected: ', testY)
		#print('SVC training score: ', score)
		scores.append(score)
		parameters.append((c_array[i], g_array[k]))
	print('----------------')
	
	
clf = SVC(C=0.7, gamma=0.001)
clf.fit(trainX, trainY) #fit all
result = clf.predict(testX)
score = clf.score(trainX, trainY)
print('SVC result: ', result)
print('expected: ', testY)
print('SVC training score: ', score)