#include "GF.h"
#include <iostream>
#include <math.h>       /* log */
#include <string>
#include <NTL/ZZ_p.h>
using namespace std;
using namespace NTL;


GF::GF(int mlen, int lengthExtension = 1)
{
	this->mlen = mlen;
	setDem(lengthExtension); //set numBlock and blockLength
	this->gf = nextPrime(pow(2, blockLength));
    ZZ_p::init(ZZ(gf));
	this->gfMinus2 = gf - 2;
}

GF::~GF()
{
}

long GF::gfdiv(long den, long num = 1)
{
	long temp = 1;
	for (long i = 0; i < gfMinus2; i++)
	{
		temp = (temp*den) % gf;
	}
	long inv = temp;
	if (inv<0)
		inv += gf;
	if (num == 1)
		return inv;
	else
		return (num*inv) % gf;
}

void GF::toString()
{
	cout << "numBlock: " + to_string(numBlock)
		+ " - blockLength: " + to_string(blockLength)
		+ " - mlen: " + to_string(mlen)
		+ " - gf: " + to_string(gf)+"\n";
}

bool GF::isPrime(long num)
{
	if (num < 2)
		return false;
	long max = sqrt(num) + 1;
	for (long i = 2; i < max; i++)
	{
		if (num % i == 0)
			return false;
	}
	return true;
}

long GF::nextPrime(long num)
{
	while (!isPrime(num))
	{
		num++;
	}
	return num;
}

void GF::setDem(int lengthExtension = 1)
{
	if (lengthExtension <= 0)
		throw "Negative length extension.";
	blockLength = lengthExtension*ceil(log2(mlen));
	if (blockLength > mlen)
		throw "Block too long.";
	numBlock = ceil(mlen / blockLength);
}