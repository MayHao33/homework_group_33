#include<iostream>
#include<string>
#include<bitset>
#include<chrono>
using namespace std;

bitset<8> s_box[16][16] = {//s盒
	{0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76},
	{0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0},
	{0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15},
	{0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75},
	{0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84},
	{0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF},
	{0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8},
	{0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2},
	{0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73},
	{0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB},
	{0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79},
	{0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08},
	{0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A},
	{0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E},
	{0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF},
	{0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16}
};
bitset<32> r_con[10] = {//用于扩展密钥操作
						 0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000,
						 0x20000000, 0x40000000, 0x80000000, 0x1B000000, 0x36000000 };



bitset<8>mix_matrix[16] = { 0x02,0x03,0x01,0x01,
						 0x01,0x02,0x03,0x01,
						 0x01,0x01,0x02,0x03,
						 0x03,0x01,0x01,0x02 };

typedef bitset<8>byte;//字节
typedef bitset<32>word;//字

//扩展密钥

word rot_word(word x) {//循环左移
	return ((x >> (32 - 8)) | (x << 8));
}

word sub_word(word x) {
	word after_sub;
	for (int i = 0; i < 32; i += 8) {
		int column = x[i] + x[i + 1] * 2 + x[i + 2] * 4 + x[i + 3] * 8;
		int row = x[i + 4] + x[i + 5] * 2 + x[i + 6] * 4 + x[i + 7] * 8;
		for (int j = 0; j < 8; j++) {
			after_sub[i + j] = (byte(s_box[row][column]))[j];
		}
	}
	return after_sub;
}

void  key_expansion(byte key[16], word w[44]) {//扩展密钥
	for (int i = 0; i < 4; i++) {
		string temp;
		temp += key[4 * i].to_string() + key[4 * i + 1].to_string()
			+ key[4 * i + 2].to_string() + key[4 * i + 3].to_string();
		//cout<<temp<<endl;
		w[i] = word(temp);
		//cout << i<<" "<<w[i]<<" ";

	}
	for (int i = 4; i < 44; i++) {
		word temp = w[i - 1];
		if (i % 4 == 0) {
			temp = sub_word(rot_word(temp)) ^ r_con[i / 4 - 1];//从0开始
		}
		w[i] = w[i - 4] ^ temp;

		//cout <<i<<" "<<w[i]<<" ";
	}
}

//AES

void add_round_key(byte state[16], word key_round[4]) {
	for (int i = 0; i < 4; i++) {
		string key_temp = key_round[i].to_string();
		//每个字加密一列
		string key_round1, key_round2, key_round3, key_round4;
		for (int j = 0; j < 8; j++) {
			key_round1 += key_temp[j];
			key_round2 += key_temp[j + 8];
			key_round3 += key_temp[j + 16];
			key_round4 += key_temp[j + 24];
		}
		state[i] ^= byte(key_round1);
		state[i + 4] ^= byte(key_round2);
		state[i + 8] ^= byte(key_round3);
		state[i + 12] ^= byte(key_round4);
	}

}

void shift_row(byte state[16]) {//行移位
	//第二 三 四行一次左移一 二 三位
	//第二行
	byte temp = state[4];
	for (int i = 0; i < 3; i++) {
		state[i + 4] = state[i + 5];
	}
	state[7] = temp;
	//第三行
	swap(state[8], state[10]);
	swap(state[9], state[11]);
	//第四行
	temp = state[15];
	for (int i = 3; i > 0; i--) {
		state[i + 12] = state[i + 11];
	}
	state[12] = temp;

}

