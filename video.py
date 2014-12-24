import matplotlib.pyplot as plt
import cv2
import numpy as np

# ============================================================================
#               Useful DSP and Video Processing Functions
# ============================================================================

def findLine():
    edges = cv2.Canny(gray, 75, 125)
    plt.subplot(121), plt.imshow(frame, cmap='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(edges, cmap='gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()

def getMedian(cap):
    total_data = []
    while cap.isOpened():
        try:
            ret, frame = cap.read()
            if frame == None:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            total_data.append(gray)
        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            break
    lin_stack = np.vstack(x.ravel() for x in total_data)
    lin_median = np.median(lin_stack,axis = 0)
    meds = np.uint8(lin_median.reshape(total_data[0].shape))
    return meds
    
def trimEdges(raw, background):
    b = np.abs(raw - background)
    indices = b > 235
    b[indices] = 0
    return b

def getContours(img):
    contours, hierarchy = cv2.findContours(img,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    radius_list = []
    x_list = []
    y_list = []
    for i in range(len(contours)):
        (x,y),radius = cv2.minEnclosingCircle(contours[i])
        if radius > 5:
            center = (int(x),int(y))
            radius_list.append(radius)
            x_list.append(x)
            y_list.append(y)
            cv2.circle(img,center,int(radius),(0,255,0),2)
    return img, contours, radius, (x, y)
    
# ============================================================================
#                           Video Analysis
# ============================================================================

#cap = cv2.VideoCapture('/Users/nicobaudoin/Desktop/DavalosLab/testvid.avi')
#cap = cv2.VideoCapture('/Users/Dan/Movies/Mitosis in 2D - HeLa cell undergoes mitosis-HD.mp4/')
cap = cv2.VideoCapture('/Users/Dan/Movies//nprot.mp4')
meds = getMedian(cap)

while cap.isOpened():
    
    try:
        ret, frame = cap.read()
        if frame == None:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subBG = trimEdges(gray, meds)
        ret,thresh = cv2.threshold(subBG,127,255,0)
        thresh, contours, radius, (x, y) = getContours(thresh)
        cv2.imshow('thresh', thresh)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
            
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break