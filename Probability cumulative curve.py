import cx_Oracle
import numpy as np
import matplotlib.pyplot as plt


def get_connection_oracle():
    conn = cx_Oracle.connect(
        'scott/cf6024584@localhost/ORCL')  # 建立oracle数据库的连接
    return conn


def free(conn, cursor):  # 关闭连接和游标
    cursor.close()
    conn.close()


# 查询5月8日至7月8日的旅行时间
# 查询条件：全路段 工作日 每天放学前半小时到放学后半小时
# 返回旅行时间的列表
def queryTravelTime(conn):
    if conn is None:
        conn = get_connection_oracle()  # 建立数据库连接

    cr = conn.cursor()  # 生成连接的游标

    querySQL_school = "SELECT TRAVEL_TIME FROM TRAVEL_TIME_LIUZHONG WHERE \
SSID_IN IN ('HK-92', 'HK-93') AND SSID_OUT IN ('HK-92', 'HK-93') AND \
JGSJ_IN BETWEEN TO_DATE('2019-05-08','YYYY-MM-DD') AND \
TO_DATE('2019-07-08','YYYY-MM-DD') AND TO_CHAR(JGSJ_OUT,'HH24:MI') \
BETWEEN '16:25' AND '17:25' AND TO_CHAR(JGSJ_IN,'HH24:MI')BETWEEN '16:25' \
AND '17:25' AND DATE_TYPES=0 order by travel_time"

    cr.execute(querySQL_school)
    queryRes_school = cr.fetchall()
    free(conn, cr)
    travelTimeList_school = []
    for data in queryRes_school:
        travelTimeList_school.append(data[0])

    print(np.mean(travelTimeList_school))

    return travelTimeList_school


# 输入旅行时间的查询结果
def cal_x_y(travelTimeList_school):
    diffEle = set(travelTimeList_school)
    diffEle_list = []  # 不同的旅行时间样本列表
    for ele in diffEle:
        diffEle_list.append(ele)
    diffEle_list.sort()  # 按从小到大排列
    # print(diffEle_list)
    # print(len(diffEle_list))
    eleNum = []
    for ele in diffEle_list:
        for i in range(len(travelTimeList_school)):
            if travelTimeList_school[i] > ele:
                eleNum.append(i)
                break
    eleNum.append(len(travelTimeList_school))
    y_list = []
    total_num = len(travelTimeList_school)
    for i in range(len(eleNum)):
        y_list.append(1.0 * eleNum[i] / total_num)
    # print(y_list)
    return diffEle_list, y_list

    # print(diffEle_list)
    # print(eleNum)
    # print(len(eleNum))


def turning_point(x_list, y_list):
    if len(x_list) != len(y_list):
        print("列表长度不相同，无法计算")
        return
    index = 0
    for i, ele in enumerate(y_list):
        if ele >= 0.965:
            index = i
            break
        else:
            continue

    return x_list[index], y_list[index]


if __name__ == '__main__':
    conn = None
    travelTimeList_school = queryTravelTime(conn)
    print(len(travelTimeList_school))
    x, y = cal_x_y(travelTimeList_school)
    x_i, y_i = turning_point(x, y)
    print(x_i, y_i)
    fig = plt.figure()

    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot([0, x_i], [y_i, y_i], 'r--')
    ax1.plot([x_i, x_i], [0, y_i], 'r--')
    ax1.scatter(x, y, c='b', marker='o', s=3)
    plt.scatter(x_i, y_i, c='r', marker='o', s=20)
    plt.annotate('(%4d, %4.1f%%)' % (x_i, y_i * 100),
                 xy=(x_i, y_i),
                 arrowprops=dict(facecolor='black', shrink=0.005),
                 xytext=(1.1 * x_i, 0.9 * y_i))
    ax1.axis([0, 3500, 0, 1.05])
    ax1.set_xlabel('Travel time(s)', fontsize=18)
    ax1.set_ylabel('Sample percentage cumulative(%)', fontsize=18)
    plt.show()
    turning_point(x, y)
    # # x_i, y_i = cal_x(travelTimeList_school, 177.23, x, y)
    # print(x_i, y_i)
