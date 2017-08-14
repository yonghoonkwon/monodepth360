import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


def read_image(image_path, shape):
    if image_path.lower().endswith("png"):
        image = tf.image.decode_png(tf.read_file(image_path))
    else:
        image = tf.image.decode_jpeg(tf.read_file(image_path))
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize_images(image, shape, tf.image.ResizeMethod.AREA)
    return tf.expand_dims(image, 0)

def tf_read_png(image_path):
    image = tf.image.decode_png(tf.read_file(image_path))
    image = tf.image.convert_image_dtype(image, tf.float32)
    return tf.expand_dims(image, 0)

def tf_read_raw(image_path):
    image = tf.image.decode_png(tf.read_file(image_path), dtype = tf.uint16)
    return tf.expand_dims(image, 0)

def encode_image(image, type = "jpg", index = 0):
    quantized_image = tf.image.convert_image_dtype(image[index, :, :, :], tf.uint8)
    if type == "png":
        return tf.image.encode_png(quantized_image)
    else:
        return tf.image.encode_jpeg(quantized_image)
        
def encode_images(images, batch_size, type = "jpg"):
    return [encode_image(images, type, index) for index in range(batch_size)]

def write_image(image_data, filename):
    with open(filename, "wb") as image_file:
        image_file.write(image_data)

def estimate_percentile(im):
    mean = tf.reduce_mean(im)
    stdev = tf.sqrt(tf.reduce_mean((im - mean) ** 2.0))
    return mean + 1.645 * stdev
    
def gray2rgb(im):
    batch_size = tf.shape(im)[0]
    height = tf.shape(im)[1]
    width = tf.shape(im)[2]
    
    im_clip = tf.clip_by_value(im * 255.0, 0.0, 255.0)
    im_flat = tf.reshape(tf.cast(im_clip, tf.int32), [-1])
    cmap = tf.constant(plt.get_cmap('plasma').colors)
    rgb_im_flat = tf.gather(cmap, im_flat)
    rgb_im = tf.reshape(rgb_im_flat, [batch_size, height, width, 3])
    
    return rgb_im

def normalize_depth(depth):
    depth = 1.0 + tf.log(1.0 + depth)
    depth = 1.0 / (depth + 1e-6)
    depth = gray2rgb(depth)
    return depth

def write_pc(pc, filename):
    num_points = pc.shape[0]
    with open(filename, "w") as pc_file:
        pc_file.write(str(num_points))

        for point_index in range(num_points):
            x = pc[point_index, 0]
            y = pc[point_index, 1]
            z = pc[point_index, 2]
            r = pc[point_index, 3]
            g = pc[point_index, 4]
            b = pc[point_index, 5]
            pc_file.write("\n{:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f}".format(x, y, z, r, g, b))