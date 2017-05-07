#ifndef UI_ESOFORM_H
#define UI_ESOFORM_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QComboBox>
#include <QtGui/QFrame>
#include <QtGui/QGridLayout>
#include <QtGui/QGroupBox>
#include <QtGui/QHBoxLayout>
#include <QtGui/QLabel>
#include <QtGui/QLineEdit>
#include <QtGui/QPushButton>
#include <QtGui/QSpacerItem>
#include <QtGui/QSplitter>
#include <QtGui/QTreeWidget>
#include <QtGui/QVBoxLayout>
#include <QtGui/QWidget>
#include "qwt_plot.h"

class Ui_EsoForm
{
public:
    QGridLayout *gridLayout;
    QSplitter *splitter;
    QSplitter *splitter_3;
    QSplitter *splitter_5;
    QFrame *frameVariableList;
    QGridLayout *gridLayout1;
    QVBoxLayout *vboxLayout;
    QGroupBox *groupBoxFileInfo;
    QGridLayout *gridLayout2;
    QLabel *labelFileInfo;
    QGroupBox *groupBoxEnvironment;
    QGridLayout *gridLayout3;
    QComboBox *comboBoxEnvironment;
    QGroupBox *groupBoxVariableInfo;
    QGridLayout *gridLayout4;
    QGroupBox *groupBoxVarInfo;
    QGridLayout *gridLayout5;
    QGridLayout *gridLayout6;
    QLabel *labelMaximum;
    QLabel *labelAvg;
    QLabel *labelMin;
    QLabel *labelAverage;
    QLabel *labelMax;
    QLabel *labelMinimum;
    QGroupBox *groupBoxVarInfoLocal;
    QGridLayout *gridLayout7;
    QHBoxLayout *hboxLayout;
    QLabel *labelMaximumLocal;
    QLabel *labelMaxLocal;
    QLabel *labelMinimumLocal;
    QLabel *labelMinLocal;
    QLabel *labelAverageLocal;
    QLabel *labelAvgLocal;
    QGroupBox *groupBoxFilter;
    QGridLayout *gridLayout8;
    QGridLayout *gridLayout9;
    QGridLayout *gridLayout10;
    QLabel *labelFilterUnit;
    QLabel *labelFilterArea;
    QLabel *labelFilterName;
    QLineEdit *lineEditFilterArea;
    QLabel *labelFilterTimestep;
    QLineEdit *lineEditFilterName;
    QLineEdit *lineEditFilterTimestep;
    QLineEdit *lineEditFilterUnit;
    QGridLayout *gridLayout11;
    QPushButton *pushButtonFilter;
    QPushButton *pushButtonClearFilter;
    QTreeWidget *treeWidget;
    QFrame *frame_2;
    QGridLayout *gridLayout12;
    QVBoxLayout *vboxLayout1;
    QwtPlot *qwtPlot;
    QHBoxLayout *hboxLayout1;
    QSpacerItem *spacerItem;
    QPushButton *pushButtonPrevious;
    QComboBox *comboBoxTimeAxis;
    QPushButton *pushButtonNext;
    QSpacerItem *spacerItem1;
    QWidget *layoutWidget_2;

