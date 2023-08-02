import random
import time
from sm3 import sm3
#生日攻击

def get_randlist(n,max_num):
    randlist=[]
    while len(randlist)<n:
        x=random.randint(0,max_num)
        if x not in randlist:
            randlist.append(x)
    return randlist

def birth_attack(n):
    max_num=2**n
    rand_num=int(max_num**0.5)

    while True:
        lst1_val=[]
        lst2_val=[]
        lst1=get_randlist(rand_num,max_num)
        lst2=get_randlist(rand_num,max_num)
        for i in range(rand_num):
            lst1_val.append(sm3(lst1[i])[0:n])
            lst2_val.append(sm3(lst2[i])[0:n]) 
        col=set(lst1_val)&set(lst2_val)
        if not col:
            continue
        else:
            col=str(list(col)[0])
            num1=lst1_val.index(col)
            num2=lst2_val.index(col)
            if lst1[num1]==lst2[num2]:
                continue
            else:
                break
    print("已成功找到前{}bit相同的消息，十六进制表示为：{:X},{:X}".format(n,lst1[num1],lst2[num2]))
t1=time.time()
birth_attack(8)
t2=time.time()
print("用时：",t2-t1)

t3=time.time()
birth_attack(16)
t4=time.time()
print("用时：",t4-t3)

t5=time.time()
birth_attack(32)
t6=time.time()
print("用时：",t6-t5)
