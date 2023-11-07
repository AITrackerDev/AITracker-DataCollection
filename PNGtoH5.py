import os
import glob
import h5py
import cv2
import numpy as np
import matplotlib.pyplot as plt

IMG_WIDTH = 150
IMG_HEIGHT = 150

h5file = 'import_images.hdf5'

nfiles = len(glob.glob('./*.png'))
# for i in range(nfiles):
#     path = f'opencv_frame_{i}.png'
#     png_img = cv2.imread(path)
#     cv2.imwrite(f'img{i}.jpg', png_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

print(f'count of image files nfiles={nfiles}')

# # resize all images and load into a single dataset
# with h5py.File(h5file,'w') as  h5f:
#     img_ds = h5f.create_dataset('images',shape=(nfiles, IMG_WIDTH, IMG_HEIGHT,3), dtype=int)
#     for cnt, ifile in enumerate(glob.iglob('./*.ppm')) :
#         img = cv2.imread(ifile, cv2.IMREAD_GRAYSCALE)
#         img_resize = cv2.resize( img, (IMG_WIDTH, IMG_HEIGHT) )
#         img_ds[cnt:cnt+1:,:,:] = img_resize


# Define the path to the folder
folder_path = 'images'

# Ensure it's a directory
if os.path.isdir(folder_path):
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        print(filename)
        file_path = os.path.join(folder_path, filename)

        # Check if it's an image file (you can customize this check)
        if filename.endswith('.png') and not filename.startswith('g'):
            # Read the image
            image = cv2.imread(file_path)

            # Convert the image to grayscale
            grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Save the grayscale image with the desired filename format
            output_filename = f'g-{os.path.splitext(filename)[0]}.png'
            output_path = os.path.join(folder_path, output_filename)
            cv2.imwrite(output_path, grayscale_image)

common_size = (128, 128)

# Create a list to store resized images and labels
resized_images = []
labels = []

# Loop through the files in the directory
for filename in os.listdir(folder_path):
    if filename.startswith('g-') and filename.endswith('.png'):
        # Load the image using cv2 and resize it to the specified dimension
        img = cv2.imread(os.path.join(folder_path, filename))
        img = cv2.resize(img, common_size)
        resized_images.append(img)

        # Use the filename (without extension) as the label
        label = os.path.splitext(filename)[0]
        labels.append(label)

# Convert the lists to NumPy arrays
resized_images = np.array(resized_images)
labels = np.array(labels, dtype='S')

# Create an HDF5 file
h5f = h5py.File('image_collection.h5', 'w')

# Create datasets for resized images and labels
h5f.create_dataset('images', data=resized_images)
h5f.create_dataset('labels', data=labels)

# Close the HDF5 file
h5f.close()

h5f = h5py.File("image_collection.h5", 'r')

# Read the 'images' and 'labels' datasets
images = h5f['images'][:]
labels = h5f['labels'][:]

# Close the HDF5 file
h5f.close()


# Open the HDF5 file for reading
h5f = h5py.File('image_collection.h5', 'r')

# Read the 'images' and 'labels' datasets
images = h5f['images'][:]
labels = h5f['labels'][:]

# Close the HDF5 file
h5f.close()

# Display the images
for i in range(len(images)):
    label = labels[i].decode()  # Decode the label from bytes to string
    plt.figure()
    plt.imshow(images[i])
    plt.title(f"Label: {label}")
    plt.show()

# # Lists to store image paths and labels
# image_paths = []
#
# # Loop through all files in the images folder
# for filename in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, filename)
#
#     # Check if it's a grayscale image file (you can customize this check)
#     if filename.startswith('g-') and filename.endswith('.png'):
#         # Add the image path and label to the lists
#         image_paths.append(file_path)
#
# # Define the common image size (adjust as needed)
# common_size = (128, 128)
#
# # Create an HDF5 file for training data (U-train.h5) with 80% of the data
# h5path = 'image_collection.hdf5'
# #with h5py.File(h5path, 'w') as h5: