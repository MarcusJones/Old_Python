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

// $Id: EsoBookmark.cpp,v 1.5 2006/11/17 21:48:33 cschiefer Exp $
#include "EsoBookmark.h"
#include <QDataStream>
#include <QString>


EsoBookmark::EsoBookmark()
{
    m_iVariable = -1;
	m_iEnvironment = -1;
	m_iTimeScale = EvViewTotal;
}


EsoBookmark& EsoBookmark::operator =(EsoBookmark const & other)
{
    m_iVariable 	= other.m_iVariable;
	m_iEnvironment 	= other.m_iEnvironment;
	m_iTimeScale 	= other.m_iTimeScale;
	m_sName			= other.m_sName;
	m_zoomRect		= other.m_zoomRect;
	return *this;
}


bool operator==(EsoBookmark const & bm1, EsoBookmark const & bm2)
{
	return (//bm1.m_sName			== bm2.m_sName &&
			bm1.m_iVariable 	== bm2.m_iVariable &&
	        bm1.m_iEnvironment 	== bm2.m_iEnvironment /*&&
			bm1.m_iTimeScale 	== bm2.m_iTimeScale*/);
}

	
void EsoBookmark::SetVariable(int iVariable)
{
	m_iVariable = iVariable;
}


void EsoBookmark::SetEnvironment(int iEnvironment)
{
    m_iEnvironment = iEnvironment;
}


void EsoBookmark::SetTimeScale(EvEsoTimeScaleView timeScale)
{
    m_iTimeScale = timeScale;
}


void EsoBookmark::SetZoomRect(QwtDoubleRect zoomRect)
{
	m_zoomRect = zoomRect;
}


int EsoBookmark::GetVariable() const
{
	return m_iVariable;
}


int EsoBookmark::GetEnvironment() const
{
	return m_iEnvironment;
}


EvEsoTimeScaleView EsoBookmark::GetTimeScale() const
{
	return m_iTimeScale;
}


QwtDoubleRect EsoBookmark::GetZoomRect() const
{
	return m_zoomRect;
}


void EsoBookmark::SetName(QString sName)
{
	m_sName = sName;
}


QString EsoBookmark::GetName() const
{
	return m_sName;
}


QDataStream& operator<<(QDataStream& os, const EsoBookmark& bm)
{
	os << bm.GetName() << (qint32)bm.GetVariable() << (qint32)bm.GetEnvironment() << (qint32)bm.GetTimeScale();
	QwtDoubleRect zr = bm.GetZoomRect();
	os << (qreal)zr.left() << (qreal)zr.top() << (qreal)zr.width() << (qreal)zr.height();
	return os;
}



QDataStream& operator>>(QDataStream& is, EsoBookmark& bm)
{
	QString sTemp;
	is >> sTemp;
	bm.SetName(sTemp);
	qint32 iTemp;
	is >> iTemp;
	bm.SetVariable(iTemp);
	is >> iTemp;
	bm.SetEnvironment(iTemp);
	is >> iTemp;
	bm.SetTimeScale( (EvEsoTimeScaleView)iTemp );
	qreal fLeft;
	qreal fTop; 
	qreal fWidth;
	qreal fHeight;
	is >> fLeft;
	is >> fTop;
	is >> fWidth;
	is >> fHeight;
	bm.SetZoomRect( QwtDoubleRect(fLeft, fTop, fWidth, fHeight) );
	return is;
}