    void setupUi(QWidget *EsoForm)
    {
    EsoForm->setObjectName(QString::fromUtf8("EsoForm"));
    EsoForm->resize(QSize(1111, 700).expandedTo(EsoForm->minimumSizeHint()));
    EsoForm->setWindowIcon(QIcon(QString::fromUtf8(":/images/xEsoViewIconBig.png")));
    gridLayout = new QGridLayout(EsoForm);
    gridLayout->setSpacing(6);
    gridLayout->setMargin(9);
    gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
    splitter = new QSplitter(EsoForm);
    splitter->setObjectName(QString::fromUtf8("splitter"));
    splitter->setOrientation(Qt::Horizontal);
    splitter_3 = new QSplitter(splitter);
    splitter_3->setObjectName(QString::fromUtf8("splitter_3"));
    splitter_3->setOrientation(Qt::Horizontal);
    splitter_5 = new QSplitter(splitter_3);
    splitter_5->setObjectName(QString::fromUtf8("splitter_5"));
    splitter_5->setOrientation(Qt::Horizontal);
    frameVariableList = new QFrame(splitter_5);
    frameVariableList->setObjectName(QString::fromUtf8("frameVariableList"));
    QSizePolicy sizePolicy(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(1));
    sizePolicy.setHorizontalStretch(0);
    sizePolicy.setVerticalStretch(0);
    sizePolicy.setHeightForWidth(frameVariableList->sizePolicy().hasHeightForWidth());
    frameVariableList->setSizePolicy(sizePolicy);
    frameVariableList->setMinimumSize(QSize(16, 48));
    frameVariableList->setFrameShape(QFrame::Panel);
    frameVariableList->setFrameShadow(QFrame::Raised);
    frameVariableList->setLineWidth(1);
    frameVariableList->setMidLineWidth(1);
    gridLayout1 = new QGridLayout(frameVariableList);
    gridLayout1->setSpacing(6);
    gridLayout1->setMargin(9);
    gridLayout1->setObjectName(QString::fromUtf8("gridLayout1"));
    vboxLayout = new QVBoxLayout();
    vboxLayout->setSpacing(6);
    vboxLayout->setMargin(0);
    vboxLayout->setObjectName(QString::fromUtf8("vboxLayout"));
    groupBoxFileInfo = new QGroupBox(frameVariableList);
    groupBoxFileInfo->setObjectName(QString::fromUtf8("groupBoxFileInfo"));
    QSizePolicy sizePolicy1(static_cast<QSizePolicy::Policy>(3), static_cast<QSizePolicy::Policy>(5));
    sizePolicy1.setHorizontalStretch(0);
    sizePolicy1.setVerticalStretch(0);
    sizePolicy1.setHeightForWidth(groupBoxFileInfo->sizePolicy().hasHeightForWidth());
    groupBoxFileInfo->setSizePolicy(sizePolicy1);
    gridLayout2 = new QGridLayout(groupBoxFileInfo);
    gridLayout2->setSpacing(4);
    gridLayout2->setMargin(2);
    gridLayout2->setObjectName(QString::fromUtf8("gridLayout2"));
    labelFileInfo = new QLabel(groupBoxFileInfo);
    labelFileInfo->setObjectName(QString::fromUtf8("labelFileInfo"));
    QSizePolicy sizePolicy2(static_cast<QSizePolicy::Policy>(13), static_cast<QSizePolicy::Policy>(5));
    sizePolicy2.setHorizontalStretch(0);
    sizePolicy2.setVerticalStretch(0);
    sizePolicy2.setHeightForWidth(labelFileInfo->sizePolicy().hasHeightForWidth());
    labelFileInfo->setSizePolicy(sizePolicy2);
    labelFileInfo->setMinimumSize(QSize(0, 30));
    labelFileInfo->setIndent(6);

    gridLayout2->addWidget(labelFileInfo, 0, 0, 1, 1);


    vboxLayout->addWidget(groupBoxFileInfo);

    groupBoxEnvironment = new QGroupBox(frameVariableList);
    groupBoxEnvironment->setObjectName(QString::fromUtf8("groupBoxEnvironment"));
    QSizePolicy sizePolicy3(static_cast<QSizePolicy::Policy>(3), static_cast<QSizePolicy::Policy>(0));
    sizePolicy3.setHorizontalStretch(0);
    sizePolicy3.setVerticalStretch(0);
    sizePolicy3.setHeightForWidth(groupBoxEnvironment->sizePolicy().hasHeightForWidth());
    groupBoxEnvironment->setSizePolicy(sizePolicy3);
    groupBoxEnvironment->setBaseSize(QSize(0, 16));
    gridLayout3 = new QGridLayout(groupBoxEnvironment);
    gridLayout3->setSpacing(4);
    gridLayout3->setMargin(2);
    gridLayout3->setObjectName(QString::fromUtf8("gridLayout3"));
    comboBoxEnvironment = new QComboBox(groupBoxEnvironment);
    comboBoxEnvironment->setObjectName(QString::fromUtf8("comboBoxEnvironment"));
    QSizePolicy sizePolicy4(static_cast<QSizePolicy::Policy>(1), static_cast<QSizePolicy::Policy>(5));
    sizePolicy4.setHorizontalStretch(0);
    sizePolicy4.setVerticalStretch(0);
    sizePolicy4.setHeightForWidth(comboBoxEnvironment->sizePolicy().hasHeightForWidth());
    comboBoxEnvironment->setSizePolicy(sizePolicy4);
    comboBoxEnvironment->setMinimumSize(QSize(0, 16));
    comboBoxEnvironment->setMaximumSize(QSize(16777215, 20));

    gridLayout3->addWidget(comboBoxEnvironment, 0, 0, 1, 1);


    vboxLayout->addWidget(groupBoxEnvironment);

    groupBoxVariableInfo = new QGroupBox(frameVariableList);
    groupBoxVariableInfo->setObjectName(QString::fromUtf8("groupBoxVariableInfo"));
    QSizePolicy sizePolicy5(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy5.setHorizontalStretch(0);
    sizePolicy5.setVerticalStretch(0);
    sizePolicy5.setHeightForWidth(groupBoxVariableInfo->sizePolicy().hasHeightForWidth());
    groupBoxVariableInfo->setSizePolicy(sizePolicy5);
    groupBoxVariableInfo->setMinimumSize(QSize(16, 55));
    gridLayout4 = new QGridLayout(groupBoxVariableInfo);
    gridLayout4->setSpacing(4);
    gridLayout4->setMargin(2);
    gridLayout4->setObjectName(QString::fromUtf8("gridLayout4"));
    groupBoxVarInfo = new QGroupBox(groupBoxVariableInfo);
    groupBoxVarInfo->setObjectName(QString::fromUtf8("groupBoxVarInfo"));
    QSizePolicy sizePolicy6(static_cast<QSizePolicy::Policy>(5), static_cast<QSizePolicy::Policy>(0));
    sizePolicy6.setHorizontalStretch(0);
    sizePolicy6.setVerticalStretch(0);
    sizePolicy6.setHeightForWidth(groupBoxVarInfo->sizePolicy().hasHeightForWidth());
    groupBoxVarInfo->setSizePolicy(sizePolicy6);
    gridLayout5 = new QGridLayout(groupBoxVarInfo);
    gridLayout5->setSpacing(4);
    gridLayout5->setMargin(2);
    gridLayout5->setObjectName(QString::fromUtf8("gridLayout5"));
    gridLayout6 = new QGridLayout();
    gridLayout6->setSpacing(4);
    gridLayout6->setMargin(0);
    gridLayout6->setObjectName(QString::fromUtf8("gridLayout6"));
    labelMaximum = new QLabel(groupBoxVarInfo);
    labelMaximum->setObjectName(QString::fromUtf8("labelMaximum"));
    labelMaximum->setMinimumSize(QSize(0, 10));

    gridLayout6->addWidget(labelMaximum, 0, 0, 1, 1);

    labelAvg = new QLabel(groupBoxVarInfo);
    labelAvg->setObjectName(QString::fromUtf8("labelAvg"));
    QSizePolicy sizePolicy7(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy7.setHorizontalStretch(0);
    sizePolicy7.setVerticalStretch(0);
    sizePolicy7.setHeightForWidth(labelAvg->sizePolicy().hasHeightForWidth());
    labelAvg->setSizePolicy(sizePolicy7);

    gridLayout6->addWidget(labelAvg, 0, 5, 1, 1);

    labelMin = new QLabel(groupBoxVarInfo);
    labelMin->setObjectName(QString::fromUtf8("labelMin"));
    QSizePolicy sizePolicy8(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy8.setHorizontalStretch(0);
    sizePolicy8.setVerticalStretch(0);
    sizePolicy8.setHeightForWidth(labelMin->sizePolicy().hasHeightForWidth());
    labelMin->setSizePolicy(sizePolicy8);

    gridLayout6->addWidget(labelMin, 0, 3, 1, 1);

    labelAverage = new QLabel(groupBoxVarInfo);
    labelAverage->setObjectName(QString::fromUtf8("labelAverage"));

    gridLayout6->addWidget(labelAverage, 0, 4, 1, 1);

    labelMax = new QLabel(groupBoxVarInfo);
    labelMax->setObjectName(QString::fromUtf8("labelMax"));
    QSizePolicy sizePolicy9(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy9.setHorizontalStretch(0);
    sizePolicy9.setVerticalStretch(0);
    sizePolicy9.setHeightForWidth(labelMax->sizePolicy().hasHeightForWidth());
    labelMax->setSizePolicy(sizePolicy9);

    gridLayout6->addWidget(labelMax, 0, 1, 1, 1);

    labelMinimum = new QLabel(groupBoxVarInfo);
    labelMinimum->setObjectName(QString::fromUtf8("labelMinimum"));

    gridLayout6->addWidget(labelMinimum, 0, 2, 1, 1);


    gridLayout5->addLayout(gridLayout6, 0, 0, 1, 1);


    gridLayout4->addWidget(groupBoxVarInfo, 0, 0, 1, 1);

    groupBoxVarInfoLocal = new QGroupBox(groupBoxVariableInfo);
    groupBoxVarInfoLocal->setObjectName(QString::fromUtf8("groupBoxVarInfoLocal"));
    QSizePolicy sizePolicy10(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy10.setHorizontalStretch(0);
    sizePolicy10.setVerticalStretch(0);
    sizePolicy10.setHeightForWidth(groupBoxVarInfoLocal->sizePolicy().hasHeightForWidth());
    groupBoxVarInfoLocal->setSizePolicy(sizePolicy10);
    gridLayout7 = new QGridLayout(groupBoxVarInfoLocal);
    gridLayout7->setSpacing(4);
    gridLayout7->setMargin(2);
    gridLayout7->setObjectName(QString::fromUtf8("gridLayout7"));
    hboxLayout = new QHBoxLayout();
    hboxLayout->setSpacing(4);
    hboxLayout->setMargin(0);
    hboxLayout->setObjectName(QString::fromUtf8("hboxLayout"));
    labelMaximumLocal = new QLabel(groupBoxVarInfoLocal);
    labelMaximumLocal->setObjectName(QString::fromUtf8("labelMaximumLocal"));
    labelMaximumLocal->setMinimumSize(QSize(0, 10));

    hboxLayout->addWidget(labelMaximumLocal);

    labelMaxLocal = new QLabel(groupBoxVarInfoLocal);
    labelMaxLocal->setObjectName(QString::fromUtf8("labelMaxLocal"));
    QSizePolicy sizePolicy11(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy11.setHorizontalStretch(0);
    sizePolicy11.setVerticalStretch(0);
    sizePolicy11.setHeightForWidth(labelMaxLocal->sizePolicy().hasHeightForWidth());
    labelMaxLocal->setSizePolicy(sizePolicy11);

    hboxLayout->addWidget(labelMaxLocal);

    labelMinimumLocal = new QLabel(groupBoxVarInfoLocal);
    labelMinimumLocal->setObjectName(QString::fromUtf8("labelMinimumLocal"));

    hboxLayout->addWidget(labelMinimumLocal);

    labelMinLocal = new QLabel(groupBoxVarInfoLocal);
    labelMinLocal->setObjectName(QString::fromUtf8("labelMinLocal"));
    QSizePolicy sizePolicy12(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy12.setHorizontalStretch(0);
    sizePolicy12.setVerticalStretch(0);
    sizePolicy12.setHeightForWidth(labelMinLocal->sizePolicy().hasHeightForWidth());
    labelMinLocal->setSizePolicy(sizePolicy12);

    hboxLayout->addWidget(labelMinLocal);

    labelAverageLocal = new QLabel(groupBoxVarInfoLocal);
    labelAverageLocal->setObjectName(QString::fromUtf8("labelAverageLocal"));

    hboxLayout->addWidget(labelAverageLocal);

    labelAvgLocal = new QLabel(groupBoxVarInfoLocal);
    labelAvgLocal->setObjectName(QString::fromUtf8("labelAvgLocal"));
    QSizePolicy sizePolicy13(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy13.setHorizontalStretch(0);
    sizePolicy13.setVerticalStretch(0);
    sizePolicy13.setHeightForWidth(labelAvgLocal->sizePolicy().hasHeightForWidth());
    labelAvgLocal->setSizePolicy(sizePolicy13);

    hboxLayout->addWidget(labelAvgLocal);


    gridLayout7->addLayout(hboxLayout, 0, 0, 1, 1);


    gridLayout4->addWidget(groupBoxVarInfoLocal, 1, 0, 1, 1);


    vboxLayout->addWidget(groupBoxVariableInfo);

    groupBoxFilter = new QGroupBox(frameVariableList);
    groupBoxFilter->setObjectName(QString::fromUtf8("groupBoxFilter"));
    QSizePolicy sizePolicy14(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(0));
    sizePolicy14.setHorizontalStretch(0);
    sizePolicy14.setVerticalStretch(0);
    sizePolicy14.setHeightForWidth(groupBoxFilter->sizePolicy().hasHeightForWidth());
    groupBoxFilter->setSizePolicy(sizePolicy14);
    gridLayout8 = new QGridLayout(groupBoxFilter);
    gridLayout8->setSpacing(4);
    gridLayout8->setMargin(2);
    gridLayout8->setObjectName(QString::fromUtf8("gridLayout8"));
    gridLayout9 = new QGridLayout();
    gridLayout9->setSpacing(4);
    gridLayout9->setMargin(0);
    gridLayout9->setObjectName(QString::fromUtf8("gridLayout9"));
    gridLayout10 = new QGridLayout();
    gridLayout10->setSpacing(2);
    gridLayout10->setMargin(0);
    gridLayout10->setObjectName(QString::fromUtf8("gridLayout10"));
    labelFilterUnit = new QLabel(groupBoxFilter);
    labelFilterUnit->setObjectName(QString::fromUtf8("labelFilterUnit"));
    labelFilterUnit->setIndent(2);

    gridLayout10->addWidget(labelFilterUnit, 0, 2, 1, 1);

    labelFilterArea = new QLabel(groupBoxFilter);
    labelFilterArea->setObjectName(QString::fromUtf8("labelFilterArea"));
    labelFilterArea->setIndent(2);

    gridLayout10->addWidget(labelFilterArea, 0, 1, 1, 1);

    labelFilterName = new QLabel(groupBoxFilter);
    labelFilterName->setObjectName(QString::fromUtf8("labelFilterName"));
    QSizePolicy sizePolicy15(static_cast<QSizePolicy::Policy>(5), static_cast<QSizePolicy::Policy>(0));
    sizePolicy15.setHorizontalStretch(0);
    sizePolicy15.setVerticalStretch(0);
    sizePolicy15.setHeightForWidth(labelFilterName->sizePolicy().hasHeightForWidth());
    labelFilterName->setSizePolicy(sizePolicy15);
    labelFilterName->setMinimumSize(QSize(0, 10));
    labelFilterName->setIndent(2);

    gridLayout10->addWidget(labelFilterName, 0, 0, 1, 1);

    lineEditFilterArea = new QLineEdit(groupBoxFilter);
    lineEditFilterArea->setObjectName(QString::fromUtf8("lineEditFilterArea"));
    QSizePolicy sizePolicy16(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy16.setHorizontalStretch(0);
    sizePolicy16.setVerticalStretch(0);
    sizePolicy16.setHeightForWidth(lineEditFilterArea->sizePolicy().hasHeightForWidth());
    lineEditFilterArea->setSizePolicy(sizePolicy16);
    lineEditFilterArea->setMaximumSize(QSize(16777215, 20));

    gridLayout10->addWidget(lineEditFilterArea, 1, 1, 1, 1);

    labelFilterTimestep = new QLabel(groupBoxFilter);
    labelFilterTimestep->setObjectName(QString::fromUtf8("labelFilterTimestep"));
    labelFilterTimestep->setIndent(2);

    gridLayout10->addWidget(labelFilterTimestep, 0, 3, 1, 1);

    lineEditFilterName = new QLineEdit(groupBoxFilter);
    lineEditFilterName->setObjectName(QString::fromUtf8("lineEditFilterName"));
    lineEditFilterName->setMinimumSize(QSize(0, 10));
    lineEditFilterName->setMaximumSize(QSize(16777215, 20));

    gridLayout10->addWidget(lineEditFilterName, 1, 0, 1, 1);

    lineEditFilterTimestep = new QLineEdit(groupBoxFilter);
    lineEditFilterTimestep->setObjectName(QString::fromUtf8("lineEditFilterTimestep"));
    QSizePolicy sizePolicy17(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy17.setHorizontalStretch(0);
    sizePolicy17.setVerticalStretch(0);
    sizePolicy17.setHeightForWidth(lineEditFilterTimestep->sizePolicy().hasHeightForWidth());
    lineEditFilterTimestep->setSizePolicy(sizePolicy17);
    lineEditFilterTimestep->setMaximumSize(QSize(16777215, 20));

    gridLayout10->addWidget(lineEditFilterTimestep, 1, 3, 1, 1);

    lineEditFilterUnit = new QLineEdit(groupBoxFilter);
    lineEditFilterUnit->setObjectName(QString::fromUtf8("lineEditFilterUnit"));
    QSizePolicy sizePolicy18(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy18.setHorizontalStretch(0);
    sizePolicy18.setVerticalStretch(0);
    sizePolicy18.setHeightForWidth(lineEditFilterUnit->sizePolicy().hasHeightForWidth());
    lineEditFilterUnit->setSizePolicy(sizePolicy18);
    lineEditFilterUnit->setMaximumSize(QSize(16777215, 20));

    gridLayout10->addWidget(lineEditFilterUnit, 1, 2, 1, 1);


    gridLayout9->addLayout(gridLayout10, 0, 0, 1, 1);

    gridLayout11 = new QGridLayout();
    gridLayout11->setSpacing(4);
    gridLayout11->setMargin(0);
    gridLayout11->setObjectName(QString::fromUtf8("gridLayout11"));
    pushButtonFilter = new QPushButton(groupBoxFilter);
    pushButtonFilter->setObjectName(QString::fromUtf8("pushButtonFilter"));
    QSizePolicy sizePolicy19(static_cast<QSizePolicy::Policy>(5), static_cast<QSizePolicy::Policy>(0));
    sizePolicy19.setHorizontalStretch(0);
    sizePolicy19.setVerticalStretch(0);
    sizePolicy19.setHeightForWidth(pushButtonFilter->sizePolicy().hasHeightForWidth());
    pushButtonFilter->setSizePolicy(sizePolicy19);
    pushButtonFilter->setMaximumSize(QSize(100, 20));

    gridLayout11->addWidget(pushButtonFilter, 0, 1, 1, 1);

    pushButtonClearFilter = new QPushButton(groupBoxFilter);
    pushButtonClearFilter->setObjectName(QString::fromUtf8("pushButtonClearFilter"));
    QSizePolicy sizePolicy20(static_cast<QSizePolicy::Policy>(5), static_cast<QSizePolicy::Policy>(0));
    sizePolicy20.setHorizontalStretch(0);
    sizePolicy20.setVerticalStretch(0);
    sizePolicy20.setHeightForWidth(pushButtonClearFilter->sizePolicy().hasHeightForWidth());
    pushButtonClearFilter->setSizePolicy(sizePolicy20);
    pushButtonClearFilter->setMinimumSize(QSize(0, 10));
    pushButtonClearFilter->setMaximumSize(QSize(100, 20));

    gridLayout11->addWidget(pushButtonClearFilter, 0, 0, 1, 1);


    gridLayout9->addLayout(gridLayout11, 1, 0, 1, 1);


    gridLayout8->addLayout(gridLayout9, 0, 0, 1, 1);


    vboxLayout->addWidget(groupBoxFilter);

    treeWidget = new QTreeWidget(frameVariableList);
    treeWidget->setObjectName(QString::fromUtf8("treeWidget"));
    QSizePolicy sizePolicy21(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(3));
    sizePolicy21.setHorizontalStretch(0);
    sizePolicy21.setVerticalStretch(0);
    sizePolicy21.setHeightForWidth(treeWidget->sizePolicy().hasHeightForWidth());
    treeWidget->setSizePolicy(sizePolicy21);
    treeWidget->setMinimumSize(QSize(0, 30));
    treeWidget->setMidLineWidth(0);
    treeWidget->setTabKeyNavigation(false);
    treeWidget->setSortingEnabled(true);

    vboxLayout->addWidget(treeWidget);


    gridLayout1->addLayout(vboxLayout, 0, 0, 1, 1);

    splitter_5->addWidget(frameVariableList);
    splitter_3->addWidget(splitter_5);
    splitter->addWidget(splitter_3);
    frame_2 = new QFrame(splitter);
    frame_2->setObjectName(QString::fromUtf8("frame_2"));
    QSizePolicy sizePolicy22(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(7));
    sizePolicy22.setHorizontalStretch(0);
    sizePolicy22.setVerticalStretch(0);
    sizePolicy22.setHeightForWidth(frame_2->sizePolicy().hasHeightForWidth());
    frame_2->setSizePolicy(sizePolicy22);
    frame_2->setFrameShape(QFrame::Panel);
    frame_2->setFrameShadow(QFrame::Raised);
    frame_2->setMidLineWidth(1);
    gridLayout12 = new QGridLayout(frame_2);
    gridLayout12->setSpacing(6);
    gridLayout12->setMargin(9);
    gridLayout12->setObjectName(QString::fromUtf8("gridLayout12"));
    vboxLayout1 = new QVBoxLayout();
    vboxLayout1->setSpacing(6);
    vboxLayout1->setMargin(0);
    vboxLayout1->setObjectName(QString::fromUtf8("vboxLayout1"));
    qwtPlot = new QwtPlot(frame_2);
    qwtPlot->setObjectName(QString::fromUtf8("qwtPlot"));
    QSizePolicy sizePolicy23(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(7));
    sizePolicy23.setHorizontalStretch(0);
    sizePolicy23.setVerticalStretch(0);
    sizePolicy23.setHeightForWidth(qwtPlot->sizePolicy().hasHeightForWidth());
    qwtPlot->setSizePolicy(sizePolicy23);

    vboxLayout1->addWidget(qwtPlot);

    hboxLayout1 = new QHBoxLayout();
    hboxLayout1->setSpacing(6);
    hboxLayout1->setMargin(0);
    hboxLayout1->setObjectName(QString::fromUtf8("hboxLayout1"));
    spacerItem = new QSpacerItem(40, 31, QSizePolicy::Expanding, QSizePolicy::Minimum);

    hboxLayout1->addItem(spacerItem);

    pushButtonPrevious = new QPushButton(frame_2);
    pushButtonPrevious->setObjectName(QString::fromUtf8("pushButtonPrevious"));

    hboxLayout1->addWidget(pushButtonPrevious);

    comboBoxTimeAxis = new QComboBox(frame_2);
    comboBoxTimeAxis->setObjectName(QString::fromUtf8("comboBoxTimeAxis"));
    comboBoxTimeAxis->setMaxVisibleItems(5);
    comboBoxTimeAxis->setMaxCount(10);

    hboxLayout1->addWidget(comboBoxTimeAxis);

    pushButtonNext = new QPushButton(frame_2);
    pushButtonNext->setObjectName(QString::fromUtf8("pushButtonNext"));

    hboxLayout1->addWidget(pushButtonNext);

    spacerItem1 = new QSpacerItem(40, 31, QSizePolicy::Expanding, QSizePolicy::Minimum);

    hboxLayout1->addItem(spacerItem1);


    vboxLayout1->addLayout(hboxLayout1);


    gridLayout12->addLayout(vboxLayout1, 0, 0, 1, 1);

    layoutWidget_2 = new QWidget(frame_2);
    layoutWidget_2->setObjectName(QString::fromUtf8("layoutWidget_2"));

    gridLayout12->addWidget(layoutWidget_2, 1, 0, 1, 1);

    splitter->addWidget(frame_2);

    gridLayout->addWidget(splitter, 0, 0, 1, 1);

    labelFilterUnit->setBuddy(lineEditFilterUnit);
    labelFilterArea->setBuddy(lineEditFilterArea);
    labelFilterName->setBuddy(lineEditFilterName);
    labelFilterTimestep->setBuddy(lineEditFilterTimestep);
    retranslateUi(EsoForm);

    QMetaObject::connectSlotsByName(EsoForm);
    } // setupUi

    void retranslateUi(QWidget *EsoForm)
    {
    EsoForm->setWindowTitle(QApplication::translate("EsoForm", "Form", 0, QApplication::UnicodeUTF8));
    groupBoxFileInfo->setTitle(QApplication::translate("EsoForm", "File-Information", 0, QApplication::UnicodeUTF8));
    labelFileInfo->setText(QApplication::translate("EsoForm", "TextLabel", 0, QApplication::UnicodeUTF8));
    groupBoxEnvironment->setTitle(QApplication::translate("EsoForm", "Environment", 0, QApplication::UnicodeUTF8));
    groupBoxVariableInfo->setTitle(QApplication::translate("EsoForm", "Variable Information", 0, QApplication::UnicodeUTF8));
    groupBoxVarInfo->setTitle(QApplication::translate("EsoForm", "Total", 0, QApplication::UnicodeUTF8));
    labelMaximum->setText(QApplication::translate("EsoForm", "Maximum:", 0, QApplication::UnicodeUTF8));
    labelAvg->setText(QApplication::translate("EsoForm", "TextLabel", 0, QApplication::UnicodeUTF8));
    labelMin->setText(QApplication::translate("EsoForm", "TextLabel", 0, QApplication::UnicodeUTF8));
    labelAverage->setText(QApplication::translate("EsoForm", "Average:", 0, QApplication::UnicodeUTF8));
    labelMax->setText(QApplication::translate("EsoForm", "TextLabel", 0, QApplication::UnicodeUTF8));
    labelMinimum->setText(QApplication::translate("EsoForm", "Minimum:", 0, QApplication::UnicodeUTF8));
    groupBoxVarInfoLocal->setTitle(QApplication::translate("EsoForm", "Visible", 0, QApplication::UnicodeUTF8));
    labelMaximumLocal->setText(QApplication::translate("EsoForm", "Maximum:", 0, QApplication::UnicodeUTF8));
    labelMaxLocal->setText(QApplication::translate("EsoForm", "TextLabel", 0, QApplication::UnicodeUTF8));
    labelMinimumLocal->setText(QApplication::translate("EsoForm", "Minimum:", 0, QApplication::UnicodeUTF8));
    labelMinLocal->setText(QApplication::translate("EsoForm", "TextLabel", 0, QApplication::UnicodeUTF8));
    labelAverageLocal->setText(QApplication::translate("EsoForm", "Average:", 0, QApplication::UnicodeUTF8));
    labelAvgLocal->setText(QApplication::translate("EsoForm", "TextLabel", 0, QApplication::UnicodeUTF8));
    groupBoxFilter->setTitle(QApplication::translate("EsoForm", "Filter", 0, QApplication::UnicodeUTF8));
    labelFilterUnit->setText(QApplication::translate("EsoForm", "Unit", 0, QApplication::UnicodeUTF8));
    labelFilterArea->setText(QApplication::translate("EsoForm", "Area", 0, QApplication::UnicodeUTF8));
    labelFilterName->setText(QApplication::translate("EsoForm", "Name", 0, QApplication::UnicodeUTF8));
    labelFilterTimestep->setText(QApplication::translate("EsoForm", "Timestep", 0, QApplication::UnicodeUTF8));
    pushButtonFilter->setText(QApplication::translate("EsoForm", "Filter", 0, QApplication::UnicodeUTF8));
    pushButtonClearFilter->setText(QApplication::translate("EsoForm", "Clear", 0, QApplication::UnicodeUTF8));
    pushButtonPrevious->setText(QApplication::translate("EsoForm", "<<", 0, QApplication::UnicodeUTF8));
    pushButtonNext->setText(QApplication::translate("EsoForm", ">>", 0, QApplication::UnicodeUTF8));
    Q_UNUSED(EsoForm);
    } // retranslateUi

};

namespace Ui {
    class EsoForm: public Ui_EsoForm {};
} // namespace Ui

#endif // UI_ESOFORM_H
