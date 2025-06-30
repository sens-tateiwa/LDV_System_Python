from pypylon import pylon

import datetime
import time
import sys
import glob

import os

import cv2

import imageProcessing
import controlMirror
import sharedFlag

#videoDirで指定した動画を分割しrootDIrに複数枚の画像として保存する
def divisionVideo2Image(timeout_ms,timelimit_s,videoDir,rootDir):
    cap = cv2.VideoCapture(videoDir)
    if not cap.isOpened():
        print("video can't open")
        return
    os.makedirs(os.path.dirname(rootDir),exist_ok=True)
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    fps = cap.get(cv2.CAP_PROP_FPS)
    start_frame = 0
    step_frame = 1
    stop_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print("fps = "+str(fps))
    print("step_frame = "+str(step_frame))
    print("stop_frame = "+str(stop_frame))

    for n in range(start_frame,stop_frame,step_frame):
        cap.set(cv2.CAP_PROP_POS_FRAMES,n)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('{}_{}.{}'.format(rootDir+'/image', str(n).zfill(digit), 'png'), frame)
        else:
            return

#画像のリストimage_list内の画像をtimeout_ms間隔で繋ぎ合わせ動画を作成する
def createVideo(image_list,fps,videoName):#fpsはフレームレート
    if len(image_list[0].shape) ==2:
        height, width = image_list[0].shape
        isConvert2Color = True
    else:
        height, width, _ = image_list[0].shape
        isConvert2Color = False

    size = (width, height)
    name = videoName+'.mp4'
    
    out = cv2.VideoWriter('C:/Users/yuto/Documents/system_python/data/'+name, cv2.VideoWriter_fourcc(*'mp4v'), fps, size,isColor=True)

    for image in image_list:
        if isConvert2Color:
            image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
        out.write(image)
    out.release()
    return

#Baslerのカメラからtimelimit_s間timeout_ms間隔で画像を取得し続ける
def getCameraImage(timeout_ms,timelimit_s=10,isPlotMatchpoint=False):

    # トランスポートレイヤーインスタンスを取得
    tl_factory = pylon.TlFactory.GetInstance()

    # InstantCameraオブジェクトの作成
    camera = pylon.InstantCamera()

    # 最初に見つかったデバイスをアタッチ
    camera.Attach(tl_factory.CreateFirstDevice())

    # カメラを開く
    camera.Open()

    # 露光時間を設定（単位はマイクロ秒）
    camera.ExposureTime.SetValue(3000)

    camera.Gain.SetValue(10.0)

    image_list = []

    X=0
    Y=0
    intervalX = 0.01/126
    intervalY = 0.01/126
    mre2 = controlMirror.setMirror()
    controlMirror.changeAngle(X,Y,mre2)

    now = datetime.datetime.now()
    videoname = now.strftime("%Y%m%d_%H%M%S")
    print("videoname is "+videoname)

    #撮影を開始---
    #camera.StartGrabbing(1)
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    t1 = time.time()
    while camera.IsGrabbing():                                                                 #カメラの起動
        grab = camera.RetrieveResult(timeout_ms, pylon.TimeoutHandling_ThrowException) #timeout_msミリ秒のタイムアウト #起動しているカメラから画像を撮影
        if grab and grab.GrabSucceeded():
            image = grab.GetArray()     #撮影した画像を配列に格納
            
            #print(timelimit_s -(time.time()-t1))

            #取得した画像の処理を実行
            #image = imageProcessing.HoughTransform(image)
            image,distance = imageProcessing.calculateCentor2FingerDistance(image,isPlotMatchpoint)
            #cv2.imshow('camera',img)
            #cv2.waitKey(1)

            image_list.append(image)
            
            X += distance[0]*intervalX/2
            Y -= distance[1]*intervalY/2
            
            controlMirror.changeAngle(X,Y,mre2)

            grab.Release()    
        #cv2.imwrite('C:/Users/yuto/Documents/system_python/data/'+str(datetime.datetime.now())+'.png', img)    #取得した配列を名前を付けてコンピュータに保存
        if((not sharedFlag.isDataAcquiring)or((time.time()-t1)>timelimit_s)):#timelimit秒後
            camera.StopGrabbing()
            print("stop")
        #---撮影の終了
    controlMirror.changeAngle(0,0,mre2)
    fps = 100/timeout_ms#本当は1000ms/timeout_msだがtimeout_msおきに撮影できているか怪しく、かなり動画が短くなるため理論上の1/10のfpsで設定
    print("create video")
    createVideo(image_list,fps,videoname)
    print("created video")

    #カメラにおける全ての処理が終了したのでカメラを閉じる
    camera.Close()
    cv2.destroyAllWindows()
    return

if __name__ == "__main__":
    timeout_ms = 10
    timelimit_s = 100
    #getCameraImage(timelimit_s,timeout_ms)
    videoname = "20250624_133309"
    videoDir = 'C:/Users/yuto/Documents/system_python/data/'+videoname+'.mp4'
    rootDir = 'C:/Users/yuto/Documents/system_python/data/'+videoname+'_list'
    try:
        os.makedirs(rootDir)
    except FileExistsError:
        pass
    divisionVideo2Image(timeout_ms,timelimit_s,videoDir,rootDir)
    image_list = []
    result_videoName = videoname+'_slow'
    
    files = glob.glob(rootDir+"/*.png")
    for file in files:
        image = cv2.imread(file, cv2.IMREAD_COLOR)
        #image = imageProcessing.HoughTransform(image)
        image,_ = imageProcessing.calculateCentor2FingerDistance(image,isPlotMatchpoint=True)
        image_list.append(image)


    createVideo(image_list,10.0,result_videoName)
