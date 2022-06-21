from gekko import GEKKO
from datetime import datetime
import pandas as pd
from numpy import cumsum
from dateutil.tz import gettz
import random
def hello():
    timezone_variable = gettz("Europe/London") 
    m = GEKKO(remote=True)
    start_end = [datetime(2022, 5, random.randint(1,29),15,0,0,0,timezone_variable).date(), datetime(2022, 6, random.randint(1,29),15,0,0,0,timezone_variable).date(),
                datetime(2022, 5, random.randint(1,29),15,0,0,0,timezone_variable).date(), datetime(2022, 6, random.randint(1,29),15,0,0,0,timezone_variable).date(),
                datetime(2022, 5, random.randint(1,29),15,0,0,0,timezone_variable).date(), datetime(2022, 6, random.randint(1,29),15,0,0,0,timezone_variable).date()]
    ects_breakdown = [100,130,160,53,20,100,130,160,53,20,100,130,160,53,20,100,130,160,53,20,100,130,160,100,130,160,53,20,100,130,160,53,20,100,130,160,100,130,160,53,20,100,130,160,53,20,100,130,160,53,20,100,130,160,53,20,100,130,160,53,20,100,130,160,53,20,100,130,160,53,20,100,130,160,53,20,100,130,160,53,20]
    n = int(len(start_end)/2)
    print(n)
    no_intervals = len(start_end)-1
    sorted_dates = start_end.copy()
    sorted_dates.sort()
    interval_days = [0] * (no_intervals)
    exist = []
    for i in range(n):
        exist.append([0]*no_intervals)
    for s in range(no_intervals):
        interval_days[s] = (sorted_dates[s+1] - sorted_dates[s]).days
    for t in range(n):
        for s in range(no_intervals):
            if start_end[t*2]<= sorted_dates[s] and sorted_dates[s+1] <= start_end[t*2+1] :
                exist[t][s] = 1
    Z = m.Var()
    intensity_val = m.Array(m.Var,(n,no_intervals))
    for i in range(n):
        for j in range(no_intervals):
                    intensity_val[i,j].lower = 0


    m.Minimize(Z)

    def test(exist,interval_days,ects_breakdown,intensity_val,n, no_intervals):
        equation = []
        for i in range(n):
            result = 0
            for j in range(no_intervals):
                if exist[i][j] == 1:
                    result = result + interval_days[j]*intensity_val[i][j]
            equation.append(result == ects_breakdown[i])
        return equation

    m.Equations([test(exist,interval_days,ects_breakdown,intensity_val,n, no_intervals)])

    def test2(Z,exist,intensity_val,n, no_intervals):
        equation = []
        for i in range(no_intervals):
            result = 0
            for j in range(n):
                if exist[j][i]:
                    result = result + intensity_val[j][i]
            equation.append(Z >=result)
        return equation


    m.Equations([test2(Z,exist,intensity_val,n, no_intervals)])
    m.solve(disp=True)
    print('Solver Time: ', m.options.SOLVETIME)
    # print(intensity_val)
    # print(intensity_val[0][0].value[0])
    # print(Z.value[0])
    # print(Z)

    # Creating data for graph
    # date_range = pd.date_range(start=sorted_dates[0], end = sorted_dates[-1]).to_pydatetime().tolist()
    # date_range = [i.strftime("%d/%m/%Y") for i in date_range]
    # print(date_range)
    # range_index = cumsum(interval_days)
    # for i in range_index:
    #     print(date_range[i])
    # print(cumsum(interval_days))
    # date_intensity = []
    # for i in intensity_val: # for each coursework
    #     temp = [i[0].value[0]]
    #     for j in range(no_intervals):
    #         for k in range(interval_days[j]):
    #             temp.append(i[j].value[0])
    #     date_intensity.append(temp)
    
    # eval_str = ""
    # for i in range(5):
    #     for j in range(9):
    #         eval_str = eval_str +  "intensity_val[" + str(i)+ "][" + str(j) + "]>=0,"
    # print(eval_str)

    # print(date_intensity)
    # return (date_intensity,date_range)
 


# def hello():
#     timezone_variable = gettz("Europe/London") 
#     m = GEKKO(remote=True)
#     start_end = [datetime(2022, 5, 4,15,0,0,0,timezone_variable).date(), datetime(2022, 5, 6,15,0,0,0,timezone_variable).date(), 
#                 datetime(2022, 5, 12,15,0,0,0,timezone_variable).date(), datetime(2022, 5, 18,15,0,0,0,timezone_variable).date(),
#                 datetime(2022, 5, 14,11,0,0,0,timezone_variable).date(), datetime(2022, 5, 20,15,0,0,0,timezone_variable).date(),
#                 datetime(2022, 5, 16,15,0,0,0,timezone_variable).date(), datetime(2022, 5, 21,15,0,0,0,timezone_variable).date(),
#                 datetime(2022, 5, 16,15,0,0,0,timezone_variable).date(), datetime(2022, 5, 30,15,0,0,0,timezone_variable).date()]
#     ects_breakdown = [100,130,160,53,20]
#     Z = None

