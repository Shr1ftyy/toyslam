import numpy as np
import cv2

# Initiate ORB detector
class DetectFeatures(object):
  def __init__(self, chosen_detector=cv2.ORB_create(5000)):
    self._detector = chosen_detector
    self.prev = None

  #TODO: Make detections window prettier!
  def detect(self, img):
  # find the keypoints and descriptors with chosen detector
    if self.prev is not None:
      h, w = np.shape(img)[0], np.shape(img)[1]
      kp1, des1 = self._detector.detectAndCompute(self.prev,None)
      kp2, des2 = self._detector.detectAndCompute(img,None)
    # BFMatcher with default params
      bf = cv2.BFMatcher()
      matches = bf.knnMatch(des1,des2,k=2)
    # Apply ratio test
      good = []

      for m,n in matches:
        if m.distance < 0.5*n.distance:
          good.append([m, n])
      
      #TODO: merge this subroutine to the other loop? 
      detection = img
      for match in good:
        M, N = match[0], match[1]
        p1 = kp1[N.queryIdx].pt
        p2 = kp2[M.trainIdx].pt
        print("******")
        print(p1)
        print(p2)
        #need to flip elements to work with cv2.imshow()
        detection = cv2.circle(detection, (int(p2[0]), int(p2[1])), 1, (0, 255, 0), 2)
        detection = cv2.line(detection, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (0, 0, 255), int(1))
        # assert np.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2) == g.distance



# cv2.drawMatchesKnn expects list of lists as matches.
#      detection = cv2.drawMatchesKnn(self.prev,kp1,img,kp2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
      self.prev = img
      return detection
    else:
      self.prev = img
      return img
