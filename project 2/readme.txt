project2：implement the Rho method of reduced SM3

项目说明：

SM3是中国密码标准算法，也是一种哈希算法，用于计算消息的摘要或者数字签名。SM3算法对长度为l(l<2^64)比特的消息m，SM3杂凑算法经过填充和迭代压缩，生成杂凑值，杂凑长度为256bit。

Rho方法是一种寻找碰撞的概率算法。该方法选择随机的起始点x_i和x_j,赋值为相同的初始值，并以不同方式计算其对应的哈希值，此后，不断迭代计算，并比较它们是否相等，直至找到碰撞。


代码运行说明：

下载sm3.py与Rho_method.py到同一目录，直接运行Rho_method.py即可。代码运行结果见result.png。


