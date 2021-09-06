import numpy as np
import cv2


# Add Frobenius Norm if needed
def getF(pts1, pts2): 
  F, mask = cv2.findFundamentalMat(pts1,pts2, method=cv2.FM_8POINT, ransacReprojThreshold=1, confidence=0.99, maxIters=5000)
  if np.linalg.matrix_rank(F) == 2:
    return F, mask
  else:
    return None, None


# Returns camera matrix given Fundamental Matrix
def getP(pts, F):
  U, S, V_T = np.linalg.svd(F)
  # Find null left and right null space of F - returns the epipoles on both images
  # The value below is the epipole in second image
  e_prime = V_T[:, -1]
  return e_prime
  

# returns a skew-symmetric matrix version of the input vector
def skew(x):
	return np.array([[0, -x[2], x[1]],
									 [x[2], 0, -x[0]],
									 [-x[1], x[0], 0]])


