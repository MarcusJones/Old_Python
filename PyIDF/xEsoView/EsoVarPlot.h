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

// $Id: EsoVarPlot.h,v 1.13 2007/02/27 21:18:22 cschiefer Exp $

#ifndef EVESOVARPLOT_H
#define EVESOVARPLOT_H
#include <QDateTime>
#include <qwt_plot.h>
#include "EsoPlotCurve.h"
#include <qwt_scale_draw.h>
#include "EsoView.h"

class EsoParser;
class EsoScrollZoomer;
class QwtPlotMarker;
class QwtPlotGrid;
class QPixmap;
class EsoBookmark;


class EsoVarPlot : public QWidget
{
	Q_OBJECT
public:
	EsoVarPlot(QWidget* parent, QwtPlot* plot);
	virtual ~EsoVarPlot();
	void SetParser(EsoParser* parser);
	void Plot();
	void SetQwtPlot(QwtPlot*);
	QwtPlot* GetQwtPlot();
	void viewMin(bool bView);
	bool viewMin();
	void viewMax(bool bView);
	bool viewMax();
	void viewMarkers(bool bView);
	bool viewMarkers();
	void viewGrid(bool bView);
	bool viewGrid();
	QString getDataAsText(bool bIncludeTime);
	QPixmap getPixmap();
	float getMax() const;
	float getMin() const;
	float getAvg() const;
	QString getTitle() const;
	int getVariable() const;
	int getEnvironment() const;
	EvEsoTimeScaleView getTimeScale() const;
	void print(QPaintDevice& p, const QwtPlotPrintFilter & = QwtPlotPrintFilter()) const;
	QwtDoubleRect GetZoomRect() const;
	EsoBookmark GetCurrentAsBookmark() const;
	void SetCurrent(EsoBookmark bm);
	QString getStart() const;
	QString getEnd() const;
	QString getStartLocal() const;
	QString getEndLocal() const;
	float getMaxLocal() const;
	float getMinLocal() const;
	float getAvgLocal() const;
	void GetStartEndIndex(QwtDoubleRect window, int & iStartIndex, int & iEndIndex) const;
	void UpdateTimeLabelFormat();
	void Redraw();
	void setSelection(int iVar, bool bSel);	
	EsoScrollZoomer* m_zoomer;
	
public slots:
	void setCurrentEnvironment(int iEnvironmentIndex);
	void setCurrentVariable(int iVariableIndex);
	void setCurrentTimeScale(EvEsoTimeScaleView iTimeScale);
	void pushButtonBack_clicked();
	void pushButtonForward_clicked();
	void redrawP();

signals:
	void updateVarInfo();
	void redraw();

private:
	int m_iEnvironment;
	int m_iVariable;
	QVector<int> m_viVars;
	EvEsoTimeScaleView m_iTimeScale;//0=hour, 1=daily, 2=weekly, 3=monthly, 4=total,
	EsoParser* m_parser;
	QDateTime m_start;
	QwtPlot* m_qwtPlot;
	QVector<EsoPlotCurve*> m_vCrv;
	QwtPlotMarker* m_crvMax;
	QwtPlotMarker* m_crvMin;
	QVector <QwtPlotMarker*> m_vLabelMarker;
	QwtPlotGrid* m_qwtGrid;
	bool m_bViewMin;
	bool m_bViewMax;
	bool m_bViewMarkers;
	bool m_bViewGrid;
	float m_fMax;
	float m_fMin;
	float m_fAvg;
	QString m_sTitle;
	std::vector<float> m_vX;
	std::vector<float> m_vY;
	std::vector< EvTimeStruct> m_vXTimeStruct;
	QString m_sLabelFormat;
	QVector <QColor> m_vColors;
};

class TimeScaleDraw : public QwtScaleDraw
{
public:
	TimeScaleDraw(const QDateTime& startTime, const QString & sLabelFormat) 
		: m_startTime(startTime), m_sLabelFormat(sLabelFormat)
	{
	}
	//returns the time axis label for a specific time (in secs from start)
	virtual QwtText label(double vTime) const
	{
		QDateTime actTime = m_startTime.addSecs((int) vTime);
		QString sLabel = actTime.toString(m_sLabelFormat);
		return QwtText(sLabel);
	}
	void SetLabelFormat(QString sFormat)
	{
		m_sLabelFormat = sFormat;
	}
private:
	QDateTime m_startTime;
	QString m_sLabelFormat;
	
};

#endif
