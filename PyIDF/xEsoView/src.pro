# Diese Datei wurde mit dem qmake-Manager von KDevelop erstellt. 
# ------------------------------------------- 
# Unterordner relativ zum Projektordner: ./src
# Das Target ist eine Anwendung:  

RESOURCES = ../xEsoview.qrc 
RC_FILE = xEsoView.rc 
PRE_TARGETDEPS = ../images/xEsoViewIcon.ico 
TARGETDEPS += ../images/xEsoViewIcon.ico
MOC_DIR = obj 
OBJECTS_DIR = obj 
CONFIG += release \
          warn_on \
          qt 
TEMPLATE = app 
FORMS += esoform.ui \
         options.ui
HEADERS += EsoMainWindow.h \
           EsoView.h \
           EsoVariableInfo.h \
           EsoEnvironment.h \
           EsoParser.h \
           EsoUtil.h \
           EsoVarPlot.h \
           EsoOptions.h \
           EsoScrollZoomer.h \
           EsoScrollBar.h \
           EsoPlotCurve.h \
           EsoBookmark.h \
           Eso.h
SOURCES += EsoMain.cpp \
           EsoMainWindow.cpp \
           EsoView.cpp \
           EsoVariableInfo.cpp \
           EsoEnvironment.cpp \
           EsoParser.cpp \
           EsoUtil.cpp \
           EsoOptions.cpp \
           EsoVarPlot.cpp \
           EsoScrollZoomer.cpp \
           EsoScrollBar.cpp \
           EsoPlotCurve.cpp \
           EsoBookmark.cpp 
VERSION = 0.3.0
win32 {
    DEFINES += QT_DLL QWT_DLL
    LIBS += C:/Programme/Qt/qwt-20060130/lib -lqwt5 \
    -LC:/Programme/Qt/4.1.0/lib
    INCLUDEPATH += C:/Programme/Qt/qwt-20060130/include
    TARGET = ../../bin/xEsoView
    CONFIG -= release

    INCLUDEPATH += .

    OBJECTS_DIR = obj

    MOC_DIR = obj

}
unix {
    LIBS += -lqwt \
            -L/home/christian/work/qwt-5.0.2/lib
    INCLUDEPATH += /home/christian/work/qwt-5.0.2/src

    TARGET = ../bin/xEsoView
    CONFIG -= release

    OBJECTS_DIR = obj

    MOC_DIR = obj

}
