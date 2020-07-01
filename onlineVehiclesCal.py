import cx_Oracle
import datetime
import pandas as pd


def get_connection_oracle():
    conn = cx_Oracle.connect(
        'scott/cf6024584@localhost/ORCL')  # 建立oracle数据库的连接
    return conn


def free(conn, cursor):  # 关闭连接和游标
    cursor.close()
    conn.close()


def queryVehicleList(conn, DATE):
    if conn is None:
        conn = get_connection_oracle()  # 建立数据库连接

    cr = conn.cursor()  # 生成连接的游标

    querySQL_upstream = (
        "SELECT HPHM,JGSJ FROM SJCJ_T_CLXX_LS WHERE SSID='HK-92' AND CDBH IN \
('7', '8', '9') AND JGSJ BETWEEN TO_DATE('%s 15:30','YYYY-MM-DD HH24:MI') AND \
TO_DATE('%s 17:55','YYYY-MM-DD HH24:MI') ORDER BY JGSJ") % (DATE, DATE)

    cr.execute(querySQL_upstream)
    queryRes_upstream = cr.fetchall()
    upstreamRes = []
    for data in queryRes_upstream:
        upstreamRes.append(data)

    querySQL_downstream = (
        "SELECT HPHM,JGSJ FROM SJCJ_T_CLXX_LS WHERE SSID='HK-107' AND CDBH IN \
('3', '4') AND JGSJ BETWEEN TO_DATE('%s 15:30','YYYY-MM-DD HH24:MI') AND \
TO_DATE('%s 17:55','YYYY-MM-DD HH24:MI') ORDER BY JGSJ") % (DATE, DATE)

    cr.execute(querySQL_downstream)
    queryRes_downstream = cr.fetchall()
    downstreamRes = []
    for data in queryRes_downstream:
        downstreamRes.append(data)

    free(conn, cr)

    return upstreamRes, downstreamRes


def quchong(lis):
    lisSet = set(lis)
    lis_new = []
    for ele in lisSet:
        lis_new.append(ele)
    return lis_new


def calOnlineNum(upstreamRes, downstreamRes, timepoint):
    time = datetime.datetime.strptime(timepoint, "%Y-%m-%d %H:%M:%S")
    # time_before = time - datetime.timedelta(minutes=30)
    upstreamORA = []
    for data in upstreamRes:
        if data[1] <= time:
            upstreamORA.append(data[0])
        else:
            break
    # 上游的检测数据要进行去重
    upstream = quchong(upstreamORA)

    # print(len(upstream))
    # print(upstream)
    downstream = []
    for data in downstreamRes:
        if data[1] <= time:
            downstream.append(data[0])
        else:
            break
    # downstream = quchong(downstream)
    # print(len(downstream))
    # print(downstream)
    vehNum = 0
    roadSection = []
    # 把上游检测到的所有车牌全加进去
    for data in upstream:
        roadSection.append(data)
    # print(len(roadSection))

    # # 构建一个出现在下游，没出现在上游的车牌号码列表
    # downAppear = []
    # for ele in downstream:
    #     if ele not in upstream:
    #         downAppear.append(ele)

    # for ele in downAppear:
    #     roadSection.append(ele)

    # 构建一个出现在上游，没出现在下游的车牌号码名单列表
    upAppear = []
    for ele in upstream:
        if ele not in downstream:
            upAppear.append(ele)
    # print(upAppear)

    for data in downstream:
        if data != '车牌':
            # roadSection.remove(data)
            # 上下游匹配成功
            if data in roadSection:
                roadSection.remove(data)
            # 出现在下游，没出现在上游的识别成功的车
            elif data not in roadSection:
                roadSection.append(data)
                roadSection.remove(data)
        if data == '车牌':
            # roadSection.remove('车牌')
            plate = upAppear.pop(0)
            roadSection.remove(plate)

    # print(upstream)
    # print(downstream)
    # print(roadSection)
    # roadSection = [ele for ele in roadSection if ele != '车牌']
    vehNum = len(roadSection)
    # print(vehNum)

    # if len(upstream) != 0 and len(downstream) != 0:
    #     vehNum = len(upstream) - len(downstream)

    return vehNum


def calOnlineVehicles(upstreamRes, downstreamRes):
    # 提取日期
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    date = strftime(upstreamRes[0][1], "%Y-%m-%d")
    seconds = 8700
    format = "%H:%M:%S"
    start = "15:30:00"
    timeListStr = [
        date + " " + strftime(
            strptime(start, format) + datetime.timedelta(seconds=i), format)
        for i in range(0, seconds, 5)
    ]
    # timeList = []
    # for data in timeListStr:
    #     timeList.append(strptime(data, "%Y-%m-%d %H:%M:%S"))
    # # print(timeList)
    vehNumList = []
    for timePoint in timeListStr:
        vehNum = calOnlineNum(upstreamRes, downstreamRes, timePoint)
        vehNumList.append(vehNum)
    print(vehNumList)
    df_dic = {"time": timeListStr, "num": vehNumList}
    df = pd.DataFrame(df_dic)
    outpath = "D:\\Python\\Python_Project\\flowspeed\\data\\1015.csv"
    df.to_csv(outpath, sep=',', index=False, header=False)


if __name__ == '__main__':
    conn = None
    upRes, downRes = queryVehicleList(conn, '2019-10-15')
    # print(upRes)
    # print(downRes)
    calOnlineVehicles(upRes, downRes)
    # calOnlineNum(upRes, downRes, "2019-10-10 17:46:05")
