import numpy as np
import cv2
import slam

# Initiate ORB detector
class DetectFeatures(object):
  def __init__(self, chosen_detector=cv2.ORB_create(3000)):
    self._detector = chosen_detector
    self.prev = None

  def detect_getF(self, img):
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
          good.append([m])

      #TODO: merge this subroutine to the other loop? - removed it 
      # Normalized 8 point algorithm to find F
      # Need to offset to centre of camera and normalize with dimensions of camera
      # TODO: YIKES
      pts1  = np.asarray([[ ((kp1[M[0].queryIdx].pt[0] - h/2)/h, (kp1[M[0].queryIdx].pt[1] - w/2)/w) ]  for M in good])
      pts2  = np.asarray([[ ((kp2[M[0].trainIdx].pt[0] - h/2)/h, (kp2[M[0].trainIdx].pt[1] - w/2)/w) ]  for M in good])
      # pts2  = np.asarray([kp2[M[0].trainIdx].pt for M in good])
      # Compute fundamental matrix
      F, inliers = slam.getF(pts1, pts2)
      if inliers is None:
        self.prev = img
        return img, None, None

      detection = img

      p1 = [kp1[good[I][0].queryIdx].pt for I in range(len(good)) if inliers[I]]
      p2 = [kp2[good[J][0].trainIdx].pt for J in range(len(good)) if inliers[J]]

      for pt in range(len(p1)):

        detection = cv2.circle(detection, (int(p2[pt][0]), int(p2[pt][1])), 1, (0, 255, 0), 3)
        detection = cv2.line(detection, (int(p1[pt][0]), int(p1[pt][1])), (int(p2[pt][0]), int(p2[pt][1])), (0, 0, 255), 2)

      


# cv2.drawMatchesKnn expects list of lists as matches.
#      detection = cv2.drawMatchesKnn(self.prev,kp1,img,kp2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
      self.prev = img
      return detection, F, pts2
    else:
      self.prev = img
      return img, None, None
