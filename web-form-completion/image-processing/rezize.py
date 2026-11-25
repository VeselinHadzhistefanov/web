import os
import io
import imageio.v3 as iio
import skimage as scimage
import pathlib
import numpy as np
from numpy import ndarray

def get_root():
  root_dir = pathlib.Path('.').absolute()
  return root_dir
root_dir = get_root()

def get_images_in_directory(dir_path) -> list[pathlib.Path]:
  file_paths = os.listdir(dir_path)
  image_paths = []
  for path in file_paths:
    file = dir_path.joinpath(path)
    if file.is_dir():
      destination_path = dir_path.joinpath(file).absolute()
      subfolder_image_paths = get_images_in_directory(destination_path)
      for subfolder_path in subfolder_image_paths:
        image_paths.append(subfolder_path)
    else :
      if file.suffix == '.jpg':
        image_paths.append(dir_path.joinpath(file))
  return image_paths

def get_ndarray_dimensions(arr):
  n = arr[0][0].size
  width = arr[0].size / n
  height = arr.size / width / n
  return (width, height, n)
  
def resize_image(img, max_resolution):
  dims = get_ndarray_dimensions(img)
  print('Input shape: ' + str(img.shape))

  factor = float(max_resolution) / max(dims[0], dims[1])
  print('Scale factor: ' + str(factor))
  resized_img = scimage.transform.rescale(img, (factor, factor, 1))
  print('Output shape: ' + str(resized_img.shape))
  return resized_img

def get_rgb_array(arr : ndarray):
  rgb_array = np.multiply(arr, 256.0)
  rgb_array = np.astype(rgb_array, 'uint8')
  print(rgb_array.dtype)
  
  return rgb_array

def read_image(img_path):
  #img_path = pathlib.Path(image_paths[n])
  print('Reading image ' + str(img_path.absolute()))
  
  # Read from path
  img = scimage.io.imread(img_path, False)
  print(img.dtype)
  
  # Resize
  rescaled_img = resize_image(img, 1500)
  
  # Create output path
  file_name = img_path.name
  output_path = root_dir.joinpath('output/' + file_name)
  print('Output file path: \n' + str(output_path.resolve()))
  
  # Write file
  output = io.BytesIO()
  #im = rescaled_img.fromarray((x * 255).astype(np.uint8))
  rescaled_img = get_rgb_array(rescaled_img)
  iio.imwrite(output_path, rescaled_img, extension = '.jpg')
 
def resize_all_images_in_path(dir):
  path = root_dir.joinpath(dir).absolute()
  image_paths = get_images_in_directory(path)

  for image_path in image_paths:
    #file = pathlib.Path(image_path)
    #read_image(image_path)
    print('Resizing image: ' + str(image_path.absolute()))
    read_image(image_path)