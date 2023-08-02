import math
import random
import time
import string
#SM3 

#初始值IV
IV='7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
#常量
T_nor=['79cc4519','7a879d8a']

#布尔函数
def FF(x,y,z,j):
    if 0<=j<=15:
        return x^y^z
    else:
        return (x&y)|(x&z)|(y&z)

def GG(x,y,z,j):
    if 0<=j<=15:
        return x^y^z
    else:
        return (x&y)|(~x&z)
#置换函数
def leftmov(m,num):
    #向左移动
    num=num%32
    m=bin(m).replace('0b','').zfill(32)
    m_left=m[num:]+m[:num]
    return int(m_left,2)
#x代表字
def P0(x):
    return x^leftmov(x,9)^leftmov(x,17)
def P1(x):    
    return x^leftmov(x,15)^leftmov(x,23)

def str2byte(m):
    #str转换成byte数组的int值
    m_mid=len(m)
    m_byte=[]
    m_bytearray=m.encode('utf-8')
    for i in range(m_mid):
        m_byte.append(m_bytearray[i])
    return int(m_byte[0])
    

#消息填充
def msgcut(msg,mem):
    lenth=len(msg)
    num=int(lenth/mem)
    tool_ary=[]
    for i in range(num):
        tool_ary.append(msg[i*mem:mem+i*mem])
    return tool_ary

def msgpop(m):
    #输入的内容作为str
    m=str(m)
    lenth=len(m)
    mid_msg=""
    for i in range(lenth):
        mid_msg+=bin(str2byte(m[i])).replace('0b','').zfill(8)
    l_msg=len(mid_msg)
    k=512-(64+(l_msg+1))%512
    msg=mid_msg+'1'+k*'0'
    add_len=bin(l_msg).replace('0b','').zfill(64)
    msg=msg+add_len
    msg=msgcut(msg,512)
    return msg

#消息扩展和迭代压缩
def msgexpd(IV,m):
    B1=msgcut(m, 32)
    B2=[]
    T=[]
    T.append(int(T_nor[0],16))
    T.append(int(T_nor[1],16))
    for i in range(16):
        B1[i]=int(B1[i],2)
    for j in range(16,68):
        num=B1[j-16]^B1[j-9]^leftmov(B1[j-3],15)
        mid=P1(num)
        re=mid^leftmov(B1[j-13],7)^B1[j-6]
        B1.append(re)
    for k in range(64):
        mid=B1[k]^B1[k+4]
        B2.append(mid)
        
    #B1是W,B2是W'
    #print(B1,'***********',B2)
    iv=[]
    for i in range(8):
        iv.append(int(IV[i],16))
    A=iv[0]
    B=iv[1]
    C=iv[2]
    D=iv[3]
    E=iv[4]
    F=iv[5]
    G=iv[6]
    H=iv[7]
    toolnum=2**32
    for j in range(64):
        if j<=15:
            mid1=(leftmov(A,12)+E+leftmov(T[0],j))%toolnum
        else:
            mid1=(leftmov(A,12)+E+leftmov(T[1],j))%toolnum
        SS1=leftmov(mid1,7)#SS1
        SS2=(SS1^leftmov(A,12))%toolnum
        TT1=(FF(A,B,C,j)+D+SS2+B2[j])%toolnum
        TT2=(GG(E,F,G,j)+H+SS1+B1[j])%toolnum
        D=C
        C=leftmov(B,9)
        B=A
        A=TT1
        H=G
        G=leftmov(F,19)
        F=E
        E=P0(TT2)
    
    v_new=[]
    v_new.append(A^iv[0])
    v_new.append(B^iv[1])
    v_new.append(C^iv[2])
    v_new.append(D^iv[3])
    v_new.append(E^iv[4])
    v_new.append(F^iv[5])
    v_new.append(G^iv[6])
    v_new.append(H^iv[7])
    return v_new

def sm3(msg):
    mid1=msgpop(msg)
    n=len(mid1)
    temp_IV=IV
    for i in mid1:   
        if i !='':
            mid_IV=msgcut(temp_IV,8)
            temp_IV=msgexpd(mid_IV,i)
            final=""
            miwen=""
            for k in range(8):
                final+=bin(temp_IV[k]).replace('0b','').zfill(32)
            for j in range(64):
                mid_str=final[4*j:4+4*j]
                mid_num=int(mid_str,2)
                miwen+=hex(mid_num).replace('0x','')
            temp_IV=miwen
    out=""
    for a in range(64):
        out+=bin(int(temp_IV[a],16)).replace('0b','').zfill(4)
    out=(hex(int(out,2)))[2:]
    return out  


