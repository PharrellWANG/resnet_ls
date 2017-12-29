# >> pha.zx: generate label*.txt file from a directory of images
# the class of each image has been indicated by their name.

import os
import z_settings
from z_utils import get_opts
from sys import argv


def generate_label_txt(action):

  train_data_folder = z_settings.PROJECT_ROOT + 'lsdata/' + action
  directory = os.fsencode(train_data_folder)
  
  counter1 = 0
  counter2 = 0
  with open(z_settings.PROJECT_ROOT + "lsdata/label_" + action + ".txt", "w") \
		as text_file:
    # text_file.write("Purchase Amount: %s" % TotalAmount)
    cnt = 0
    for file in os.listdir(directory):
      cnt += 1
      # on macOS, skip .DS_Store, maybe in linux no need.
      # if no need to skip the first file,
      # just change below line to `cnt == 0`
      if cnt == z_settings.SKIP_FIRST_FILE:
        continue
      else:
        filename = os.fsdecode(file)
        if filename.__contains__("benign"):
          text_file.write(filename + ' 0\n')
          # print('~~~~~~xx1')
          # print(str(directory))
          # print(type(str(directory)))
          # print('~~~~~~111')
          # print('~~~~~~xx2')
          # print(filename)
          # print(type(filename))
          # print('~~~~~~222')
          counter1 += 1
        # print('1')
        # print(os.path.join(str(directory), filename))
        # print('')
        # continue
        else:
          
          text_file.write(filename + ' 0\n')
          counter2 += 1
        # print('2')
        # print(os.path.join(directory, filename))
        # print('')
    # continue
  #
  print('======= 1 benign:')
  print(counter1)  # >> 38
  print('======= 2 :')
  print(counter2)  # >> 32
  # assert(counter1 == 30)
  # assert(counter2 == 30)


if __name__ == '__main__':
  my_args = get_opts(argv)
  action_x = my_args['-i']
	
  generate_label_txt(action_x)
