from matplotlib import pyplot as plt
import csv
import datetime
'''
本代码用于根据路段平均速度的折线图
画出2019.10.14~2019.10.18（整改前）
和2019.10.21~2019.10.25（整改后）
'''


# 按路径读取平均速度表的第2列，将路段平均速度转为float类型并返回
def read_csv(filename):
    dataPath = "D:\\Python\\Python_Project\\flowspeed\\data\\平均速度\\"
    filePath = dataPath + filename
    with open(filePath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = [round(float(row[1]), 3) for row in reader]

    return data


def averageSpeedMap():
    # 整改前的结果读取
    mondayBefore = read_csv("整改前\\1014.csv")
    tuesdayBefore = read_csv("整改前\\1015.csv")
    wednesdayBefore = read_csv("整改前\\1016.csv")
    thursdayBefore = read_csv("整改前\\1017.csv")
    fridayBefore = read_csv("整改前\\1018.csv")
    # 整改后的结果读取
    mondayAfter = read_csv("整改后\\1021.csv")
    tuesdayAfter = read_csv("整改后\\1022.csv")
    wednesdayAfter = read_csv("整改后\\1023.csv")
    thursdayAfter = read_csv("整改后\\1024.csv")
    fridayAfter = read_csv("整改后\\1025.csv")
    # 生成横轴
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    timeListStr = [
        strftime(
            strptime("16:02", "%H:%M") + datetime.timedelta(minutes=i),
            "%H:%M") for i in range(0, 118, 2)
    ]

    # 开始画图
    f, (ax1, ax2) = plt.subplots(figsize=(8, 6), nrows=2)
    # 绘制子图1（整改前）
    ax1.plot(timeListStr, mondayBefore, label="Monday", ls='--')
    ax1.plot(timeListStr, tuesdayBefore, label="Tuesday", ls='-')
    ax1.plot(timeListStr, wednesdayBefore, label="Wednesday", ls='-.')
    ax1.plot(timeListStr, thursdayBefore, label="Thursday", ls=':')
    ax1.plot(timeListStr, fridayBefore, label="Friday", ls='--')
    for tick in ax1.get_xticklabels():
        tick.set_rotation(90)
    ax1.set_title('Road speed after adjustment (2019.10.21-2019.10.25)', fontsize=22)
    ax1.annotate('(%s, %.2f)' % ('16:42', 6.95),
                 xy=('16:42', 6.95),
                 arrowprops=dict(facecolor='red', shrink=0.005),
                 xytext=(14, 0.95*6.95)
                 )
    ax1.set_ylabel('Average speed(km/h)', fontsize=18)
    # plt.tight_layout()
    # ax1.tight_layout()
    ax1.legend()
    # 绘制子图2（整改后）
    ax2.plot(timeListStr, mondayAfter, label="Monday", ls='--')
    ax2.plot(timeListStr, tuesdayAfter, label="Tuesday", ls='-')
    ax2.plot(timeListStr, wednesdayAfter, label="Wednesday", ls='-.')
    ax2.plot(timeListStr, thursdayAfter, label="Thursday", ls=':')
    ax2.plot(timeListStr, fridayAfter, label="Friday", ls='--')
    for tick in ax2.get_xticklabels():
        tick.set_rotation(90)
    # ax2.set_title('Average speed after adjustment (2019.10.21-2019.10.25)', fontsize=18)
    ax2.set_xlabel('Time', fontsize=18)
    ax2.set_ylabel('Average speed(km/h)', fontsize=18)
    ax2.annotate('(%s, %.2f)' % ('17:04', 14.33),
                 xy=('17:04', 14.33),
                 arrowprops=dict(facecolor='red', shrink=0.005),
                 xytext=(24.5, 0.985 * 14.33)
                 )
    ax2.legend()

    # plt.legend()
    plt.show()




if __name__ == '__main__':
    averageSpeedMap()
