import sys
import glob
import h5py
import cv2
import numpy as np

IMG_WIDTH = 30
IMG_HEIGHT = 30

h5file = 'import_images.hdf5'

nfiles = len(glob.glob('./*.jpg'))
for i in range(nfiles):
    path = f'opencv_frame_{i}.png'
    png_img = cv2.imread(path)
    cv2.imwrite(f'img{i}.jpg', png_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

print(f'count of image files nfiles={nfiles}')

# resize all images and load into a single dataset
with h5py.File(h5file,'w') as  h5f:
    img_ds = h5f.create_dataset('images',shape=(nfiles, IMG_WIDTH, IMG_HEIGHT,3), dtype=int)
    for cnt, ifile in enumerate(glob.iglob('./*.ppm')) :
        img = cv2.imread(ifile, cv2.IMREAD_GRAYSCALE)
        img_resize = cv2.resize( img, (IMG_WIDTH, IMG_HEIGHT) )
        img_ds[cnt:cnt+1:,:,:] = img_resize

    fileR = h5py.File("import_images.hdf5", "r")
    data = np.array(img_ds)
    print("Example Data:")
    print(data)
