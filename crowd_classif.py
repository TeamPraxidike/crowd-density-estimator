import pandas as pd
import random
import numpy as np
import matplotlib
import os
import tensorflow as tf
from PIL import Image
from tensorflow import keras
from tensorflow.keras import datasets, layers, models
import matplotlib.image as mp
from  matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflowjs as tfjs

# Функция за извличане на снимките от dataset-а

img_width = 64
img_height = 64

def create_dataset(img_folder):
    
    img_data_array=[]
    img_labels=[]
    class_name=[]
    for dir1 in os.listdir(img_folder):
        for file in os.listdir(os.path.join(img_folder, dir1)):
       
            if dir1=='Large density': img_labels.append(1)
            if dir1=='Average density': img_labels.append(0)
            if dir1=='No density': img_labels.append(2)
            image_path= os.path.join(img_folder, dir1,  file)
            
            image= Image.open(image_path)#.convert('L')
            image.thumbnail((img_height, img_width), Image.ANTIALIAS)
            
            image = np.array(image)
            image= np.resize(image,(img_height,img_width,3))
            image = image.astype('float32')
            image /= 255
            img_data_array.append(image)
        class_name.append(dir1)
    return img_data_array , class_name, img_labels

# Делене на снимките от dataset-а на training и test
X, class_names, y = create_dataset(r'Crowds COMBINED')

train_images, test_images, train_labels, test_labels = train_test_split(X, y, test_size=0.25, random_state=1)

train_images = np.array(train_images)
train_labels = np.array(train_labels)

test_images = np.array(test_images)
test_labels = np.array(test_labels)

# Създаване на модела на невронна мрежа

data_augmentation = keras.Sequential(
  [
    layers.experimental.preprocessing.RandomFlip("horizontal", 
                                                 input_shape=(img_height, 
                                                              img_width,
                                                              3)),
    layers.experimental.preprocessing.RandomRotation(0.1),
    layers.experimental.preprocessing.RandomZoom(0.1),
  ]
)

model = models.Sequential([
    data_augmentation,
    layers.experimental.preprocessing.Rescaling(1./255),
    layers.Conv2D(32, (2, 2), activation='relu', input_shape=(img_height, img_width, 3)),
    layers.MaxPooling2D((2, 2)),
    #layers.Conv2D(64, (3, 3), activation='relu'),
    #layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.1),
    layers.Flatten(),
    layers.Dense(96, activation='relu'),
    layers.Dense(3)])

# Компилираме на модела

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()

epochs = 100

# Обучение на модела и запазване

history = model.fit(train_images, train_labels, validation_data=(test_images, test_labels), epochs=epochs)

# Създаване на графика

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()
