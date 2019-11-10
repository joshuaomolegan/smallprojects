# -*- coding: utf-8 -*-
"""CatsVsDogs.ipynb

Automatically generated by Colaboratory.

This code splits the Kaggle Dogs vs. Cats dataset into training and test data, then uses the VGG16 convolutional base 
and a new densely connected classifier to classify images of dogs and cats with extremely high accuracy.

The dataset can be found here: www.kaggle.com/c/dogs-vs-cats/data
"""

import os, shutil
original_dir = "/content/train"
val_dir = "/content/validation"
train_dir = "/content/training"
cat_train_dir = "/content/training/cats"
dog_train_dir = "/content/training/dogs"
cat_val_dir = "/content/validation/cats"
dog_val_dir = "/content/validation/dogs"
os.mkdir(val_dir)
os.mkdir(train_dir)
os.mkdir(cat_val_dir)
os.mkdir(dog_val_dir)
os.mkdir(cat_train_dir)
os.mkdir(dog_train_dir)

fnames = ["cat.{}.jpg".format(i) for i in range(2500)]
for fname in fnames:
  src = os.path.join(original_dir, fname)
  dst = os.path.join(cat_val_dir, fname)
  shutil.move(src, dst)

fnames = ["cat.{}.jpg".format(i) for i in range(2500, 12500)]
for fname in fnames:
  src = os.path.join(original_dir, fname)
  dst = os.path.join(cat_train_dir, fname)
  shutil.move(src, dst)

fnames = ["dog.{}.jpg".format(i) for i in range(2500)]
for fname in fnames:
  src = os.path.join(original_dir, fname)
  dst = os.path.join(dog_val_dir, fname)
  shutil.move(src, dst)

fnames = ["dog.{}.jpg".format(i) for i in range(2500, 12500)]
for fname in fnames:
  src = os.path.join(original_dir, fname)
  dst = os.path.join(dog_train_dir, fname)
  shutil.move(src, dst)

from keras import layers, models, optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.applications import VGG16
import matplotlib.pyplot as plt

train_dir = "/content/training"
val_dir = "/content/validation"

train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
		train_dir,
		target_size=(150, 150),
		batch_size=20,
		class_mode="binary")

val_generator = train_datagen.flow_from_directory(
		val_dir,
		target_size=(150, 150),
		batch_size=20,
		class_mode="binary")

conv_base = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))

model = models.Sequential()
model.add(conv_base)
model.add(layers.Flatten())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

early_stopping_monitor = EarlyStopping(patience=3)
model_checkpoint = ModelCheckpoint(filepath="CatsAndDogs.h5", save_best_only=True)

model.compile(loss="binary_crossentropy", optimizer=optimizers.RMSprop(lr=1e-4), metrics=["acc"])

history = model.fit_generator(train_generator, steps_per_epoch=200, epochs=100, validation_data=val_generator, validation_steps=50, callbacks=[early_stopping_monitor])

acc = history.history["acc"]
val_acc = history.history["val_acc"]
loss = history.history["loss"]
val_loss = history.history["val_loss"]

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, "bo", label="Training acc")
plt.plot(epochs, val_acc, "b", label="Validation acc")
plt.title("Training and Validation accuracy")
plt.legend()

plt.figure()

plt.plot(epochs, loss, "bo", label="Training loss")
plt.plot(epochs, val_loss, "b", label="Validation loss")
plt.title("Training and Validation loss")
plt.legend()

plt.show()
