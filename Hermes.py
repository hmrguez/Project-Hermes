import json
import cv2
import tensorflow, numpy as np
import Text.Cleaning

# Loads the models
text_model = tensorflow.keras.models.load_model('Text\profanity_model.h5')
image_model = tensorflow.keras.models.load_model('Image\sfw_nswf_identifier.h5')


# Loads the tokenizer
with open('Text/tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tensorflow.keras.preprocessing.text.tokenizer_from_json(data)

def predict_text(comment) -> dict:

    # Cleans the comment for stopwords, removing symbols, etc
    comment = Text.Cleaning.clean(comment)

    # Turns it into a vector with 1 element
    comment = np.expand_dims(comment,0)

    # Tokenizes the comment and pads it to 100 words
    token = tokenizer.texts_to_sequences(comment)
    token = tensorflow.keras.preprocessing.sequence.pad_sequences(token, 100)

    # Predicts the batch and takes the first element which is the comment
    result = text_model.predict(token)[0]

    # Returns a dictionary with each category and prediction
    result_dict = {'toxic': result[0], 'severe_toxic': result[1], 'obscene': result[2], 'threat': result[3], 'insult': result[4], 'identity_hate': result[5]}
    return result_dict



def predict_image(image_path):

    # Turns the image into a (H,W,3) tensor
    image = cv2.imread(image_path)

    # Resizes it to fit the model, batches it and normalizes the tensor to between 0 and 1
    image = tensorflow.image.resize(image, (256,256))
    image = np.expand_dims(image/255, 0)

    result = image_model.predict(image)
    return result


print(predict_image('Image/data/sfw/focused_250842800-stock-photo-happy-young-professional-asian.jpg'))