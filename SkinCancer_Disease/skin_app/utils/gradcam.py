import cv2
import numpy as np
import tensorflow as tf

from utils.prediction import model


def generate_gradcam(
        img_array,
        image_path,
        output_path
):

    # ResNet50 base model
    resnet = model.get_layer("resnet50")


    # Create GradCAM model
    grad_model = tf.keras.models.Model(
        inputs=resnet.input,
        outputs=[
            resnet.get_layer(
                "conv5_block3_out"
            ).output,
            resnet.output
        ]
    )


    # Calculate gradients
    with tf.GradientTape() as tape:

        conv_outputs, features = grad_model(
            img_array
        )


        x = model.get_layer(
            "global_average_pooling2d"
        )(features)


        x = model.get_layer(
            "dense"
        )(x)


        x = model.get_layer(
            "dropout"
        )(
            x,
            training=False
        )


        predictions = model.get_layer(
            "dense_1"
        )(x)


        predicted_class = tf.argmax(
            predictions[0]
        )


        loss = predictions[:, predicted_class]


    gradients = tape.gradient(
        loss,
        conv_outputs
    )


    pooled_gradients = tf.reduce_mean(
        gradients,
        axis=(0,1,2)
    )


    conv_outputs = conv_outputs[0]


    heatmap = conv_outputs @ pooled_gradients[..., tf.newaxis]


    heatmap = tf.squeeze(
        heatmap
    )


    heatmap = tf.maximum(
        heatmap,
        0
    )


    heatmap /= (
        tf.reduce_max(heatmap)
        + 1e-8
    )


    heatmap = heatmap.numpy()


    # Original image

    original = cv2.imread(
        image_path
    )


    original = cv2.resize(
        original,
        (224,224)
    )


    # Heatmap

    heatmap = cv2.resize(
        heatmap,
        (224,224)
    )


    heatmap = np.uint8(
        heatmap * 255
    )


    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )


    # Overlay

    output = cv2.addWeighted(
        original,
        0.6,
        heatmap,
        0.4,
        0
    )


    cv2.imwrite(
        output_path,
        output
    )


    print(
        "GradCAM saved:",
        output_path
    )


    return output_path