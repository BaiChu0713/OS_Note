#include<iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <algorithm>

struct STATE
{
    short PSW;//状态标志位 0/1=用户态/内核态；中断则引发用户态转向内核态；内核态转用户态则使用特权指令

};


using namespace std;
int main(){
    printf("Hello world!");
    return 0;
}