#include<iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <algorithm>

typedef int controler;
typedef int memory;//存储器类前缀，通常是addr
typedef int alu;//运算器相关前缀
struct STATE//先把最基础的相关内容找到，未添加分区
{
    short PSW;//状态标志位 0/1=用户态/内核态；中断则引发用户态转向内核态；内核态转用户态则使用特权指令
    controler PC;//程序计数器
    controler IR;//指令集
    controler CU;//执行
    memory MAR;//memory address register,理论上应该是个指针
    memory MDR;//memory data register
    alu ACC;
    alu ALU;
    alu X;
    alu MQ;
};


using namespace std;
int main(){
    printf("Hello world!");
    return 0;
}