def findLine():
    edges = cv2.Canny(gray, 100, 200)
    # Canny edge detection Parameters; p1 = input image, p2 = minVal;
    # p2 = maxVal, (p4 = aperture size)
    plt.subplot(121), plt.imshow(frame, cmap='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(edges, cmap='gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show()

cap = cv2.VideoCapture('/Users/nicobaudoin/Desktop/DavalosLab/testvid.avi')

while (cap.isOpened()):
    # returns True while video is open
    ret, frame = cap.read()
# cap.read() "grabs, decodes, and returns the next video frame"


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    findLine()

    cv2.imshow('frame', gray)
    # imshow... cv2.imshow(winname, mat); mat is image to be shown??
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        cap.release()
    # closes video file
        cv2.destroyAllWindows()