void sub_byte(byte state[16]) {
	for (int i = 0; i < 16; i++) {
		int column = state[i][0] + state[i][1] * 2 + state[i][2] * 4 + state[i][3] * 8;
		int row = state[i][4] + state[i][5] * 2 + state[i][6] * 4 + state[i][7] * 8;
		state[i] = s_box[row][column];
	}
}
byte multiply(byte a, byte b) {
	byte p = 0;
	byte bit_set;
	for (int counter = 0; counter < 8; counter++) {
		if ((b & byte(0x01)) != 0) {
			p ^= a;
		}
		bit_set = (byte)(a & byte(0x80));
		a <<= 1;
		if (bit_set != 0) {
			a ^= 0x1b;
		}
		b >>= 1;
	}
	return p;
}
void mix_column(byte state[16]) {//列混合
	byte matrix_column[4];
	for (int i = 0; i < 4; i++) {
		for (int j = 0; j < 4; j++) {
			matrix_column[j] = state[i + 4 * j];
		}
		state[i] = multiply(mix_matrix[0], matrix_column[0]) ^ multiply(mix_matrix[1], matrix_column[1])
			^ matrix_column[2] ^ matrix_column[3];
		state[i + 4] = multiply(mix_matrix[5], matrix_column[1]) ^ multiply(mix_matrix[6], matrix_column[2])
			^ matrix_column[0] ^ matrix_column[3];
		state[i + 8] = multiply(mix_matrix[10], matrix_column[2]) ^ multiply(mix_matrix[11], matrix_column[3])
			^ matrix_column[0] ^ matrix_column[1];
		state[i + 12] = multiply(mix_matrix[12], matrix_column[0]) ^ multiply(mix_matrix[15], matrix_column[3])
			^ matrix_column[1] ^ matrix_column[2];
	}
}

void encrypt(byte state[16], word w[44]) {
	word key[4];
	//1
	for (int i = 0; i < 4; i++) {
		key[i] = w[i];
	}
	add_round_key(state, key);
	//2-10
	for (int i = 1; i < 10; i++) {
		sub_byte(state);
		shift_row(state);
		mix_column(state);
		for (int j = 0; j < 4; j++) {
			key[j] = w[4 * i + j];
		}
		add_round_key(state, key);
	}
	//11
	sub_byte(state);
	shift_row(state);
	for (int i = 0; i < 4; i++) {
		key[i] = w[40 + i];
	}
	add_round_key(state, key);

	/*for (int i = 0; i < 16; i++) {
		if (i % 4 == 0) { cout << endl; }
		cout << state[i] << " ";
	}*/
}


int main() {

	string msg = "202100150027";
	byte ap[16];//bit后
	word w_a[44];
	auto total_duration = std::chrono::microseconds::zero();
	//cout << w_a;

	//bit
	for (int i = 0; i < 12; i++) {
		ap[i] = byte(msg[i]);

	}
	for (int i = 12; i < 16; i++) {
		ap[i] = 0x00;
	}

	//输出
	cout << "明文和密钥均分别为" << endl;
	//明文密钥一样
	for (int i = 0; i < 16; i++) {
		if (i % 4 == 0) { cout << endl; }
		cout << hex << ap[i].to_ulong() << "\t";
	}
	cout << endl;

	cout << endl << endl;

	//生成密钥字

	key_expansion(ap, w_a);

	//cout << w_b[0]<<endl;
	//for(int i=0;i<44;i++){cout << word(w_b[i])<<" "; }
	//cout << w_b;



	/*cout << "密钥字" << endl;
	for (int i = 0; i < 44; i++) {
		if (i % 4 == 0) { cout << endl; }
		cout << hex << w_a[i].to_ullong() << " ";
	}*/

	//加密
	auto start_time = std::chrono::steady_clock::now();//加密开始时间
	for (int i = 0; i < 10000; i++)
		encrypt(ap, w_a);
	auto end_time = std::chrono::steady_clock::now();        //加密结束时间
	auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
	total_duration += duration;
	cout << "密文为" << endl;


	for (int i = 0; i < 16; i++) {
		if (i % 4 == 0) { cout << endl; }
		cout << hex << ap[i].to_ulong() << "\t";
	}
	cout << endl;

	/*cout << bitset<8>(a[0]) << endl;
	byte val = s_box[1][1];
	cout << val<<endl;
	string n=byte(s_box[1][1]).to_string()+ bitset<8>(a[0]).to_string();
	cout << bitset<16>(n) << endl;
	cout << ((bitset<16>(n) << 5)>>5)<<endl;
	cout<< byte(n).to_ullong() << endl;
	cout << bitset<3>(byte(n).to_ullong());*/

	double total_time = total_duration.count() / 1000.0;
	cout << "一次加密时间:" << total_time / 10000 << "ms" << endl;
	return 0;
}