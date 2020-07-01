from matplotlib import pyplot as plt
import xlrd
import datetime
import seaborn as sns
import pandas as pd
import numpy as np


def read_xlsx(filename):
    dataPath = "D:\\Python\\Python_Project\\flowspeed\\data\\"
    filePath = dataPath + filename
    # print(filePath)
    workbook = xlrd.open_workbook(filePath, encoding_override="utf-8")
    sheet = workbook.sheet_by_name("Sheet1")
    allData = sheet.col_values(2)
    # print(allData)
    data = []
    for i in range(len(allData)):
        if i % 12 == 0:
            data.append(round(allData[i], 3))
    # print(data)
    # print(len(data))
    return data


def heatMap():
    # 整改前的结果读取并处理成dataframe
    mondayBefore = read_xlsx("整改前\\1014.xlsx")
    tuesdayBefore = read_xlsx("整改前\\1015.xlsx")
    wednesdayBefore = read_xlsx("整改前\\1016.xlsx")
    thursdayBefore = read_xlsx("整改前\\1017.xlsx")
    fridayBefore = read_xlsx("整改前\\1018.xlsx")
    saturdayBefore = read_xlsx("整改前\\1019.xlsx")
    sundayBefore = read_xlsx("整改前\\1020.xlsx")
    framesBefore = [
        mondayBefore, tuesdayBefore, wednesdayBefore, thursdayBefore,
        fridayBefore, saturdayBefore, sundayBefore
    ]
    dataBefore = np.array(framesBefore)
    heatDataBefore = pd.DataFrame(dataBefore)
    # 整改后的结果读取并处理成dataframe
    mondayAfter = read_xlsx("整改后\\1021.xlsx")
    tuesdayAfter = read_xlsx("整改后\\1022.xlsx")
    wednesdayAfter = read_xlsx("整改后\\1023.xlsx")
    thursdayAfter = read_xlsx("整改后\\1024.xlsx")
    fridayAfter = read_xlsx("整改后\\1025.xlsx")
    saturdayAfter = read_xlsx("整改后\\1026.xlsx")
    sundayAfter = read_xlsx("整改后\\1027.xlsx")
    framesAfter = [
        mondayAfter, tuesdayAfter, wednesdayAfter, thursdayAfter, fridayAfter,
        saturdayAfter, sundayAfter
    ]
    dataAfter = np.array(framesAfter)
    heatDataAfter = pd.DataFrame(dataAfter)

    indexName = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    timeListStr = [
        strftime(
            strptime("15:55", "%H:%M") + datetime.timedelta(minutes=i),
            "%H:%M") for i in range(0, 112)
    ]
    # print(timeListStr)
    colName = {}
    for index, value in enumerate(timeListStr):
        colName[index] = value
    drawDataBefore = heatDataBefore.rename(index=indexName, columns=colName)
    drawDataAfter = heatDataAfter.rename(index=indexName, columns=colName)


    f, (ax1, ax2) = plt.subplots(figsize=(6, 4), nrows=2)
    # 调整前的热图
    sns.heatmap(drawDataBefore,
                ax=ax1,
                vmin=0,
                vmax=1,
                cmap='rainbow',
                robust=True,
                linewidths=0.05,
                linecolor='white')
    ax1.set_title('Road saturation before adjustment (2019.10.14-2019.10.20)',
                  fontsize=18)
    for tick in ax1.get_xticklabels():
        tick.set_rotation(360)

    # 调整后的热图
    sns.heatmap(drawDataAfter,
                ax=ax2,
                vmin=0,
                vmax=1,
                cmap='rainbow',
                robust=True,
                linewidths=0.05,
                linecolor='white')
    ax2.set_title('Road saturation after adjustment (2019.10.21-2019.10.27)',
                  fontsize=18)
    for tick in ax2.get_xticklabels():
        tick.set_rotation(360)

    plt.xlabel('Time', fontsize=13)

    # f.title(
    #     'Road saturation before & after adjustment (2019.10.14-2019.10.27)',
    #     y=1.05,
    #     size=18)
    plt.show()


if __name__ == '__main__':
    # read_xlsx("1014.xlsx")
    heatMap()
