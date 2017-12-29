# pha.zx >> this example shows how to convert jpeg to bin file.

from PIL import Image
import numpy as np

im = Image.open('24benign.JPEG')
im = (np.array(im))
print(im.shape)

r = im.flatten()
# r = im[:, :, 0].flatten()
# g = im[:, :, 1].flatten()
# b = im[:, :, 2].flatten()
label = [1]

# out = np.array(list(label) + list(r) + list(g) + list(b), np.uint8)
out = np.array(list(label) + list(r), np.uint8)
out.tofile("24benignJPEG.bin")
