import numpy as np
import pandas as pd
from keras.datasets import mnist
from keras.models import Sequential
classifier = Sequential()
from  keras.utils import np_utils
from  keras.utils import np_utils
from keras.layers import Dense, Dropout, Activation, Flatten, MaxPool2D
from keras.layers import Conv2D, BatchNormalization
from keras.preprocessing.image import ImageDataGenerator

#############  load the dataset   #####################
(X_train, y_train) , (X_test, y_test) = mnist.load_data()

#################  Normalizing the input ######################
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

################   adding layers ######################

classifier.add(Conv2D(32, (3,3), input_shape=(28,28,1)))
BatchNormalization(axis=-1) #Axis -1 is always the features axis
classifier.add(Activation('relu'))
 
classifier.add(Conv2D(32, (3,3)))
BatchNormalization(axis=-1)
classifier.add(Activation('relu'))
classifier.add(MaxPool2D(pool_size=(2,2)))
BatchNormalization(axis=-1)
classifier.add(Conv2D(64, (3,3)))
BatchNormalization(axis=-1)
classifier.add(Activation('relu'))
classifier.add(Conv2D(64, (3,3)))
classifier.add(Activation('relu'))
classifier.add(MaxPool2D(pool_size=(2,2)))
classifier.add(Flatten())
BatchNormalization()
classifier.add(Dense(512))
BatchNormalization()
classifier.add(Activation('relu'))
classifier.add(Dropout(0.2))
classifier.add(Dense(10))
classifier.add(Activation('softmax'))

###########  compile the model  ############## 
classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


#######  applying transformation to image``` ##############3
train_gen = ImageDataGenerator(rotation_range=8, 
                               width_shift_range=0.08, 
                               shear_range=0.3, 
                               height_shift_range=0.08, 
                               zoom_range=0.08 )
test_gen = ImageDataGenerator()

######### train the model   ##################
training_set= train_gen.flow(X_train, y_train, batch_size=64)
test_set= train_gen.flow(X_test, y_test, batch_size=64)

classifier.fit_generator(training_set, 
                         steps_per_epoch=60000//64, 
                         validation_data= test_set, 
                         validation_steps=10000//64, 
                         epochs=50)

 
classifier.save("final.h5")
print("model saved")

#### Evaluate the model performance
test_loss, test_acc = classifier.evaluate(x=X_test, y=y_test)
######  Print out the model accuracy 
print('\nTest accuracy:', test_acc)           

