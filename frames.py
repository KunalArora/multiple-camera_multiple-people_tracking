import cv2
vidcap = cv2.VideoCapture('data/WalkByShop1front.mpg')
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite("data/WalkByShop1front/frame%d.jpg" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1

