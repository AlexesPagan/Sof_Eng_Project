from sklearn.neural_network import MLPClassifier

x = [ [0,0], [1,1] ]
y = [0,1]

clf = MLPClassifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(5,2), random_state=1, verbose=True)

clf.fit(x,y)
p = clf.predict(([[2,2 ], [-2,-1] ]))
print('\nPredicted :', p)
print('\nCLF Object\n', clf)

def plotData(df, y):
    plf.scatter(x[50:100,0], x[50:100,1], color='blue')