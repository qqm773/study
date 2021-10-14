#include "imagework.h"

ImageWork::ImageWork(QWidget *parent) : QWidget(parent)
{

}

const int row = 14, col = 14;
const int Max = 784;

std::vector<int> ImageWork::Mat2Vector(cv::Mat src, int flag){// flag = 0 适用于BayesClassfy flag = 1 适用于Template Matching
    int count[row][col] = {{0}};//count数组为分块计数的数组
    int temp;
    for (int i = 0; i < src.rows; i++) {
       for (int j = 0; j < src.cols; j++) {
           temp = int(src.Mat::at<uchar>(i, j));
           if (temp > 127) count[i /2][j /2]++;
       }
    }

    //将count数组存储到特征库
    std::vector<int> srcData;
    if (flag == 0){
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                srcData.push_back(count[i][j]);
            }
        }
    } else if (flag == 1){
        for (int i = 0; i < row; i++){
            for (int j = 0; j < col; j++){
                if (count[i][j] > 1)
                    srcData.push_back(1);
                else
                    srcData.push_back(0);
            }
        }
    }
    return srcData;
};

int ImageWork::BayesClassify(std::vector<int> testData, std::vector<std::vector<int>> trainData, const float Ni[]){
    using namespace std;

    double Prop[10][row*col] ;
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < row * col; j++) {
            Prop[i][j] = 0;
        }
    }
    int temp = 0;
    int num = 0;//指向分块的下标
    int curNum;
    double maxPro=-1;
    double tempPro = 0;
    int maxNO = -1;
    //类条件概率计算
    for (int i = 0; i < int(trainData.size()); i++) {
        num = 0;
         curNum = trainData[i][0];
        for (int j = 0 ; j < int(testData.size()) ;j++) {
               Prop[curNum][num++] += double(trainData[i][j+1])/(double(28/row)*double(28/col));
            }
        temp++;
    }
    //后验概率
    temp = 0;
        //cout << "图片" << test[temp] << "：";
    for (int i = 0; i < 10; i++) {//对于当前测试图片对每个数字的联合概率
        num = 0; tempPro = 0;
        for (vector<int>::iterator it = testData.begin(); it !=testData.end(); it++) {
            tempPro += double(*(it)) / (double(28 / row) * double(28 / col)) * Prop[i][num++];
        }
        tempPro = tempPro * Ni[i];//后验概率
        if (tempPro > maxPro) {
            maxPro = tempPro;
            maxNO = i;
        }
    }
    return maxNO;
};

int ImageWork::TemplateMatching(std::vector<int> testData, std::vector<std::vector<int>> trainData) {

    int distance;//记录当前距离
    int mindis;//记录最小距离
    int minNum;//最小距离对应图片数字
    int curNum;

    mindis = Max;
    minNum = -1;
    for (int i = 0; i < int(trainData.size()); i++) {
        distance = 0;
        curNum = trainData[i][0];
        for (int j = 0 ; j < int(testData.size()) ;j++) {
            if (testData[j] ^ trainData[i][j+1]) distance++;
        }
        if (distance == mindis) {
            if ( curNum != minNum) {
                minNum = -1;
            }
        }
        else if (distance < mindis){
            mindis = distance;
            minNum = curNum;
        }
    }
    return minNum;
}

