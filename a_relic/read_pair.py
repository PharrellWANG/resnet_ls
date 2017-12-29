# pha.zx >> this file shows how to read lines in text file.
# note: need to add a blank line at the end of the `image_list_file`


def read_labeled_image_list(image_list_file):
	"""Reads a .txt file containing pathes and labeles
	Args:
		 image_list_file: a .txt file with one /path/to/image per line
		 label: optionally, if set label will be pasted after each line
	Returns:
		 List with all filenames in file image_list_file
	"""
	f = open(image_list_file, 'r')
	filenames = []
	labels = []
	for line in f:
		filename, label = line[:-1].split(' ')
		print(type(filename))
		print(type(label))
		filenames.append(filename)
		labels.append(int(label))
	return filenames, labels


file = '/Users/Pharrell_WANG/lsdata/Ls_ImageNameAndLabel.txt'
filenames, labels = read_labeled_image_list(file)
print(filenames)
print(labels)
