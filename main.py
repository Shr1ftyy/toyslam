import cv2
import numpy as np
from detector import DetectFeatures
import slam
# initialize detector class
dtctr = DetectFeatures()

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('vids/v.mp4')

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:

    # Display the resulting frame

    D, F, pts = dtctr.detect_getF(frame)
    cv2.imshow('Detections',D)
    if F is not None:
      e_p = slam.getP(pts, F) 
      #find P
      e_x = slam.skew(e_p)
      P_p = np.column_stack((np.dot(e_x, F), e_p.T))
      print(P_p)
      

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  # Break the loop
  else: 
    break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
