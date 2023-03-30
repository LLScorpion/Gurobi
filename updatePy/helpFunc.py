import csv
import os
import json
import random
import numpy as np


# 写入csv，内容为单行
def writeCSVRow(Path,subDataPath,content = []):
    if not os.path.exists(Path):
        os.mkdir(Path)
    dataPath = Path  + subDataPath
    with open(dataPath,'w') as csvfile:
        fw = csv.writer(csvfile)
        fw.writerow(content)

# 写入csv，内容为多行
def writeCSVRows(Path,subDataPath,content = []):
    if not os.path.exists(Path):
        os.mkdir(Path)
    dataPath = Path + subDataPath
    with open(dataPath,'w') as csvfile:
        fw = csv.writer(csvfile)
        fw.writerows(content)


def printStorage(RNILF = [], s_l = [], s_f = [], x_l = [],x_f = [],z = []):
    print(">>>printStorage():")
    R = RNILF[0]
    N = RNILF[1]
    I = RNILF[2]
    L = RNILF[3]
    F = RNILF[4]
    print("    * The storage granularity rst: ")
    totalStorage = 0
    for r in range(R):
        print("    Registry ", r + 1, " stores: ", end="")
        if (z[r] == 0):
            total_storage = 0
            for l in range(L):
                total_storage += s_l[l] * x_l[r][l]
            print("layer, with storage consumption ", total_storage, end="")
            totalStorage += total_storage
        else:
            total_storage = 0
            for f in range(F):
                total_storage += s_f[f] * x_f[r][f]
            print("file, with storage consumption ", total_storage, end="")
            totalStorage += total_storage
        print("")
    print("    * Total Storage Consumption:", totalStorage)
    # 打印x_l x_f
    print("    * The layer placement rst:")
    for r in range(R):
        storedLayerNum = sum(x_l[r])
        storedFileNum = sum(x_f[r])
        print("    Registry ", r + 1, " stores", storedLayerNum, "layers,", storedFileNum, "files.")

def printConnection(RNILF = [], yr = []):
    print(">>>printConnection():")
    R = RNILF[0]
    N = RNILF[1]
    I = RNILF[2]
    L = RNILF[3]
    F = RNILF[4]
    totalConnectionNum = 0
    for r in range(R):
        conNum = 0
        for n in range(N):
            for i in range(I):
                for l in range(L):
                    conNum += yr[r][n][i][l]
        totalConnectionNum += conNum
        print("    Registry %d used %d connections." % (r + 1, conNum))
    print("    * Total edge connection number is %d." % totalConnectionNum)

def placeLayerInFRegistry(RNILF = [], s_l = [], z = [], x_l = []):
    print(">>>placeLayerInFRegistry():")
    R = RNILF[0]
    N = RNILF[1]
    I = RNILF[2]
    L = RNILF[3]
    F = RNILF[4]
    for r in range(R):
        if(z[r] == 1):
            expr = 0
            for l in range(L):
                expr += s_l[l] * x_l[r][l]
            print("    If store layer in registry",r + 1,", storage consumption is",expr)

def checkConstraints(RNILF = [], theta_n_il = [], x_l = [], yr = [], yc = []):
    print(">>>checkConstraints():")
    R = RNILF[0]
    N = RNILF[1]
    I = RNILF[2]
    L = RNILF[3]
    F = RNILF[4]
    #
    for r in range(R):
        for n in range(N):
            for i in range(I):
                for l in range(L):
                    if(yr[r][n][i][l] > x_l[r][l]):
                        print("    Constraint not satisfied!")
    #
    for n in range(N):
        for i in range(I):
            for l in range(L):
                expr = 0
                for r in range(R):
                    expr += yr[r][n][i][l]
                expr += yc[n][i][l]
                if(expr != theta_n_il[n][i][l]):
                    print("    Constraint not satisfied!")

def checkCompleteness(RNILF = [], x_f = [], omega_l_f = [], x_l = [], z = []):
    print(">>>checkCompleteness():")
    R = RNILF[0]
    N = RNILF[1]
    I = RNILF[2]
    L = RNILF[3]
    F = RNILF[4]
    # layer在 则其文件必须在
    for r in range(R):
        for l in range(L):
            if (x_l[r][l] == 1):
                for f in range(F):
                    if (omega_l_f[l][f] == 1 and x_f[r][f] == 0):
                        print(
                            "Layer %d is placed in registry %d, and file %d belongs to it, but file is not placed." % (
                            l + 1, r + 1, f + 1))
    # layer的文件全在 则layer在
    for r in range(R):
        if (z[r] == 1):
            for l in range(L):
                expr = 0
                expr1 = 0
                for f in range(F):
                    expr += x_f[r][f] * omega_l_f[l][f]
                    expr1 += omega_l_f[l][f]
                if (expr == expr1 and x_l[r][l] == 0):
                    print("All the file of layer %d is placed in registry %d, but the layer is not placed." % (
                    l + 1, r + 1))


def printStorage_LL(RNILF = [], s_l = [], x_l = []):
    print(">>>printStorage_LL():")
    R = RNILF[0]
    N = RNILF[1]
    I = RNILF[2]
    L = RNILF[3]
    F = RNILF[4]
    totalStorage = 0
    for r in range(R):
        total_storage = 0
        for l in range(L):
            total_storage += s_l[l] * x_l[r][l]
        print("    Registry ", r + 1, " with storage consumption:",total_storage)
        totalStorage += total_storage
        print("")
    print("    * Total Storage Consumption:", totalStorage)
    # 打印x_l
    print("    * The layer placement rst:")
    for r in range(R):
        storedLayerNum = sum(x_l[r])
        print("    Registry ", r + 1, " stores", storedLayerNum, "layers.")