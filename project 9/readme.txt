project9： AES / SM4 software implementation

项目说明：

高级加密标准【1】（AES），是美国联邦政府采用的一种区块加密标准。大多数AES计算是在一个特别的有限域完成的。

AES加密过程是在一个4×4的字节矩阵上运作，其初值就是一个明文区块（矩阵中一个元素大小就是明文区块中的一个Byte）。加密时，各轮AES加密循环（除最后一轮外）均包含4个步骤：

1.AddRoundKey—矩阵中的每一个字节都与该次回合密钥（round key）做XOR运算；每个子密钥由密钥生成方案产生。
2.SubBytes—透过一个非线性的替换函数，用查找表的方式把每个字节替换成对应的字节。
3.ShiftRows—将矩阵中的每个横列进行循环式移位。
4.MixColumns—为了充分混合矩阵中各个直行的操作。这个步骤使用线性转换来混合每内联的四个字节。最后一个加密循环中省略MixColumns步骤，而以另一个AddRoundKey取代。

SM4是一种分组密码算法【2】，由我国国家密码管理局在2012年发布，常用于无线互联网加密等领域。其分组长度为128位（即16字节，4字），密钥长度也为128位（即16字节，4字）。其加解密过程采用了32轮迭代机制（与DES、AES类似），每一轮需要一个轮密钥（与DES、AES类似）。


代码运行说明：

下载AES_cpp在Visual Studio中打开作为源.cpp即可运行。
下载SM4.py即可运行。
AES加密算法运行结果见AES_result.png，SM4加密算法运行结果见SM4_result.png。

参考文献：
【1】https://zh.wikipedia.org/wiki/%E9%AB%98%E7%BA%A7%E5%8A%A0%E5%AF%86%E6%A0%87%E5%87%86
【2】https://zhuanlan.zhihu.com/p/363900323

