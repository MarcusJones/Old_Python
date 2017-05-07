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

// $Id: EsoPlotCurve.h,v 1.3 2006/11/17 21:48:33 cschiefer Exp $

#ifndef ESOPLOTCURVE_H
#define ESOPLOTCURVE_H

#include <qwt_plot_curve.h>
class QPainter;
class QwtScaleMap;

class EsoPlotCurve : public QwtPlotCurve
{
public:
	explicit EsoPlotCurve(const QString &title = QString::null);
	void draw(QPainter *painter, const QwtScaleMap &xMap, const QwtScaleMap &yMap, int from, int to) const;
	void setData( std::vector<float> &xData, std::vector<float> &yData, int size);
private:
	std::vector<int> m_viFrom;
	std::vector<int> m_viTo;
};

#endif
