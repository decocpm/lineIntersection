# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy
import numpy.linalg

width, height = 800, 600
begin = 0
point = 0
pointList = []
lineList = []
intersectionList = []
pointSeq = 0
lineSeq = 0
interSeq = 0

class Point():
    id = 0
    def __init__(self, x, y):
        global pointSeq
        self.x = x
        self.y = y
        pointSeq += 1
        self.id = pointSeq
        print "P%s(%s,%s) created" % (self.id, self.x, self.y)
    
class Line():
    id = 0
    def __init__(self, p1, p2):
        global lineSeq
        self.p1 = p1
        self.p2 = p2
        lineSeq += 1
        self.id = lineSeq
        print "L%s(P%s,P%s) created" % (self.id, self.p1.id, self.p2.id)
        
class Intersection():
    id = 0
    def __init__(self, p, l1, l2):
        global interSeq
        self.p = p
        self.l1 = l1
        self.l2 = l2
        interSeq += 1
        self.id = interSeq
        print "I%s(L%s,L%s) created" % (self.id, self.l1.id, self.l2.id)
    
def orientation(p1, p2, p3):
    matrix = [[1, 1, 1], [p1.x, p2.x, p3.x], [p1.y, p2.y, p3.y]]
    return numpy.linalg.det(matrix)

def checkIntersections(line):
    for l in lineList:
        #check intersection
        if ((orientation(line.p1, line.p2, l.p1) * orientation(line.p1, line.p2, l.p2) < 0) and 
              (orientation(l.p1, l.p2, line.p1) * orientation(l.p1, l.p2, line.p2) < 0)):
            getIntersectionPoint(line, l)

def getIntersectionPoint(l1, l2):
    global intersectionList
    
    L1 = line([l1.p1.x, l1.p1.y], [l1.p2.x, l1.p2.y])
    L2 = line([l2.p1.x, l2.p1.y], [l2.p2.x, l2.p2.y])
    
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    x = Dx / D
    y = Dy / D
    print 'Intersection point: P(%s,%s)' % (x, y)
    i = Intersection(Point(x, y), l1, l2)
    intersectionList.append(i)
    
 
def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C
    
def display():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glColor3f(1.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glFlush()

def drawLine(p1, p2):
    global pointList, lineList, intersectionList
    
    line = Line(p1, p2)
    checkIntersections(line)
    lineList.append(line)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLineWidth(2.0)
    glPointSize(6.0)
    
    #Draw lines
    glBegin(GL_LINES)
    for l in lineList:
        glVertex2i(l.p1.x, l.p1.y)
        glVertex2i(l.p2.x, l.p2.y)
    glEnd()
    
    #Draw intersection points
    glBegin(GL_POINTS)
    for i in intersectionList:
        glVertex2i(i.p.x, i.p.y)
    glEnd()    
    glFlush()
    
def mouse(btn, state, x, y):
    global begin, point
    if (btn == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
        if (begin == 0):
            point = Point(x, height - y)
            begin = 1
        elif (begin == 1):
            drawLine(point, Point(x, height - y))
            begin = 0
    elif (btn == GLUT_RIGHT_BUTTON and state == GLUT_DOWN):
        reset() 
        display()  

def reset():
    global pointSeq, lineSeq, interSeq
    del lineList[:]
    del pointList[:]
    del intersectionList[:]
    pointSeq = 0
    lineSeq = 0 
    interSeq = 0
    print 'Clean and reset'

def init():
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, GLdouble(width), 0.0, GLdouble(height))
    glMatrixMode(GL_MODELVIEW)
    
    print 'Initializing'
    
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
glutCreateWindow("Trabalho 1 - Andre Moreira")
glutDisplayFunc(display)
init()
glutMouseFunc(mouse)
glutMainLoop()

