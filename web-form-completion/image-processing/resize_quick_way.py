import imageio.v3 as iio
from pathlib import Path

def get_image_paths(dir):
  image_paths = list()
  path = Path('.').joinpath(dir).resolve()
  print(path)
  for file in Path.iterdir(path):
      if not file.is_file():
        continue
      if not (file.suffix == '.jpg' or file.suffix == '.jpeg'):
        continue
      image_paths.append(file)
      print(file.resolve())
  return image_paths

def get_images(list):
  images = []
  for file in list:
    images.append(iio.imread(file))
  return images

root = Path().resolve()
paths = get_image_paths('inputs')
images = get_images(paths)

