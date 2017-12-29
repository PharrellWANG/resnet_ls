# >> pha.zx: this file is used to counter the number of samples

import os


directory_in_str = '/Users/Pharrell_WANG/lsdata/input_for_classify'
directory = os.fsencode(directory_in_str)

counter1 = 0
counter2 = 0
for file in os.listdir(directory):
	filename = os.fsdecode(file)
	if filename.__contains__("benign"):
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
		counter2 += 1
		# print('2')
		# print(os.path.join(directory, filename))
		# print('')
	# continue
	
print('======= 1 benign:')
print(counter1)  # >> 38
print('======= 2 :')
print(counter2)  # >> 32