#     n = int(len(start_end)/2)
#     no_intervals = len(start_end)-1
#     sorted_dates = start_end.copy()
#     sorted_dates.sort()

#     print(sorted_dates)
#     interval_days = [0] * (9)
#     exist = []
#     for i in range(5):
#         exist.append([0]*9)
#     intensity_val = []
#     for i in range(5):
#         intensity_val.append([0]*9)
#     print(interval_days)
#     print(exist)
#     for s in range(no_intervals):
#         interval_days[s] = (sorted_dates[s+1] - sorted_dates[s]).days
#     print("This is it: ",interval_days)
#     for t in range(n):
#         for s in range(no_intervals):
#             if start_end[t*2]<= sorted_dates[s] and sorted_dates[s+1] <= start_end[t*2+1] :
#                 exist[t][s] = 1
#     print("Exist: ", exist)

#     intensity_val[0][0],intensity_val[0][1],intensity_val[0][2],intensity_val[0][3],intensity_val[0][4],intensity_val[0][5],intensity_val[0][6],intensity_val[0][7],intensity_val[0][8],intensity_val[1][0],intensity_val[1][1],intensity_val[1][2],intensity_val[1][3],intensity_val[1][4],intensity_val[1][5],intensity_val[1][6],intensity_val[1][7],intensity_val[1][8],intensity_val[2][0],intensity_val[2][1],intensity_val[2][2],intensity_val[2][3],intensity_val[2][4],intensity_val[2][5],intensity_val[2][6],intensity_val[2][7],intensity_val[2][8],intensity_val[3][0],intensity_val[3][1],intensity_val[3][2],intensity_val[3][3],intensity_val[3][4],intensity_val[3][5],intensity_val[3][6],intensity_val[3][7],intensity_val[3][8],intensity_val[4][0],intensity_val[4][1],intensity_val[4][2],intensity_val[4][3],intensity_val[4][4],intensity_val[4][5],intensity_val[4][6],intensity_val[4][7],intensity_val[4][8],Z = m.Array(m.Var,46)


#     m.Minimize(Z)

#     def test(exist,interval_days,ects_breakdown,intensity_val,n):
#         result = 0
#         for i in range(n):
#             result = result + exist[0][i]*interval_days[i]*intensity_val[0][i]
            
#         return result == ects_breakdown[0]

#     m.Equation([test(exist,interval_days,ects_breakdown,intensity_val,n),
#                 exist[1][0]*interval_days[0]*intensity_val[1][0]+exist[1][1]*interval_days[1]*intensity_val[1][1]+exist[1][2]*interval_days[2]*intensity_val[1][2]+exist[1][3]*interval_days[3]*intensity_val[1][3]+exist[1][4]*interval_days[4]*intensity_val[1][4]+exist[1][5]*interval_days[5]*intensity_val[1][5]+exist[1][6]*interval_days[6]*intensity_val[1][6]+exist[1][7]*interval_days[7]*intensity_val[1][7]+exist[1][8]*interval_days[8]*intensity_val[1][8]==ects_breakdown[1],
#                 exist[2][0]*interval_days[0]*intensity_val[2][0]+exist[2][1]*interval_days[1]*intensity_val[2][1]+exist[2][2]*interval_days[2]*intensity_val[2][2]+exist[2][3]*interval_days[3]*intensity_val[2][3]+exist[2][4]*interval_days[4]*intensity_val[2][4]+exist[2][5]*interval_days[5]*intensity_val[2][5]+exist[2][6]*interval_days[6]*intensity_val[2][6]+exist[2][7]*interval_days[7]*intensity_val[2][7]+exist[2][8]*interval_days[8]*intensity_val[2][8]==ects_breakdown[2],
#                 exist[3][0]*interval_days[0]*intensity_val[3][0]+exist[3][1]*interval_days[1]*intensity_val[3][1]+exist[3][2]*interval_days[2]*intensity_val[3][2]+exist[3][3]*interval_days[3]*intensity_val[3][3]+exist[3][4]*interval_days[4]*intensity_val[3][4]+exist[3][5]*interval_days[5]*intensity_val[3][5]+exist[3][6]*interval_days[6]*intensity_val[3][6]+exist[3][7]*interval_days[7]*intensity_val[3][7]+exist[3][8]*interval_days[8]*intensity_val[3][8]==ects_breakdown[3],
#                 exist[4][0]*interval_days[0]*intensity_val[4][0]+exist[4][1]*interval_days[1]*intensity_val[4][1]+exist[4][2]*interval_days[2]*intensity_val[4][2]+exist[4][3]*interval_days[3]*intensity_val[4][3]+exist[4][4]*interval_days[4]*intensity_val[4][4]+exist[4][5]*interval_days[5]*intensity_val[4][5]+exist[4][6]*interval_days[6]*intensity_val[4][6]+exist[4][7]*interval_days[7]*intensity_val[4][7]+exist[4][8]*interval_days[8]*intensity_val[4][8]==ects_breakdown[4]])


