#include "Encoder.h"
#include <NTL/mat_ZZ_p.h>
#include <iostream>
using namespace std;

Encoder::Encoder(int mlen, int numVec, int lengthExtension):GF(mlen, lengthExtension){
    this->numVec=numVec;
    setEnVec(numVec);
}
Encoder::~Encoder(){
}
void Encoder:: setEnVec(int numVec){
    enVec.SetDims(numBlock,numVec);
    for(int m = 1; m <= enVec.NumRows(); m++){
        for(int n = 1; n <= enVec.NumCols(); n++){
           enVec(m)(n) = ZZ_p(1)/ZZ_p((m+n-1));
        }
    }
}
void Encoder::toString(){
    GF::toString();
    cout << "EnVec: \n";
	cout << enVec;
}
Vec<ZZ_p> Encoder::paritize(Vec<ZZ_p> data){
    return data*enVec;
}
Vec<ZZ_p> Encoder::paritize(string s){
    return paritize(bin2zz(breakString(s)));
}
Vec<ZZ_p> Encoder::bin2zz(vector<string> binVec){
    Vec<ZZ_p> zzVec;
    zzVec.SetLength(binVec.size());
    for(long i = 0; i<binVec.size(); i++){
        zzVec[i] = stol(binVec[i],0,2);
        }
    return zzVec;
}
string Encoder::zz2bin(ZZ_p zz, int size){
    return zz2bin(conv<long>(zz), size);
}
string Encoder::zz2bin(long n, int size){
    string s = "";
    int count = 0;
    while (n > 0) {
        s = to_string(n % 2) + s;
        count++;
        n /= 2;
    }
    int remain = size - count;
    for (int i = 0; i < remain; i++) {
        s = "0" + s;
    }
    return s;
}
vector<string> Encoder::zz2bin(Vec<ZZ_p> vec, int size){
    vector<string> ret(vec.length());
    for (int i = 0; i < vec.length(); i++) {
        ret[i]=zz2bin(vec[i],size);
    }
    return ret;
}
vector<string> Encoder::zz2bin(Vec<ZZ_p> vec, vector<int> size){
    vector<string> ret(vec.length());
    for (int i = 0; i < vec.length(); i++) {
        ret[i]=zz2bin(vec[i],size[i]);
    }
    return ret;
}
vector<string> Encoder::breakString(string s, vector<long> dels){
    vector<int> lens(numBlock, blockLength);
    vector<string> ret(numBlock);

    // Cal length for each block.
    for (int i = 0; i < dels.size(); i++) {
        lens[dels[i]] -= 1;
    }

    long cursor=0;
    long lidx = lens.size()-1;
    for (int i = 0; i <= lidx; i++) {
        ret[i]=s.substr(cursor,lens[i]);
        cursor+=lens[i];
    }
    int numZeros=lens[lidx]-ret[lidx].length();
    for (int i = 0; i < numZeros; i++) {
        ret[lidx]="0"+ret[lidx];
    }
    
    return ret;
}
string Encoder::randBin() {
    long baseLength = 16;
    long n = mlen / baseLength;
    long maxNum = pow(2, baseLength);
    string s = "";
    for (int i = 0; i < n; ++i) {
        s += zz2bin(rand() % maxNum, baseLength);
    }
    return s;
}

string Encoder::erase(string s, long idx){
    s.erase(idx, 1);
    return s;
}
string Encoder::erase(string s, vector<long> idxs){
    sort(idxs.begin(),idxs.begin()+idxs.size());
    for (int i = idxs.size()-1; i > -1; i--) {
        s.erase(idxs[i], 1);
    }
    return s;
}