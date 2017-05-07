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
 **************************************************************************/

// $Id: EsoUtil.cpp,v 1.13 2006/11/24 22:15:23 cschiefer Exp $

#include "EsoUtil.h"
#include "EsoBookmark.h"

#include <QDateTime>
#include <QLocale>
#include <QStyle>
#include <QMetaObject>
#include <QSettings>
#include <QtDebug>
#include "qwt_symbol.h"
#include <float.h>
#include <QBuffer>
#include <QFile>
#include <QFileInfo>


QString ConvertToString(EvReportStep const & reportStep)
{
	switch (reportStep)
	{
		case EvDetailed:
			return "Detailed";
		case EvTimeStep:
			return "TimeStep";
		case EvHourly:
			return "Hourly";
		case EvDaily:
			return "Daily";
		case EvMonthly:
			return "Monthly";
		case EvRunPeriod:
			return "RunPeriod";
		default:
			return "";
	}
}

EvDayType ToDayType(QString const & sDayType)
{
	if (sDayType.toLower() == "sunday")
		return EvSunday;
	else if (sDayType.toLower() == "monday")
		return EvMonday;
	else if (sDayType.toLower() == "tuesday")
		return EvTuesday;
	else if (sDayType.toLower() == "wednesday")
		return EvWednesday;
	else if (sDayType.toLower() == "thursday")
		return EvThursday;
	else if (sDayType.toLower() == "friday")
		return EvFriday;
	else if (sDayType.toLower() == "saturday")
		return EvSaturday;
	else if (sDayType.toLower() == "summerdesignday")
		return EvSummerdesignday;
	else if (sDayType.toLower() == "winterdesignday")
		return EvWinterdesignday;
	else if (sDayType.toLower() == "holiday")
		return EvHoliday;
	else if (sDayType.toLower() == "customday1")
		return EvCustomday1;
	else if (sDayType.toLower() == "customday2")
		return EvCustomday2;
	return EvMonday;
}


EvReportStep ToReportStep(QString const & sReportStep)
{
	if (sReportStep.toLower() == "detailed")
		return EvDetailed;
	else if (sReportStep.toLower() == "timestep")
		return EvTimeStep;
	else if (sReportStep.toLower() == "hourly")
		return EvHourly;
	else if (sReportStep.toLower() == "daily")
		return EvDaily;
	else if (sReportStep.toLower() == "monthly")
		return EvMonthly;
	else if (sReportStep.toLower() == "runperiod")
		return EvRunPeriod;

	qWarning() << "Invalid report step string '%s' detected - using 'hourly' instead!" << sReportStep;
	return EvHourly;
}


Qt::DayOfWeek ConvertToQDayOfWeek(EvDayType iDayType)
{
    if (iDayType == EvSunday)
    	return Qt::Sunday;
    else if (iDayType == EvMonday)
        return Qt::Monday;
	else if (iDayType == EvTuesday)
		return Qt::Tuesday;
	else if (iDayType == EvWednesday)
		return Qt::Wednesday;
	else if (iDayType == EvThursday)
		return Qt::Thursday;
	else if (iDayType == EvFriday)
		return Qt::Friday;
	else if (iDayType == EvSaturday)
		return Qt::Saturday;
	else if (iDayType == EvSummerdesignday)
		return Qt::Thursday;
	else if (iDayType == EvWinterdesignday)
		return Qt::Thursday;
	else if (iDayType == EvHoliday)
		return Qt::Sunday;
	else if (iDayType == EvCustomday1)
		return Qt::Sunday;
	else if (iDayType == EvCustomday2)
		return Qt::Sunday;
	else
	{
		qWarning() << "ConvertToQDayOfWeek: invalid day type: " << iDayType;
	}
	return Qt::Monday;
}

QString ConvertToString(double fNum)
{
	//Dont' use locale - use locale according to selected decimal point
	QLocale locale;
	QSettings settings(ESO_ORG, ESO_APP);
	QString sDecimalPoint = settings.value("DecimalPointForCopy", ".").toString();
	if (sDecimalPoint == ",")
		locale = QLocale("de");
	else
		locale = QLocale("C");
	return locale.toString(fNum);
}


QString ConvertToString(QDateTime dt)
{
	//convert according to format from options
	QSettings settings(ESO_ORG, ESO_APP);
	QString sDTFormat = settings.value("DateTimeFormatForCopy", "yyyy-MM-dd hh:mm:ss").toString();
	return dt.toString(sDTFormat);
}


