import tensorflow as tf
import scipy 
import matplotlib.pyplot as plt
import numpy as np
import cv2



def predict(image):
    
    print(type(image))
    print(image.shape)
    predictions = model.predict(image) # Make prediction
    print(predictions) # Print out the number
    print(np.argmax(predictions[0]))
    plt.imshow(image[0], cmap="gray")
    plt.show()
    '''
    predictions = model.predict([x_test]) # Make prediction
    print(np.argmax(predictions[99])) # Print out the number
    print(predictions[99])
    plt.imshow(x_test[99], cmap="gray") # Import the image
    plt.show() # Show the image
    #predictions = model.predict([x_test]) # Make prediction
    print(np.argmax(predictions[2005])) # Print out the number
    plt.imshow(x_test[2005], cmap="gray") # Import the image
    plt.show() # Show the image 
    '''
mnist = tf.keras.datasets.mnist # Object of the MNIST dataset
(x_train, y_train),(x_test, y_test) = mnist.load_data() # Load data
plt.imshow(x_train[0], cmap="gray") # Import the image
plt.show() # Plot the image
# Normalize the train dataset
x_train = tf.keras.utils.normalize(x_train, axis=1)
# Normalize the test dataset
x_test = tf.keras.utils.normalize(x_test, axis=1)
#Build the model object
model = tf.keras.models.Sequential()
# Add the Flatten Layer
model.add(tf.keras.layers.Flatten())
# Build the input and the hidden layers
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
# Build the output layer
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
# Compile the model
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(x=x_train, y=y_train, epochs=1) # Start training process
# Evaluate the model performance
test_loss, test_acc = model.evaluate(x=x_test, y=y_test)
# Print out the model accuracy 
print('\nTest accuracy:', test_acc)
print(type(x_test))
print(x_test.shape)
#predict(x_test)
