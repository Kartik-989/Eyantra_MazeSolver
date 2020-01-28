import tensorflow as tf
import numpy as np
import pandas as pd
from keras.datasets import mnist
import matplotlib.pyplot as plt
import numpy as np
import wget

from  keras.utils import np_utils


############## predict function ##################
def predict(image):
    
    predictions = new_model.predict(image) # Make prediction
    digit=np.argmax(predictions[0])
    #plt.imshow(image[0], cmap="gray")
    #plt.show()
    return digit
    
############# code to download model from drive ###########
'''
url='https://drive.google.com/uc?export=download&confirm=Uq6r&id=1Akn4mrJDA3YeIup0r2MKa0eh06yx_RdO'
print("downloading....")
wget.download(url)
print("download complete")
'''

################## code to load model ################

(X_train, y_train) , (X_test, y_test) = mnist.load_data()
jj=y_test
# Normalizing the input
X_train= X_train.reshape(X_train.shape[0], 28, 28, 1)
X_train = X_train.astype('float32')
X_train/=255
X_test = X_test.reshape(X_test.shape[0],28,28,1)
X_test = X_test.astype('float32')
X_test/=255
#print(X_train.shape)
#print(X_test.shape)



y_train = np_utils.to_categorical(y_train)
y_test= np_utils.to_categorical(y_test)
#print(y_train[0])

new_model=tf.keras.models.load_model('final.h5')
# Evaluate the model performance
test_loss, test_acc = new_model.evaluate(x=X_test, y=y_test)
# Print out the model accuracy 
print('\nTest accuracy:', test_acc,test_loss)





