import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

import tensorflow_hub as hub
import tensorflow as tf


style_image = plt.imread("images/1.jpg")

style_image = style_image.astype(np.float32)[np.newaxis, ...] / 255.
# Optionally resize the images. It is recommended that the style image is about
# 256 pixels (this size was used when training the style transfer network).
# The content image can be any size.
# style_image = tf.image.resize(style_image, (512, 512))


model = hub.load("https://hub.tensorflow.google.cn/captain-pool/esrgan-tf2/1")
# To add an extra dimension for batch, use tf.expand_dims()
low_resolution_image =style_image # Low Resolution Image of shape [batch_size, height, width, 3]
low_resolution_image = tf.constant(tf.cast(low_resolution_image, tf.float32))
super_resolution = model(low_resolution_image) # Perform Super Resolution here

stylized_image =tf.cast(tf.clip_by_value(super_resolution[0], 2048, 2048), tf.uint8)

plt.imshow(stylized_image)
plt.axis('off')

# from io import BytesIO
# figfile = BytesIO()
# plt.savefig('figfile.png', format='png')
# plt.savefig(figfile, format='png')
# figfile.seek(0)
# import base64
# figdata_png = base64.b64encode(figfile.getvalue())
# print(figfile)

# plt.imshow(stylized_image[0])
plt.show()