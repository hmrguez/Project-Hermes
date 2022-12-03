# Project-Hermes

Hermes is a sentiment text classifier for profanity detection and an innapropiate image classifier.

## `Introduction`

The idea behind this repository is to see how content filtering on places like forums or social media works.

Also this is a part of a series of projects being delivered by the team in the AI scientific group of students at Havana University

## `Description`

### `Text Classifier`

The text classifier is a multi-hot-encoding LSTM text classifier with the categories as follows: toxic, severe toxic, obscene, threat, insult and identity hate. 

`Full code` [here](Text/TrainingModel.ipynb)

First of all the text becomes "cleaned". It is performed by the clean method which removes every stopword, ip adress, non alphabetic symbol, etc, so that only "important" word gets through and to remove unnecesary noise in the network.

It uses a model serving as follows:

``` py
inp = Input(shape=(100, ))

# size of the vector space
embed_size = 128
x = Embedding(20000, embed_size)(inp)

output_dimention = 60
x = LSTM(output_dimention, return_sequences=True, name='lstm_layer')(x)
# reduce dimention
x = GlobalMaxPool1D()(x)
# disable 10% precent of the nodes
x = Dropout(0.1)(x)
# pass output through a RELU function
x = Dense(50, activation="relu")(x)
# another 10% dropout
x = Dropout(0.1)(x)
# pass the output through a sigmoid layer, since 
# we are looking for a binary (0,1) classification 
x = Dense(6, activation="sigmoid")(x)

model = Model(inputs=inp, outputs=x)
# we use binary_crossentropy because of binary classification
# optimise loss by Adam optimiser
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
```

Given a sataset of around 160k written Wikipedia forum comments the networks behaved with an overall validation accuracy of 98%

Full dataset can be found [here](https://www.kaggle.com/c/8076/download/train.csv.zip). Once downloaded in order to test it it must be placed within the Text/Raw Dataset folder or changed int the code.

The testing script can be located [here](Text\TestingModel.ipynb)

### `Image Classifier`

The image classifier is a binary classifier where values <= 0.5 mean unnappropiate and in any other case it means appropriate.

The full code can be found [here](Image\TrainingModel.ipynb)

To load the data it creates a tensorflow.data.Dataset pipeline by labeling elements within the two folder in the data folder, batching them and resizing them to a default of 256x256. The only thing done manually is filtering the data so that only items that can be read by the model are present, which is done with the cv2 and imghdr modules.

The model can be summarized as follows:

```py
model = tf.keras.models.Sequential()

model.add(tf.keras.layers.Conv2D(16, (3,3), 1, activation='relu', input_shape=(256,256,3)))
model.add(tf.keras.layers.MaxPooling2D())

model.add(tf.keras.layers.Conv2D(32, (3,3), 1, activation='relu'))
model.add(tf.keras.layers.MaxPooling2D())

model.add(tf.keras.layers.Conv2D(16, (3,3), 1, activation='relu'))
model.add(tf.keras.layers.MaxPooling2D())

model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(256,activation='relu'))
model.add(tf.keras.layers.Dense(1,activation='sigmoid'))

model.compile('adam', loss='binary_crossentropy')
```

Dataset is made entirely by random google images that serve the purpose of the labels. Actually the model is so flexible that the same repository can be used to any binary classification, not only the one it is currently being used for

## Using

### Requirements
- Tensorflow
- Numpy
- OpenCV
- NLTK
- Matplotlib


1. Clone the repo and download the necessary databases as indicated in the sections above
2. Open the TrainingModel.ipynb of the one you wish to test and run all cells, it should create the model.h5 file
3. In the repo root folder should be the Hermes.py with two functions: predict_text and predict_images. Follow the instructions in there and you should be good to go