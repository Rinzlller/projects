#!/usr/bin/env python3

from sys import argv
from time import time

'''
AES Encryption with 128-bit key
'''


SBox = [
	[99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118],
	[202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192],
	[183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21],
	[4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117],
	[9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132],
	[83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207],
	[208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168],
	[81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210],
	[205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115],
	[96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219],
	[224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121],
	[231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8],
	[186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138],
	[112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158],
	[225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223],
	[140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]
]

RevSBox = [
	[82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251],
	[124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203],
	[84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78],
	[8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37],
	[114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146],
	[108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132],
	[144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6],
	[208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107],
	[58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115],
	[150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110],
	[71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27],
	[252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244],
	[31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95],
	[96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239],
	[160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97],
	[23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125]
]

CirMatrix = [2, 3, 1, 1, 1, 2, 3, 1, 1, 1, 2, 3, 3, 1, 1, 2]

RevCirMatrix = [14, 11, 13, 9, 9, 14, 11, 13, 13, 9, 14, 11, 11, 13, 9, 14]

RCon = [1, 2, 4, 8, 16, 32, 64, 128, 27, 54]

a = [int("2b", 16), int("28", 16), int("ab", 16), int("09", 16), int("7e", 16), int("ae", 16), int("f7", 16), int("cf", 16), int("15", 16), int("d2", 16), int("15", 16), int("4f", 16), int("16", 16), int("a6", 16), int("88", 16), int("3c", 16)]
b = [int("32", 16), int("88", 16), int("31", 16), int("e0", 16), int("43", 16), int("5a", 16), int("31", 16), int("37", 16), int("f6", 16), int("30", 16), int("98", 16), int("07", 16), int("a8", 16), int("8d", 16), int("a2", 16), int("34", 16)]


def main():
	if "-d" in argv:
		CipherBlocks = ReadFile()
		KeyBlock = ReadKey()
		Mode, VectorBlock = SelectMode()
		PlaintextBlocks = Decryption(CipherBlocks, KeyBlock, Mode, VectorBlock)
	
		print("\nDecrypted Blocks:\n")
		write( PlaintextBlocks )
		WriteFile(PlaintextBlocks)
	
	else:
		PlaintextBlocks = ReadFile() #Two One Nine Two
		KeyBlock = ReadKey() #Thats my Kung Fu
		Mode, VectorBlock = SelectMode()

		time_1 = time()
		CipherBlocks = Encryption(PlaintextBlocks, KeyBlock, Mode, VectorBlock)
		time_2 = time()

		print(f"Time of encryption:{time_2 - time_1}")
		
		#print("\nEncrypted Blocks:\n")
		#write( CipherBlocks )
		#WriteFile(CipherBlocks)


def SelectMode():
	if "-cbc" in argv:
		Mode = "cbc"
	elif "-pcbc" in argv:
		Mode = "pcbc"
	elif "-cfb" in argv:
		Mode = "cfb"
	elif "-ofb" in argv:
		Mode = "ofb"
	else:
		return "ecb", None
	return Mode, ReadVector()


