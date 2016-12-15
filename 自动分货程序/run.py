import csv
import copy
import random

#配置
#单款基本库存量
BASE_AMOUNT=20

def readCSV(path):
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        d=[]
        for row in spamreader:
            d.append(row)
        return d[1:]
    return None

def tint(str):
    try:
        return int(str)
    except:
        return 0

#二维转一维
def readinv(d):
    r={}
    s=0
    for i in d:
        r[i[0]]={'inv':{
                         '215':tint(i[1]),
                         '220':tint(i[2]),
                         '225':tint(i[3]),
                         '230':tint(i[4]),
                         '235':tint(i[5]),
                         '240':tint(i[6]),
                         '245':tint(i[7]),
                         '250':tint(i[8])
                        },
                 'sum':tint(i[1])+tint(i[2])+tint(i[3])+tint(i[4])+tint(i[5])+tint(i[6])+tint(i[7])+tint(i[8]),
                 'target':tint(i[9])
                 }
        s+=r[i[0]]['target']
    print('总库存 %d'%s)
    return r
    


inv=readinv(readCSV('data\\inventory.csv'))
units=readCSV('data\\unit.csv')


sum_target=0
#调整库存到目标库存
for i in inv:
    if(inv[i]['target']<inv[i]['sum']):
        #目标库存与现有库存不一致 进行调整
        p_inv=inv[i]['inv']
        t_inv=copy.deepcopy(inv[i]['inv'])
        s=0
        #按比例下减
        for j in t_inv:
            t_inv[j]=int(inv[i]['target']/inv[i]['sum']*p_inv[j])
            s+=t_inv[j]
        #随机补齐
        while(s<inv[i]['target']):
            key,amount= random.sample(t_inv.items(),1)[0]
            if(t_inv[key]+1<=p_inv[key]):
                t_inv[key]+=1
                s+=1
        inv[i]['inv']=copy.deepcopy(t_inv)
        inv[i]['sum']=s
    sum_target+=inv[i]['sum']

print('目标数 %d'%sum_target)

#分配库存

sum_d=0
result={}
for i in inv:
    #根据基础量确定分配仓数
    m=copy.deepcopy(inv[i])
    num_to_u=min(int(m['sum']/BASE_AMOUNT)+1,len(units))
    #print(i,m['sum'],num_to_u)

    #随机抽取目标仓库
    t_unit=random.sample(units,num_to_u)
    
    #库存分配权重
    p_sum=0
    for u in t_unit:
        p_sum+=int(u[1])

    #分配库存
    r={}  # r={'size':{'unit1':amount,'unit2',amount}}
    for s in m['inv']:
        r[s]={}

        t_size_s=0
        #按比例分配
        for u in t_unit:
            r[s][u[0]]=int(m['inv'][s]*(int(u[1])/p_sum))
            t_size_s+=r[s][u[0]]
        #随机补齐
        while(t_size_s<m['inv'][s]):
            for z in t_unit:
                if(t_size_s<m['inv'][s]):
                    r[s][z[0]]+=1
                    t_size_s+=1
                else:
                    break
        sum_d+=t_size_s

    result[i]=copy.deepcopy(r)

print('分配数 %d'%sum_d)

data=[]

#输出
with open('data\\result.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerow(['货号', '尺码', '单位', '数量'])
    for code in result:
        for size in result[code]:
            for unit in result[code][size]:
                spamwriter.writerow([code,size,unit,result[code][size][unit]])


