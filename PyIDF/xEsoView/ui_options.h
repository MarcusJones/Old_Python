#ifndef UI_OPTIONS_H
#define UI_OPTIONS_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QComboBox>
#include <QtGui/QDialog>
#include <QtGui/QFrame>
#include <QtGui/QGridLayout>
#include <QtGui/QGroupBox>
#include <QtGui/QHBoxLayout>
#include <QtGui/QLabel>
#include <QtGui/QLineEdit>
#include <QtGui/QPushButton>
#include <QtGui/QSpacerItem>
#include <QtGui/QVBoxLayout>

class Ui_DialogOptions
{
public:
    QGridLayout *gridLayout;
    QGroupBox *groupBoxCopyDataFormat;
    QGridLayout *gridLayout1;
    QVBoxLayout *vboxLayout;
    QHBoxLayout *hboxLayout;
    QLabel *labelDecimalPoint;
    QLineEdit *lineEditDecimalPoint;
    QHBoxLayout *hboxLayout1;
    QLabel *labelDateFormat;
    QLineEdit *lineEditDateFormat;
    QHBoxLayout *hboxLayout2;
    QLabel *labelColumSep;
    QLineEdit *lineEditColumnSep;
    QGroupBox *groupBoxDisplayGraph;
    QGridLayout *gridLayout2;
    QHBoxLayout *hboxLayout3;
    QLabel *label;
    QFrame *frame_BackgroundColor;
    QPushButton *pushButtonColorBackground;
    QHBoxLayout *hboxLayout4;
    QLabel *labelLineColor;
    QFrame *frameLine;
    QGridLayout *gridLayout3;
    QFrame *lineColor;
    QPushButton *pushButtonLineColor;
    QHBoxLayout *hboxLayout5;
    QLabel *labelLineColorMaxMin;
    QFrame *frameLineMaxMin;
    QGridLayout *gridLayout4;
    QFrame *lineColorMaxMin;
    QPushButton *pushButtonLineColorMaxMin;
    QHBoxLayout *hboxLayout6;
    QLabel *labelColorMarker;
    QFrame *frameMarker;
    QGridLayout *gridLayout5;
    QFrame *lineColorMarker;
    QPushButton *pushButtonColorMarker;
    QHBoxLayout *hboxLayout7;
    QLabel *labelMarkerStyle;
    QComboBox *comboBoxMarkerStyle;
    QHBoxLayout *hboxLayout8;
    QSpacerItem *spacerItem;
    QPushButton *okButton;
    QPushButton *cancelButton;
    QGroupBox *groupBoxGeneral;
    QVBoxLayout *vboxLayout1;
    QHBoxLayout *hboxLayout9;
    QLabel *labelAppStyle;
    QComboBox *comboBoxAppStyle;

