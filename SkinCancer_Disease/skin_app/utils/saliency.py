import cv2
import numpy as np
import tensorflow as tf

from utils.prediction import model



def generate_saliency(
        img_array,
        image_path,
        output_path
):


    input_tensor = tf.convert_to_tensor(
        img_array
    )


    with tf.GradientTape() as tape:

        tape.watch(
            input_tensor
        )


        predictions = model(
            input_tensor
        )


        predicted_class = tf.argmax(
            predictions[0]
        )


        loss = predictions[
            :,
            predicted_class
        ]


    gradients = tape.gradient(
        loss,
        input_tensor
    )


    gradients = tf.abs(
        gradients
    )


    saliency = tf.reduce_max(
        gradients,
        axis=-1
    )


    saliency = saliency[0].numpy()


    saliency -= saliency.min()


    saliency /= (
        saliency.max()
        + 1e-8
    )


    saliency = np.uint8(
        saliency * 255
    )


    saliency = cv2.applyColorMap(
        saliency,
        cv2.COLORMAP_HOT
    )


    original = cv2.imread(
        image_path
    )


    original = cv2.resize(
        original,
        (224,224)
    )


    output = cv2.addWeighted(
        original,
        0.6,
        saliency,
        0.4,
        0
    )


    cv2.imwrite(
        output_path,
        output
    )


    print(
        "Saliency saved:",
        output_path
    )


    return output_path