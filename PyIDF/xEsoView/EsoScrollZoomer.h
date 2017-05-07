/***************************************************************************
 *   Copyright (C) 2007 	Christian Schiefer, Vienna, Austria 		   *
 *   based on the work of the Qwt project - example 'real time plot'       *
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

// $Id: EsoScrollZoomer.h,v 1.6 2006/11/17 21:48:33 cschiefer Exp $

#ifndef ESOSCROLLZOOMER_H
#define ESOSCROLLZOOMER_H

#include <qglobal.h>
#if QT_VERSION < 0x040000
#include <qscrollview.h>
#endif
#include <qwt_plot_zoomer.h>

#include <qdatetime.h>

class ScrollData;
class EsoScrollBar;

class EsoScrollZoomer : public QwtPlotZoomer
{
	Q_OBJECT
public:
	enum ScrollBarPosition { AttachedToScale, OppositeToScale };

	EsoScrollZoomer(QwtPlotCanvas*);
	virtual ~EsoScrollZoomer();

	EsoScrollBar* horizontalScrollBar() const;
	EsoScrollBar* verticalScrollBar() const;

#if QT_VERSION < 0x040000
	void setHScrollBarMode(QScrollView::ScrollBarMode);
	void setVScrollBarMode(QScrollView::ScrollBarMode);

	QScrollView::ScrollBarMode vScrollBarMode() const;
	QScrollView::ScrollBarMode hScrollBarMode() const;
#else
	void setHScrollBarMode(Qt::ScrollBarPolicy);
	void setVScrollBarMode(Qt::ScrollBarPolicy);

	Qt::ScrollBarPolicy vScrollBarMode() const;
	Qt::ScrollBarPolicy hScrollBarMode() const;
#endif

	void setHScrollBarPosition(ScrollBarPosition);
	void setVScrollBarPosition(ScrollBarPosition);

	ScrollBarPosition hScrollBarPosition() const;
	ScrollBarPosition vScrollBarPosition() const;

	QWidget* cornerWidget() const;
	virtual void setCornerWidget(QWidget*); 

	virtual bool eventFilter(QObject*, QEvent*);

	virtual void rescale();

	QDateTime m_startTime;
	
signals:
	void redrawZ();
	
protected:
	virtual EsoScrollBar* scrollBar(Qt::Orientation);
	virtual void updateScrollBars();
	virtual void layoutScrollBars(const QRect&);
	virtual QwtText trackerText(const QwtDoublePoint& pos) const;

private slots:
	void scrollBarMoved(Qt::Orientation o, float min, float max);

private:
	bool needScrollBar(Qt::Orientation) const;
	int oppositeAxis(int) const;

	QWidget* d_cornerWidget;

	ScrollData* d_hScrollData;
	ScrollData* d_vScrollData;

	bool d_inZoom;
};


#endif

