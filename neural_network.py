from keras.layers import Conv2D, UpSampling2D, Input, Reshape, concatenate, MaxPooling2D, Dropout, BatchNormalization, \
    GaussianDropout, AlphaDropout
from keras.models import Model, load_model
from keras.preprocessing.image import img_to_array, load_img, ImageDataGenerator
from keras.optimizers import Adamax
from skimage.color import rgb2lab, lab2rgb, rgb2gray, gray2rgb
import keras
import numpy as np
import os


class NeuralNetwork(object):
    def __init__(self, training_path, epochs=1, batch_size=30, path_to_model=None):
        self.training_path = training_path
        self.training_images = [filename for filename in os.listdir(self.training_path)[::100] if filename.endswith(".png")]
        self.epochs = epochs
        self.batch_size = batch_size
        if path_to_model is None:
            self.model = NeuralNetwork.neural_network_structure()
        else:
            self.model = NeuralNetwork.load_model_from_file(path_to_model)

    @staticmethod
    def neural_network_structure():
        network_input = Input(shape=(256, 256, 1,))

        first_path = Conv2D(4, (3, 3), padding='same', activation='relu')(network_input)
        first_path = Conv2D(8, (3, 3), padding='same', activation='relu')(first_path)
        second_path = Conv2D(8, (3, 3), padding='same', activation='relu')(network_input)
        second_path = Conv2D(8, (3, 3), padding='same', activation='relu')(second_path)
        third_path = Conv2D(8, (3, 3), padding='same', activation='relu')(network_input)
        third_path = Conv2D(16, (3, 3), padding='same', activation='relu')(third_path)

        inception_output = concatenate([first_path, second_path, third_path], axis=3)

        network = Conv2D(16, (3, 3), activation='relu', padding='same')(inception_output)
        network = Conv2D(16, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(16, (3, 3), activation='relu', padding='same')(network)
        # network = BatchNormalization()(network)
        network = MaxPooling2D((2, 2))(network)
        network = GaussianDropout(0.2)(network)
        network = Conv2D(32, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(32, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(32, (3, 3), activation='tanh', padding='same')(network)
        # network = BatchNormalization()(network)
        network = MaxPooling2D((2, 2))(network)
        network = GaussianDropout(0.2)(network)
        network = Conv2D(64, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(64, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(64, (3, 3), activation='relu', padding='same')(network)
        # network = BatchNormalization()(network)
        network = MaxPooling2D((2, 2))(network)
        network = GaussianDropout(0.2)(network)
        network = Conv2D(128, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(128, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(128, (3, 3), activation='tanh', padding='same')(network)
        # network = BatchNormalization()(network)
        network = MaxPooling2D((2, 2))(network)
        network = GaussianDropout(0.2)(network)
        network = Conv2D(256, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(256, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(256, (3, 3), activation='relu', padding='same')(network)
        # network = BatchNormalization()(network)
        network = UpSampling2D((2, 2))(network)
        network = GaussianDropout(0.2)(network)
        network = Conv2D(128, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(128, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(128, (3, 3), activation='tanh', padding='same')(network)
        # network = BatchNormalization()(network)
        network = UpSampling2D((2, 2))(network)
        network = GaussianDropout(0.2)(network)
        network = Conv2D(64, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(64, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(64, (3, 3), activation='relu', padding='same')(network)
        # network = BatchNormalization()(network)
        network = UpSampling2D((2, 2))(network)
        network = GaussianDropout(0.2)(network)
        network = Conv2D(32, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(32, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(32, (3, 3), activation='tanh', padding='same')(network)
        # network = BatchNormalization()(network)
        network = UpSampling2D((2, 2))(network)
        network = GaussianDropout(0.2)(network)
        network = Conv2D(16, (3, 3), activation='relu', padding='same')(network)
        network = Conv2D(16, (3, 3), activation='tanh', padding='same')(network)
        network = Conv2D(16, (3, 3), activation='relu', padding='same')(network)
        # network = BatchNormalization()(network)

        first_path_2 = Conv2D(16, (3, 3), padding='same', activation='relu')(network)
        first_path_2 = Conv2D(8, (3, 3), padding='same', activation='relu')(first_path_2)
        second_path_2 = Conv2D(8, (3, 3), padding='same', activation='relu')(network)
        second_path_2 = Conv2D(8, (3, 3), padding='same', activation='relu')(second_path_2)
        third_path_2 = Conv2D(8, (3, 3), padding='same', activation='relu')(network)
        third_path_2 = Conv2D(4, (3, 3), padding='same', activation='relu')(third_path_2)

        inception_output_2 = concatenate([first_path_2, second_path_2, third_path_2], axis=3)

        network = Conv2D(4, (3, 3), activation='relu', padding='same')(inception_output_2)
        network_output = Conv2D(2, (3, 3), activation='tanh', padding='same')(network)

        return Model(inputs=network_input, outputs=network_output)

    @staticmethod
    def load_model_from_file(filename):
        return load_model(filename)
        
    def image_a_b_gen(self):
        datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, rotation_range=20, horizontal_flip=True)
        for batch in datagen.flow_from_directory(self.training_path):
            grayscaled_rgb = gray2rgb(rgb2gray(batch))
            embed = create_inception_embedding(grayscaled_rgb)
            lab_batch = rgb2lab(batch)
            X_batch = lab_batch[:,:,:,0]
            X_batch = X_batch.reshape(X_batch.shape+(1,))
            Y_batch = lab_batch[:,:,:,1:] / 128
            yield ([X_batch, create_inception_embedding(grayscaled_rgb)], Y_batch)

    def train(self):
        # tensorboard --logdir=path/to/log-directory
        opt = Adamax(lr=0.001)
        tb_callback = keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=32, write_graph=True,
                                                  write_grads=False, write_images=False, embeddings_freq=0,
                                                  embeddings_layer_names=None, embeddings_metadata=None)
        self.model.compile(optimizer=opt, loss='mse', metrics=['mae', 'acc'])
        self.model.fit_generator(self.image_a_b_gen(), epochs=self.epochs,
                                 steps_per_epoch=len(self.training_images),
                                 callbacks=[tb_callback])

    def save_model(self):
        self.model.save_weights('weights_{}e_{}pic.h5'.format(self.epochs, self.training_images.__len__()))
        self.model.save('model_{}e_{}pic_m.h5'.format(self.epochs, self.training_images.__len__()))

    def run(self):

        self.train()
        self.save_model()
