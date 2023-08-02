import random
import time
from sm3 import sm3
#Rho method

def Rho_method(n):
    num = int(n/4)               
    time = 1
    #利用x随机选取起始值
    x = hex(random.randint(0, 2**(n+1)-1))[2:]
    x_i = sm3(x)                
    x_j = sm3(x_i)
    #寻找碰撞，若无碰撞，则持续迭代计算
    while x_i[:num] != x_j[:num]:
        time += 1
        x_i = sm3(x_i)  
        x_j = sm3(sm3(x_j))     
    x_j = x_i           
    x_i = x             
    for k in range(time):
        if sm3(x_i)[:num] == sm3(x_j)[:num]:
            print("已成功找到前{}bit相同的消息，16进制表示为:".format(n))
            print("消息1：{}\n消息2：{}".format(x_i,x_j))
            return
        else:
            x_i = sm3(x_i)
            x_j = sm3(x_j)



Rho_method(8)
Rho_method(16)


