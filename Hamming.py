#!/usr/bin/env python3
from  sys import argv

SBox = [2, 4, 5, 6, 8, 9, 10, 11]


def main():
	if "-f" in argv:
		filename = input("Enter filename: ")
		bits = file2bit(filename)
		codes = encode(bits)
		file = open("CodesFile.txt", 'w')
		file.write(codes)
		file.close()
		print(f"\nCodes of your data in \"CodesFile.txt\"")
		filename = input("Enter filename with received codes: ")
		file = open(filename, 'r')
		new_codes = file.read()
		file.close()
		new_bits = decode(new_codes)
		bit2file(new_bits)
		print("\nDecoded data of your codes in \"DataFile\"")
	else:
		text = input("Enter your text: ")
		bits = txt2bit(text)
		print(f"\nBits of your text:\n{bits}")
		codes = encode(bits)
		print(f"\nCodes of your text:\n{codes}\n")
		codes = input("Enter received codes: ")
		new_bits = decode(codes)
		new_text = bit2txt(new_bits)
		print(f"\nDecoded text of your codes: \"{new_text}\"")


def txt2bit(text: str) -> str:
	b = ""
	for c in text:
		bit = bin(ord(c))[2:]
		print(f"\n{c} ->", "0" * (8 - len(bit)) + bit )
		b += "0" * (8 - len(bit)) + bit 
	return b


def file2bit(filename: str) -> str:
	f = None
	try: 
		f = open(filename, 'rb')
		inside = f.read()
	finally: 
	 	if f is not None: 
	 		f.close()
	b = ""
	for byte in inside:
		bit = bin(byte)[2:]
		b += "0" * (8 - len(bit)) + bit
	return b



def bit2file(bits: str):
	inside = []
	for i in range(len(bits) // 8 - 1):
		inside.append(int(bits[i * 8: (i + 1) * 8], 2))
	inside = bytes(inside)
	f = None
	try: 
		f = open("DataFile", 'wb')
		f.write(inside)
	finally: 
		if f is not None: 
	 		f.close()


def bit2txt(bits: str) -> str:
	text = ""
	for i in range(len(bits) // 8):
		text += chr(int(bits[i * 8: (i + 1) * 8], 2))
	return text


def encode(bits: str) -> str:
	new_bits = ""
	if len(bits) % 8:
		bits += "0" * (8 - len(bits) % 8)
	for n in range(len(bits) // 8):
		b = bits[n * 8:(n + 1) * 8]
		word = [b[i] for i in range(8)]
		code = [0] * 12

		if "-f" not in argv:
			print("\n" + b + ":")
			print("\t" + 12 * "_", "-> ", end="")
			printcode = ""
			k = 0
			for i in range(12):
				if i in SBox:
					printcode += str(word[k])
					k += 1
				else:
					printcode += "_"
			print(printcode, "-> ", end="")

		for i in range(8):
			code[SBox[i]] = word[i]

		buff = 0
		for i in [0, 2, 4, 6, 8, 10]:
			buff ^= int(code[i])
		code[0] = str(buff)

		buff = 0
		for i in [1, 2, 5, 6, 9, 10]:
			buff ^= int(code[i])
		code[1] = str(buff)

		buff = 0
		for i in [3, 4, 5, 6, 11]:
			buff ^= int(code[i])
		code[3] = str(buff)

		buff = 0
		for i in [7, 8, 9, 10, 11]:
			buff ^= int(code[i])
		code[7] = str(buff)

		if "-f" not in argv:
			print("".join(code))
		
		new_bits += "".join(code) + "."
	return new_bits[:-1]


def decode(codes: str) -> str:
	bits = ""
	for b in codes.split("."):

		if "-f" not in argv:
			print(f"\n{b}:")

		b1 = int(b[0]) ^ int(b[2]) ^ int(b[4]) ^ int(b[6]) ^ int(b[8]) ^ int(b[10])
		b2 = int(b[1]) ^ int(b[2]) ^ int(b[5]) ^ int(b[6]) ^ int(b[9]) ^ int(b[10])
		b4 = int(b[3]) ^ int(b[4]) ^ int(b[5]) ^ int(b[6]) ^ int(b[11])
		b8 = int(b[7]) ^ int(b[8]) ^ int(b[9]) ^ int(b[10]) ^ int(b[11])

		num = b1 * 1 + b2 * 2 + b4 * 4 + b8 * 8

		if "-f" not in argv:
			print(f"1({b1}), 2({b2}), 4({b4}), 8({b8}) => {num}")
			print(f"{b} -> ", end="")

		if num and num < 12:
			b = [c for c in b]
			b[num - 1] = str(int(b[num - 1]) ^ 1)
			b = "".join(b)

		if "-f" not in argv:
			print(b)

		bits += "".join([b[i] for i in SBox])
	return bits


if __name__ == '__main__':
	main()