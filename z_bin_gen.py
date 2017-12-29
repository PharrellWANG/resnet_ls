from PIL import Image
import numpy as np
import z_settings
from sys import argv
from z_utils import get_opts


"""Collect command-line options in a dictionary

# usage1: ``python z_bin_gen.py -i train``
# usage2: ``python z_bin_gen.py -i test``

"""


def read_label_txt(label_txt, action):
  """Reads a .txt file containing file name and labels
  Args:
    label_txt: a .txt file with each line containing image file name
    and the label.
    
    action: obtained from command line, either `train` or `test`, both are of
    type string.
  """

  f = open(label_txt, 'r')
  # filenames = []
  # labels = []
  concat = []
  x = 0
  for line in f:
    x += 1
    if x < 61:
      filename, label = line[:-1].split(' ')
      # print(filename)
      # print(label)
      im = Image.open(z_settings.PROJECT_ROOT + 'lsdata/' + action + '/' + filename)
      im = (np.array(im))
      # print(im.shape)
      
      r = im.flatten()
      label = [int(label)]
      concat += list(label) + list(r)
  
  out = np.array(concat, np.uint8)
  out.tofile(z_settings.PROJECT_ROOT + "lsdata/bin/" + action + ".bin")


# file = '/Users/Pharrell_WANG/next-workspace/models/research/resnet/lsdata/Ls_ImageNameAndLabel.txt'
if __name__ == '__main__':
  my_args = get_opts(argv)
  # if '-i' in myargs:  # Example usage.
  #     print(myargs['-i'])
  # print(myargs)
  # print(my_args['-i'])
  # print(type(my_args['-i']))
  action_x = my_args['-i']
  file = z_settings.PROJECT_ROOT + 'lsdata/label_' + action_x + '.txt'
  read_label_txt(file, action_x)