def txt2mx(text: str) -> list:
	massiv = [byte for byte in text.encode()]
	matrix = [[0] * 16 for _ in range((len(massiv) + 15) // 16)]
	for i in range((len(massiv) + 15) // 16):
		for j in range(16):
			if(i * 16 + j < len(massiv)):
				matrix[i][(j * 4) % 16 + j // 4] = massiv[i * 16 + j]
			else:
				matrix[i][(j * 4) % 16 + j // 4] = 16 - len(massiv) % 16
	return matrix


def file2mx(filename: str) -> list:
	file = open(filename, "rb")
	Bytes = file.read()
	file.close()
	massiv = [byte for byte in Bytes]
	matrix = [[0] * 16 for _ in range((len(massiv) + 15) // 16)]
	for i in range((len(massiv) + 15) // 16):
		for j in range(16):
			if(i * 16 + j < len(massiv)):
				matrix[i][(j * 4) % 16 + j // 4] = massiv[i * 16 + j]
			else:
				matrix[i][(j * 4) % 16 + j // 4] = 16 - len(massiv) % 16
	return matrix


def mx2txt(matrix: list):
	result = ""
	for massiv in matrix:
		text = "".join([chr(massiv[(i * 4) % 16 + i // 4]) for i in range(16)])
		if ord(text[15]) <= 16:
			if text[16 - ord(text[15]):16] == ord(text[15]) * text[15]:
				result += text[:16 - ord(text[15])]
		else:
			result += text
	return result


def mx2file(matrix: list, filename: str):
	file = open(filename, "wb")
	for massiv in matrix:
		order = [massiv[(i * 4) % 16 + i // 4] for i in range(16)]
		if order[15] <= 16 and order == matrix[len(matrix) - 1]:
			if order[16 - order[15]:16] == [order[15]] * order[15]:
				order = order[:16 - order[15]]
		order = bytes(order)
		file.write(order)
	file.close()


def ReadText() -> list:
	Text = input("Enter the text: ")
	TextBlocks = txt2mx(Text)
	print("\nTextBlocks:")
	write( TextBlocks )
	return TextBlocks


def ReadFile() -> list:
	filename = input("\nEnter the filename: ")
	DataBlocks = file2mx(filename)
	print("\nDataBlocks:\n")
	write( DataBlocks )
	return DataBlocks


def WriteBlocks( Blocks: list ):
	text = mx2txt(Blocks)
	print( f"Text: \"{text}\"" )


def WriteFile( Blocks: list ):
	filename = input("\nEnter the filename: ")
	mx2file(Blocks, filename)
	print( f"Your data in the \"{filename}\"" )


def ReadKey() -> list: #add key check
	Key = input("\nEnter the 128-bit Key: ")
	KeyBlock = txt2mx(Key)[0]
	print("\nKeyBlock:\n")
	write( [KeyBlock] )
	print()
	return KeyBlock


def ReadVector() -> list: #add vector check
	Vector = input("\nEnter the 128-bit Vector: ")
	VectorBlock = txt2mx(Vector)[0]
	print("\nVectorBlock:\n")
	write( [VectorBlock] )
	print()
	return VectorBlock


def Encryption(DataBlocks: list, KeyBlock: list, Mode = None, VectorBlock = None):
	RoundKeys = KeySchedule(KeyBlock)
	if "-v" in argv:
		print("\n"+8*"+"+" KeySchedule "+8*"+", end="\n\n")
		write(RoundKeys)

	CiphertextBlocks = []
	if Mode == "cbc":
		for DataBlock in DataBlocks:
			EncBlock = xor(DataBlock, VectorBlock)
			EncBlock = AESenc(EncBlock, RoundKeys)
			CiphertextBlocks.append(EncBlock)
			VectorBlock = EncBlock

	elif Mode == "pcbc":
		for DataBlock in DataBlocks:
			EncBlock = xor(DataBlock, VectorBlock)
			EncBlock = AESenc(EncBlock, RoundKeys)
			CiphertextBlocks.append(EncBlock)
			VectorBlock = xor(DataBlock, EncBlock)

	elif Mode == "cfb":
		for DataBlock in DataBlocks:
			EncBlock = AESenc(VectorBlock, RoundKeys)
			VectorBlock = xor(DataBlock, EncBlock)
			CiphertextBlocks.append(VectorBlock)

	elif Mode == "ofb":
		for DataBlock in DataBlocks:
			VectorBlock = AESenc(VectorBlock, RoundKeys)
			EncBlock = xor(DataBlock, VectorBlock)
			CiphertextBlocks.append(EncBlock)

	else:
		for DataBlock in DataBlocks:
			CiphertextBlocks.append(AESenc(DataBlock, RoundKeys))
	
	return CiphertextBlocks


def Decryption(DataBlocks: list, KeyBlock: list, Mode = None, VectorBlock = None):
	RoundKeys = KeySchedule(KeyBlock)
	PlaintextBlocks = []
	if Mode == "cbc":
		for DataBlock in DataBlocks:
			DecBlock = AESdec(DataBlock, RoundKeys)
			DecBlock = xor(DecBlock, VectorBlock)
			PlaintextBlocks.append(DecBlock)
			VectorBlock = DataBlock

	elif Mode == "pcbc":
		for DataBlock in DataBlocks:
			DecBlock = AESdec(DataBlock, RoundKeys)
			DecBlock = xor(DecBlock, VectorBlock)
			PlaintextBlocks.append(DecBlock)
			VectorBlock = xor(DecBlock, DataBlock)

	elif Mode == "cfb":
		for DataBlock in DataBlocks:
			DecBlock = AESenc(VectorBlock, RoundKeys)
			DecBlock = xor(DecBlock, DataBlock)
			PlaintextBlocks.append(DecBlock)
			VectorBlock = DataBlock

	elif Mode == "ofb":
		for DataBlock in DataBlocks:
			VectorBlock = AESenc(VectorBlock, RoundKeys)
			DecBlock = xor(VectorBlock, DataBlock)
			PlaintextBlocks.append(DecBlock)

	else:
		for DataBlock in DataBlocks:
			PlaintextBlocks.append(AESdec(DataBlock, RoundKeys))

	
	return PlaintextBlocks


def AESenc(DataBlock: list, RoundKeys: list):
	DataBlock = AddRoundKey(DataBlock, RoundKeys[0])
	
	if "-v" in argv:
		print("\n"+8*"-"+" Encryption "+8*"-", end="\n")
		print("\nAdding a key of [0] round:\n")
		write([DataBlock])

	for i in range(1, 10):
		if "-v" in argv:
			print("\n"+4*"<"+f" Round [{i}] "+4*">", end="\n")
		
		DataBlock = SubBytes(DataBlock, SBox)
		
		if "-v" in argv:
			print("\nSubBytes:\n")
			write([DataBlock])

		DataBlock = ShiftRows(DataBlock)
		
		if "-v" in argv:
			print("\nShiftRows:\n")
			write([DataBlock])

		DataBlock = MixColumns(DataBlock, CirMatrix)
		
		if "-v" in argv:
			print("\nMixColumns:\n")
			write([DataBlock])

		DataBlock = AddRoundKey(DataBlock, RoundKeys[i])
		
		if "-v" in argv:
			print(f"\nAdding a key of [{i}] round:\n")
			write([DataBlock])

	if "-v" in argv:
		print("\n"+4*"<"+f" Round [10] "+4*">", end="\n")
	
	DataBlock = SubBytes(DataBlock, SBox)
	
	if "-v" in argv:
		print("\nSubBytes:\n")
		write([DataBlock])

	DataBlock = ShiftRows(DataBlock)
	
	if "-v" in argv:
		print("\nShiftRows:\n")
		write([DataBlock])

	DataBlock = AddRoundKey(DataBlock, RoundKeys[10])
	
	if "-v" in argv:
		print(f"\nAdding a key of [10] round:\n")
		write([DataBlock])

	return DataBlock

def AESdec(DataBlock: list, RoundKeys: list):
	DataBlock = AddRoundKey(DataBlock, RoundKeys[10])
	DataBlock = RevShiftRows(DataBlock)
	DataBlock = SubBytes(DataBlock, RevSBox)

	for i in range(1, 10)[::-1]:
		DataBlock = AddRoundKey(DataBlock, RoundKeys[i])
		DataBlock = MixColumns(DataBlock, RevCirMatrix)
		DataBlock = RevShiftRows(DataBlock)
		DataBlock = SubBytes(DataBlock, RevSBox)

	DataBlock = AddRoundKey(DataBlock, RoundKeys[0])

	return DataBlock

def xor(a: list, b: list) -> list:
	c = [a[i]^b[i] for i in range(len(a))]
	return c


def AddRoundKey(Block: list, RoundKey: list) -> list:
	return xor(Block, RoundKey)


def SubBytes(Block: list, SBox: list) -> list:
	return [SBox[byte // 16][byte % 16] for byte in Block]


def rotate(Block: list, StrNumber: int) -> list:
	buff = Block[StrNumber * 4]
	for i in range(StrNumber * 4, (StrNumber + 1) * 4 - 1):
		Block[i] = Block[i + 1]
	Block[(StrNumber + 1) * 4 - 1] = buff
	return Block


def ShiftRows(Block: list) -> list:
	for i in range(4):
		for j in range(i):
			Block = rotate(Block, i)
	return Block


def RevShiftRows(Block: list) -> list:
	for i in range(1, 4):
		for j in range(4 - i):
			Block = rotate(Block, i)
	return Block


def x2(a: int) -> int:
	a *= 2
	if a >= 256:
		a = (a - 256) ^ 27
	return a


def x3(a: int) -> int:
	a = a ^ x2(a)
	return a


def x9(a: int) -> int:
	a = a ^ x2(x2(x2(a)))
	return a


def x11(a: int) -> int:
	a = a ^ x2(a ^ x2(x2(a)))
	return a


def x13(a: int) -> int:
	a = a ^ x2(x2(a ^ x2(a)))
	return a


def x14(a: int) -> int:
	a = x2(a ^ x2(a ^ x2(a)))
	return a


def MixColumns(Block: list, MixMatrix: list) -> list:
	NewBlock = [0] * 16
	for i in range(4):
		for s in range(4):
			buff = 0
			for j in range(4):
				if MixMatrix[s * 4 + j] == 1: buff ^= Block[j * 4 + i]
				if MixMatrix[s * 4 + j] == 2: buff ^= x2(Block[j * 4 + i])
				if MixMatrix[s * 4 + j] == 3: buff ^= x3(Block[j * 4 + i])
				if MixMatrix[s * 4 + j] == 9: buff ^= x9(Block[j * 4 + i])
				if MixMatrix[s * 4 + j] == 11: buff ^= x11(Block[j * 4 + i])
				if MixMatrix[s * 4 + j] == 13: buff ^= x13(Block[j * 4 + i])
				if MixMatrix[s * 4 + j] == 14: buff ^= x14(Block[j * 4 + i])
			NewBlock[s * 4 + i] = buff
	return NewBlock


def KeySchedule(Block: list) -> list:
	Blocks = [Block]
	for n in range(0, 10):
		FirstColumn = [Blocks[n][i*4+3] for i in range(1,4)]
		FirstColumn.append(Blocks[n][3])
		FirstColumn = SubBytes(FirstColumn, SBox)
		FirstColumn = [FirstColumn[i]^Blocks[n][i*4] for i in range(4)]
		FirstColumn[0] ^= RCon[n]
		SecondColumn = [FirstColumn[i]^Blocks[n][i*4+1] for i in range(4)]
		ThirdColumn = [SecondColumn[i]^Blocks[n][i*4+2] for i in range(4)]
		FourthColumn = [ThirdColumn[i]^Blocks[n][i*4+3] for i in range(4)]
		NewBlock = []
		for i in range(4):
			NewBlock.append(FirstColumn[i])
			NewBlock.append(SecondColumn[i])
			NewBlock.append(ThirdColumn[i])
			NewBlock.append(FourthColumn[i])
		Blocks.append(NewBlock)
	return Blocks


def write(Blocks: list):
	Ntabs = 3
	rows = [""] * 4
	for Block in Blocks:
		for i in range(4):
			for j in range(4):
				HEX = hex(Block[i * 4 + j])[2:]
				rows[i] += "0"*(2-len(HEX))+HEX+" "
			rows[i] += " "*Ntabs
	for row in rows:
		print(row)


if __name__ == '__main__':
	main()