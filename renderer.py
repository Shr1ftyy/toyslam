import numpy as np 
import cv2
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

points = (
        (-1, 0.5, 0), (1, 0.5, 0), (-1, -0.5, 0), (1, -0.5, 0),
        (-1, 0.5, -3), (1, 0.5, -3), (1, -0.5, -3), (-1, -0.5, -3),
        )   

edges = (   (0,1), (0,2), (0,4), (2,3), (3,1), (1,5), (6,3), (6,5),
        (4,5), (2,7), (4,7), (6,7),)


class Renderer(object):
	def __init__(self):
    pass
