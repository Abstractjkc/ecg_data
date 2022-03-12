import os
import datetime

import wfdb
import pywt
import seaborn
import numpy as np
#import tensorflow as tf
# import matplotlib.pyplot as plt
# from sklearn.metrics import confusion_matrix

# 项目目录
project_path = ".\\"
# 定义日志目录,必须是启动web应用时指定目录的子目录,建议使用日期时间作为子目录名
log_dir = project_path + "logs\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
model_path = project_path + "ecg_model.h5"

# 测试集在数据集中所占的比例
RATIO = 0.3


# 小波去噪预处理
def denoise(data):
    # 小波变换
    coeffs = pywt.wavedec(data=data, wavelet='db5', level=9)
    cA9, cD9, cD8, cD7, cD6, cD5, cD4, cD3, cD2, cD1 = coeffs

    # 阈值去噪
    threshold = (np.median(np.abs(cD1)) / 0.6745) * (np.sqrt(2 * np.log(len(cD1))))
    cD1.fill(0)
    cD2.fill(0)
    for i in range(1, len(coeffs) - 2):
        coeffs[i] = pywt.threshold(coeffs[i], threshold)

    # 小波反变换,获取去噪后的信号
    rdata = pywt.waverec(coeffs=coeffs, wavelet='db5')
    return rdata


# 读取心电数据和对应标签,并对数据进行小波去噪
def getDataSet(number, X_data, Y_data):
    ecgClassSet = ['N', 'A', 'V', 'L', 'R']

    # 读取心电数据记录
    print("正在读取 " + number + " 号心电数据...")
    record = wfdb.rdrecord('ecg_data/' + number, channel_names=['MLII'])
    data = record.p_signal.flatten()
    rdata = denoise(data=data)

    # 获取心电数据记录中R波的位置和对应的标签
    annotation = wfdb.rdann('ecg_data/' + number, 'atr')
    Rlocation = annotation.sample
    Rclass = annotation.symbol

    # 去掉前后的不稳定数据
    start = 10
    end = 5
    i = start
    j = len(annotation.symbol) - end

    # 因为只选择NAVLR五种心电类型,所以要选出该条记录中所需要的那些带有特定标签的数据,舍弃其余标签的点
    # X_data在R波前后截取长度为300的数据点
    # Y_data将NAVLR按顺序转换为01234
    while i < j:
        try:
            lable = ecgClassSet.index(Rclass[i])
            x_train = rdata[Rlocation[i] - 99:Rlocation[i] + 201]
            X_data.append(x_train)
            Y_data.append(lable)
            i += 1
        except ValueError:
            i += 1
    return


# 加载数据集并进行预处理
def loadData():
    numberSet = ['100', '101', '103', '105', '106', '107', '108', '109', '111', '112', '113', '114', '115',
                 '116', '117', '119', '121', '122', '123', '124', '200', '201', '202', '203', '205', '208',
                 '210', '212', '213', '214', '215', '217', '219', '220', '221', '222', '223', '228', '230',
                 '231', '232', '233', '234']
    dataSet = []
    lableSet = []
    for n in numberSet:
        getDataSet(n, dataSet, lableSet)

    # 转numpy数组,打乱顺序
    dataSet = np.array(dataSet).reshape(-1, 300)
    lableSet = np.array(lableSet).reshape(-1, 1)
    train_ds = np.hstack((dataSet, lableSet))
    np.random.shuffle(train_ds)

    # 数据集及其标签集
    X = train_ds[:, :300].reshape(-1, 300, 1)
    Y = train_ds[:, 300]

    # 测试集及其标签集
    shuffle_index = np.random.permutation(len(X))
    test_length = int(RATIO * len(shuffle_index))
    test_index = shuffle_index[:test_length]
    train_index = shuffle_index[test_length:]
    X_test, Y_test = X[test_index], Y[test_index]
    X_train, Y_train = X[train_index], Y[train_index]
    return X_train, Y_train, X_test, Y_test

def main() :
    trainnum = 64535
    testnum = 27657
    X_train, Y_train, X_test, Y_test = loadData()
    ecgClassSet = ['N', 'A', 'V', 'L', 'R']
    datafile = open('traindata.txt', 'w')
    for i in range(0, trainnum) :
        for j in range(0, 300) :
            datafile.write(str(float(X_train[i][j][0])) + ' ')
        datafile.write(str(int(Y_train[i])) + '\n')
    datafile.close()
    testfile = open('testdata.txt', 'w')
    for i in range(0, testnum) :
        for j in range(0, 300) :
            testfile.write(str(float(X_test[i][j][0])) + ' ')
        testfile.write(str(int(Y_test[i])) + '\n')
    testfile.close()
if __name__ == '__main__':
    main()