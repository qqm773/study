#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "imagework.h"
#include <opencv2/opencv.hpp>
#include <QFileDialog>
#include <QDebug>
#include <vector>
#include <map>
#include <string>
#include <QMessageBox>

const float Ni[10] = {0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1};

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->imgwork = new ImageWork(this);
    cv::Mat src;
    cv::Mat dst;
    std::vector<int> testData;
    std::vector<std::vector<int>> trainData;
}

MainWindow::~MainWindow()
{
    delete ui;

}


void MainWindow::on_actionopen_triggered()
{
    QString path=QFileDialog::getOpenFileName(this,"Open_File","E:\\image","Images (*.png *.jpg *.bmp)");
    if (path.isEmpty()) { return; }
    this->src=cv::imread(path.toStdString(),cv::COLOR_BGR2GRAY);
    QImage* img=new QImage;
    img->load(path);
    ui->showlabel->setPixmap(QPixmap::fromImage(*img));
    delete img;
}


void MainWindow::on_actionsave_triggered()
{
    QString path=QFileDialog::getSaveFileName(this, "Save_File");
    if (path.isEmpty()||dst.empty()) { return; }
    cv::imwrite(path.toStdString(),dst);
}

void MainWindow::on_templatematching_triggered()
{
    this->testData.clear();
    this->testData= this->imgwork->Mat2Vector(src,1);
    if (this->testData.empty()||this->trainData.empty()) { return; }
    int source = this->imgwork->TemplateMatching(this->testData, this->trainData);
    QString num;
    num.setNum(source);
    //qDebug()<<num;
    QMessageBox::information(this,"Finish","this pic is num "+num);
}

void MainWindow::on_bayesclassify_triggered()
{
    this->testData.clear();
    this->testData= this->imgwork->Mat2Vector(src,0);
    if (this->testData.empty()||this->trainData.empty()) { return; }
    int source = this->imgwork->BayesClassify(this->testData, this->trainData, Ni);
    QString num;
    num.setNum(source);
    QMessageBox::information(this,"Finish","this pic is num "+num);
}

void MainWindow::on_actionimport_triggered()
{
    QString path=QFileDialog::getOpenFileName(this,"Open_File","E:\\image","Text (*.txt)");
    if (path.isEmpty()) { return; }
    QFile txt(path);
    this->trainData.clear();
    if (txt.open(QIODevice::ReadOnly | QIODevice::Text)){
        QByteArray train = txt.readAll();
        QString str1(train);
        std::string trainstr = str1.toStdString();
        std::vector<int> data;
        int num = 0;
        char temp;
        for (unsigned long long i = 0; i < trainstr.length();i++){
            temp = trainstr[i];
            if ('0'<=temp&&temp<='9'){
                data.push_back(temp-'0');
                num++;
            }
            if (num%197==0&&!data.empty()){
                this->trainData.push_back(data);
                data.clear();
            }

        }
    }
}

