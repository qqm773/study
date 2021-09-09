// Handwritten Digit Recognition.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
/*
* 问题1：如何将图片读入
* 答：利用opencv库函数imread
* 问题2：如何将Mat格式的图片像素提取，转化为易于计算的数组
* 答：利用Mat的data指针逐个读取像素值，转存到数组中。保存在外存
* 
* 目前待解决：
* 1.提取特征，将784位像素降维到28位
* 2.将数据保存到模板库
* 3.进行欧氏距离计算，寻找最小距离
* 4.将匹配到的数据和模板关联
* 5.统计识别数据
*/
#include <iostream>
#include<string>
#include<fstream>
#include<opencv2/opencv.hpp>
#include<vector>
#include<Python.h>
const int Max = 784;

//从外存中读入图片数据，二值化后转存为数组。argc1为临时数组，存储当前图片像素值；argc2位照片路径。
void getImage(int src[], std::string imgpath) {
    using namespace std;
    using namespace cv;
    
    Mat srcc = imread(imgpath,COLOR_BGR2GRAY);
    if (srcc.empty()) {
        cout << "读取失败" << endl;
        return;     //中断读入
    }
    threshold(srcc, srcc, 127, 255,THRESH_BINARY);
    
    //显示图像
    //namedWindow("test", WINDOW_FREERATIO);
    //imshow("test", srcc);
    //waitKey(0);
    //destroyWindow("srcc");

    if (srcc.isContinuous()) {
        cout << "图片是连续的" << endl;
        cout << imgpath << std::endl;
    }
    else return;

    int temp = 0,t;
    
    //逐个读取像素值，存入数组
    for (int i = 0; i < srcc.rows; i++) {
        for (int j = 0; j < srcc.cols; j++) {
            t= int(*srcc.data++);
            if (t == 255)src[temp++] = 1;
            else src[temp++] = 0;
        }
    }

    //检查数组
    for (int i=0;i<Max;i++)
        cout << src[i] << " ";
    return ;
}

//批量化处理图片。argc1为临时数组，存储当前图片像素值；argc2位照片路径。argc3为图片开始编号，argc4位图片结束编号
void getdata(int src[], std::string path,int begin,int end) {
    using namespace std;
    
    string imgpath,datapath; 
    char name[100];   
    fstream fs;
    datapath = path + "data.txt";
    fs.open(datapath, ios::app|ios::in|ios::binary);
    //根据文件命名规则，批量加载
    for (int i = 0; i < 10; i++) {
        int j = begin;
        for (j; j < end; j++) {
            sprintf_s(name, "%d_%d.bmp", i, j);
            imgpath = path + name;
            getImage(src, imgpath);
            //写入内存
            fs << name << " ";
            for (int t = 0; t < Max; t++)
                fs << src[t];
            fs << "\n";
        }
    }
    fs.close();
    return;
}
int main()
{
    std::string path1 = "E:/image/train-images/";
    std::string path2 = "E:/image/test-images/";
    int src[Max];

    Py_Initialize();//使用python之前，要调用Py_Initialize();这个函数进行初始化
    PyRun_SimpleString("print('hello world!')");
    

    Py_Finalize();
    //获取模板（训练集）数据
    getdata(src,path1,11,20);

    //获取测试集数据
    getdata(src,path2,0,10);
    
    std::cout << "Hello World!\n";
}
