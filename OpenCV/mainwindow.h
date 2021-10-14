#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <imagework.h>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    ImageWork* imgwork;
    cv::Mat src;
    cv::Mat dst;
    std::vector<int> testData;
    std::vector<std::vector<int>> trainData;
public:
    MainWindow(QWidget *parent = nullptr);

    ~MainWindow();

private slots:
    void on_actionopen_triggered();

    void on_actionsave_triggered();

    void on_templatematching_triggered();

    void on_bayesclassify_triggered();

    void on_actionimport_triggered();



private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
