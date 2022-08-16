#!/usr/bin/env python3
from  sys import argv


def main():
	if "-f" in argv:
		filename = input("Enter filename: ")
		bits = file2bit(filename)
		bits = padding(bits)
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
		new_bits = unpadding(new_bits)
		bit2file(new_bits)
		print("\nDecoded data of your codes in \"DataFile\"")
	else:
		text = input("Enter your text: ")
		bits = txt2bit(text)
		print(f"\nBits of your text before padding:\n{bits}")
		bits = padding(bits)
		print(f"\nBits of your text after padding:\n{bits}")
		codes = encode(bits)
		print(f"\nCodes of your text:\n{codes}\n")
		codes = input("Enter received codes: ")
		new_bits = decode(codes)
		print(f"\nBits of your text after unpadding:\n{new_bits}")
		new_bits = unpadding(new_bits)
		print(f"\nBits of your text before unpadding:\n{new_bits}")
		new_text = bit2txt(new_bits)
		print(f"\nDecoded text of your codes: \"{new_text}\"")


def txt2bit(text: str) -> str:
	b = ""
	for c in text:
		bit = bin(ord(c))[2:]
		b += "0" * (8 - len(bit)) + bit
		print(f"\n{c} ->", "0" * (8 - len(bit)) + bit )
	return b


def bit2txt(bits: str) -> str:
	text = ""
	for i in range(len(bits) // 8):
		text += chr(int(bits[i * 8: (i + 1) * 8], 2))
	return text


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


def padding(bits: str) -> str:
	if len(bits) % 7 != 0:
		n = 7 - len(bits) % 7
		byte = "0" * (7 - len(bin(n)[2:])) + bin(n)[2:]
		bits += "0" * n + byte
	return bits


def unpadding(bits: str) -> str:
	n = int(bits[-7:], 2)
	return bits[:-7 - n]


def encode(bits: str) -> str:
	new_bits = ""
	for i in range(len(bits) // 7):
		info = bits[i * 7: (i + 1) * 7] + "0" * 8		
		check = div(info, "111010001")
		
		if "-f" not in argv:
			print(f"\n{info[:-8]}:")
			print(f"{info} div 111010001 == {check}\n{info} xor {check} == ", end="")
		
		info = xor(info, check)
		
		if "-f" not in argv:
			print(info)
		
		new_bits += info + "."
	return new_bits[:-1]


def decode(codes: str) -> str:
	new_codes = ""
	for code in codes.split("."):
		if "1" in div(code, "111010001"):
			
			if "-f" not in argv:
				print()

			for i in range(len(code)):
				R = div(code, "111010001")

				if "-f" not in argv:
					print("\t" * i + f"{code} div 111010001 == {R} (" + str(R.count("1")) + ")" )

				if R.count("1") <= 2:
					
					if "-f" not in argv:
						print("\t" * i + f"{code} xor {R} == ", end="")

					code = xor(code, R)
					
					if "-f" not in argv:
						print(code)

					for j in range(i):
						code = code[-1] + code[:-1]
						
						if "-f" not in argv:
							print("\t" * (i - j - 1) + code)

					break
				else:
					code = code[1:] + code[0]

		else:
			if "-f" not in argv:
				d = div(code, "111010001")
				print(f"\n{code} div 111010001 == 000000000000000")
		
		new_codes += code[:7]
	return new_codes


def div(data: str, px: str) -> str:
	pxcmp = "1"+"0"*(len(px)-1)
	while int(data, 2) >= int(pxcmp, 2):
		#print(f"{data}({int(data, 2)}) > {pxcmp}({int(pxcmp, 2)})")
		i = len(px)
		while int(data[:i], 2) < int(pxcmp, 2):
			#print(f":{data[:i]}", int(data[:i], 2))
			i += 1
		#print(f":{data[:i]}", int(data[:i], 2))
		res = xor("0" * (len(data[:i]) - len(px)) + px, data[:i])
		#print("\t", "0" * (len(data[:i]) - len(px)) + px, data[:i], res)
		data = res + data[i:]
	return data


def xor(a: str, b:str):
	return "".join([str((int(a[i]) + int(b[i])) % 2) for i in range(len(a))])


if __name__ == '__main__':
	main()