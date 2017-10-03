/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   Decoder.h
 * Author: hn
 *
 * Created on August 10, 2017, 12:55 PM
 */

#ifndef DECODER_H
#define DECODER_H
#include "Encoder.h"
#include <iostream>
using namespace std;

class Decoder: public Encoder{
public:
    Decoder(int mlen, int numDel, int numChecker, int lengthExtension);
    /**
     Recover the deleted sequence. The result will be stored back to s.

    @param s Reference to the deleted sequence.

    @param p The list of parity that comes with the sequence.
    */
    void decode(string &s,Vec<ZZ_p>p);
    /**
    A recursive function that loop through all guesses. As looping through each guess, it also maintains pprime
     decodes the guess. This call will return as soon as it sees the first decoding results that passes all the tests
     (parity checks).

    @param first The left bound of the index of the block containing deletions.
    @param last The right bound of the index of the block containing deletions.
    @param idx The order of deletion.
    @param pprime The right side of the system of equation to be solved in each guess.
    @param root Deletion indices (will think of a more accurate name).
    @param d A 2-D array of all possible block value (to avoid duplicated conversions between bin2zz).

    @return Whether a valid result has been found.
    */
    bool CaseGenFast_rec(long first, long last, long idx, Vec<ZZ_p> pprime, vector<long> root, vector<Vec<ZZ_p>> d);
    vector<Vec<ZZ_p>> baseCase(string s);
    /**
    One deletion solver. The result is stored in x (a class variable).

    @param pprime The right side of the equation.
    @param dels The index of the block whose value needs to be decoded.

    @return Whether a valid result has been found.
    */
    bool solveGC(Vec<ZZ_p> pprime, vector<long> dels);
    /**
    Multiple deletions solver. The result is stored in x (a class variable).

    @param pprime The right side of the equation.
    @param dels The indices of the blocks whose value needs to be decoded.

    @return Whether a valid result has been found.
    */
    bool solveGC(Vec<ZZ_p> pprime, long dels);
    /**
    Prints out all values of a vector.

    @param vec The vector
    @param name The display name.
    */
    void print(vector<long> vec, string name);
    Vec<ZZ_p> x;
    string* s;
    int numDel;
private:

};

#endif /* DECODER_H */

