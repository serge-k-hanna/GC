/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   Decoder.cpp
 * Author: hn
 * 
 * Created on August 10, 2017, 12:55 PM
 */

#include "Decoder.h"


Decoder::Decoder(int mlen, int numDel, int numChecker, int lengthExtension = 1):Encoder( mlen, numDel+numChecker, lengthExtension){
    this->numDel = numDel;
    x.SetLength(numDel);
}
void Decoder::decode(string &s, Vec<ZZ_p> p){
    this->s = &s;
    vector<Vec<ZZ_p>> d = baseCase(s);
    //for (int i = 0; i < d.size(); ++i) {
        //cout << d[i] <<endl;
    //}
    Vec<ZZ_p> pprime;
    pprime = p - (d[numDel]*enVec);
    //cout << pprime <<endl;
    vector<long> root(numDel, 0);
    if(CaseGenFast_rec(0, numBlock, 0, pprime, root, d)==true){
        return;
        //get bin string
    }
    cout<<"Decoding failure"<<endl;
    //raise exception
}
bool Decoder::CaseGenFast_rec(long first, long last, long idx, Vec<ZZ_p> pprime, vector<long> root, vector<Vec<ZZ_p>> d) {
    if(idx!=numDel-1){
        for (long current = first; current < last; current++) {
            if (current > first){
                pprime+=d[numDel][current] * enVec[current];
            }
            root[idx] = current;
            if(CaseGenFast_rec(current, last, idx + 1, pprime, root, d)==true){
                //recover the message

                return true;
            }
            if (idx==0 || current > first){
                pprime-=d[idx][current]*enVec[current];
            }
        }
    }
    else{
        for (long current = first; current < last; current++){
            root[idx] = current;
            if (current != first){
                pprime+=d[numDel][current]*enVec[current];
            }
            vector<long> uroot;
            uroot.push_back(root[0]);
            int count = 0;
            for (int j = 0; j < root.size(); ++j) {
                if(root[j]!=uroot[count]){
                    uroot.push_back(root[j]);
                    count++;
                }
            }

            //print(root,"root");
            //print(uroot,"uroot");

            //cout<<"pprime: "<<pprime<<endl;

            if(solveGC(pprime, uroot)==true){
                for (int i = 0; i < uroot.size(); ++i) {
                    long l = std::count(root.begin(),root.end(),uroot[i]);
                    s->replace(uroot[i]*blockLength,blockLength-l,zz2bin(x[i],blockLength));
                }
                //cout<<"success: x = "<<x<<endl;
                return true;
            }
//            cout<<endl;
            if (idx==0 || current != first){
                pprime-=d[idx][current]*enVec[current];
            }
        }
    }
    return false;
}
vector<Vec<ZZ_p>> Decoder::baseCase(string s) {
    vector<long> dels(numDel,numBlock-1);
    vector<Vec<ZZ_p>> d(numDel+1);
    d[0]=bin2zz(breakString(s, dels));
    d[0][numBlock-1]=0;
    for (int i = 1; i <= numDel; i++) {
        dels[i-1]=0;
        d[i]=bin2zz(breakString(s, dels));
        for (int j = 0; j < dels.size(); ++j) {
            d[i][dels[j]]=0;
        }
    }
    return d;
}
bool Decoder::solveGC(Vec<ZZ_p> pprime, vector<long> dels) {
    long numDelBlock=dels.size();
    if(numDelBlock==1){
//        cout<<"called one"<<endl;
        return solveGC(pprime,dels[0]);
    }
    else {
        Mat<ZZ_p> A;
        A.SetDims(numDelBlock, numVec);
        for (int i = 0; i < numDelBlock; ++i) {
            A[i] = enVec[dels[i]];
        }
        A = transpose(A);

        A.SetDims(numDelBlock, numDelBlock);
        pprime.SetLength(numDelBlock);

        ZZ_p det = determinant(A);

        solve(det, A, x, pprime);

        A.SetDims(numVec, numDelBlock);

        pprime.SetLength(numVec);

        ZZ_p y;
        for (int j = numDelBlock; j < numVec; ++j) {
            InnerProduct(y, A[j], x);
            if (y != pprime[j]) {
                return false;
            }
        }
        return true;
    }
}
bool Decoder::solveGC(Vec<ZZ_p> pprime, long dels) {
    x.SetLength(1);
    div(x[0], pprime[0], enVec[dels][0]);
    for (int j = 1; j < numVec; j++) {
//        cout<<enVec[dels][j] * x[0]<<" and "<<pprime[j]<<endl;
        if (enVec[dels][j] * x[0] != pprime[j]) {
            return false;
        }
    }
    return true;
}
void Decoder::print(vector<long> vec, string name) {
    cout<<name<<": ";
    for (int i = 0; i < vec.size(); ++i) {
        cout<<vec[i]<<" ";
    }
    cout<<endl;
}