#     m.Equations([Z>=exist[0][0]*intensity_val[0][0]+exist[1][0]*intensity_val[1][0]+exist[2][0]*intensity_val[2][0]+exist[3][0]*intensity_val[3][0]+exist[4][0]*intensity_val[4][0],
#                 Z>=exist[0][1]*intensity_val[0][1]+exist[1][1]*intensity_val[1][1]+exist[2][1]*intensity_val[2][1]+exist[3][1]*intensity_val[3][1]+exist[4][1]*intensity_val[4][1],
#                 Z>=exist[0][2]*intensity_val[0][2]+exist[1][2]*intensity_val[1][2]+exist[2][2]*intensity_val[2][2]+exist[3][2]*intensity_val[3][2]+exist[4][2]*intensity_val[4][2],
#                 Z>=exist[0][3]*intensity_val[0][3]+exist[1][3]*intensity_val[1][3]+exist[2][3]*intensity_val[2][3]+exist[3][3]*intensity_val[3][3]+exist[4][3]*intensity_val[4][3],
#                 Z>=exist[0][4]*intensity_val[0][4]+exist[1][4]*intensity_val[1][4]+exist[2][4]*intensity_val[2][4]+exist[3][4]*intensity_val[3][4]+exist[4][4]*intensity_val[4][4],
#                 Z>=exist[0][5]*intensity_val[0][5]+exist[1][5]*intensity_val[1][5]+exist[2][5]*intensity_val[2][5]+exist[3][5]*intensity_val[3][5]+exist[4][5]*intensity_val[4][5],
#                 Z>=exist[0][6]*intensity_val[0][6]+exist[1][6]*intensity_val[1][6]+exist[2][6]*intensity_val[2][6]+exist[3][6]*intensity_val[3][6]+exist[4][6]*intensity_val[4][6],
#                 Z>=exist[0][7]*intensity_val[0][7]+exist[1][7]*intensity_val[1][7]+exist[2][7]*intensity_val[2][7]+exist[3][7]*intensity_val[3][7]+exist[4][7]*intensity_val[4][7],
#                 Z>=exist[0][8]*intensity_val[0][8]+exist[1][8]*intensity_val[1][8]+exist[2][8]*intensity_val[2][8]+exist[3][8]*intensity_val[3][8]+exist[4][8]*intensity_val[4][8]])
#     m.solve()
#     print(intensity_val)
#     print(intensity_val[0][0].value[0])
#     print(Z.value[0])
#     print(Z)

#     # Creating data for graph
#     date_range = pd.date_range(start=sorted_dates[0], end = sorted_dates[-1]).to_pydatetime().tolist()
#     date_range = [i.strftime("%d/%m/%Y") for i in date_range]
#     print(date_range)
#     range_index = cumsum(interval_days)
#     for i in range_index:
#         print(date_range[i])
#     print(cumsum(interval_days))
#     date_intensity = []
#     for i in intensity_val: # for each coursework
#         temp = [i[0].value[0]]
#         for j in range(no_intervals):
#             for k in range(interval_days[j]):
#                 temp.append(i[j].value[0])
#         date_intensity.append(temp)
    
#     eval_str = ""
#     for i in range(5):
#         for j in range(9):
#             eval_str = eval_str +  "intensity_val[" + str(i)+ "][" + str(j) + "]>=0,"
#     print(eval_str)

#     print(date_intensity)
#     return (date_intensity,date_range)
 


# def hello():
#     timezone_variable = gettz("Europe/London") 
#     m = GEKKO(remote=True)
#     start_end = [datetime(2022, 5, 4,15,0,0,0,timezone_variable).date(), datetime(2022, 5, 6,15,0,0,0,timezone_variable).date(), 
#                 datetime(2022, 5, 12,15,0,0,0,timezone_variable).date(), datetime(2022, 5, 18,15,0,0,0,timezone_variable).date(),
#                 datetime(2022, 5, 14,11,0,0,0,timezone_variable).date(), datetime(2022, 5, 20,15,0,0,0,timezone_variable).date()]
#     ects_breakdown = [100,130,160]
#     Z = None

