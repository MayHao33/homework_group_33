project3：implement length extension attack for SM3, SHA256, etc.

项目说明：

SM3是中国密码标准算法，也是一种哈希算法，用于计算消息的摘要或者数字签名。SM3算法对长度为l(l<2^64)比特的消息m，SM3杂凑算法经过填充和迭代压缩，生成杂凑值，杂凑长度为256bit。

SHA256是由NIST设计的单向散列函数，散列值为256bit，消息长度上限接近于2^64bit。

长度扩展攻击（length extension attack)【1】,是指针对某些允许包含额外信息的加密散列函数的攻击手段。对于满足以下条件的散列函数，都可以作为攻击对象：
1.加密前将待加密的明文按一定规则填充到固定长度（例如512或1024bit）的倍数；
2.按照该固定长度，将明文分块加密，并用前一个块的加密结果，作为下一块加密的初始向量（IV）。

满足上述要求的散列函数称为Merkle–Damgard散列函数,简称为MD结构。SHA256是典型的MD结构,SM3的迭代过程与MD5类似，也是MD结构，但与MD5相比，SM3使用消息扩展得到的消息字进行运算，设计更加复杂。因此，SHA256与SM3均可进行长度扩展攻击。

长度扩展攻击的原理是：攻击者知道原始哈希值H和输入数据M，他可以通过构造一个新的数据块M'，然后计算出新的哈希值H'，满足H'=SHA-256(M'||P)，其中P是攻击者自己添加的任意数据。攻击者不需要知道M的具体内容，只需要知道M的长度即可进行攻击。

代码运行说明：

下载SM3_length_extension_attack.py文件后即可运行；
下载SHA256_length_extension_attack.py文件后即可运行。
SM3长度扩展攻击代码运行结果见SM3_result.png，SHA256长度扩展攻击代码运行结果见SHA256_result.png。

参考文献：
【1】https://blog.csdn.net/szuaurora/article/details/78125585