QDateTime ConverttoQDateTime(struct EvTimeStruct ev, int iDefYear)
{
	QDateTime dt;
	if (ev.iMonth == -1) // ev not initialized
	{
		QDate date(1900, 1, 1);
		dt.setDate(date);
		return dt;
	}
	//find year which match week day
	if (iDefYear<1752)
	{
		Qt::DayOfWeek weekday = ConvertToQDayOfWeek(ev.iDayType);
		for (int iYear=2005; iYear>1980; iYear--)
		{

    	   	QDate date(iYear, ev.iMonth, ev.iDayOfMonth);
			dt.setDate(date);
       		if (date.dayOfWeek() == weekday)
				break;
		}
	}
	else
	{
        QDate date(iDefYear, ev.iMonth, ev.iDayOfMonth);
		dt.setDate(date);
	}
	//QTime time( ev.bDST_Indicator? (ev.iHour-1):ev.iHour, ev.iStartMinute);
	QTime time(ev.iHour, ev.iStartMinute);
	dt.setTime(time);
	return dt;
}


int GetCurrentAppStyle()
{
	QString sCurStyle(QApplication::style()->metaObject()->className());
	//remove Q and Style
	sCurStyle.replace(QRegExp("^Q"), "");
	sCurStyle.replace(QRegExp("Style$"), "");
	QStringList styleList = QStyleFactory::keys();
	return styleList.indexOf(sCurStyle);
}


QwtSymbol::Style GetCurrentMarkerStyle()
{
	QSettings settings(ESO_ORG, ESO_APP);
	int iMarkerStyle = settings.value("GraphMarkerStyle", 7).toInt();
	switch (iMarkerStyle)
	{
		case 0:
			return QwtSymbol::Ellipse;
		case 1:
			return QwtSymbol::Rect;
		case 2:
			return QwtSymbol::Diamond;
		case 3:
			return QwtSymbol::DTriangle;
		case 4:
			return QwtSymbol::UTriangle;
		case 5:
			return QwtSymbol::LTriangle;
		case 6:
			return QwtSymbol::RTriangle;
		case 7:
			return QwtSymbol::Cross;
		case 8:
			return QwtSymbol::XCross;
	}
	return QwtSymbol::XCross;
}


float maxIgnNAN(std::vector<float> const & vVal , int iStart, int iEnd)
{
	if (iStart<0)
		iStart=0;
	if (iEnd<0 || iEnd> (int)vVal.size())
		iEnd = (int)vVal.size()-1;
	float fMax=-DBL_MAX;
	for (int i=iStart;i<=iEnd; ++i)
	{
		if (vVal[i]>fMax && vVal[i]!= ESONAN)
		    fMax=vVal[i];
	}
	return fMax;
}


float minIgnNAN(std::vector<float> const & vVal , int iStart, int iEnd)
{
	if (iStart<0)
		iStart=0;
	if (iEnd<0|| iEnd> (int)vVal.size())
		iEnd = (int)vVal.size()-1;
	float fMin=DBL_MAX;
	for (int i=iStart;i<=iEnd; ++i)
	{
		if (vVal[i]<fMin && vVal[i]!= ESONAN)
		    fMin=vVal[i];
	}
	return fMin;
}

float avgIgnNAN(std::vector<float> const & vVal , int iStart, int iEnd)
{
	if (iStart<0)
		iStart=0;
	if (iEnd<0)
		iEnd = (int)vVal.size()-1;
	float fAvg=0.l;
	unsigned iVal=0;
	for (int i=iStart;i<=iEnd; ++i)
	{
		if (vVal[i]!= ESONAN)
		{
			fAvg += vVal[i];
			++iVal;
		}
	}
	if (iVal>0)
		fAvg /= iVal;
	return fAvg;
}

bool GetFlag(QString sFlag, QString sEsoFile)
{
	qDebug() << "GetFlag("<<sFlag << ", "<< sEsoFile <<") - start";
	QSettings settings(ESO_ORG, ESO_APP);
	bool bFlag=true;	
	//read bookmarks
	int iNumRecent = settings.beginReadArray("recent");
	for (int i=0; i< iNumRecent; ++i)
	{
		settings.setArrayIndex(i);
		if (settings.value("fileName").toString() == sEsoFile)
		{
			bFlag = settings.value(sFlag,  false).toBool();
		}
	}
	settings.endArray();	
	qDebug() << "GetFlag("<<sFlag << ", "<< sEsoFile <<") returns "<< bFlag;
	return bFlag;
}


