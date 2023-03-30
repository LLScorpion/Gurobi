import time
import numpy as np
from datetime import datetime
from solveModelByGurobi import sModel
from helpFunc import writeCSVRows, writeCSVRow
from systemInfo import myEnvDataPath,myRstDataPath,R,b_r,S_r,C_r,b_c



################################ 读出已经有的输入数据 ##########################################
nodeList = np.loadtxt(myEnvDataPath + "nodeList.csv", dtype = str, delimiter = ',')
imageList = np.loadtxt(myEnvDataPath + "imageList.csv", dtype = str, delimiter = ',')
layerList = np.loadtxt(myEnvDataPath + "layerList.csv", dtype = str, delimiter = ',')
fileList = np.loadtxt(myEnvDataPath + "fileList.csv", dtype = str, delimiter = ',')
N = len(nodeList)
I = len(imageList)
L = len(layerList)
F = len(fileList)
RNILF = [R,N,I,L,F]
# 文件的大小 和 层的大小
s_f = np.loadtxt(myEnvDataPath + "s_f.csv", dtype = float, delimiter = ',')
s_l = np.loadtxt(myEnvDataPath + "s_l.csv", dtype = float, delimiter = ',')
print(">>>Basic info:\n    N = %d, I = %d, L = %d, F = %d." % (N,I,L,F))
print("    F = %5d with total size sum(s_f) = %f" % (F,sum(s_f)))
print("    L = %5d with total size sum(s_l) = %f" % (L,sum(s_l)))
print("    The ratio sum(s_f) / sum(s_f) is",sum(s_f) / sum(s_l))

################## 算力节点是否请求镜像
sigma_n_i = np.loadtxt(myEnvDataPath + "sigma.csv", dtype = int, delimiter = ',')
# 检查一下是否每个镜像都有被请求到
for i in range(I):
    expr = 0
    for n in range(N):
        expr += sigma_n_i[n][i]
    if(expr == 0):
        print("    Image %d is not requested by any node." % (i + 1))
################## 算力节点请求镜像的次数
lamda_n_i = np.loadtxt(myEnvDataPath + "lamda.csv", dtype = int, delimiter = ',')
# 计算一下算力节点的总请求频次
requestTimes = 0
for n in range(N):
    requestTimes += sum(lamda_n_i[n])
print("    The nodes request images for %d times." % requestTimes)
################### 镜像和层之间的从属关系 I行L列
psi_i_l = np.loadtxt(myEnvDataPath + "psi.csv", dtype = int, delimiter = ',')
################### 层和文件之间的从属关系
omega_l_f = np.loadtxt(myEnvDataPath + "omega.csv", dtype = int, delimiter = ',')
################### 计算theta_n_il 算力节点n是否请求i的l
theta_n_il = []
for n in range(N):
    theta_n = []
    for i in range(I):
        theta_n_i = []
        for l in range(L):
            theta_n_i.append(sigma_n_i[n][i] * psi_i_l[i][l])
        theta_n.append(theta_n_i)
    theta_n_il.append(theta_n)
# 计算一下同一时刻最多connection总数
totalConnectionNum = 0
for n in range(N):
    for i in range(I):
        for l in range(L):
            totalConnectionNum += theta_n_il[n][i][l]
print("    totalConnectionNum =",totalConnectionNum)

print(">>>Other Info:")
# tau_l 先设置为0，还没有找到详细量化这部分的文章
tau_l = []
for l in range(L):
    tau_l.append(1.0)
print("    tau_l is",tau_l)
print("    R =",R)
print("    S_r is",S_r)
print("    C_r is",C_r)
print("    b_r is",b_r)


######################################### 定义决策变量 #############################################
x_l = []
x_f = []
yr = []
yc = []
z = []
t = []

##################################### Gurobi解模型 #####################################
print("\n>>>Gurobi solving model......\n")
start = time.perf_counter()
sModel(b_c, RNILF, s_f, s_l, S_r, b_r, C_r, lamda_n_i, omega_l_f, tau_l, theta_n_il, x_l, x_f, yr, yc, z, t)
end = time.perf_counter()
print("\n    Gurobi求解时间为: %.4f" % (end - start) + "s")


##################################### 将gurobi结果写csv #####################################
# 将x_l,x_f,y,z和t存入csv文件
writeCSVRows(myRstDataPath,"x_l.csv",x_l)
writeCSVRows(myRstDataPath,"x_f.csv",x_f)
for r in range(R):
    for n in range(N):
        subPath = "yr" + str(r) + "_n" + str(n) + ".csv"
        writeCSVRows(myRstDataPath,subPath,yr[r][n])
for n in range(N):
    subPath = "yc" + "_n" + str(n) + ".csv"
    writeCSVRows(myRstDataPath,subPath,yc[n])
writeCSVRow(myRstDataPath,"z.csv",z)
writeCSVRows(myRstDataPath,"t.csv",t)
print(">>>Successfully write (1)x_l (2)x_f (3)yr (4)yc (5)z (6)t, at time = ",datetime.now())
