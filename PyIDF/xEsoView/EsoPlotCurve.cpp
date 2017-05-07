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

// $Id: EsoPlotCurve.cpp,v 1.3 2006/11/17 21:48:33 cschiefer Exp $

#include "EsoPlotCurve.h"
#include "EsoUtil.h"
#include <QPainter>
#include <QtDebug>
#include <qwt_scale_map.h>
#include <math.h>

EsoPlotCurve::EsoPlotCurve(const QString &title) : QwtPlotCurve(title)
{
	
}


void EsoPlotCurve::draw(QPainter *painter, const QwtScaleMap &xMap, const QwtScaleMap &yMap, int from, int to) const
 {
	for (unsigned i=0; i<m_viFrom.size(); ++i)
	{
	    QwtPlotCurve::draw(painter, xMap, yMap, m_viFrom[i], m_viTo[i]);
	}
 }


//void EsoPlotCurve::setData( float* xData, float* yData, int size)
void EsoPlotCurve::setData( std::vector<float> &xDataF, std::vector<float> &yDataF, int size)
{
	std::vector<double> xData(size);
	std::vector<double> yData(size);
	qDebug() << "EsoPlotCurve::setData";
    m_viFrom.clear();
    m_viTo.clear();
    bool bSkip=true;
    for (int i=0; i<size; ++i)
    {
		xData[i] = xDataF[i];
		yData[i] = yDataF[i];
		if (yData[i] == ESONAN)
		{
			yData[i]=0.0;
    		if (!bSkip)
			    m_viTo.push_back(i-1);
			bSkip=true;
		}
		else
		{
			if (bSkip)
			    m_viFrom.push_back(i);
			bSkip=false;
		}
	}
	if (yData[size-1] != -1111111.1)
		m_viTo.push_back(size-1);
	if (m_viTo.size() != m_viFrom.size())
	{
		qCritical() << "EsoPlotCurve::setData - from and to vector have different sizes! from:"<<m_viFrom.size() <<" to:"<< m_viTo.size();
		m_viTo.resize(m_viFrom.size());
	}
	QwtPlotCurve::setData(&xData[0], &yData[0], size);
}
