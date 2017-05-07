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

// $Id: EsoUtil.h,v 1.11 2006/11/17 21:48:33 cschiefer Exp $

#ifndef EVESOUTIL_H
#define EVESOUTIL_H

//Includes
#include <sstream>
#include <iomanip>
#include <QList>
#include <QString>
#include <QApplication>
#include <QStyleFactory>

#include "Eso.h"
#include "EsoVariableInfo.h"
#include "qwt_symbol.h"

#include "EsoBookmark.h"

class QDateTime;
QString ConvertToString(double fNum);
QString ConvertToString(QDateTime dt);

QDateTime ConverttoQDateTime(struct EvTimeStruct, int iYear=-1);
Qt::DayOfWeek ConvertToQDayOfWeek(EvDayType iDayType);

int GetCurrentAppStyle();
QwtSymbol::Style GetCurrentMarkerStyle();


//! Convert report step string to enum.
EvReportStep ToReportStep(QString const & sReportStep);

//! Convert report step enum to string.
QString ConvertToString(EvReportStep const & reportStep);

EvDayType ToDayType(QString const & sDayType);

//! Calculate maximum (ignore NANs).
float maxIgnNAN(std::vector<float> const & vVal , int iStart=-1, int iEnd=-1);

//! Calculate minimum (ignore NANs).
float minIgnNAN(std::vector<float> const & vVal , int iStart=-1, int iEnd=-1);

//! Calculate average (ignore NANs).
float avgIgnNAN(std::vector<float> const & vVal , int iStart=-1, int iEnd=-1);

//! Get recent files from config.
QVector<QString> GetRecentfiles();

//! Set recent files in config.
void SetRecentfiles(QVector<QString> vsRecent);

//! Get bookmarks of recent file from config.
QList<EsoBookmark> GetRecentBookmarks(QString sEsoFile);

//! Set bookmarks of recent file in config.
void SetBookmarks(QString sEsoFile, QList<EsoBookmark> vBookmarks);

//! Get current view as bookmark in config.
EsoBookmark GetCurrent( QString sEsoFile);

//! Set current view as bookmark in config.
void SetCurrent( QString sEsoFile, EsoBookmark bm);

//! Get flag from config.
bool GetFlag(QString sFlag, QString sEsoFile);

//! Set flag in config.
void SetFlag(QString sFlag, QString sEsoFile, bool bFlag);

//!Check if specified file is an eso or xEso file returns 
//! EvFileType_Invalid if file is not an eso nor an xeso file,
//! EvFileType_NotFound if file is not found or could not be opened,
//! EvFileType_Eso if it is an eso file, 
//! EvFileType_xEso if it is an xeso file
EvFileType IsxEsoFile(QString sFilename);
#endif

