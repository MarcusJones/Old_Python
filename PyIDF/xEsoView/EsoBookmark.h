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

// $Id: EsoBookmark.h,v 1.4 2006/11/17 21:48:33 cschiefer Exp $
#ifndef ESOBOOKMARK_H
#define ESOBOOKMARK_H

#include "Eso.h"
#include <qwt_double_rect.h>
#include <QString>

class QDataStream;



class EsoBookmark
{
public:
	EsoBookmark();
	void SetVariable(int iVariable);
	void SetEnvironment(int iEnvironment);
	void SetTimeScale(EvEsoTimeScaleView timeScale);
	void SetZoomRect(QwtDoubleRect zoomRect);
	void SetName(QString sName);

	int GetVariable() const;
	int GetEnvironment() const;
	EvEsoTimeScaleView GetTimeScale() const;
	QwtDoubleRect GetZoomRect() const;
	QString GetName() const;

	friend QDataStream& operator<<(QDataStream& os, const EsoBookmark& bm);
  	friend QDataStream& operator>>(QDataStream& is, EsoBookmark& bm);
	friend bool operator==(EsoBookmark const & bm1, EsoBookmark const & bm2);
	/** Assignment operator. */
	EsoBookmark& operator =(EsoBookmark const & other);

private:
    int m_iVariable;
	int m_iEnvironment;
	QString m_sName;
	EvEsoTimeScaleView m_iTimeScale;
	QwtDoubleRect m_zoomRect;
};


#endif
