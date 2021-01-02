import numpy as np
import cv2

def shape_detect(color, contours, shape_list) :
    for cnt in contours:
        shape = str()
        precision = 0.01*cv2.arcLength(cnt, True)
        vertices = cv2.approxPolyDP(cnt, precision, True)
        #print(vertices)
        if (len(vertices) == 3) : 
            shape = "Triangle"
        elif (len(vertices) == 4) :
            #print(vertices)
            x1 = vertices[0][0][0]
            y1 = vertices[0][0][1]
            x2 = vertices[1][0][0]
            y2 = vertices[1][0][1]
            x3 = vertices[2][0][0]
            y3 = vertices[2][0][1]
            x4 = vertices[3][0][0]
            y4 = vertices[3][0][1]
            #print("(", x1, " ", y1, ")", "(", x2, " ", y2, ")", "(", x3, " ", y3, ")", "(", x4, " ", y4 ,")")
            if (((x2 - 3) <= x1) and (x1 <= (x2 + 3))) :
                x2 = x1
            if (((x3 - 3) <= x1) and (x1 <= (x3 + 3))) :
                x3 = x1
            if (((x4 - 3) <= x1) and (x1 <= (x4 + 3))) :
                x4 = x1
            if (((x3 - 3) <= x2) and (x2 <= (x3 + 3))) :
                x3 = x2
            if (((x4 - 3) <= x2) and (x2 <= (x4 + 3))) :
                x4 = x2
            if (((x4 - 3) <= x3) and (x3 <= (x4 + 3))) :
                x4 = x3
            if (((y2 - 3) <= y1) and (y1 <= (y2 + 3))) :
                y2 = y1
            if (((y3 - 3) <= y1) and (y1 <= (y3 + 3))) :
                y3 = y1
            if (((y4 - 3) <= y1) and (y1 <= (y4 + 3))) :
                y4 = y1
            if (((y3 - 3) <= y2) and (y2 <= (y3 + 3))) :
                y3 = y2
            if (((y4 - 3) <= y2) and (y2 <= (y4 + 3))) :
                y4 = y2
            if (((y4 - 3) <= y3) and (y3 <= (y4 + 3))) :
                y4 = y3

            #print("(", x1, " ", y1, ")", "(", x2, " ", y2, ")", "(", x3, " ", y3, ")", "(", x4, " ", y4 ,")")
       
            if (x1 != x2) : 
                s12 = round((y1 - y2)/(x1 - x2), 4)
                if(s12 == 0) :
                    s12 = 0.0001
            else :
                s12 = 9999
            
            if (x2 != x3) : 
                s23 = round((y2 - y3)/(x2 - x3), 4)
                if(s23 == 0) :
                    s23 = 0.0001
            else :
                s23 = 9999
            
            if (x3 != x4) : 
                s34 = round((y3 - y4)/(x3 - x4), 4)
                if(s34 == 0) :
                    s34 = 0.0001
            else :
                s34 = 9999
            
            if (x4 != x1) : 
                s41 = round((y4 - y1)/(x4 - x1), 4)
                if(s41 == 0) :
                    s41 = 0.0001
            else :
                s41 = 9999

            d12 = int(((x1 - x2)**2 + (y1 - y2)**2)**0.5)
            d23 = int(((x2 - x3)**2 + (y2 - y3)**2)**0.5)
            d34 = int(((x3 - x4)**2 + (y3 - y4)**2)**0.5)
            d41 = int(((x4 - x1)**2 + (y4 - y1)**2)**0.5)
            if (((s34 - 0.1) <= s12) and (s12 <= (s34 + 0.1)) or ((s41 - 0.1) <= s23) and (s23 <= (s41 + 0.1))) :
                if (((s34 - 0.1) <= s12) and (s12 <= (s34 + 0.1)) and ((s41 - 0.1) <= s23) and (s23 <= (s41 + 0.1))) :
                    if (((d23 - 3) <= d12) and (d12 <= (d23 + 3)) and ((d41 - 3) <= d34) and (d34 <= (d41 + 3))) :
                        if(round(s12*s23, 1) == 1) :
                            shape = "Square "
                        else :
                            shape = "Rhombus"
                    else :
                        shape = "Parallelogram"
                else :
                    shape = "Trapezium"
            else : 
                shape = "Quadrilateral"
         
        elif (len(vertices) == 5) :
            shape = "Pentagon"
        elif (len(vertices) == 6) :
            shape = "Hexagon"
        else :
            shape = "Circle"
        
        #printing area
        area = cv2.contourArea(cnt)
        
        #finding centroid
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        print(color, shape, area, cX, cY)
        shape_list.append([shape, color, area, cX, cY])
        
    return shape_list


## MAIN FUNCTION ##

#reading of image and conversion of BGR to HSV (Hue Saturation Value) 
img = cv2.imread('Test2.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#blue color
lower_blue = np.array([110,1,50])
upper_blue = np.array([170,255,255])

#green color
lower_green = np.array([50,1,50])
upper_green = np.array([80,255,255])

#red color
lower_red = np.array([0,1,255])
upper_red = np.array([40,255,255])

#masking the HSV image to highlighten a shape of particular color 
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
green_mask = cv2.inRange(hsv, lower_green, upper_green)
red_mask = cv2.inRange(hsv, lower_red, upper_red)
kernel = np.ones((2,2), np.uint8)
blue_edges = cv2.dilate(blue_mask, kernel, iterations = 1)
green_edges = cv2.dilate(green_mask, kernel, iterations = 1)
red_edges = cv2.dilate(red_mask, kernel, iterations = 1)

#finding contours of masked images
blue_contour, blue_hierarchy = cv2.findContours(blue_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
green_contour, green_hierarchy = cv2.findContours(green_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
red_contour, red_hierarchy = cv2.findContours(red_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#shape_list: a list in which shapes with their parameters are appended
shape_list = list()

shape_list = shape_detect('blue', blue_contour, shape_list)

#cv2.imshow("GREEN", green_mask)
shape_list = shape_detect('green', green_contour, shape_list)

#cv2.imshow("RED", red_mask)
shape_list = shape_detect('red', red_contour, shape_list)

print(shape_list)

shapes = dict()

#shape_list is sorted in descending order using lambda function by setting reverse = True 
shape_list.sort(key = lambda x: x[2], reverse = True)
for item in shape_list :
    Shape = item[0].strip()
    color = item[1].strip()
    area = item[2]
    cX = item[3]
    cY = item[4]
    shapes[Shape] = [color, area, cX, cY]
##################################################

#the final appended list is returned to the main body of the program
print(shapes)
cv2.imshow("BLUE", blue_edges)
cv2.imshow("GREEN", green_edges)
cv2.imshow("RED", red_edges)
cv2.waitKey(0)
