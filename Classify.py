import numpy as np
import pickle

f = open('userData/gesture.dat', 'rb')
gestureData = pickle.load(f)

print gestureData.shape
