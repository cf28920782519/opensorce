import cx_Oracle
import matplotlib.pyplot as plt


def get_connection_oracle():
    conn = cx_Oracle.connect('scott/cf6024584@localhost/ORCL')
    return conn


def free(conn, cursor):
    cursor.close()
    conn.close()


def queryTravelTime(conn):
    if conn is None:
        conn = get_connection_oracle()  # 建立数据库连接

    cr = conn.cursor()  # 生成连接的游标
    querySQL_summer = (
        "SELECT travel_time FROM travel_time_liuzhong WHERE JGSJ_IN BETWEEN TO_DATE('2019-08-12','YYYY-MM-DD') AND TO_DATE('2019-08-18','YYYY-MM-DD') AND TO_CHAR(JGSJ_OUT,'HH24:MI') BETWEEN '16:25' AND '17:25' ORDER BY TRAVEL_TIME"
    )
    querySQL_school = (
        "SELECT travel_time FROM travel_time_liuzhong WHERE JGSJ_IN BETWEEN TO_DATE('2019-05-13','YYYY-MM-DD') AND TO_DATE('2019-05-19','YYYY-MM-DD') AND TO_CHAR(JGSJ_OUT,'HH24:MI') BETWEEN '16:25' AND '17:25' ORDER BY TRAVEL_TIME"
    )
    cr.execute(querySQL_summer)
    queryRes_summer = cr.fetchall()
    cr.execute(querySQL_school)
    queryRes_school = cr.fetchall()
    free(conn, cr)

    travelTimeList_summer = []
    for data in queryRes_summer:
        travelTimeList_summer.append(data[0])
    travelTimeList_school = []
    for data in queryRes_school:
        travelTimeList_school.append(data[0])
    # travelTimeList = [i for i in travelTimeList if i < 400]
    # travelTimeList = [i for i in travelTimeList if i > 400]
    return travelTimeList_school, travelTimeList_summer


if __name__ == '__main__':
    conn = None
    travelTimeList_school, travelTimeList_summer = queryTravelTime(conn)
    # print(travelTimeList_school)
    travelTimeList_summer = [i for i in travelTimeList_summer if i < 400]
    # print(travelTimeList_summer)
    travelTimeList_schoolLocal = [i for i in travelTimeList_school if i > 400]
    # print(travelTimeList_schoolLocal)
    # print(len(travelTimeList_schoolLocal))
    

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.hist(travelTimeList_summer, bins=50, rwidth=0.8, color='green')
    ax1.set_xlabel("travel time(s)", fontsize=13)
    ax1.set_ylabel("number of samples", fontsize=13)
    ax1.set_title("The histogram of travel time distribution from August 12-18", fontsize=15)

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.hist(travelTimeList_school, bins=500, rwidth=0.8, color='red')
    ax2.set_xlabel("travel time(s)", fontsize=13)
    ax2.set_ylabel("number of samples", fontsize=13)
    ax2.set_title("The histogram of travel time distribution from May 13-19", fontsize=15)

    ax3 = fig.add_subplot(2, 1, 2)
    ax3.hist(travelTimeList_schoolLocal, bins=50, rwidth=0.8, color='blue')
    ax3.set_xlabel("travel time(s)", fontsize=13)
    ax3.set_ylabel("number of samples", fontsize=13)
    ax3.set_title("The local area of travel time (>400) distribution from May 13-19", fontsize=15)
    plt.show()

