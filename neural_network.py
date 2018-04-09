from keras.layers import Conv2D, UpSampling2D, Input, Reshape, concatenate, MaxPooling2D, Dropout
from keras.models import Model
from keras.preprocessing.image import img_to_array, load_img
from keras.optimizers import Adamax
from skimage.color import rgb2lab, lab2rgb, rgb2gray, gray2rgb
from skimage.transform import resize
from skimage.io import imsave
import keras
import numpy as np
import os
import tensorflow as tf


X = []

for filename in [filename for filename in os.listdir('frames_from_movies/')[:300] if filename.endswith(".png")]:
    X.append(img_to_array(load_img('frames_from_movies/' + filename)))


X = np.array(X, dtype=float)
Xtrain = (1.0 / 255) * X

network_input = Input(shape=(256, 256, 1,))

first_path = Conv2D(4, (3,3), padding='same', activation='relu')(network_input)
first_path = Conv2D(8, (3,3), padding='same', activation='relu')(first_path)
second_path = Conv2D(8, (3,3), padding='same', activation='relu')(network_input)
second_path = Conv2D(8, (3,3), padding='same', activation='relu')(second_path)
third_path = Conv2D(8, (3,3), padding='same', activation='relu')(network_input)
third_path = Conv2D(16, (3,3), padding='same', activation='relu')(third_path)

inception_output = concatenate([first_path, second_path, third_path], axis = 3)

network = Conv2D(16, (3, 3), activation='relu', padding='same')(inception_output)
network = Conv2D(16, (3, 3), activation='tanh', padding='same')(network)
network = MaxPooling2D((2,2))(network)
network = Dropout(0.25)(network)
network = Conv2D(32, (3, 3), activation='relu', padding='same')(network)
network = Conv2D(32, (3, 3), activation='tanh', padding='same')(network)
network = Conv2D(32, (3, 3), activation='relu', padding='same')(network)
network = MaxPooling2D((2,2))(network)
network = Dropout(0.25)(network)
network = Conv2D(64, (3, 3), activation='tanh', padding='same')(network)
network = Conv2D(64, (3, 3), activation='relu', padding='same')(network)
network = Conv2D(64, (3, 3), activation='tanh', padding='same')(network)
network = MaxPooling2D((2,2))(network)
network = Dropout(0.4)(network)
network = Conv2D(128, (3, 3), activation='relu', padding='same')(network)
network = Conv2D(128, (3, 3), activation='tanh', padding='same')(network)
network = Conv2D(128, (3, 3), activation='relu', padding='same')(network)
network = MaxPooling2D((2,2))(network)
network = Dropout(0.4)(network)
network = Conv2D(256, (3, 3), activation='tanh', padding='same')(network)
network = Conv2D(256, (3, 3), activation='relu', padding='same')(network)
network = Conv2D(256, (3, 3), activation='tanh', padding='same')(network)
network = UpSampling2D((2, 2))(network)
network = Dropout(0.4)(network)
network = Conv2D(128, (3, 3), activation='relu', padding='same')(network)
network = Conv2D(128, (3, 3), activation='tanh', padding='same')(network)
network = Conv2D(128, (3, 3), activation='relu', padding='same')(network)
network = UpSampling2D((2, 2))(network)
network = Dropout(0.4)(network)
network = Conv2D(64, (3, 3), activation='relu', padding='same')(network)
network = Conv2D(64, (3, 3), activation='tanh', padding='same')(network)
network = Conv2D(64, (3, 3), activation='relu', padding='same')(network)
network = UpSampling2D((2, 2))(network)
network = Dropout(0.25)(network)
network = Conv2D(32, (3, 3), activation='tanh', padding='same')(network)
network = Conv2D(32, (3, 3), activation='relu', padding='same')(network)
network = Conv2D(32, (3, 3), activation='tanh', padding='same')(network)
network = UpSampling2D((2, 2))(network)
network = Dropout(0.25)(network)
network = Conv2D(16, (3, 3), activation='tanh', padding='same')(network)
network = Conv2D(16, (3, 3), activation='relu', padding='same')(network)
network = Conv2D(16, (3, 3), activation='tanh', padding='same')(network)

first_path_2 = Conv2D(8, (3,3), padding='same', activation='relu')(network)
first_path_2 = Conv2D(4, (3,3), padding='same', activation='relu')(first_path_2)
second_path_2 = Conv2D(4, (3,3), padding='same', activation='relu')(network)
second_path_2 = Conv2D(4, (3,3), padding='same', activation='relu')(second_path_2)
third_path_2 = Conv2D(4, (3,3), padding='same', activation='relu')(network)
third_path_2 = Conv2D(2, (3,3), padding='same', activation='relu')(third_path_2)

inception_output_2 = concatenate([first_path_2, second_path_2, third_path_2], axis = 3)

network = Conv2D(2, (3, 3), activation='relu', padding='same')(inception_output_2)
network_output = Conv2D(2, (3, 3), activation='tanh', padding='same')(network)

model = Model(inputs=network_input, outputs=network_output)

batch_size = 1
EPOCHS = 20

def image_a_b_gen(batch_size):
    while True:
        for batch in Xtrain:
            batch = batch.reshape((1,) + batch.shape)
            lab_batch = rgb2lab(batch)
            X_batch = lab_batch[:, :, :, 0] / 128
            X_batch = X_batch.reshape(X_batch.shape + (1,))
            Y_batch = lab_batch[:, :, :, 1:] / 128
            yield (X_batch, Y_batch)

opt = Adamax(lr=0.001)
tbCallback = keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=32, write_graph=True, write_grads=False, write_images=False, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None)
model.compile(optimizer=opt, loss='mse', metrics=['mse', 'acc'])
model.fit_generator(image_a_b_gen(batch_size), epochs=EPOCHS, steps_per_epoch=len(Xtrain), callbacks=[tbCallback])

model.save_weights('model_{}e_1000pic.h5'.format(EPOCHS))
model.save('model_{}e_1000pic_m.h5'.format(EPOCHS))

color_me = []
for filename in [filename for filename in os.listdir('test/')[:200:5] if filename.endswith(".png")]:
    color_me.append(img_to_array(load_img('test/' + filename)))
color_me = np.array(color_me, dtype=float)
color_me = rgb2lab((1.0 / 255) * color_me)[:, :, :, 0] / 128
color_me = color_me.reshape(color_me.shape + (1,))


output = model.predict(color_me)
output = output * 128


if not os.path.exists('result'):
    os.mkdir('result')

for i in range(len(output)):
    cur = np.zeros((256, 256, 3))
    cur[:, :, 0] = color_me[i][:, :, 0] * 128
    cur[:, :, 1:] = output[i][:, :, :]
    imsave("result/img_" + str(i) + ".png", lab2rgb(cur))

