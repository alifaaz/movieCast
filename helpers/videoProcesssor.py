from helpers.vidCam import  VideoCam
import pytesseract
import cv2
# here where all video proccessing happing
def videoProcess(vidUrl):
    v1 = VideoCam(vidUrl)
    v1.check_camera(v1.cap)
    SKIPFRAME = 100
    prevCast = ''
    castCount = 0
    timesOfFrames = []
    ct=0
    ltime=0.0
    prevFrame=None
    while True:
        # extract fraome from video
        ct += 1
        try:
            ret = v1.cap.grab()
            # skip frames
            if ct % SKIPFRAME == 0:  # skip some frames
                ret, frame = v1.get_frame()
                if not ret:
                    break

                # frame HERE
                # calculate histogram
                cast1Hist = cv2.calcHist([prevFrame], [0], None, [50], [0, 50])
                cast2Hist = cv2.calcHist([frame], [0], None, [50], [0, 50])

                histDiff = cv2.compareHist(cast1Hist, cast2Hist, cv2.HISTCMP_CORREL)
                time = v1.get_frame_time()
                ltime = time
                if histDiff <= 0:
                    timesOfFrames.append(time)


                if frame is None:
                    break
                # if cound AND CastLoaded successfully
                # if  "cast"   not  in   casts.strip().lower():
                if castCount < 4:
                    ret, thresh1 = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY_INV)
                    prevCast = pytesseract.image_to_string(thresh1, lang='eng')
                    # to read only first 5 names after cast appear on screen
                    if 'CAST' in prevCast.strip() and castCount < 4:
                        casts2 = prevCast
                        castCount += 1

                # assigning prevFrame
                prevFrame = frame

        except KeyboardInterrupt:
            v1.close_cam()
            exit(0)
    timesOfFrames.append(ltime)
    return casts2,timesOfFrames




