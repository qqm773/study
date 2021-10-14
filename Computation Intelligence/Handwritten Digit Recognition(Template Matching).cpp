// Handwritten Digit Recognition.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
/*
* 问题1：如何将图片读入
* 答：利用opencv库函数imread
* 问题2：如何将Mat格式的图片像素提取，转化为易于计算的数组
* 答：利用Mat的data指针逐个读取像素值，转存到vector中。
*       根据像素压缩的需求，将data指针更换成基于Mat.at<>()成员函数的行列表示
* 问题3：像素压缩，特征降维
* 答：分块计数，阈值分割
* 
* 问题4：如何将数字->图片->测试集->训练集->图片->数字关联起来
* 答：通过map关联容器，根据图片命名规则和读入顺序固定，设定编号和图片名的映射；
        测试集数据匹配测试集结果，根据编号重新映射获取图片名，进而获取匹配数字结果
* 
* 2.将数据保存到模板库（目前保存在内存中）
* 3.进行欧氏距离计算，寻找最小距离(0,1的欧式距离运算简化为异或运算)
* 4.将匹配到的数据和模板关联(通过map关联容器进行间接比对)
* 5.统计识别数据
* 
*/

#include <iostream>
#include<fstream>
#include<opencv2/opencv.hpp>
#include<string>
#include<vector>
#include<map>

const int Max = 784;

//输出像素数据，用于检验
void VectorPrint(std::vector<std::vector<int>> allData) {
    int temp=0;
    for (std::vector<std::vector<int>>::iterator it = allData.begin(); it != allData.end(); it++) {
        std::cout << "第" << temp++ << "张：";
        for (std::vector<int>::iterator itit = (*it).begin(); itit != (*it).end(); itit++) {
            std::cout << *itit;
        }
        std::cout << "\n";
    }
}

//输出Map中的关联数据
void MapPrint(std::map<int, std::string> mapData) {
    using namespace std;
    std::map<int, std::string>::iterator it;
    for (it = mapData.begin(); it != mapData.end(); it++) {
        cout << it->first << ":" << it->second << endl;
    }
}

//保存数据到外存
void VectorSave(std::vector<std::vector<int>> allData,std::string path, std::map<int, std::string>& NOToName) {
    std::fstream fs;
    int temp=0;
    fs.open(path + "data.txt", std::ios::out | std::ios::app | std::ios::binary);
    for (std::vector<std::vector<int>>::iterator it = allData.begin(); it != allData.end(); it++) {
        fs << NOToName[temp++][0]<<" ";
        for (std::vector<int>::iterator itit = (*it).begin(); itit != (*it).end(); itit++) {
            fs << *itit;
        }
        fs << "\n";
    }
}

//从外存中读入图片数据，二值化后转存为数组。 参数说明: argc1 容易引用，存储当前图片像素值, argc2 照片路径。
void GetImage(std::vector<std::vector<int>>& allData, std::string imgPath) {
    using namespace std;
    using namespace cv;

    Mat srcData = imread(imgPath, COLOR_BGR2GRAY);//读入图片
    
    if (srcData.empty()) {
        cout << "读取失败" << endl;
        return;
    }

    ////显示图像
    //namedWindow("test", WINDOW_FREERATIO);
    //imshow("test", srcData);
    //waitKey(0);
    //destroyWindow("srcData");
    
    int count[14][14] = { 0 };//count数组为分块计数的数组，用于压缩图像矩阵
    int temp;
    for (int i = 0; i < srcData.rows; i++) {
        for (int j = 0; j < srcData.cols; j++) {
            temp = int(srcData.Mat::at<uchar>(i, j));
            //cout << temp << "  ";//查看像素值
            if (temp > 127) count[i /2][j /2]++;
        }
    }

    //将count数组的值转化为01串，形成特征量
    vector<int> src;
    for (int i = 0; i < 14; i++)
        for (int j = 0; j < 14; j++)
            if (count[i][j] > 1)
                src.push_back(1);
            else
                src.push_back(0);

    allData.push_back(src);
}

/*批量化处理图片,获取数据
参数说明: argc1 嵌套容器引用，存储当前图片像素值, argc2 照片路径, argc3 图片开始编号, argc4 图片结束编号, argc5 map关联容器，将编号与图片关联*/
void GetData(std::vector<std::vector<int>>& allData, std::string path,int begin,int end, std::map<int, std::string> &NOToName) {
    using namespace std;
    
    string imgPath;
    char name[100];   
     //根据文件命名规则，批量加载
    int temp = 0;
    for (int i = 0; i < 10; i++) {
        int j = begin;
        for (j; j < end; j++) {
            sprintf_s(name, "%d_%d.bmp", i, j);
            imgPath = path + name;
            GetImage(allData, imgPath);
            NOToName.insert(pair<int, string>(temp++, name));//保存顺序编号和文件名的映射
        }
    }
    return;
}

