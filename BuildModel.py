# -----Imports-----
import numpy as np
import keras

from keras.layers import Dense, Flatten
from keras.models import Model
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.utils import load_img, img_to_array

# -----Create a base model-----
base_model = InceptionV3(input_shape=(255, 255, 3), include_top=False)

for layer in base_model.layers:
  layer.trainable = False

# -----Take the output of the base model and add that to the actual model-----
X = Flatten()(base_model.output)
X = Dense(units=2, activation="sigmoid")(X)

# Final model
model = Model(base_model.input, X)

# -----Compile the model-----
model.compile(optimizer="adam", loss=keras.losses.binary_crossentropy, metrics=["accuracy"])

# -----Pre-process data-----
train_datagen = ImageDataGenerator(
    rescale=1./255.,
    featurewise_center=True,
    rotation_range=0.4,
    width_shift_range=0.3,
    horizontal_flip=True,
    preprocessing_function=preprocess_input,
    zoom_range=0.4,
    shear_range=0.4
)

# -----Generate trainining and validation data-----
# Training
train_data = train_datagen.flow_from_directory(
    directory="./Data/Train", 
    target_size=(255,255), 
    batch_size=10
)

# Validation
valid_data = train_datagen.flow_from_directory(
    directory="./Data/Valid", 
    target_size=(255,255), 
    batch_size=5
)

# -----Define checkpoint and earlystopping-----
# Checkpoint
mc = ModelCheckpoint(
    filepath="./Model/final_model.h5", 
    monitor="val_accuracy", 
    save_best_only=True,
    verbose=1
)

# Earlystopping
es = EarlyStopping(
    monitor="val_accuracy",
    min_delta=0.01,
    patience=5,
    verbose=1
)

# Callback
cb = [mc, es]

# -----Fit the model-----
his = model.fit_generator(
    train_data,
    steps_per_epoch=20,
    epochs=10,
    validation_data=valid_data,
    validation_steps=5,
    callbacks=cb
)