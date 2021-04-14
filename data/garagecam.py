import numpy as np
import cv2
import os
from urllib.request import urlopen
from datetime import datetime

def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	return image

def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)

def normalize_image(image, width):
  r = width / image.shape[1]
  height = int(image.shape[0] * r)
  dim = (width, height) # desired size (tuple)
  # perform the actual resizing of the image
  resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
  return resized


desiredwidth = 500

while(True):
  # read image from URL
  imageL1 = url_to_image('http://10.0.0.197:8080/shot.jpg')
  imageL1 = normalize_image(imageL1,desiredwidth)

  imageP1 = url_to_image('http://10.0.0.109:8080/shot.jpg')
  imageP1 = normalize_image(imageP1,desiredwidth)

  # crop
  height = imageL1.shape[0]
  width = int(desiredwidth / 2)
  #imageL = imageL1[0:height, width:desiredwidth]
  imageL = imageL1[0:height, 0:width]

  print(width)

  #imageP = imageP1[0:height, 0:width]
  imageP = imageP1[0:height, width:desiredwidth]

  # concat
  image = hconcat_resize_min([imageL, imageP])

  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  cv2.putText(image, dt_string, 
  (10,40), # position
  cv2.FONT_HERSHEY_SIMPLEX, #font family
  1, #font size
  (209, 80, 0, 255), #font color
  2) #font stroke

  cv2.imwrite('www/left-tmp.png', imageL1)
  os.rename('www/left-tmp.png', 'www/left.png')

  cv2.imwrite('www/right-tmp.png', imageP1)
  os.rename('www/right-tmp.png', 'www/right.png')

  cv2.imwrite('www/output-tmp.png', image)
  os.rename('www/output-tmp.png', 'www/output.png')
