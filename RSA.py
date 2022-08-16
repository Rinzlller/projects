from random import randint

hard = 16

def main():

	print()

	text = "Hello world!"
	print( f"Text is:\n{text}\n" )

	message = text_to_nums( text )
	print( "Message is:" )
	print( *message, end="\n\n" )

	n, e, d, encrypt_message = RSA_encrypt( hard, message )

	print( f"Public key is (N, E):" )
	print( f"N = {n}" )
	print( f"E = {e}\n" )

	print( f"Private key is (N, D)" )
	print( f"N = {n}" )
	print( f"D = {d}\n" )

	print( f"Encrypt message is:" )
	print( *encrypt_message, end="\n\n" )

	decryption = RSA_decrypt( n, d, encrypt_message )
	print( "Decryption is:" )
	print( *decryption, end="\n\n" )

	received_text = nums_to_text( decryption )
	print( f"Received text is:\n{received_text}\n" )

def RSA_encrypt( hard: int, message ):

	p = Prime_number( hard, 1 )
	#print( f"p = {p}" )

	q = Prime_number( hard, p )
	#print( f"q = {q}" )

	n = p * q
	#print( f"N = {n}" )

	f = (p - 1) * (q - 1)
	
	e = Prime_number( hard, f )
	#print( f"E = {e}" )

	d = Euklid( f, e )
	#print( f"d = {d}" )

	cihpertext = []

	for num in message:
		cihpertext.append( pow( num, e, n ) )

	return n, e, d, cihpertext
	

def text_to_nums( text ):

	nums = []

	for letter in text:
		nums.append(ord(letter))
	"""
	for i in nums:
		print( i, end=" " )
	"""
	return nums


def nums_to_text( nums ):

	text = ""

	for num in nums:
		text += chr(num)
	
	return text


def RSA_decrypt( n: int, d: int, cihpertext ):

	decryption = []

	for num in cihpertext:
		decryption.append( pow( num, d, n ) )
	
	return decryption


def Prime_number( n: int, ex: int ) -> int:
	
	l = pow( 10, n - 1 ) + 2
	#print( f"l = {l}" )
	r = pow( 10, n ) - 4
	#print( f"r = {r}" )

	x = l + 6 * randint( 0, (r - l) / 6 )
	#print( f"x = {x}" )

	while True:

		is_prime = True

		for i in x - 1, x + 1:

			#print( f"i = {i}" )

			if pow( 2, i - 1, i ) != 1:
				is_prime = False

			if is_prime:
				if ex % i != 0:
					return i

		x += 6
		if x > r: x = l


def Euklid( a: int, b: int ):
	
	act, old = 0, 1

	a0 = a
	b0 = b

	while ((a != 0) and (b != 0)):
		
		if a > b:
			q = a // b
			a %= b
		else:
			q = b // a
			b %= a
		
		if ((a != 0) and (b != 0)):
			new = old - q * act
			old = act
			act = new

	nod = a + b
	k = (nod - new * a0) // b0

	if k < 0:
		k += a0

	return k


def Crypt( mes: int, x: int, module: int ):
	return pow( mes, x, module )


if __name__ == '__main__':
	main()	