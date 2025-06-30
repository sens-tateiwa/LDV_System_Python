import matplotlib
matplotlib.use('Agg') # GUIを使わないAggバックエンドを指定

import numpy as np
import os
import datetime
import time
import matplotlib.pyplot as plt
import pandas as pd

import sharedFlag

from Polytec_Python.acquisition_examples import acquire_streaming
from Polytec_Python.acquisition_examples import changeBandwidthandRange

def fftplt_indiv(file_name, sample_count, dt):
    #rootdir = 'C:/Users/yuto/Documents/optotune/measuredData/'
    #dt = 4.57142857*10**(-6)#得られたデータのtimestampの間隔
    f_s = 1/dt
    #N = 1000#run2のsmplecountに合わせる
    N = sample_count

    
    df = []
    df = pd.read_csv(file_name)    
    text=df.to_string()

    text = text.split('\n')
    
    for j in range(0,N,1):
        text[j] = text[j].split(";")
    text = text[0:N]
    csv_velocity = [float(x[1]) for x in text]  
    X=np.fft.fft(csv_velocity)
            
    f = np.fft.fftfreq(N,dt)
                    
    #plt.rcParams["font.size"]=60
    plt.figure()
    plt.xlabel('time [s]')
    plt.ylabel('Velocity [m/s]')
    #plt.ylim(-0.011,0.011)
    #plt.tick_params(labelsize=45)
    plt.subplots_adjust(0.2,0.15,0.97,0.95)
    t = np.linspace(0,dt*N,N)
    plt.plot(t, csv_velocity) # 入力信号
    plt.savefig(file_name+'_velocity.png')
    
    #plt.rcParams["font.size"]=60
    plt.figure()
    plt.xlabel('Frequency [Hz]')
    #plt.xlim(f[1],500)
    plt.xlim(f[1],50)
    plt.ylabel('Amplitude')
    #plt.ylim(0,0.25)
    #plt.tick_params(labelsize=45)
    plt.subplots_adjust(0.2,0.15,0.97,0.95)
    #plt.plot(f[1:int(N/2)],np.abs((X)/(N/2))[1:int(N/2)])
    plt.plot(f[1:int(N/2)],np.abs((X)/np.sqrt(N))[1:int(N/2)])
    plt.savefig(file_name+'_frequency.png')
        
    #plt.show()

def run(sample_count=2**17, new_bandwidth="100 kHz", new_range="10 mm/s"):
    ip_address = "192.168.137.1"
    rootDir = 'C:/Users/yuto/Documents/system_python/data/LDVdata'
    now = datetime.datetime.now()
    name = now.strftime("%Y%m%d_%H%M%S")
    file_name = rootDir + '/' + name + '.txt'
    try:
        os.makedirs(rootDir)
    except FileExistsError:
        pass
    
    changeBandwidthandRange.run(ip_address, new_bandwidth,new_range)

    velocity = ""
    
    #sample_count = 2**17 # 2^17 = 131,072
    data_time_interval = 1/218750
    
    sharedFlag.set_flag(True)
    #start = time.time()
    velocity += acquire_streaming.run(ip_address,sample_count)
    #end = time.time()
    sharedFlag.set_flag(False)
  
    #print(f"time is {end - start}")
    print(f"expected time is {data_time_interval*(sample_count-1)}")

    text = velocity.split('\n')
    text = text[0:sample_count]
    #print(text)
    #velocity = [float(x) for x in text[0:sample_count]]

    np.savetxt(file_name, text,fmt='%s')
    
    fftplt_indiv(file_name, sample_count,data_time_interval)

    return

if __name__ == "__main__":
    ip_address = "192.168.137.1"
    rootDir = 'C:/Users/yuto/Documents/system_python/data/LDVdata'
    now = datetime.datetime.now()
    name = now.strftime("%Y%m%d_%H%M%S")
    try:
        os.makedirs(rootDir)
    except FileExistsError:
        pass
    
    changeBandwidthandRange.run(ip_address, "1 kHz")
    print("changeBandwidthandRange was Done\n")

    velocity = ""
    
    sample_count = 2**17 # 2^17 = 131,072
    data_time_interval = 1/218750
    
    #start = time.time()
    velocity += acquire_streaming.run(ip_address,sample_count)
    #end = time.time()
    print("acquisition was Done\n")
    #print(f"time is {end - start}")
    print(f"expected time is {data_time_interval*(sample_count-1)}")

    text = velocity.split('\n')
    text = text[0:sample_count]
    #print(text)
    #velocity = [float(x) for x in text[0:sample_count]]

    np.savetxt(rootDir + "/" + name + ".txt", text,fmt='%s')
    print("savetxt was Done\n")
    
    fftplt_indiv(rootDir+"/"+name + ".txt", sample_count,data_time_interval)

