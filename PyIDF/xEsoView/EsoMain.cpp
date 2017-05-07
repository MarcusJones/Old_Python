/***************************************************************************
 *   Copyright (C) 2007 	Christian Schiefer, Vienna, Austria 		   *
 *  																	   *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.								   *
 *  																	   *
 *   This program is distributed in the hope that it will be useful,	   *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of 	   *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the  	   *
 *   GNU General Public License for more details.   					   *
 *  																	   *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the  					   *
 *   Free Software Foundation, Inc.,									   *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.  		   *
 ***************************************************************************/

// $Id: EsoMain.cpp,v 1.5 2006/11/17 21:48:33 cschiefer Exp $

#include <QApplication>
#include <QMessageBox>
#include <QDateTime>
#include <QDir>
#include <QTextStream>
#include <QSettings>
#include <QStyleFactory>
#include <QIcon>

#include "Eso.h"
#include "EsoUtil.h"

#include "EsoMainWindow.h"

using namespace std;

QTextStream* logfile;

void myMessageOutput(QtMsgType type, const char* msg)
{
	switch (type)
	{
		case QtDebugMsg:
			*logfile << "Debug: " << msg << endl;
			break;
		case QtWarningMsg:
			*logfile << "Warning: " << msg << endl;
			break;
		case QtCriticalMsg:
			*logfile << "Critical: " << msg << endl;
			break;
		case QtFatalMsg:
			*logfile << "Fatal: " << msg << endl;
			abort();
	}
}




int main(int argc, char* argv[])
{
	QApplication app(argc, argv);
	
	QSettings settings(ESO_ORG, ESO_APP);
	QStringList styleList = QStyleFactory::keys();
	int iStyle = settings.value("ApplicationStyle", -1).toInt();
	if (iStyle > 0 && iStyle < styleList.size())
	{
		QStyle* style = QStyleFactory::create(styleList[iStyle]);
		QApplication::setStyle(style);
	}

	QFileInfo fileInfo(app.applicationDirPath(), "log.txt");
	QFile file(fileInfo.absoluteFilePath());
	if (file.open(QIODevice::Text | QIODevice::WriteOnly | QFile::Truncate))
	{
		logfile = new QTextStream(&file);
		qInstallMsgHandler(myMessageOutput);
	}
	//    Q_INIT_RESOURCE(esoview);
	QDateTime dt = QDateTime::currentDateTime();
	qDebug("Start xEsoView log at %s", dt.toString().toLatin1().data());

	EsoMainWindow mainWin;
	mainWin.setWindowIcon(QIcon(":/images/xEsoViewIconBig.png"));
	mainWin.show();
	if (app.argc() == 2)
	{
		QString sFileArg = app.argv()[1];
		mainWin.loadEso(sFileArg);
	}
	app.exec();
	file.close();
	return 0;
}