    void setupUi(QDialog *DialogOptions)
    {
    DialogOptions->setObjectName(QString::fromUtf8("DialogOptions"));
    DialogOptions->resize(QSize(369, 455).expandedTo(DialogOptions->minimumSizeHint()));
    DialogOptions->setWindowIcon(QIcon(QString::fromUtf8(":/images/xEsoViewIconBig.png")));
    DialogOptions->setModal(true);
    gridLayout = new QGridLayout(DialogOptions);
    gridLayout->setSpacing(6);
    gridLayout->setMargin(9);
    gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
    groupBoxCopyDataFormat = new QGroupBox(DialogOptions);
    groupBoxCopyDataFormat->setObjectName(QString::fromUtf8("groupBoxCopyDataFormat"));
    groupBoxCopyDataFormat->setAcceptDrops(false);
    gridLayout1 = new QGridLayout(groupBoxCopyDataFormat);
    gridLayout1->setSpacing(6);
    gridLayout1->setMargin(9);
    gridLayout1->setObjectName(QString::fromUtf8("gridLayout1"));
    vboxLayout = new QVBoxLayout();
    vboxLayout->setSpacing(6);
    vboxLayout->setMargin(0);
    vboxLayout->setObjectName(QString::fromUtf8("vboxLayout"));
    hboxLayout = new QHBoxLayout();
    hboxLayout->setSpacing(6);
    hboxLayout->setMargin(0);
    hboxLayout->setObjectName(QString::fromUtf8("hboxLayout"));
    labelDecimalPoint = new QLabel(groupBoxCopyDataFormat);
    labelDecimalPoint->setObjectName(QString::fromUtf8("labelDecimalPoint"));
    labelDecimalPoint->setMinimumSize(QSize(150, 0));

    hboxLayout->addWidget(labelDecimalPoint);

    lineEditDecimalPoint = new QLineEdit(groupBoxCopyDataFormat);
    lineEditDecimalPoint->setObjectName(QString::fromUtf8("lineEditDecimalPoint"));
    lineEditDecimalPoint->setEnabled(true);

    hboxLayout->addWidget(lineEditDecimalPoint);


    vboxLayout->addLayout(hboxLayout);

    hboxLayout1 = new QHBoxLayout();
    hboxLayout1->setSpacing(6);
    hboxLayout1->setMargin(0);
    hboxLayout1->setObjectName(QString::fromUtf8("hboxLayout1"));
    labelDateFormat = new QLabel(groupBoxCopyDataFormat);
    labelDateFormat->setObjectName(QString::fromUtf8("labelDateFormat"));
    labelDateFormat->setMinimumSize(QSize(150, 0));

    hboxLayout1->addWidget(labelDateFormat);

    lineEditDateFormat = new QLineEdit(groupBoxCopyDataFormat);
    lineEditDateFormat->setObjectName(QString::fromUtf8("lineEditDateFormat"));
    lineEditDateFormat->setEnabled(true);

    hboxLayout1->addWidget(lineEditDateFormat);


    vboxLayout->addLayout(hboxLayout1);

    hboxLayout2 = new QHBoxLayout();
    hboxLayout2->setSpacing(6);
    hboxLayout2->setMargin(0);
    hboxLayout2->setObjectName(QString::fromUtf8("hboxLayout2"));
    labelColumSep = new QLabel(groupBoxCopyDataFormat);
    labelColumSep->setObjectName(QString::fromUtf8("labelColumSep"));
    labelColumSep->setMinimumSize(QSize(150, 0));

    hboxLayout2->addWidget(labelColumSep);

    lineEditColumnSep = new QLineEdit(groupBoxCopyDataFormat);
    lineEditColumnSep->setObjectName(QString::fromUtf8("lineEditColumnSep"));

    hboxLayout2->addWidget(lineEditColumnSep);


    vboxLayout->addLayout(hboxLayout2);


    gridLayout1->addLayout(vboxLayout, 0, 0, 1, 1);


    gridLayout->addWidget(groupBoxCopyDataFormat, 0, 0, 1, 1);

    groupBoxDisplayGraph = new QGroupBox(DialogOptions);
    groupBoxDisplayGraph->setObjectName(QString::fromUtf8("groupBoxDisplayGraph"));
    QSizePolicy sizePolicy(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy.setHorizontalStretch(0);
    sizePolicy.setVerticalStretch(0);
    sizePolicy.setHeightForWidth(groupBoxDisplayGraph->sizePolicy().hasHeightForWidth());
    groupBoxDisplayGraph->setSizePolicy(sizePolicy);
    gridLayout2 = new QGridLayout(groupBoxDisplayGraph);
    gridLayout2->setSpacing(6);
    gridLayout2->setMargin(9);
    gridLayout2->setObjectName(QString::fromUtf8("gridLayout2"));
    hboxLayout3 = new QHBoxLayout();
    hboxLayout3->setSpacing(6);
    hboxLayout3->setMargin(0);
    hboxLayout3->setObjectName(QString::fromUtf8("hboxLayout3"));
    label = new QLabel(groupBoxDisplayGraph);
    label->setObjectName(QString::fromUtf8("label"));
    label->setMinimumSize(QSize(150, 0));
    label->setMaximumSize(QSize(120, 16777215));

    hboxLayout3->addWidget(label);

    frame_BackgroundColor = new QFrame(groupBoxDisplayGraph);
    frame_BackgroundColor->setObjectName(QString::fromUtf8("frame_BackgroundColor"));
    QSizePolicy sizePolicy1(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy1.setHorizontalStretch(0);
    sizePolicy1.setVerticalStretch(0);
    sizePolicy1.setHeightForWidth(frame_BackgroundColor->sizePolicy().hasHeightForWidth());
    frame_BackgroundColor->setSizePolicy(sizePolicy1);
    QPalette palette;
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(0), QColor(0, 0, 0));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(1), QColor(221, 223, 228));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(2), QColor(255, 255, 255));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(3), QColor(255, 255, 255));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(4), QColor(85, 85, 85));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(5), QColor(199, 199, 199));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(6), QColor(0, 0, 0));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(7), QColor(255, 255, 255));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(8), QColor(0, 0, 0));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(9), QColor(255, 255, 255));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(10), QColor(239, 239, 239));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(11), QColor(0, 0, 0));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(12), QColor(103, 141, 178));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(13), QColor(255, 255, 255));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(14), QColor(0, 0, 238));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(15), QColor(82, 24, 139));
    palette.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(16), QColor(232, 232, 232));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(0), QColor(0, 0, 0));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(1), QColor(221, 223, 228));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(2), QColor(255, 255, 255));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(3), QColor(255, 255, 255));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(4), QColor(85, 85, 85));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(5), QColor(199, 199, 199));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(6), QColor(0, 0, 0));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(7), QColor(255, 255, 255));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(8), QColor(0, 0, 0));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(9), QColor(255, 255, 255));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(10), QColor(239, 239, 239));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(11), QColor(0, 0, 0));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(12), QColor(103, 141, 178));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(13), QColor(255, 255, 255));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(14), QColor(0, 0, 238));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(15), QColor(82, 24, 139));
    palette.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(16), QColor(232, 232, 232));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(0), QColor(128, 128, 128));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(1), QColor(221, 223, 228));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(2), QColor(255, 255, 255));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(3), QColor(255, 255, 255));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(4), QColor(85, 85, 85));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(5), QColor(199, 199, 199));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(6), QColor(199, 199, 199));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(7), QColor(255, 255, 255));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(8), QColor(128, 128, 128));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(9), QColor(239, 239, 239));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(10), QColor(239, 239, 239));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(11), QColor(0, 0, 0));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(12), QColor(86, 117, 148));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(13), QColor(255, 255, 255));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(14), QColor(0, 0, 238));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(15), QColor(82, 24, 139));
    palette.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(16), QColor(232, 232, 232));
    frame_BackgroundColor->setPalette(palette);
    frame_BackgroundColor->setAutoFillBackground(true);
    frame_BackgroundColor->setFrameShape(QFrame::StyledPanel);
    frame_BackgroundColor->setFrameShadow(QFrame::Raised);

    hboxLayout3->addWidget(frame_BackgroundColor);

    pushButtonColorBackground = new QPushButton(groupBoxDisplayGraph);
    pushButtonColorBackground->setObjectName(QString::fromUtf8("pushButtonColorBackground"));
    QSizePolicy sizePolicy2(static_cast<QSizePolicy::Policy>(1), static_cast<QSizePolicy::Policy>(0));
    sizePolicy2.setHorizontalStretch(0);
    sizePolicy2.setVerticalStretch(0);
    sizePolicy2.setHeightForWidth(pushButtonColorBackground->sizePolicy().hasHeightForWidth());
    pushButtonColorBackground->setSizePolicy(sizePolicy2);
    pushButtonColorBackground->setMinimumSize(QSize(80, 0));

    hboxLayout3->addWidget(pushButtonColorBackground);


    gridLayout2->addLayout(hboxLayout3, 0, 0, 1, 1);

    hboxLayout4 = new QHBoxLayout();
    hboxLayout4->setSpacing(6);
    hboxLayout4->setMargin(0);
    hboxLayout4->setObjectName(QString::fromUtf8("hboxLayout4"));
    labelLineColor = new QLabel(groupBoxDisplayGraph);
    labelLineColor->setObjectName(QString::fromUtf8("labelLineColor"));
    labelLineColor->setMinimumSize(QSize(150, 0));

    hboxLayout4->addWidget(labelLineColor);

    frameLine = new QFrame(groupBoxDisplayGraph);
    frameLine->setObjectName(QString::fromUtf8("frameLine"));
    QSizePolicy sizePolicy3(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy3.setHorizontalStretch(0);
    sizePolicy3.setVerticalStretch(0);
    sizePolicy3.setHeightForWidth(frameLine->sizePolicy().hasHeightForWidth());
    frameLine->setSizePolicy(sizePolicy3);
    frameLine->setMinimumSize(QSize(40, 16));
    QPalette palette1;
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(0), QColor(0, 0, 0));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(1), QColor(221, 223, 228));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(2), QColor(255, 255, 255));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(3), QColor(255, 255, 255));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(4), QColor(85, 85, 85));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(5), QColor(199, 199, 199));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(6), QColor(0, 0, 0));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(7), QColor(255, 255, 255));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(8), QColor(0, 0, 0));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(9), QColor(255, 255, 255));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(10), QColor(239, 239, 239));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(11), QColor(0, 0, 0));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(12), QColor(103, 141, 178));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(13), QColor(255, 255, 255));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(14), QColor(0, 0, 238));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(15), QColor(82, 24, 139));
    palette1.setColor(QPalette::Active, static_cast<QPalette::ColorRole>(16), QColor(232, 232, 232));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(0), QColor(0, 0, 0));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(1), QColor(221, 223, 228));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(2), QColor(255, 255, 255));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(3), QColor(255, 255, 255));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(4), QColor(85, 85, 85));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(5), QColor(199, 199, 199));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(6), QColor(0, 0, 0));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(7), QColor(255, 255, 255));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(8), QColor(0, 0, 0));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(9), QColor(255, 255, 255));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(10), QColor(239, 239, 239));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(11), QColor(0, 0, 0));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(12), QColor(103, 141, 178));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(13), QColor(255, 255, 255));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(14), QColor(0, 0, 238));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(15), QColor(82, 24, 139));
    palette1.setColor(QPalette::Inactive, static_cast<QPalette::ColorRole>(16), QColor(232, 232, 232));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(0), QColor(128, 128, 128));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(1), QColor(221, 223, 228));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(2), QColor(255, 255, 255));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(3), QColor(255, 255, 255));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(4), QColor(85, 85, 85));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(5), QColor(199, 199, 199));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(6), QColor(199, 199, 199));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(7), QColor(255, 255, 255));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(8), QColor(128, 128, 128));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(9), QColor(239, 239, 239));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(10), QColor(239, 239, 239));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(11), QColor(0, 0, 0));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(12), QColor(86, 117, 148));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(13), QColor(255, 255, 255));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(14), QColor(0, 0, 238));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(15), QColor(82, 24, 139));
    palette1.setColor(QPalette::Disabled, static_cast<QPalette::ColorRole>(16), QColor(232, 232, 232));
    frameLine->setPalette(palette1);
    frameLine->setFrameShape(QFrame::StyledPanel);
    frameLine->setFrameShadow(QFrame::Raised);
    gridLayout3 = new QGridLayout(frameLine);
    gridLayout3->setSpacing(6);
    gridLayout3->setMargin(9);
    gridLayout3->setObjectName(QString::fromUtf8("gridLayout3"));
    lineColor = new QFrame(frameLine);
    lineColor->setObjectName(QString::fromUtf8("lineColor"));
    lineColor->setFrameShape(QFrame::HLine);

    gridLayout3->addWidget(lineColor, 0, 0, 1, 1);


    hboxLayout4->addWidget(frameLine);

    pushButtonLineColor = new QPushButton(groupBoxDisplayGraph);
    pushButtonLineColor->setObjectName(QString::fromUtf8("pushButtonLineColor"));
    QSizePolicy sizePolicy4(static_cast<QSizePolicy::Policy>(1), static_cast<QSizePolicy::Policy>(0));
    sizePolicy4.setHorizontalStretch(0);
    sizePolicy4.setVerticalStretch(0);
    sizePolicy4.setHeightForWidth(pushButtonLineColor->sizePolicy().hasHeightForWidth());
    pushButtonLineColor->setSizePolicy(sizePolicy4);
    pushButtonLineColor->setMinimumSize(QSize(80, 0));

    hboxLayout4->addWidget(pushButtonLineColor);


    gridLayout2->addLayout(hboxLayout4, 1, 0, 1, 1);

    hboxLayout5 = new QHBoxLayout();
    hboxLayout5->setSpacing(6);
    hboxLayout5->setMargin(0);
    hboxLayout5->setObjectName(QString::fromUtf8("hboxLayout5"));
    labelLineColorMaxMin = new QLabel(groupBoxDisplayGraph);
    labelLineColorMaxMin->setObjectName(QString::fromUtf8("labelLineColorMaxMin"));
    labelLineColorMaxMin->setMinimumSize(QSize(150, 0));

    hboxLayout5->addWidget(labelLineColorMaxMin);

    frameLineMaxMin = new QFrame(groupBoxDisplayGraph);
    frameLineMaxMin->setObjectName(QString::fromUtf8("frameLineMaxMin"));
    QSizePolicy sizePolicy5(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy5.setHorizontalStretch(0);
    sizePolicy5.setVerticalStretch(0);
    sizePolicy5.setHeightForWidth(frameLineMaxMin->sizePolicy().hasHeightForWidth());
    frameLineMaxMin->setSizePolicy(sizePolicy5);
    frameLineMaxMin->setMinimumSize(QSize(40, 16));
    frameLineMaxMin->setFrameShape(QFrame::StyledPanel);
    frameLineMaxMin->setFrameShadow(QFrame::Raised);
    gridLayout4 = new QGridLayout(frameLineMaxMin);
    gridLayout4->setSpacing(6);
    gridLayout4->setMargin(9);
    gridLayout4->setObjectName(QString::fromUtf8("gridLayout4"));
    lineColorMaxMin = new QFrame(frameLineMaxMin);
    lineColorMaxMin->setObjectName(QString::fromUtf8("lineColorMaxMin"));
    lineColorMaxMin->setFrameShape(QFrame::HLine);

    gridLayout4->addWidget(lineColorMaxMin, 0, 0, 1, 1);


    hboxLayout5->addWidget(frameLineMaxMin);

    pushButtonLineColorMaxMin = new QPushButton(groupBoxDisplayGraph);
    pushButtonLineColorMaxMin->setObjectName(QString::fromUtf8("pushButtonLineColorMaxMin"));
    QSizePolicy sizePolicy6(static_cast<QSizePolicy::Policy>(1), static_cast<QSizePolicy::Policy>(0));
    sizePolicy6.setHorizontalStretch(0);
    sizePolicy6.setVerticalStretch(0);
    sizePolicy6.setHeightForWidth(pushButtonLineColorMaxMin->sizePolicy().hasHeightForWidth());
    pushButtonLineColorMaxMin->setSizePolicy(sizePolicy6);
    pushButtonLineColorMaxMin->setMinimumSize(QSize(80, 0));

    hboxLayout5->addWidget(pushButtonLineColorMaxMin);


    gridLayout2->addLayout(hboxLayout5, 2, 0, 1, 1);

    hboxLayout6 = new QHBoxLayout();
    hboxLayout6->setSpacing(6);
    hboxLayout6->setMargin(0);
    hboxLayout6->setObjectName(QString::fromUtf8("hboxLayout6"));
    labelColorMarker = new QLabel(groupBoxDisplayGraph);
    labelColorMarker->setObjectName(QString::fromUtf8("labelColorMarker"));
    labelColorMarker->setMinimumSize(QSize(150, 0));

    hboxLayout6->addWidget(labelColorMarker);

    frameMarker = new QFrame(groupBoxDisplayGraph);
    frameMarker->setObjectName(QString::fromUtf8("frameMarker"));
    QSizePolicy sizePolicy7(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(5));
    sizePolicy7.setHorizontalStretch(0);
    sizePolicy7.setVerticalStretch(0);
    sizePolicy7.setHeightForWidth(frameMarker->sizePolicy().hasHeightForWidth());
    frameMarker->setSizePolicy(sizePolicy7);
    frameMarker->setMinimumSize(QSize(40, 16));
    frameMarker->setFrameShape(QFrame::StyledPanel);
    frameMarker->setFrameShadow(QFrame::Raised);
    gridLayout5 = new QGridLayout(frameMarker);
    gridLayout5->setSpacing(6);
    gridLayout5->setMargin(9);
    gridLayout5->setObjectName(QString::fromUtf8("gridLayout5"));
    lineColorMarker = new QFrame(frameMarker);
    lineColorMarker->setObjectName(QString::fromUtf8("lineColorMarker"));
    lineColorMarker->setFrameShape(QFrame::HLine);

    gridLayout5->addWidget(lineColorMarker, 0, 0, 1, 1);


    hboxLayout6->addWidget(frameMarker);

    pushButtonColorMarker = new QPushButton(groupBoxDisplayGraph);
    pushButtonColorMarker->setObjectName(QString::fromUtf8("pushButtonColorMarker"));
    QSizePolicy sizePolicy8(static_cast<QSizePolicy::Policy>(1), static_cast<QSizePolicy::Policy>(0));
    sizePolicy8.setHorizontalStretch(0);
    sizePolicy8.setVerticalStretch(0);
    sizePolicy8.setHeightForWidth(pushButtonColorMarker->sizePolicy().hasHeightForWidth());
    pushButtonColorMarker->setSizePolicy(sizePolicy8);
    pushButtonColorMarker->setMinimumSize(QSize(80, 0));

    hboxLayout6->addWidget(pushButtonColorMarker);


    gridLayout2->addLayout(hboxLayout6, 3, 0, 1, 1);

    hboxLayout7 = new QHBoxLayout();
    hboxLayout7->setSpacing(6);
    hboxLayout7->setMargin(0);
    hboxLayout7->setObjectName(QString::fromUtf8("hboxLayout7"));
    labelMarkerStyle = new QLabel(groupBoxDisplayGraph);
    labelMarkerStyle->setObjectName(QString::fromUtf8("labelMarkerStyle"));
    labelMarkerStyle->setMinimumSize(QSize(150, 0));

    hboxLayout7->addWidget(labelMarkerStyle);

    comboBoxMarkerStyle = new QComboBox(groupBoxDisplayGraph);
    comboBoxMarkerStyle->setObjectName(QString::fromUtf8("comboBoxMarkerStyle"));
    QSizePolicy sizePolicy9(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(0));
    sizePolicy9.setHorizontalStretch(0);
    sizePolicy9.setVerticalStretch(0);
    sizePolicy9.setHeightForWidth(comboBoxMarkerStyle->sizePolicy().hasHeightForWidth());
    comboBoxMarkerStyle->setSizePolicy(sizePolicy9);

    hboxLayout7->addWidget(comboBoxMarkerStyle);


    gridLayout2->addLayout(hboxLayout7, 4, 0, 1, 1);


    gridLayout->addWidget(groupBoxDisplayGraph, 1, 0, 1, 1);

    hboxLayout8 = new QHBoxLayout();
    hboxLayout8->setSpacing(6);
    hboxLayout8->setMargin(0);
    hboxLayout8->setObjectName(QString::fromUtf8("hboxLayout8"));
    spacerItem = new QSpacerItem(131, 31, QSizePolicy::Expanding, QSizePolicy::Minimum);

    hboxLayout8->addItem(spacerItem);

    okButton = new QPushButton(DialogOptions);
    okButton->setObjectName(QString::fromUtf8("okButton"));

    hboxLayout8->addWidget(okButton);

    cancelButton = new QPushButton(DialogOptions);
    cancelButton->setObjectName(QString::fromUtf8("cancelButton"));

    hboxLayout8->addWidget(cancelButton);


    gridLayout->addLayout(hboxLayout8, 3, 0, 1, 1);

    groupBoxGeneral = new QGroupBox(DialogOptions);
    groupBoxGeneral->setObjectName(QString::fromUtf8("groupBoxGeneral"));
    groupBoxGeneral->setAlignment(Qt::AlignLeading);
    vboxLayout1 = new QVBoxLayout(groupBoxGeneral);
    vboxLayout1->setSpacing(6);
    vboxLayout1->setMargin(9);
    vboxLayout1->setObjectName(QString::fromUtf8("vboxLayout1"));
    hboxLayout9 = new QHBoxLayout();
    hboxLayout9->setSpacing(6);
    hboxLayout9->setMargin(0);
    hboxLayout9->setObjectName(QString::fromUtf8("hboxLayout9"));
    labelAppStyle = new QLabel(groupBoxGeneral);
    labelAppStyle->setObjectName(QString::fromUtf8("labelAppStyle"));
    labelAppStyle->setMinimumSize(QSize(150, 0));

    hboxLayout9->addWidget(labelAppStyle);

    comboBoxAppStyle = new QComboBox(groupBoxGeneral);
    comboBoxAppStyle->setObjectName(QString::fromUtf8("comboBoxAppStyle"));
    QSizePolicy sizePolicy10(static_cast<QSizePolicy::Policy>(7), static_cast<QSizePolicy::Policy>(0));
    sizePolicy10.setHorizontalStretch(0);
    sizePolicy10.setVerticalStretch(0);
    sizePolicy10.setHeightForWidth(comboBoxAppStyle->sizePolicy().hasHeightForWidth());
    comboBoxAppStyle->setSizePolicy(sizePolicy10);

    hboxLayout9->addWidget(comboBoxAppStyle);


    vboxLayout1->addLayout(hboxLayout9);


    gridLayout->addWidget(groupBoxGeneral, 2, 0, 1, 1);

    labelDecimalPoint->setBuddy(lineEditDecimalPoint);
    labelDateFormat->setBuddy(lineEditDateFormat);
    labelColumSep->setBuddy(lineEditColumnSep);
    label->setBuddy(pushButtonColorBackground);
    labelLineColor->setBuddy(pushButtonLineColor);
    labelLineColorMaxMin->setBuddy(pushButtonLineColorMaxMin);
    labelColorMarker->setBuddy(pushButtonColorMarker);
    labelAppStyle->setBuddy(comboBoxAppStyle);
    QWidget::setTabOrder(lineEditDecimalPoint, lineEditDateFormat);
    QWidget::setTabOrder(lineEditDateFormat, lineEditColumnSep);
    QWidget::setTabOrder(lineEditColumnSep, pushButtonColorBackground);
    QWidget::setTabOrder(pushButtonColorBackground, pushButtonLineColor);
    QWidget::setTabOrder(pushButtonLineColor, pushButtonLineColorMaxMin);
    QWidget::setTabOrder(pushButtonLineColorMaxMin, pushButtonColorMarker);
    QWidget::setTabOrder(pushButtonColorMarker, comboBoxMarkerStyle);
    QWidget::setTabOrder(comboBoxMarkerStyle, comboBoxAppStyle);
    QWidget::setTabOrder(comboBoxAppStyle, okButton);
    QWidget::setTabOrder(okButton, cancelButton);
    retranslateUi(DialogOptions);
    QObject::connect(okButton, SIGNAL(clicked()), DialogOptions, SLOT(accept()));
    QObject::connect(cancelButton, SIGNAL(clicked()), DialogOptions, SLOT(reject()));

    QMetaObject::connectSlotsByName(DialogOptions);
    } // setupUi

    void retranslateUi(QDialog *DialogOptions)
    {
    DialogOptions->setWindowTitle(QApplication::translate("DialogOptions", "xEsoView - Options", 0, QApplication::UnicodeUTF8));
    groupBoxCopyDataFormat->setTitle(QApplication::translate("DialogOptions", "Settings for copying data", 0, QApplication::UnicodeUTF8));
    labelDecimalPoint->setText(QApplication::translate("DialogOptions", "Decimal point character", 0, QApplication::UnicodeUTF8));
    lineEditDecimalPoint->setToolTip(QApplication::translate("DialogOptions", "Set decimal point character", 0, QApplication::UnicodeUTF8));
    lineEditDecimalPoint->setText(QApplication::translate("DialogOptions", ",", 0, QApplication::UnicodeUTF8));
    labelDateFormat->setText(QApplication::translate("DialogOptions", "Date/Time format", 0, QApplication::UnicodeUTF8));
    lineEditDateFormat->setToolTip(QApplication::translate("DialogOptions", "Set the time format string e.g. \"yyyy-MM-dd hh:mm\"", 0, QApplication::UnicodeUTF8));
    labelColumSep->setText(QApplication::translate("DialogOptions", "Column separator", 0, QApplication::UnicodeUTF8));
    lineEditColumnSep->setToolTip(QApplication::translate("DialogOptions", "Set column separator", 0, QApplication::UnicodeUTF8));
    groupBoxDisplayGraph->setTitle(QApplication::translate("DialogOptions", "Settings for displaying the graph", 0, QApplication::UnicodeUTF8));
    label->setText(QApplication::translate("DialogOptions", "Background color", 0, QApplication::UnicodeUTF8));
    pushButtonColorBackground->setText(QApplication::translate("DialogOptions", "Select color ...", 0, QApplication::UnicodeUTF8));
    labelLineColor->setText(QApplication::translate("DialogOptions", "Line color", 0, QApplication::UnicodeUTF8));
    pushButtonLineColor->setText(QApplication::translate("DialogOptions", "Select color ...", 0, QApplication::UnicodeUTF8));
    labelLineColorMaxMin->setText(QApplication::translate("DialogOptions", "Line color for max/min", 0, QApplication::UnicodeUTF8));
    pushButtonLineColorMaxMin->setText(QApplication::translate("DialogOptions", "Select color ...", 0, QApplication::UnicodeUTF8));
    labelColorMarker->setText(QApplication::translate("DialogOptions", "Marker color", 0, QApplication::UnicodeUTF8));
    pushButtonColorMarker->setText(QApplication::translate("DialogOptions", "Select color ...", 0, QApplication::UnicodeUTF8));
    labelMarkerStyle->setText(QApplication::translate("DialogOptions", "Marker style", 0, QApplication::UnicodeUTF8));
    okButton->setText(QApplication::translate("DialogOptions", "OK", 0, QApplication::UnicodeUTF8));
    cancelButton->setText(QApplication::translate("DialogOptions", "Cancel", 0, QApplication::UnicodeUTF8));
    groupBoxGeneral->setTitle(QApplication::translate("DialogOptions", "General settings", 0, QApplication::UnicodeUTF8));
    labelAppStyle->setText(QApplication::translate("DialogOptions", "Application style", 0, QApplication::UnicodeUTF8));
    comboBoxAppStyle->setToolTip(QApplication::translate("DialogOptions", "The changes become effective after restarting the application.", 0, QApplication::UnicodeUTF8));
    comboBoxAppStyle->setStatusTip(QApplication::translate("DialogOptions", "", 0, QApplication::UnicodeUTF8));
    Q_UNUSED(DialogOptions);
    } // retranslateUi

};

namespace Ui {
    class DialogOptions: public Ui_DialogOptions {};
} // namespace Ui

#endif // UI_OPTIONS_H