void SetFlag(QString sFlag, QString sEsoFile, bool bFlag)
{
	qDebug() << "SetFlag("<<sFlag << ", "<< sEsoFile <<", "<< bFlag << ") - start";
	
	QSettings settings(ESO_ORG, ESO_APP);
	int iNumRecent = settings.beginReadArray("recent");
	for (int i=0; i< iNumRecent; ++i)
	{
		settings.setArrayIndex(i);
		if (settings.value("fileName").toString() == sEsoFile)
		{
			settings.setValue(sFlag, bFlag);
		}
	}
	settings.endArray();
	qDebug() << "SetFlag("<<sFlag << ", "<< sEsoFile <<", "<< bFlag << ") - end";
}


EsoBookmark GetCurrent( QString sEsoFile)
{
	qDebug() << "GetCurrent(" << sEsoFile <<  ") - start";
	EsoBookmark bm;
	QSettings settings(ESO_ORG, ESO_APP);
	
	int iNumRecent = settings.beginReadArray("recent");
	for (int i=0; i< iNumRecent; ++i)
	{
		settings.setArrayIndex(i);
		if (settings.value("fileName").toString() == sEsoFile)
		{
			QByteArray xb;
			xb = settings.value("current").toByteArray();
			if (xb.isNull() || xb.isEmpty())
				continue;
			QBuffer buf(&xb);
			buf.open(QBuffer::ReadOnly);
			QDataStream x(&buf);
			x >> bm;
		}
	}
	settings.endArray();
	qDebug() << "GetCurrent(" << sEsoFile <<  "): Env:" << bm.GetEnvironment() << " Var:" << bm.GetVariable() << " - end";
	return bm;
}


QList<EsoBookmark> GetRecentBookmarks(QString sEsoFile)
{
	qDebug() << "GetRecentBookmarks(" << sEsoFile <<  ") - start";
	QList<EsoBookmark> vBM;
	QSettings settings(ESO_ORG, ESO_APP);
	
	//read bookmarks
	int iNumRecent = settings.beginReadArray("recent");
	for (int i=0; i< iNumRecent; ++i)
	{
		settings.setArrayIndex(i);
		if (settings.value("fileName").toString() == sEsoFile)
		{
			int iNumBm = settings.beginReadArray("bookmarks");
			for (int iBm = 0; iBm < iNumBm; ++iBm)
			{
				settings.setArrayIndex(iBm);
				QByteArray xb;
				xb = settings.value("bm").toByteArray();
				EsoBookmark bm;
				QBuffer buf(&xb);
				buf.open(QBuffer::ReadOnly);
				QDataStream x(&buf);
				x >> bm;
				vBM.append(bm);
			}
			settings.endArray();	
			break;
		}
	}
	settings.endArray();
	qDebug() << "GetRecentBookmarks(" << sEsoFile <<  ") - end";
	
	return vBM;
}


QVector<QString> GetRecentfiles()
{
	qDebug() << "GetRecentfiles() - start";
	QVector<QString> vRec;
	QSettings settings(ESO_ORG, ESO_APP);
	
	//read recent files
	int iNumRecent = settings.beginReadArray("recent");
	for (int i=0; i< iNumRecent; ++i)
	{
		settings.setArrayIndex(i);
		vRec.push_back(settings.value("fileName").toString());
	}
	settings.endArray();	
	
	qDebug() << "GetRecentfiles() - end";
	return vRec;
}


void SetCurrent( QString sEsoFile, EsoBookmark bm)
{
	qDebug() << "SetCurrent("<< sEsoFile <<") - start";
	QSettings settings(ESO_ORG, ESO_APP);
	int iNumRecent = settings.beginReadArray("recent");
	for (int i=0; i< iNumRecent; ++i)
	{
		settings.setArrayIndex(i);
		if (settings.value("fileName").toString() == sEsoFile)
		{
			QBuffer buf;
			buf.open(QBuffer::WriteOnly);
			QDataStream x(&buf);
			x << bm;
			QVariant qv(buf.data());
			settings.setValue("current", qv);
		}
	}
	settings.endArray();
	qDebug() << "SetCurrent(" << sEsoFile <<  "): Env:" << bm.GetEnvironment() << " Var:" << bm.GetVariable() << " - end";
}


