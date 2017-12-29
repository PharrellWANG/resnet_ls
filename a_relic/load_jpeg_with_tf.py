# >> pha.zx: this file is used to make experiments on how to load jpeg in tf,
# and how to get label according to file names.

# Typical setup to include TensorFlow.
import tensorflow as tf
import os


def extract_label(s):
    # path to label logic for dataset
    # benign is 0; bad is 1.
    return 0 if os.path.basename(str(s)).__contains__('benign') else 1


# Make a queue of file names including all the JPEG images files in the relative
# image directory.
jpeg_dir = '/Users/Pharrell_WANG/lsdata/input_for_classify/*.JPEG'
filename_queue = tf.train.string_input_producer(
    tf.train.match_filenames_once(jpeg_dir))

# Read an entire image file which is required since they're JPEGs, if the images
# are too large they could be split in advance to smaller files or use the Fixed
# reader to split up the file.
image_reader = tf.WholeFileReader()

# Read a whole file from the queue, the first returned value in the tuple is the
# filename which we are ignoring.
# print('==================')
# print(filename_queue)
# print(type(filename_queue))
# print('==================')
file_name, image_file = image_reader.read(filename_queue)
# label = extract_label()
label = tf.cast(tf.py_func(extract_label, [file_name], tf.int64), tf.int32)
# label = tf.reshape(label, [])
# print('~~~~~~~~~~~~~~~~~~~~')
# print(label)
# print(type(image_file))
# print(image_file)
#
# Decode the image as a JPEG file, this will turn it into a Tensor which we can
# then use in training.
image = tf.image.decode_jpeg(image_file)

# Start a new session to show example output.
with tf.Session() as sess:
    # Required to get the filename matching to run.
    # >> Deprecated!! tf.global_variables_initializer().run()
    
    # >>
    # use this only has no problem:
    sess.run(tf.local_variables_initializer())
    # use this only has error:
    sess.run(tf.global_variables_initializer())
    # but if you use above two together, still no error :D
    # <<

    # Coordinate the loading of image files.
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    # Get an image tensor and print its value.
    image_tensor = sess.run([image])
    # file_name = sess.run([file_name])
    file_label = sess.run([label])
    # print(file_name[0])
    print('=======')
    # print(type(file_label))
    print(file_label[0])
    # print('benign' in str(str(file_name[0])))
    # print('=======')
    
    # >>
    # print(type(image_tensor))
    #<class 'list'>
    # print(len(image_tensor))
    # 1
    # print(type(image_tensor[0]))
    # (256, 400, 1)
    # print(image_tensor[0].shape)
    # <class 'numpy.ndarray'>
    # <<

    # Finish off the filename queue coordinator.
    coord.request_stop()
    coord.join(threads)
