# About This Repository.
This repository contains C++ and Python implementations of [Guess & Check (GC) codes](https://arxiv.org/abs/1705.09569). The GC codes were first implemented using Python, which is easy to code, but slow. The codes were later implemented using C++, in an attempt to optimize the decoding performance. However, this is not a fully completed work. All we did was to translate what we had in Python to C++. We believe there is still a lot of room for optimization because of C++'s control over lower levels of computers' resources. Below are some of areas can be optimized:
1. The use of variables (try to reuse or maintain often used variable, don't make uneccessary copies when passing them to other fucnitons.)
2. NTL's Multithreading: NTL has its own multithreading library to speed up some matrix calculations.
3. Levenshtein Distance check (to minimize failure probability): this is available only in the Python implementation.

The implementations in this repository were done by Hieu Nguyen, who was an intern in the [CSI Lab](http://eceweb1.rutgers.edu/csi/CSILab.html) during Summer 2017.
# Guess & Check Codes
This project is based on the [Guess & Check (GC) codes](https://arxiv.org/abs/1705.09569), introduced by [Serge Kas Hanna](http://www.eden.rutgers.edu/~sk1976/) and [Salim El Rouayheb](http://eceweb1.rutgers.edu/csi/). GC codes are binary codes that can correct multiple deletions (or insertions) with high probability. These codes have a redundancy that is logarithmic in the length of the information message. The encoding and decoding schemes of GC codes are deterministic and polynomial time. The decoding may fail in some cases, but the probability of failure is proven to be low in theory (asymptotically vanishing) and in practice. For instance, one of the simulations shows that a GC code with rate 0.8 can correct up to 4 deletions in a message of 1024 bits with no decoding failure detected within 10000 runs of simulations.
# Installation Guide for C++
## Requirements
1. [Number Theory Library (NTL)](http://www.shoup.net/ntl/) by Victor Shoup: You must install this library to your machine and correctly add the include path to its header files.
2. Recomended OS: Unix (Mac or Linux).
3. Compiler: `g++` (because of NTL)
## Additional Library
This implimentation is so much easier thanks to the help of [Number Theory Library (NTL)](http://www.shoup.net/ntl/).
This is a wonderful library that effectively deals with calculations in finite fields.
Some of the helpful features include performing basic mathematical calculations in finite field, simulating abitrary sized numbers, and performing matrix manipulations in finite fields. 
A detailed installation guide can be found in Shoup's website. However, below are some tips and IDE settings that might be helpful to you.
## Tips
Here is one quick way to compile this project in terminal is (assuming you have install NTL in `/usr/local`).

In *Terminal*:
```
cd /to/your/project/folder
```
```
g++ -g -O2 main.cpp -o main -lntl -lgmp -lm
```
## Setup IDE
All of these settings are for your IDE to be able to compile NTL library.
1. Suggested IDE: CLion because this was done in CLion, but anything uses g++ compiler should work (with the right settings, see below).
2. Add additional linking flags to your linker setting: `-lntl` `-lgmp` `-lm`.
3. Add additional compiling flags to your compiler setting: `-g` `-O2`.
4. Change your default C++ compiler to `g++` (if it is not already in used). Check this folder `/usr/bin/g++` (although it could be at somewhere else depending on the Unix package manager you use.)

## Warning to Windows Users.
We did not verify if the code (as is) compiles using Visual Studio's complier (MSVC). If you are testing these codes in a Windows machine, make sure you use g++ to compile this project. MinGW and Cygwin are the two tools that could help you to get the g++ compiler and Unix like Terminal.