void SetBookmarks(QString sEsoFile, QList<EsoBookmark> vBookmarks)
{
	qDebug() << "SetBookmarks("<< sEsoFile <<") - start";
	
	QSettings settings(ESO_ORG, ESO_APP);
	int iNumRecent = settings.beginReadArray("recent");
	for (int i=0; i< iNumRecent; ++i)
	{
		settings.setArrayIndex(i);
		if (settings.value("fileName").toString() == sEsoFile)
		{
			//write bookmarks
			settings.remove("bookmarks");
			settings.beginWriteArray("bookmarks");
			for (int iBm = 0; iBm < vBookmarks.size(); ++iBm)
			{
				settings.setArrayIndex(iBm);
				QBuffer buf;
				buf.open(QBuffer::WriteOnly);
				QDataStream x(&buf);
				x << vBookmarks[iBm];
				QVariant qv(buf.data());
				settings.setValue("bm", qv);
			}
			settings.endArray();	
		}
	}
	settings.endArray();
	qDebug() << "SetBookmarks("<< sEsoFile <<") - end";
}

void SetRecentfiles(QVector<QString> vsRecent)
{
	qDebug() << "SetRecentfiles() - start";
	//Read all recent files
	QVector<QString> vsRecent_old = GetRecentfiles();
	
	QSettings settings(ESO_ORG, ESO_APP);
	settings.beginGroup("recent");
	
	QStringList keys = settings.allKeys();  //keys look like "1\filename" or "1\viewGrid" or ""1\bookmarks\1\bm
	QMap<QString, QVariant> kv;
	for (int j=0; j<keys.size(); ++j)
	{
		kv[keys[j]] = settings.value(keys[j]);
		//qDebug()<< "SetRecentfiles() - got key:"<< keys[j];
	}
	settings.endGroup();
	
	//find old index
	QMap<int,int> viNewOld;
	for (int i=0; i< vsRecent.size(); ++i)
	{
		viNewOld[i] = -1;
		for (int j=0; j<vsRecent_old.size(); ++j)
		{
			if ( vsRecent_old[j] == vsRecent[i] )
			{
				//qDebug()<< "SetRecentfiles() - new:"<< i << " index old:"<<j ;
				viNewOld[i] = j;
			}
		}
	}
	settings.remove("recent");
	
	//replace index
	settings.beginWriteArray("recent");
	for (int iNew=0; iNew< vsRecent.size(); ++iNew)
	{
		settings.setArrayIndex(iNew);
		QString sKey;
		int iOld = viNewOld[iNew];
		if (iOld>=0)
		{
			//qDebug()<< "SetRecentfiles() - replace old:"<< iOld+1 << " new :"<<iNew+1;
			QString sreg= QString("^%1\\b").arg(iOld+1);
			//qDebug()<< "SetRecentfiles() - sreg:"<< sreg;
			QRegExp rx(sreg);
			for (int j=0; j<keys.size(); ++j)
			{
				sKey = keys[j];
				if (sKey == "size")
					continue;
				//qDebug()<< "SetRecentfiles() - replace old key :"<< sKey;
				if ( rx.indexIn(sKey)>=0 )
				{
					sKey = sKey.replace(rx, "");
					settings.setValue(sKey, kv[keys[j]]);
				}
			}
		}
		else //new entry
		{
			qDebug()<< "SetRecentfiles() - add new entry: '"<< vsRecent[iNew] <<"' at position "<< iNew;
			settings.setValue("filename", vsRecent[iNew]);
		}
	}
	settings.endArray();
}

EvFileType IsxEsoFile(QString sFilename)
{
	QFile file(sFilename);
	if (!file.open(QIODevice::ReadOnly))
	{
		qDebug() << "IsxEsoFile: Can't open file "<< sFilename;
		return EvFileType_Invalid;
	}
	
	QDataStream in(&file);
	quint32 iMagic;
	in >> iMagic;
	if (iMagic == 0x7845736F) //xEso
	{
		file.close();
		qDebug() << "IsxEsoFile - xEso file";
		return EvFileType_xEso;
	}
	
	QTextStream textStream(&file);
	static QRegExp eNumRecs(".*=?\\s*(\\d+)\\s*$", Qt::CaseInsensitive);

	textStream.seek(QFileInfo(file).size()- 26*sizeof(char)); //go to the end - 12 chars
	int iNumLines = 0;
	if (eNumRecs.indexIn(textStream.readLine()) != -1)
	{
		iNumLines = eNumRecs.cap(1).toInt();
	}
	file.close();
	if (iNumLines>0)
	{
		qDebug() << "IsxEsoFile - Eso file with "<< iNumLines << " lines.";
		return EvFileType_Eso;
	}
	
	qDebug() << "IsxEsoFile - Not an xeso nor an eso file: "<< sFilename;
	
	return EvFileType_Invalid;
	
	
}
