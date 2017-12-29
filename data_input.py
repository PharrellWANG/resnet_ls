# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Dataset input module.
"""

import tensorflow as tf
import os

#
# def extract_label(s):
#     # path to label logic for dataset
#     # benign is 0; bad is 1.
#     return 0 if os.path.basename(str(s)).__contains__('benign') else 1


def build_input(dataset, data_path, batch_size, mode):
  """Build CIFAR image and labels.

  Args:
    dataset: Either 'cifar10' or 'cifar100'.
    data_path: Filename for data.
    batch_size: Input batch size.
    mode: Either 'train' or 'eval'.
  Returns:
    images: Batches of images. [batch_size, image_size, image_size, 3]
    labels: Batches of labels. [batch_size, num_classes]
  Raises:
    ValueError: when the specified dataset is not supported.
  """
  # image_size = 32
  if dataset == 'cifar10' or dataset == 'cifar100':
    if dataset == 'cifar10':
      depth = 3
      image_height = 32
      image_width = 32
      label_bytes = 1
      label_offset = 0
      num_classes = 10
    elif dataset == 'cifar100':
      depth = 3
      image_height = 32
      image_width = 32
      label_bytes = 1
      label_offset = 1
      num_classes = 100
    # elif dataset == 'lsdata':
    #   depth = 1
    #   image_height = 256
    #   image_width = 400
    #   label_bytes = 1
    #   label_offset = 1
    #   num_classes = 100
    else:
      raise ValueError('Not supported dataset %s', dataset)
  
    # depth = 3
    image_bytes = image_height * image_width * depth
    record_bytes = label_bytes + label_offset + image_bytes
  
    data_files = tf.gfile.Glob(data_path)
    file_queue = tf.train.string_input_producer(data_files, shuffle=True)
    # Read examples from files in the filename queue.
    reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)
    _, value = reader.read(file_queue)
  
    # Convert these examples to dense labels and processed images.
    record = tf.reshape(tf.decode_raw(value, tf.uint8), [record_bytes])
    label = tf.cast(tf.slice(record, [label_offset], [label_bytes]), tf.int32)
    # Convert from string to [depth * height * width] to [depth, height, width].
    depth_major = tf.reshape(tf.slice(record, [label_offset + label_bytes], [image_bytes]),
                             [depth, image_height, image_width])
    # Convert from [depth, height, width] to [height, width, depth].
    #  (256, 400, 1)
    image = tf.cast(tf.transpose(depth_major, [1, 2, 0]), tf.float32)
    if mode == 'train':
      # image = tf.image.resize_image_with_crop_or_pad(
      #     image, image_height+4, image_width+4)
      # image = tf.random_crop(image, [image_height, image_width, depth])
      image = tf.image.random_flip_left_right(image)
      # Brightness/saturation/constrast provides small gains .2%~.5% on cifar.
      # image = tf.image.random_brightness(image, max_delta=63. / 255.)
      # image = tf.image.random_saturation(image, lower=0.5, upper=1.5)
      # image = tf.image.random_contrast(image, lower=0.2, upper=1.8)
      image = tf.image.per_image_standardization(image)
  
      example_queue = tf.RandomShuffleQueue(
        capacity=16 * batch_size,
        min_after_dequeue=8 * batch_size,
        dtypes=[tf.float32, tf.int32],
        shapes=[[image_height, image_width, depth], [1]])
      num_threads = 16
    else:
      # image = tf.image.resize_image_with_crop_or_pad(
      #     image, image_height, image_width)
      image = tf.image.per_image_standardization(image)
  
      example_queue = tf.FIFOQueue(
        3 * batch_size,
        dtypes=[tf.float32, tf.int32],
        shapes=[[image_height, image_width, depth], [1]])
      num_threads = 1
    
  # elif dataset == 'lsdata':
  else:
    depth = 1
    image_height = 256
    image_width = 400
    label_bytes = 1
    label_offset = 0
    num_classes = 2

    image_bytes = image_height * image_width * depth
    record_bytes = label_bytes + label_offset + image_bytes

    data_files = tf.gfile.Glob(data_path)
    file_queue = tf.train.string_input_producer(data_files, shuffle=True)
    # Read examples from files in the filename queue.
    reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)
    _, value = reader.read(file_queue)

    # Convert these examples to dense labels and processed images.
    record = tf.reshape(tf.decode_raw(value, tf.uint8), [record_bytes])
    label = tf.cast(tf.slice(record, [label_offset], [label_bytes]), tf.int32)
    # Convert from string to [depth * height * width] to [depth, height, width].
    depth_major = tf.reshape(
      tf.slice(record, [label_offset + label_bytes], [image_bytes]),
      [depth, image_height, image_width])
    # Convert from [depth, height, width] to [height, width, depth].
    #  (256, 400, 1)
    image = tf.cast(tf.transpose(depth_major, [1, 2, 0]), tf.float32)
    
    # ========= does not work because of the label issue, pha.zx
    # Make a queue of file names including all the JPEG images files in the relative
    # image directory.
    # jpeg_dir = data_path
    # filename_queue = tf.train.string_input_producer(
    #   tf.train.match_filenames_once(jpeg_dir))
		#
    # # Read an entire image file which is required since they're JPEGs, if the images
    # # are too large they could be split in advance to smaller files or use the Fixed
    # # reader to split up the file.
    # image_reader = tf.WholeFileReader()
		#
    # # Read a whole file from the queue, the first returned value in the tuple is the
    # # filename which we are ignoring.
    # # print('==================')
    # # print(filename_queue)
    # # print(type(filename_queue))
    # # print('==================')
    # file_name, image_file = image_reader.read(filename_queue)
    # label = 0 if os.path.basename(str(file_name)).__contains__('benign') else 1
    # # label = extract_label()
    # # label = tf.cast(tf.py_func(extract_label, [file_name], tf.int64), tf.int32)
    # label = tf.cast(label, tf.int32)
    # # label = tf.cast(label, tf.int32)
    # label = tf.reshape(label, (1,))
    # # label = tf.reshape(label, [])
    # # print('~~~~~~~~~~~~~~~~~~~~')
    # # print(label)
    # # print(type(image_file))
    # # print(image_file)
    # #
    # # Decode the image as a JPEG file, this will turn it into a Tensor which we can
    # # then use in training.
    # image = tf.image.decode_jpeg(image_file)
    # image = tf.cast(image, tf.float32)
    # ========= does not work because of the label issue, pha.zx

    if mode == 'train':
      # image = tf.image.resize_image_with_crop_or_pad(
      #     image, image_height+4, image_width+4)
      # image = tf.random_crop(image, [image_height, image_width, depth])
      image = tf.image.random_flip_left_right(image)
      # Brightness/saturation/constrast provides small gains .2%~.5% on cifar.
      # image = tf.image.random_brightness(image, max_delta=63. / 255.)
      # image = tf.image.random_saturation(image, lower=0.5, upper=1.5)
      # image = tf.image.random_contrast(image, lower=0.2, upper=1.8)
      image = tf.image.per_image_standardization(image)
  
      example_queue = tf.RandomShuffleQueue(
          capacity=4 * batch_size,
          min_after_dequeue=2 * batch_size,
          dtypes=[tf.float32, tf.int32],
          shapes=[[image_height, image_width, depth], [1]])
      num_threads = 16
    else:
      # image = tf.image.resize_image_with_crop_or_pad(
      #     image, image_height, image_width)
      image = tf.image.per_image_standardization(image)
  
      example_queue = tf.FIFOQueue(
          2 * batch_size,
          dtypes=[tf.float32, tf.int32],
          shapes=[[image_height, image_width, depth], [1]])
      num_threads = 1

  example_enqueue_op = example_queue.enqueue([image, label])
  tf.train.add_queue_runner(tf.train.queue_runner.QueueRunner(
      example_queue, [example_enqueue_op] * num_threads))

  # Read 'batch' labels + images from the example queue.
  images, labels = example_queue.dequeue_many(batch_size)
  labels = tf.reshape(labels, [batch_size, 1])
  indices = tf.reshape(tf.range(0, batch_size, 1), [batch_size, 1])
  labels = tf.sparse_to_dense(
      tf.concat(values=[indices, labels], axis=1),
      [batch_size, num_classes], 1.0, 0.0)

  assert len(images.get_shape()) == 4
  assert images.get_shape()[0] == batch_size
  assert images.get_shape()[-1] == depth
  assert len(labels.get_shape()) == 2
  assert labels.get_shape()[0] == batch_size
  assert labels.get_shape()[1] == num_classes

  # Display the training images in the visualizer.
  tf.summary.image('images', images)
  return images, labels
