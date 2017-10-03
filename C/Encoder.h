#ifndef ENCODER_H
#define ENCODER_H

#include "GF.h"
#include <NTL/mat_ZZ_p.h>
#include <vector>
using namespace NTL;
using namespace std;

class Encoder: public GF
{
public:
    Encoder(int mlen, int numVec, int lengthExtension = 1);
    ~Encoder();
    int numVec;
    Mat<ZZ_p> enVec;

    /**
    Set encoding/decoding matrix (Hilbert Matrix, a special case of Cauchy Matrix, was used by default)

    @param numVec The number of columns of the matrix, which is equal to number of decoding parity + number of checker parity.
    */
    void setEnVec(int numVec);
    /**
    Print to screen the specifications of the encoder.
    */
    void toString();
    /**
    Returns a list of parities (done in sender's side).

    @param data A list of integers representing the original binary sequence.

    @return A list of parities.
    */
    Vec<ZZ_p> paritize(Vec<ZZ_p> data);
    /**
    Returns a list of parities (done in sender's side).

    @param s The original binary sequence.

    @return A list of parities.
    */
    Vec<ZZ_p> paritize(string s);
    /**
    Converts a list of binary strings to integers (NTL ZZ_p).

    @param v A list of binary strings.

    @return A list of integers (NTL ZZ_p.
    */
    Vec<ZZ_p> bin2zz(vector<string> v);
    /**
    Converts a number to a binary string.

    @param zz A number.

    @param size The bit length of the output binary string.

    @return A binary string represents the input number.
    */
    string zz2bin(ZZ_p zz, int size);
    /**
    Converts a number to a binary string.

    @param n A number.

    @param size The bit length of the output binary string.

    @return A binary string represents the input number.
    */
    string zz2bin(long n, int size);
    /**
    Converts a list numbers to a list binary strings.

    @param vec A list of numbers.

    @param size The bit length of the output binary strings.

    @return A list binary strings represents the input numbers.
    */
    vector<string> zz2bin(Vec<ZZ_p> vec, int size);
    /**
    Converts a list numbers to a list binary string.

    @param vec A list of numbers.

    @param size The list of corresponding bit lengths of the output binary strings.

    @return A list binary strings represents the input numbers.
    */
    vector<string> zz2bin(Vec<ZZ_p> vec, vector<int> size);
    /**
    Break a long binary string into blocks of smaller binary strings
    with each block has the length of blocklength - number of deletion in that block.

    @param s The full string.

    @param dels The list block indices where a bit is deleted.

    @return A list sub binary strings broken from the input binary string.
    */
    vector<string> breakString(string s, vector<long> dels = vector<long>());
    /**
    Generate a random binary string of size mlen. mlen should is a multiple of 16 bits.

    @return A random binary string sized mlen (a class variable).
    */
    string randBin();
    /**
    Delete one bit from string s at index idx.

    @param s The binary string.

    @param idx The index of the deleted bit.

    @return A copy of string s with the bit at idx deleted.
    */
    string erase(string s, long idx);
    /**
    Delete several bits from string s.

    @param s The binary string.

    @param idxs The list of indices of the deletions.

    @return A copy of string s with several bits deleted.
    */
    string erase(string s, vector<long> idxs);
};


#endif // ENCODER_H
