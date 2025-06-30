import imageProcessing
import controlCamera
import controlMirror
import controlLDV



if __name__ == "__main__":
    #print("Hello world")
    timeout_ms = 10
    timelimit_s = 10
    input('start')

    controlCamera.getCameraImage(timelimit_s,timeout_ms)