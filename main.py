import imageProcessing
import controlCamera
import controlMirror
import controlLDV
import sharedFlag

import threading



if __name__ == "__main__":
    #print("Hello world")
    timeout_ms = 10
    timelimit_s = 10
    sample_count=2**17
    new_bandwidth="100 kHz"
    new_range="10 mm/s"
    isPlotMatchpoint=True
    input('start')
    #controlCamera.getCameraImage(timeout_ms,timelimit_s)

    controlCameraThread = threading.Thread(target=controlCamera.getCameraImage, args=(timeout_ms,timelimit_s,isPlotMatchpoint))
    controlLDVThread = threading.Thread(target=controlLDV.run, args=(sample_count, new_bandwidth, new_range))

    controlCameraThread.start()
    controlLDVThread.start()
