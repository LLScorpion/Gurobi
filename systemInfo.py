# 所有涉及到的path

# readIBMTrace.py
# jsonPath = "IBM-docker-registry-traces/data_centers/dal09/prod-dal09-logstash-2017.06.20-0-1_2830.json" # 2830条数据 5个边缘节点 请求104个镜像
# jsonPath = "IBM-docker-registry-traces/data_centers/dal09/prod-dal09-logstash-2017.06.20-0-2_2830.json" # 2830条数据 6个边缘节点 请求147个镜像
# jsonPath = "IBM-docker-registry-traces/data_centers/dal09/prod-dal09-logstash-2017.06.20-0-1_560.json" # 560条数据 5个边缘节点 请求35个镜像
jsonPath = "IBM-docker-registry-traces/data_centers/dal09/prod-dal09-logstash-2017.06.20-0-1_560_modified.json" # 560条数据 3个边缘节点（我自己改的） 请求35个镜像


# readIBMTrace.py \ generateInput.py
# myEnvDataPath = "myEnv/dal620-0-1_2830/"
# myEnvDataPath = "myEnv/dal620-0-1-archlinux/"
myEnvDataPath = "myEnv/dal620-0-1-archlinux-compressed_file/"

# main.py
# myRstDataPath = "myRst/dal620-0-1-600/"
# myRstDataPath = "myRst/dal620-0-1-500/"
# myRstDataPath = "myRst/dal620-0-1-400/"
# myRstDataPath = "myRst/dal620-0-1-300/"
# myRstDataPath = "myRst/dal620-0-1-200/"
# myRstDataPath = "myRst/dal620-0-1-150/"
# myRstDataPath = "myRst/dal620-0-1-100/"
# myRstDataPath = "myRst/dal620-0-1-100-linear/"
# myRstDataPath = "myRst/dal620-0-1-archlinux-3g/"
# myRstDataPath = "myRst/dal620-0-1-archlinux-1.5g/"
# 第一组
# myRstDataPath = "myRst/dal620-0-1-archlinux-3g-compressed_file/"
# S_r = [3221225472,3221225472,3221225472] # 3GB
# 第二组
myRstDataPath = "myRst/dal620-0-1-archlinux-1.5g-compressed_file/"
S_r = [1610612736,1610612736,1610612736] # 1.5GB
# 第三组
# myRstDataPath = "myRst/dal620-0-1-archlinux-1g-compressed_file/"
# S_r = [1073741824,1073741824,1073741824] # 1GB
# 第四组
# myRstDataPath = "myRst/dal620-0-1-archlinux-0.4g-compressed_file/"
# S_r = [429496729,429496729,429496729] # 0.4GB
# 第五组
# myRstDataPath = "myRst/dal620-0-1-archlinux-0.3g-compressed_file/"
# S_r = [322122547,322122547,322122547] # 0.3GB



# 对比组：competitor_LL.py
# rstLLDataPath = "rstLL/dal620-0-1-600/"
# rstLLDataPath = "rstLL/dal620-0-1-500/"
# rstLLDataPath = "rstLL/dal620-0-1-400/"
# rstLLDataPath = "rstLL/dal620-0-1-300/"
# rstLLDataPath = "rstLL/dal620-0-1-200/"
# rstLLDataPath = "rstLL/dal620-0-1-150/"
# rstLLDataPath = "rstLL/dal620-0-1-100/"
rstLLDataPath = "rstLL/dal620-0-1-archlinux-3g/"
# rstLLDataPath = "rstLL/dal620-0-1-archlinux-1.5g/"


############################## 自定义关于r的输入数据 ###############################################
R = 3
b_r = [1.25,1.25,1.25] # 10Mbps = 1.25MB/s
b_c = 0.625 # 5Mbps = 0.625MB/s
# 目前给的资源是完全够的
# S_r = [629145600,629145600,629145600] # 600MB
# S_r = [524288000,524288000,524288000] # 500MB
# S_r = [419430400,419430400,419430400] # 400MB
# S_r = [314572800,314572800,314572800] # 300MB
# S_r = [209715200,209715200,209715200] # 200MB
# S_r = [157286400,157286400,157286400] # 150MB
# S_r = [104857600,104857600,104857600] # 100MB
C_r = [1024,1024,1024]

# generateInput.py
layerCompressionRatio = 3.5
fileCompressionRatio = 2.0