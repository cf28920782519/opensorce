# import pandas as pd
import matplotlib.pyplot as plt

x_time = [
    '16:40', '16:45', '16:50', '16:55', '17:00', '17:05', '17:10', '17:15',
    '17:20', '17:25', '17:30', '17:35', '17:40'
]

myfont = {'size': 13}

# 20190814
# y_linkflow = [47, 56, 49, 42, 53, 40, 47, 49, 56, 62, 58, 54, 51]
# y_averagespeed = [23, 22, 18, 21, 14, 10, 11, 9, 12, 12, 10, 11, 15]

# 20190815
y_linkflow_schooldays = [51, 57, 42, 38, 46, 44, 50, 48, 51, 57, 58, 51, 49]
y_averagespeed_schooldays = [22, 19, 20, 15, 15, 11, 9, 14, 17, 17, 16, 18, 21]

# # 20190816
# y_linkflow = [59, 60, 47, 41, 50, 39, 52, 54, 49, 60, 54, 47, 49]
# y_averagespeed = [20, 22, 21, 19, 17, 15, 13, 10, 14, 15, 14, 15, 18]

# # 20190817
# y_linkflow = [39, 48, 47, 44, 56, 43, 38, 51, 52, 56, 50, 51, 46]
# y_averagespeed = [26, 26, 24, 21, 23, 24, 23, 27, 24, 27, 26, 25, 28]

# # 20190513
# y_linkflow = [42, 48, 47, 40, 49, 34, 42, 41, 49, 63, 57, 54, 51]
# y_averagespeed = [25, 26, 24, 25, 26, 24, 21, 22, 24, 22, 24, 23, 21]

# # 20190514
# y_linkflow = [39, 47, 45, 48, 49, 36, 49, 54, 53, 53, 56, 61, 62]
# y_averagespeed = [25, 24, 24, 25, 26, 23, 22, 24, 25, 24, 22, 23, 22]

# # 20190515
# y_linkflow = [39, 50, 51, 39, 45, 48, 44, 42, 50, 59, 58, 61, 62]
# y_averagespeed = [26, 27, 28, 27, 25, 23, 24, 23, 24, 22, 21, 19, 20]

# 20190516
y_linkflow_summer = [41, 48, 49, 38, 49, 49, 42, 45, 58, 63, 62, 53, 56]
y_averagespeed_summer = [24, 27, 23, 24, 24, 22, 22, 25, 23, 25, 25, 23, 22]

# # 20190517
# y_linkflow = [42, 49, 47, 38, 49, 40, 43, 43, 52, 51, 62, 53, 55]
# y_averagespeed = [28, 27, 26, 27, 26, 23, 24, 23, 23, 25, 21, 22, 22]

# # 20190518
# y_linkflow = [41, 43, 57, 49, 59, 43, 41, 42, 59, 60, 59, 53, 56]
# y_averagespeed = [25, 26, 26, 26, 27, 24, 24, 24, 25, 25, 25, 26, 24]

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

l1 = ax1.plot(x_time, y_linkflow_summer, 'm^-', label="link flow on summer holiday")
l2 = ax1.plot(x_time, y_linkflow_schooldays, 'c^-', label="link flow on school day")
ax1.set_ylim(0, 80, 10)
l3 = ax2.plot(x_time, y_averagespeed_summer, 'bo--', label="road speed on summer holiday")
l4 = ax2.plot(x_time, y_averagespeed_schooldays, 'ro--', label="road speed on school day")
ax2.set_ylim(0, 30, 5)
ax1.set_xlabel('Time', fontsize=13)

ax1.set_ylabel('Link flow every 5min (veh)', color='k', fontsize=13)

ax2.set_ylabel('Average speed (km/h)', color='k', fontsize=13)

ax1.set_title("Summer Holiday-2019.08.15 v.s. School Day-2019.05.16", fontsize=18)
lns = l1 + l2 + l3 + l4
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc='lower center', prop=myfont)

plt.show()
