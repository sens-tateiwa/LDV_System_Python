DataAcquiring = False

def set_flag(bool):
    global DataAcquiring
    if(bool == True):
        DataAcquiring = True
    else:
        DataAcquiring = False
    return

def isDataAcquiring():
    global DataAcquiring
    return DataAcquiring