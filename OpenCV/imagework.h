#ifndef IMAGEWORK_H
#define IMAGEWORK_H

#include <QWidget>
#include <vector>
#include <opencv2/opencv.hpp>
class ImageWork : public QWidget
{
    Q_OBJECT
public:
    explicit ImageWork(QWidget *parent = nullptr);

signals:


public:
    std::vector<int> Mat2Vector(cv::Mat src, int flag=0);
    int BayesClassify(std::vector<int> testData, std::vector<std::vector<int>> trainData, const float Ni[]);
    int TemplateMatching(std::vector<int> testData, std::vector<std::vector<int>> trainData);
    void TemplateMa(std::vector<int> testData, std::vector<std::vector<int>> trainData, int &min);
};

#endif // IMAGEWORK_H
