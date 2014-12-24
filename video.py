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

def getContours(img, fit_type = 'ellipse'):
    CELL_RADIUS_THRESHOLD = 4
    contours, hierarchy = cv2.findContours(img,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    coord_list = []
    for i in range(len(contours)):
        if fit_type == 'circle':
            radius_list = []
            center_list = []
            (x,y),radius = cv2.minEnclosingCircle(contours[i])
            if radius > CELL_RADIUS_THRESHOLD:
                center = (int(x), int(y))
                center_list.append(center)
                radius_list.append(radius)
                cv2.circle(img,center,int(radius),(0,255,0),-11)
            coord_list.append([center_list, radius_list])
            
        elif fit_type == 'ellipse':
            if len(contours[i]) >= 5:
                ellipse = cv2.fitEllipse(contours[i])
                area = np.pi*np.product(ellipse[1])
                if area >= 200 and area < 2000:
                    cv2.ellipse(img,ellipse,(0,255,0),-1)
    return img, contours, coord_list
    
def getFiltered(img, CELL_BINARY_THRESHOLD = 127):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subBG = trimEdges(gray, meds)
    thresh = cv2.erode(subBG, None, 10)
    thresh = cv2.dilate(thresh, None, 10)
    ret,thresh = cv2.threshold(subBG,CELL_BINARY_THRESHOLD,255,0)
    thresh, contours, coord_list = getContours(thresh)
    return thresh, contours, coord_list
    
def getCanny(img, CELL_BINARY_THRESHOLD = 127):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subBG = trimEdges(gray, meds)
    thresh = cv2.erode(subBG, None, 10)
    thresh = cv2.dilate(thresh, None, 10)
    ret,thresh = cv2.threshold(subBG,CELL_BINARY_THRESHOLD,255,0)
    thresh = cv2.Canny(thresh, 5, 10)
    return thresh
    
# ============================================================================
#                           Video Analysis
# ============================================================================

#cap = cv2.VideoCapture('/Users/nicobaudoin/Desktop/DavalosLab/testvid.avi')
#cap = cv2.VideoCapture('/Users/Dan/Movies/Mitosis in 2D - HeLa cell undergoes mitosis-HD.mp4/')
cap = cv2.VideoCapture('/Users/Dan/Movies/nprot.mp4')
meds = getMedian(cap)

while cap.isOpened():
    try:
        ret, frame = cap.read()
        if frame != None:
            thresh, contours, coord_list = getFiltered(frame)
            #thresh = getCanny(frame) 
        else:
            break
        cv2.imshow('thresh', thresh)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
        
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break