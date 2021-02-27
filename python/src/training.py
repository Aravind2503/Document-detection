from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
# from tensorflow.keras.applications.inception_v3 import InceptionV3
from keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
import numpy as np
from glob import glob
import shutil


def train_model():

    shutil.rmtree('../model/model2')

    IMAGE_SIZE = [224, 224]

    train_path = '../resources/ml/train'
    test_path = '../resources/ml/test'


    # Import the inception v3 library as shown below and add preprocessing layer to the front of VGG
    # Here we will be using imagenet weights

    inception = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)



    # don't train existing weights
    for layer in inception.layers:
        layer.trainable = False

    # useful for getting number of output classes
    folders = glob(train_path+'/*')
    print(folders)


    # our layers - you can add more if you want
    x = Flatten()(inception.output)


    prediction = Dense(len(folders), activation='softmax')(x)

    # create a model object
    model = Model(inputs=inception.input, outputs=prediction)


    # view the structure of the model
    model.summary()


    # tell the model what cost and optimization method to use
    model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
    )

    # Use the Image Data Generator to import the images from the dataset
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    train_datagen = ImageDataGenerator(rescale = 1./255,
                                    shear_range = 0.2,
                                    zoom_range = 0.2,
                                    horizontal_flip = True)

    test_datagen = ImageDataGenerator(rescale = 1./255)


    # Make sure you provide the same target size as initialied for the image size
    training_set = train_datagen.flow_from_directory(train_path,
                                                    target_size = (224, 224),
                                                    batch_size = 2,
                                                    class_mode = 'categorical')


    test_set = test_datagen.flow_from_directory(test_path,
                                                target_size = (224, 224),
                                                batch_size = 2,
                                                class_mode = 'categorical')


    # fit the model
    # Run the cell. It will take some time to execute
    r = model.fit(
    training_set,
    validation_data=test_set,
    epochs=3,
    steps_per_epoch=len(training_set),
    validation_steps=len(test_set)
    )


    model.save('../model/model2')


if __name__=='__main__':
    train_model()