//计算欧氏距离，进行模板匹配，获取识别结果的统计数据。 参数说明: argc1 训练集数据, argc2 测试集数据, argc3 测试集关联, argc4 训练集关联, argc5 匹配结果
void CalculateDistance(std::vector<std::vector<int>> trainData, std::vector<std::vector<int>> testData  , std::map<int, std::string> train,std::map<int, std::string> test, std::map<int, std::string>& testTomin) {
    using namespace std;

    int temp;//训练集图片编号
    int n = 0;//测试集图片编号
    int distance;//记录当前距离
    int mindis;//记录最小距离
    int minNO;//最小距离对应训练集图片编号
    int rCount[10] = { 0 }; //计数每个数字匹配正确的个数
    int wCount[10] = { 0 }; //计数每个数字匹配错误的个数
    int dCount[10] = { 0 }; //计数每个数字匹配拒绝识别的个数
    

    for (vector<vector<int>>::iterator it = testData.begin(); it != testData.end(); it++) {
        temp = 0; 
        mindis = Max; 
        minNO = -1;
        for (vector<vector<int>>::iterator it1 = trainData.begin(); it1 != trainData.end(); it1++) {
            distance = 0;
            for (vector<int>::iterator itit1 = (*it1).begin(),itit =(*it).begin(); itit1 != (*it1).end(); itit1++,itit++) {
                if (*(itit) ^ *(itit1)) distance++;
            }
            if (distance == mindis) {
                if (train[temp][0] != train[minNO][0]) {
                    minNO = -1;
                }
            }
            else
            if (distance < mindis){
                mindis = distance;
                minNO = temp;
            }
            temp ++;
        }
        
        if (minNO == -1) {
            cout << "第" << n << "张图片" << test[n] << "   拒绝识别\n";
            dCount[(test)[n][0] - '0']++;
            testTomin[n] = minNO;
        }
        else if (test[n][0] == train[minNO][0]) {
            cout << "第" << n << "张图片"<<test[n]<<"   识别结果为" << train[minNO][0] << "   匹配对象：" 
                   << train[minNO] << "  距离为：" << mindis << "\n";
            rCount[(test)[n][0] - '0']++;
            testTomin[n] = train[minNO][0];
        }
        else {
            cout << "第" << n+1 << "张图片" << test[n] << "   识别结果为" << train[minNO][0] << "   匹配对象：" 
                   << train[minNO] << "   匹配失败"<<"\n";
            wCount[(test)[n][0] - '0']++;
            testTomin[n] = train[minNO][0];
        } 
        n++;
    }

    int singleSum = 0,allSum=0,rightSum=0,wrongSum=0,declainSum=0; //总数统计
    float rate = 0;
    for (int i = 0; i < 10; i++) {
        singleSum = rCount[i] + wCount[i]+dCount[i];
        allSum += singleSum;
        rightSum += rCount[i];
        wrongSum += wCount[i];
        declainSum += dCount[i];
        rate = rCount[i] / (singleSum*0.01);
        cout << "数字" << i << "   测试图像共" << singleSum << "张    其中识别正确：" << rCount[i] << "张   错误：" << wCount[i] << "张   拒绝识别："<<dCount[i]<<"张  识别正确率：" << rate << " % \n";
    }

    cout << "本次运行共测试识别" <<  allSum<< "张图像     其中识别正确" << rightSum << "张，识别错误" << wrongSum << "张   拒绝识别：" << declainSum << "张  总体识别正确率:" << rightSum/ (allSum * 0.01) << "%   错误率:" << wrongSum / (allSum * 0.01) << "%   拒绝识别率:" << declainSum / (allSum * 0.01) << "%\n";

}



int main()
{
    std::string path1 = "E:/image/train-images/";
    std::string path2 = "E:/image/test-images/";
    
    std::vector<std::vector<int>> trainData,testData;
    std::map<int, std::string> trainMap, testMap;
    std::map<int, std::string> testTomin;
    
    //获取模板（训练集）数据
    GetData(trainData,path1,20,100,trainMap);

    //获取测试集数据
    GetData(testData,path2,0,20,testMap);

    //写入外存
    VectorSave(trainData, path1, trainMap);

    //计算欧氏距离,匹配识别结果，统计识别数据
    CalculateDistance(trainData, testData,trainMap,testMap, testTomin);

}
