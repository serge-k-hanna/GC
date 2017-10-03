#ifndef GF_H
#define GF_H

class GF
{
public:
	GF(int mlen, int lengthExtension);
	~GF();
	int numBlock;
	int blockLength;
	long gf;
	long gfMinus2;
	int mlen;
	long gfdiv(long den, long num);
	void toString();
private:
    /**
    Check if the input number is a prime number.

    @param num The input number.

    @return whether the input number is  a prime number.
    */
	bool isPrime(long num);
    /**
    Find the smallest prime number that is greater than the input number.

    @param num The input number.

    @return The next prime number.
    */
	long nextPrime(long num);
    /**
    Find the smallest prime number that is greater than the input number.

    @param num The input number.

    @return The next prime number.
    */
	void setDem(int lengthExtension);
    /**
     The input sequence will be divided  smaller blocks of sequences. This function calculates
     the block length and the number of blocks needed to contain the decoding sequence.

    @param lengthExtension blockLength = lengthExtension * log (mlen) .
    */
};

#endif // GF_H