#     n = int(len(start_end)/2)
#     no_intervals = len(start_end)-1
#     sorted_dates = start_end.copy()
#     sorted_dates.sort()

#     print(sorted_dates)
#     interval_days = [0] * (no_intervals)
#     exist = []
#     for i in range(n):
#         exist.append([0]*no_intervals)
#     intensity_val = []
#     for i in range(n):
#         intensity_val.append([0]*no_intervals)
#     print(interval_days)
#     print(exist)
#     for s in range(no_intervals):
#         interval_days[s] = (sorted_dates[s+1] - sorted_dates[s]).days
#     print(interval_days)
#     for t in range(n):
#         for s in range(no_intervals):
#             if start_end[t*2]<= sorted_dates[s] and sorted_dates[s+1] <= start_end[t*2+1] :
#                 exist[t][s] = 1
#     print(exist)
#     definition = ""
#     for i in range(n):
#         for j in range(no_intervals):
#             definition = definition + "intensity_val[" + str(i)+ "][" + str(j) + "],"
#             if (i+1)*(j+1) == n*no_intervals:
#                 definition = definition + "Z = m.Array(m.Var," + str(n*no_intervals+1) + ")"

#     print(definition)
#     exec(definition)


#     m.Minimize(Z)
#     # pyth_str = "exist[0]*interval_days[0]*a[0]+exist[1]*interval_days[1]*a[1]+exist[2]*interval_days[2]*a[2]+exist[3]*interval_days[3]*a[3]+ exist[4]*interval_days[4]*a[4] == etcs_breakdown[0],exist[5]*interval_days[0]*b[0]+exist[6]*interval_days[1]*b[1]+exist[7]*interval_days[2]*b[2]+exist[8]*interval_days[3]*b[3]+ exist[9]*interval_days[4]*b[4] == etcs_breakdown[1],exist[10]*interval_days[0]*c[0]+exist[11]*interval_days[1]*c[1]+exist[12]*interval_days[2]*c[2]+exist[13]*interval_days[3]*c[3]+ exist[14]*interval_days[4]*c[4] == etcs_breakdown[2]"
#     eval_str = ""
#     for i in range(n):
#         for j in range(no_intervals):
#             eval_str = eval_str +  "exist[" + str(i) + "][" + str(j) + "]*interval_days[" + str(j) + "]*intensity_val[" + str(i)+ "][" + str(j) + "]"
#             if j != no_intervals-1:
#                 eval_str = eval_str + "+"
#         eval_str = eval_str + "==ects_breakdown[" + str(i)+ "]"
#         if i!=n-1:
#             eval_str = eval_str + ","
#     print(eval_str)
#     m.Equation([eval(eval_str)])

#     inequality_str = ""
#     for j in range(no_intervals):
#         inequality_str = inequality_str + "Z>="
#         for i in range(n):
#             inequality_str = inequality_str +  "exist[" + str(i) + "][" + str(j) + "]*intensity_val[" + str(i)+ "][" + str(j) + "]"
#             if i != n-1:
#                 inequality_str = inequality_str + "+"
#         if j!=no_intervals-1:
#             inequality_str = inequality_str + ","
#     print(inequality_str)
#     m.Equations([eval(inequality_str)])
#     print(eval(inequality_str))
#     m.solve()
#     print(intensity_val)
#     print(intensity_val[0][0].value[0])
#     print(Z.value[0])
#     print(Z)

#     # Creating data for graph
#     date_range = pd.date_range(start=sorted_dates[0], end = sorted_dates[-1]).to_pydatetime().tolist()
#     print(date_range)
#     range_index = cumsum(interval_days)
#     for i in range_index:
#         print(date_range[i])
#     print(cumsum(interval_days))
#     date_intensity = []
#     for i in intensity_val: # for each coursework
#         temp = [i[0].value[0]]
#         for j in range(no_intervals):
#             for k in range(interval_days[j]):
#                 temp.append(i[j].value[0])
#         date_intensity.append(temp)

#     print(date_intensity)

hello()

# from datetime import datetime
# from dateutil.tz import gettz
# timezone_variable = gettz("Europe/London") 
# d1 = datetime(2022, 6, 17,15,0,0,0,timezone_variable)
# d2 = datetime(2022, 6, 19,12,0,0,0,timezone_variable)
# d3 = datetime(2022, 6, 19,15,0,0,0,timezone_variable)
# dates = [d2.date(),d1.date(),d3.date()]
# for f in range(len(dates)-1):
#     for s in range(5):
#         print(s*2)
# print(dates)
# dates.sort()
# print(dates)
# delta = d2.date()-d1.date()
# print(delta.days)

