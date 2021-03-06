from keras.layers import Conv2D, UpSampling2D, Input, Reshape, concatenate, MaxPooling2D, Dropout, BatchNormalization, \
    GaussianDropout, AlphaDropout, LeakyReLU
from keras.models import Model, load_model
from keras.preprocessing.image import img_to_array, load_img, ImageDataGenerator
from keras.optimizers import Adamax
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from skimage.color import rgb2lab, lab2rgb, rgb2gray, gray2rgb
from math import ceil
import keras
import numpy as np
import os


class NeuralNetwork(object):
    def __init__(self, training_path, epochs=10, batch_size=1, path_to_model=None,image_size=256):
        self.training_path = training_path
        self.image_size = image_size
        self.epochs = epochs
        self.batch_size = batch_size

        self.training_set_size = 0
        for direct in [dirname for dirname in os.listdir(self.training_path)]:
            self.training_set_size += len([filename for filename in os.listdir(self.training_path + "/" + direct) if filename.endswith(".png")])
        self.datagen = ImageDataGenerator(shear_range=0.2, zoom_range=0.2, rotation_range=20, horizontal_flip=True)
        if path_to_model is None:
            self.model = self.neural_network_structure()
        else:
            self.model = NeuralNetwork.load_model_from_file(path_to_model)

    def neural_network_structure(self):
        network_input = Input(shape=(self.image_size, self.image_size, 1,))

        #encoder

        network = Conv2D(16, (3, 3), activation='relu', padding='same')(network_input)
        network = Conv2D(16, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(16, (3, 3), activation='relu', padding='same')(network)

        network = MaxPooling2D((2, 2))(network)
        network = BatchNormalization()(network)


        network = Conv2D(32, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(32, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(32, (3, 3), activation='relu', padding='same')(network)
        network = MaxPooling2D((2, 2))(network)
        network = BatchNormalization()(network)

        network = Conv2D(64, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(64, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(64, (3, 3), activation='relu', padding='same')(network)
        network = MaxPooling2D((2, 2))(network)
        network = BatchNormalization()(network)

        network = Conv2D(128, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(128, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(128, (3, 3), activation='relu', padding='same')(network)
        network = MaxPooling2D((2, 2))(network)
        network = BatchNormalization()(network)

        #decoder

        network = Conv2D(256, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(256, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(256, (3, 3), activation='relu', padding='same')(network)
        network = BatchNormalization()(network)
        network = UpSampling2D((2, 2))(network)


        network = Conv2D(128, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(128, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(128, (3, 3), activation='relu', padding='same')(network)
        network = UpSampling2D((2, 2))(network)
        network = BatchNormalization()(network)

        network = Conv2D(64, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(64, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(64, (3, 3), activation='relu', padding='same')(network)
        network = UpSampling2D((2, 2))(network)
        network = BatchNormalization()(network)

        network = Conv2D(32, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(32, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(32, (3, 3), activation='relu', padding='same')(network)
        network = UpSampling2D((2, 2))(network)
        network = BatchNormalization()(network)

        network = Conv2D(16, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(16, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(16, (3, 3), activation='relu', padding='same')(network)
        network = BatchNormalization()(network)

        network = Conv2D(4, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(4, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(4, (3, 3), activation='relu', padding='same')(network)
        network_output = Conv2D(2, (3, 3), activation='tanh', padding='same')(network)

        return Model(inputs=network_input, outputs=network_output)

    @staticmethod
    def load_model_from_file(filename):
        return load_model(filename)
        
    def image_a_b_gen(self):

        for batch in self.datagen.flow_from_directory(self.training_path, target_size=(self.image_size,self.image_size), batch_size=self.batch_size):
            _batch = (1.0 / 255) * batch[0]
            lab_batch = rgb2lab(_batch)
            x_batch = lab_batch[:, :, :, 0] / 512
            x_batch = x_batch.reshape(x_batch.shape + (1,))
            y_batch = lab_batch[:, :, :, 1:] / 512
            yield (x_batch, y_batch)

    def train(self):
        # tensorboard --logdir=path/to/log-directory
        opt = Adamax(lr=0.001)
        patience = 50
        tb_callback = keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=self.batch_size, write_graph=True,
                                                  write_grads=False, write_images=False, embeddings_freq=0,
                                                  embeddings_layer_names=None, embeddings_metadata=None)
        model_names = 'model.{epoch:02d}-{loss:.10f}.hdf5'
        model_checkpoint = ModelCheckpoint(os.path.join('models', model_names), monitor='loss', verbose=1, save_best_only=True)
        early_stop = EarlyStopping('loss', patience=patience)
        reduce_lr = ReduceLROnPlateau('loss', factor=0.1, patience=int(patience / 4), verbose=1)
        self.model.compile(optimizer=opt, loss='mse', metrics=['mae', 'acc'])
        self.model.fit_generator(self.image_a_b_gen(), epochs=self.epochs,
                                 steps_per_epoch=int(ceil(float(self.training_set_size) / self.batch_size)),
                                 callbacks=[tb_callback, early_stop, reduce_lr, model_checkpoint])

    def save_model(self):
        self.model.save_weights('weights_{}e_pic.h5'.format(self.epochs))
        self.model.save('model_{}e_pic_m.h5'.format(self.epochs))

    def run(self):
        self.train()
        self.save_model()
