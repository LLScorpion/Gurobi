import json
import numpy as np
from datetime import datetime
from helpFunc import writeCSVRows,writeCSVRow
from systemInfo import myEnvDataPath,layerCompressionRatio,fileCompressionRatio


# TODO:
#     获取layer的大小
def getLayerSize(L, layerCompressionRatio, layerList = []):
    print(">>>getLayerSize():")
    print("    * layerCompressionRatio =",layerCompressionRatio)
    # 初始化s_l
    s_l = []
    for l in range(L):
        s_l.append(0)
    # 获取s_l
    # j = 1
    j = 99
    layer_count = L
    while (layer_count > 0):
        uc_layer_info_path = "inputParameter/image_" + str(j) + "/uc_layer_info.json"
        print("    Open file...",uc_layer_info_path)
        # 读取json文件
        with open(uc_layer_info_path, 'r', encoding='utf-8') as f:
            uc_layer_info = json.load(f)
        # 获取layersize
        for l in range(L):
            currentLayer = layerList[l]
            if (uc_layer_info.get(currentLayer) != None):
                layer_count -= 1
                s_l[l] = uc_layer_info.get(currentLayer) / layerCompressionRatio
        j += 1
    # 打印s_l
    # for l in range(L):
    #     print("    %d %s | size = %f" % (l + 1,layerList[l],s_l[l]))
    return s_l

# TODO:
#     获取file的大小
def getFileSize(F, fileCompressionRatio, fileList = []):
    print(">>>getFileSize():")
    print("    * layerCompressionRatio =", fileCompressionRatio)
    # 初始化s_f
    s_f = []
    for f in range(F):
        s_f.append(0)
    # j = 1
    j = 99
    file_count = F
    while (file_count > 0):
        file_info_path = "inputParameter/image_" + str(j) + "/file_info.json"
        print("    Open file...", file_info_path)
        # 读取json文件
        with open(file_info_path, 'r', encoding='utf-8') as f:
            file_info = json.load(f)
        # 获取filesize
        for f in range(F):
            currentFile = fileList[f]
            if (file_info.get(currentFile) != None):
                file_count -= 1
                s_f[f] = file_info.get(currentFile) / fileCompressionRatio
        j += 1
    # 打印s_f
    # for f in range(F):
    #     if(s_f[f] == 0):
    #         print(fileList[f])
    #     print("    %d %s | size = %f" % (f + 1, fileList[f], s_f[f]))
    return s_f

# TODO:
#     获取psi
def getPsi(I, L, imageList = [], layerList = []):
    print(">>>getPsi():")
    # 初始化psi
    psi_i_l = []
    for i in range(I):
        psi_i = []
        for l in range(L):
            psi_i.append(0)
        psi_i_l.append(psi_i)
    # j = 1
    j = 99
    image_count = I
    while (image_count > 0):
        image_layer_diff_ids_path = "inputParameter/image_" + str(j) + "/image_layer_diff_ids.json"
        print("    Open file...", image_layer_diff_ids_path)
        # 读取json文件
        with open(image_layer_diff_ids_path, 'r', encoding='utf-8') as f:
            image_layer_diff_ids = json.load(f)
        # 获取psi
        for i in range(I):
            currentImage = imageList[i]
            image_layer_list = image_layer_diff_ids.get(currentImage)
            if(image_layer_list != None):
                image_count -= 1
                # print(image_layer_list)
                for l in range(L):
                    currentLayer = layerList[l]
                    if(currentLayer in image_layer_list):
                        psi_i_l[i][l] = 1
        j += 1
    # 打印一下
    for l in range(L):
        expr = 0
        for i in range(I):
            expr += psi_i_l[i][l]
        if(expr == 0):
            print("    * Layer %d does not belong to any image." % (l + 1))
    return psi_i_l

# TODO:
#     获取omega
def getOmega(L, F, layerList = [], fileList = []):
    print(">>>getOmega():")
    # 初始化
    omega_l_f = []
    for l in range(L):
        omega_l = []
        for f in range(F):
            omega_l.append(0)
        omega_l_f.append(omega_l)
    # j = 1
    j = 99
    layer_count = L
    while (layer_count > 0):
        layer_file_path = "inputParameter/image_" + str(j) + "/layer_file.json"
        print("    Open file...", layer_file_path)
        # 读取json文件
        with open(layer_file_path, 'r', encoding='utf-8') as f:
            layer_file = json.load(f)
        # 获得omega
        for l in range(L):
            currentLayer = layerList[l]
            layer_file_list = layer_file.get(currentLayer)
            if (layer_file_list != None):
                layer_count -= 1
                for f in range(F):
                    currentFile = fileList[f]
                    if(currentFile in layer_file_list):
                        omega_l_f[l][f] = 1

        j += 1
    # 打印一下
    for f in range(F):
        expr = 0
        for l in range(L):
            expr += omega_l_f[l][f]
        if (expr == 0):
            print("    * File %d does not belong to any layer." % (f + 1))
    return omega_l_f



############################ 读取nodeList.csv imageList.csv layerList.csv fileList.csv #########################
######################################## 获得N I L F ###########################################################
nodeList = np.loadtxt(myEnvDataPath + "nodeList.csv", dtype=str, delimiter=',')
imageList = np.loadtxt(myEnvDataPath + "imageList.csv", dtype=str, delimiter=',')
layerList = np.loadtxt(myEnvDataPath + "layerList.csv", dtype=str, delimiter=',')
fileList = np.loadtxt(myEnvDataPath + "fileList.csv", dtype=str, delimiter=',')
N = len(nodeList)
I = len(imageList)
L = len(layerList)
F = len(fileList)
print(">>>Basic info:\n    N = %d, I = %d, L = %d, F = %d." % (N,I,L,F))
################################################# 获取s_l 和 s_f ##############################################
s_l = getLayerSize(L, layerCompressionRatio, layerList)
s_f = getFileSize(F, fileCompressionRatio,fileList)
####################################### 获取psi_i_l 和 omega_l_f ###############################################
psi_i_l = getPsi(I, L, imageList, layerList)
omega_l_f = getOmega(L, F, layerList, fileList)
imageLayerNum = 0
for i in range(I):
    imageLayerNum += sum(psi_i_l[i])
print(">>>Total layer number before deduplicate: %d" % imageLayerNum)
imageFileNum = 0
for i in range(I):
    for l in range(L):
        if(psi_i_l[i][l] == 1):
            imageFileNum += sum(omega_l_f[l])
print(">>>Total file number before deduplicate: %d" % imageFileNum)
######################################### 把上述写入csv文件 ####################################################
writeCSVRow(myEnvDataPath, "s_l.csv", s_l)
writeCSVRow(myEnvDataPath, "s_f.csv", s_f)
writeCSVRows(myEnvDataPath, "psi.csv", psi_i_l)
writeCSVRows(myEnvDataPath, "omega.csv", omega_l_f)
print(">>>Successfully write (1)s_l (2)s_f (3)psi_i_l (4)omega_l_f, at time = ",datetime.now())
######################################### 查看总文件和总层的大小 ####################################################
print("    F = %5d with total size sum(s_f) = %f" % (F,sum(s_f)))
print("    L = %5d with total size sum(s_l) = %f" % (L,sum(s_l)))
print("    The ratio sum(s_f) / sum(s_f) is",sum(s_f) / sum(s_l))