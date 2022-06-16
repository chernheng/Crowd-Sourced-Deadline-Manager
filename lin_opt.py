from gekko import GEKKO
from datetime import datetime
from dateutil.tz import gettz
timezone_variable = gettz("Europe/London") 
m = GEKKO(remote=False)
start_end = [datetime(2022, 5, 4,15,0,0,0,timezone_variable).date(), datetime(2022, 6, 4,15,0,0,0,timezone_variable).date(), 
            datetime(2022, 5, 12,15,0,0,0,timezone_variable).date(), datetime(2022, 6, 1,15,0,0,0,timezone_variable).date(),
            datetime(2022, 5, 22,11,0,0,0,timezone_variable).date(), datetime(2022, 6, 18,15,0,0,0,timezone_variable).date()]

sorted_dates = start_end.copy()
sorted_dates.sort()
print(start_end)
print(sorted_dates)
interval_days = [0,0,0,0,0]
exist = [0]*15
for s in range(len(sorted_dates)-1):
    interval_days[s] = (sorted_dates[s+1] - sorted_dates[s]).days
print(interval_days)
for t in range(3):
    for s in range(len(sorted_dates)-1):
        if start_end[t*2]<= sorted_dates[s] and sorted_dates[s+1] <= start_end[t*2+1] :
            exist[t*5+s] = 1
print(exist)
a = [0] * 5
b = [0] * 5
c = [0] * 5
ects_breakdown = [100,130,160]
a[0],a[1],a[2],a[3],a[4],b[0],b[1],b[2],b[3],b[4],c[0],c[1],c[2],c[3],c[4],Z = m.Array(m.Var,16)
m.Minimize(Z)
pyth_str = "exist[0]*interval_days[0]*a[0]+exist[1]*interval_days[1]*a[1]+exist[2]*interval_days[2]*a[2]+exist[3]*interval_days[3]*a[3]+ exist[4]*interval_days[4]*a[4] == etcs_breakdown[0],exist[5]*interval_days[0]*b[0]+exist[6]*interval_days[1]*b[1]+exist[7]*interval_days[2]*b[2]+exist[8]*interval_days[3]*b[3]+ exist[9]*interval_days[4]*b[4] == etcs_breakdown[1],exist[10]*interval_days[0]*c[0]+exist[11]*interval_days[1]*c[1]+exist[12]*interval_days[2]*c[2]+exist[13]*interval_days[3]*c[3]+ exist[14]*interval_days[4]*c[4] == etcs_breakdown[2]"
eval_str = ""
n = 3
for i in range(n):
    for j in range(n*2-1):
        eval_str = eval_str +  "exist[" + str(i*(n*2-1)+j) + "]*interval_days[" + str(j) + "]*"
        if i ==0:
            eval_str = eval_str+"a["
        elif i==1:
            eval_str = eval_str+"b["
        elif i==2:
            eval_str = eval_str+"c["
        elif i==3:
            eval_str = eval_str+"d["
        elif i==4:
            eval_str = eval_str+"e["
        eval_str = eval_str+ str(j) + "]"
        if j != n*2-2:
            eval_str = eval_str + "+"
    eval_str = eval_str + "==ects_breakdown[" + str(i)+ "]"
    if i!=n-1:
        eval_str = eval_str + ","
print(eval_str)
# print(fh)
m.Equation([eval(eval_str)])
m.Equations([Z>=exist[0]*a[0]+exist[5]*b[0]+exist[10]*c[0],
             Z>=exist[1]*a[1]+exist[6]*b[1]+exist[11]*c[1],
             Z>=exist[2]*a[2]+exist[7]*b[2]+exist[12]*c[2],
             Z>=exist[3]*a[3]+exist[8]*b[3]+exist[13]*c[3],
             Z>=exist[4]*a[4]+exist[9]*b[4]+exist[14]*c[4]])
m.solve()
print(a)
print(a[0].value[0])
print(a[1].value[0])
print(a[2].value[0])
print(a[3].value[0])
print(a[4].value[0])
print(b[0].value[0])
print(b[1].value[0])
print(b[2].value[0])
print(b[3].value[0])
print(b[4].value[0])
print(c[0].value[0])
print(c[1].value[0])
print(c[2].value[0])
print(c[3].value[0])
print(c[4].value[0])
# print('x1: ',a[1].value[0])
# print('x2: ',a[2].value[0])
# print('x3: ',a[3].value[0])
# print('x1: ',b[0].value[0])
# print('x2: ',b[1].value[0])
# print('x3: ',b[2].value[0])
print('Z:  ',Z.value[0])

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