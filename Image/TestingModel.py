import tensorflow as tf, numpy as np, cv2

model = tf.keras.models.load_model('sfw_nswf_identifier.h5')


img_name_and_ext = ''

img1test = cv2.imread(img_name_and_ext)
resize = tf.image.resize(img1test, (256,256))
yhat = model.predict(np.expand_dims(resize/255,0))
print(yhat)