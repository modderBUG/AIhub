import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub


# Load content and style images (see example in the attached colab).

def stylization(content_image, style_image):
    # Convert to float32 numpy array, add batch dimension, and normalize to range [0, 1]. Example using numpy:
    content_image = content_image.astype(np.float32)[np.newaxis, ...] / 255.
    style_image = style_image.astype(np.float32)[np.newaxis, ...] / 255.
    # Optionally resize the images. It is recommended that the style image is about
    # 256 pixels (this size was used when training the style transfer network).
    # The content image can be any size.
    style_image = tf.image.resize(style_image, (256, 256))

    # Load image stylization module.
    hub_module = hub.load('https://hub.tensorflow.google.cn/google/magenta/arbitrary-image-stylization-v1-256/2')

    # Stylize image.
    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0]

    plt.imshow(stylized_image[0], aspect='equal')
    plt.axis('off')
    from io import BytesIO
    figfile = BytesIO()
    # plt.savefig('figfile.png', format='png')
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    import base64
    figdata_png = base64.b64encode(figfile.getvalue())
    return figfile,figdata_png
    # plt.imshow(stylized_image[0], aspect='equal')
    # plt.axis('off')
    # plt.savefig('title' + '.png', bbox_inches='tight', dpi=300, pad_inches=0.0)
    # plt.show()




if __name__ =="__main__":
    pass

