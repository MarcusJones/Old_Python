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

// $Id: EsoVarPlot.cpp,v 1.22 2007/02/27 21:18:22 cschiefer Exp $

#include <QtDebug>
#include <QPixmap>
#include <QLocale>
#include <QSettings>
#include <qwt_plot_curve.h>
#include <qwt_plot_zoomer.h>
#include <qwt_symbol.h>
#include <qwt_plot_grid.h>
#include <qwt_plot_marker.h>
#include <qwt_legend.h>
#include <algorithm>

#include "EsoScrollZoomer.h"
#include "EsoVarPlot.h"
#include "EsoParser.h"
#include "EsoBookmark.h"

EsoVarPlot::EsoVarPlot(QWidget* parent, QwtPlot* plot)
	: QWidget(parent)
{
	m_parser = NULL;
	m_iEnvironment = -1;
	m_iVariable = -1;
	m_zoomer = new EsoScrollZoomer(plot->canvas());
	m_zoomer->setTrackerMode(QwtPicker::AlwaysOn);
	m_zoomer->setRubberBandPen(QPen(Qt::black, 0, Qt::DotLine));
	m_zoomer->setTrackerPen(QPen(Qt::black));
	m_iTimeScale = EvViewTotal;
	m_qwtPlot = plot;
	m_bViewMin = false;
	m_bViewMax = false;
	m_bViewMarkers = false;
	m_bViewGrid = false;
	m_crvMax = NULL;
	m_crvMin = NULL;
	m_qwtGrid = NULL;
	m_fAvg = 0;
	m_fMax = 0;
	m_fMin = 0;
	m_sLabelFormat = "MMM dd hh:mm";
	
	connect(m_zoomer, SIGNAL(redrawZ()), this, SLOT(redrawP()));
	m_vColors << Qt::red << Qt::green << Qt::blue << Qt::cyan << Qt::magenta << Qt::yellow << Qt::black << Qt::darkRed << Qt::darkGreen  <<  Qt::darkBlue << Qt::darkCyan << Qt::darkMagenta << Qt::darkYellow  <<  Qt::darkGray << Qt::lightGray;
}

void EsoVarPlot::UpdateTimeLabelFormat()
{
	//Enabling this will lead to false results because axis ticks are currrently not in 1h/1day steps!!!!
	//TODO: if axis ticks are show in 1h/1day steps we can enable this.
	//TODO: The updating is currently one step behind - axes are not refreshed!
/*
	m_sLabelFormat = "MMM dd hh:mm";
	if (m_qwtPlot == NULL)
		return;
	
	int iStartIndex=-1;
	int iEndIndex=-1;
	GetStartEndIndex( GetZoomRect(), iStartIndex, iEndIndex);
	float fRange=m_vX[iEndIndex] -m_vX[iStartIndex];
	fRange = fRange/3600; //in hours
	qDebug()<< "EsoVarPlot::UpdateTimeLabelFormat() - iStartIndex:"<<iStartIndex <<" iEndIndex:"<<iEndIndex<< " range:"<<fRange<<"h";
	if (fRange <=24) //<1day
		m_sLabelFormat = "MMM dd hh:mm";
	else if (fRange <= 24*14)//<1day-2Weeks
		m_sLabelFormat = "MMM dd hh'h'"; 
	else //> 1Month 
		m_sLabelFormat = "MMM dd";
	TimeScaleDraw* d = dynamic_cast<TimeScaleDraw*>(m_qwtPlot->axisScaleDraw(QwtPlot::xBottom)); 
	if (d!=NULL)
	{
		d->SetLabelFormat(m_sLabelFormat);
		qDebug()<< "EsoVarPlot::UpdateTimeLabelFormat() - label format: "<<m_sLabelFormat;
	}
*/
}


void EsoVarPlot::redrawP()
{
	qDebug()<< "EsoVarPlot::redrawP()";
	m_qwtPlot->replot();
	UpdateTimeLabelFormat();
	m_qwtPlot->replot();
	emit redraw(); //this will update the local variableinfo
}


EsoVarPlot::~EsoVarPlot()
{
	//curves are deleted within qwtplot - nothing to do here
}

void EsoVarPlot::SetQwtPlot(QwtPlot* plot)
{
	m_qwtPlot = plot;
}


QwtPlot* EsoVarPlot::GetQwtPlot()
{
	return m_qwtPlot;
}


void EsoVarPlot::SetParser(EsoParser* parser)
{
	m_parser = parser;
}


void EsoVarPlot::setSelection(int iVar, bool bSel)
{
	
	//remove var from list
	int iInd = m_viVars.indexOf(iVar);
	if (iInd>-1)
		m_viVars.remove(iInd);

	//append var to list if selected
	if (bSel)
		m_viVars.push_back(iVar);
	qDebug() << "EsoVarPlot::setSelection: Number selcted:"<<m_viVars.size();
	Plot();
}


void EsoVarPlot::setCurrentVariable(int iVariable)
{
	qDebug("EsoVarPlot::setCurrentVariable(%d)", iVariable);
	QwtDoubleRect rect = m_zoomer->zoomRect();
	bool bInit = (m_iVariable < 0 || m_iEnvironment < 0);
	m_iVariable = iVariable;
	
//	m_viVars.resize(1);
//	m_viVars[0] = iVariable;

	m_qwtPlot->setUpdatesEnabled(false);
	Plot();
	m_qwtPlot->setUpdatesEnabled(true);
	//restore x-area
	if (!bInit)
	{
		QwtDoubleRect rectNew = m_zoomer->zoomRect();
		rectNew.setLeft(rect.left());
		rectNew.setRight(rect.right());
		if (rectNew.left() != rectNew.right())
			m_zoomer->zoom(rectNew);
		else
			setCurrentTimeScale(m_iTimeScale);
	}
}


void EsoVarPlot::Plot()
{
	int iColor = 0;
	QString sTitle;
	int iVar;
	float fMin, fMax, fAvg;

	qDebug() << "EsoVarPlot::Plot - Start plotting of var " << m_iVariable << " within environment " << m_iEnvironment;
	if (m_iVariable < 0 || m_iEnvironment < 0)
	{
		qDebug() << "EsoVarPlot::Plot - Invalid index: can't plot variable " << m_iVariable << " within environment " << m_iEnvironment;
		return;
	}
	if (!m_qwtPlot)
	{
		qDebug() << "EsoVarPlot::Plot - qwtPlot not initialized";
		return;
	}
	//m_qwtPlot->setUpdatesEnabled(false);
	qDebug() << "EsoVarPlot::Plot - clear";
		QVector<int> viVars;
	viVars = m_viVars;
	int iCurVarPos = m_viVars.indexOf(m_iVariable);
	if (iCurVarPos == -1)
	{
		viVars.prepend(m_iVariable);
		iCurVarPos = 0;
	}
	else
	{
		iColor++;
	}


	if (m_vCrv.size() != m_vLabelMarker.size())
		m_vLabelMarker.resize(m_vCrv.size());
	for (int iCrvs=0; iCrvs< m_vCrv.size(); ++iCrvs)
	{
		if (m_vCrv[iCrvs])
			m_vCrv[iCrvs]->detach();
		if (m_vLabelMarker[iCrvs])
			m_vLabelMarker[iCrvs]->detach();
	}
	
	

	if (m_qwtGrid)
		m_qwtGrid->detach();
	m_qwtPlot->clear();
	qDebug() << "EsoVarPlot::Plot - after clear";

	//add plot
	EsoEnvironment env;
	m_parser->GetEnvironment(m_iEnvironment, env);
	
	m_qwtPlot->setAutoReplot(false);
	
	

	QSettings settings(ESO_ORG, ESO_APP);
	QColor colorBg = settings.value("GraphBackgroundColor", QColor(Qt::white)).value< QColor>();
	m_qwtPlot->setCanvasBackground(colorBg);
	
	QColor colorLine = settings.value("GraphLineColor", QColor(Qt::blue)).value< QColor>();
	QPen pen(colorLine);
	m_sTitle = "";
	
	if (viVars.size()==1)
		m_qwtPlot->insertLegend(NULL);
	else
		m_qwtPlot->insertLegend(new QwtLegend(), QwtPlot::TopLegend);
	
	
	for (int iCrvs=0; iCrvs< viVars.size(); ++iCrvs)
	{
		colorLine = m_vColors[iColor];
		iColor++;
		pen.setColor(colorLine);
		if (iColor>= m_vColors.size())
			iColor=0;
		iVar = viVars[iCrvs];
		sTitle = m_parser->GetVariableTitle( iVar );
		EsoVariableInfo info = m_parser->GetVariableInfo(iVar);
		sTitle = info.GetColumnInfo(1).m_sName + " " + info.GetColumnInfo(0).m_sName;
		
		m_sTitle += ((iCrvs>0)? "\n":"") + sTitle;
			
		m_vCrv.append(new EsoPlotCurve());

		m_vCrv[iCrvs]->setTitle(sTitle + " ["+info.GetColumnInfo(1).m_sUnit+"] ");
		m_vCrv[iCrvs]->setPen(pen);
		m_vCrv[iCrvs]->attach(m_qwtPlot);
		qDebug() << "EsoVarPlot::Plot - after attach crv";
	
		m_vY.clear();
		m_vXTimeStruct.clear();
		env.GetDataVector(iVar, m_vY);
		env.GetTimeVector(info.GetReportStep(), m_vXTimeStruct);
		m_vX.clear();
		m_vX.resize(m_vY.size());
		if (m_vXTimeStruct.empty())
		{
			qDebug("EsoVarPlot::Plot - empty time vector");
			for (unsigned i = 0; i < m_vX.size(); ++i)
				m_vX[i] = i;
		} else
		{
			m_start = ConverttoQDateTime(m_vXTimeStruct[0], -1);
			for (unsigned i = 0; i < m_vX.size(); ++i)
				m_vX[i] = m_start.secsTo(ConverttoQDateTime(m_vXTimeStruct[i], m_start.date().year())); //seconds
			qDebug("EsoVarPlot::Plot - vector lengths: %d %d", m_vX.size(), m_vY.size());
			for (unsigned j = 0; j < 6; ++j)
			{
				if (j < m_vX.size())
					qDebug() << "EsoVarPlot::Plot - time " << j << ": " << ConverttoQDateTime(m_vXTimeStruct[j]).toString();
			}
		}
	
		//Only for the current highlighted variable
		if (iCrvs==0)
		{
			m_fAvg=m_fMin=m_fMax=0;
			fAvg=fMin=fMax=0;
			fMax = m_fMax = maxIgnNAN(m_vY);
			fMin = m_fMin = minIgnNAN(m_vY);
			fAvg = m_fAvg = avgIgnNAN(m_vY);
			emit updateVarInfo();
		}
		else
		{
			float fMaxN = maxIgnNAN(m_vY);
			float fMinN = minIgnNAN(m_vY);
			if (fMaxN > fMax) fMax=fMaxN;
			if (fMinN < fMin) fMin=fMinN;
		}
		
		
	
		// copy the data into the curves
		m_vCrv[iCrvs]->setData(m_vX, m_vY, (int) m_vY.size());
	
		//set x and y label
	
		m_qwtPlot->setAxisTitle(QwtPlot::yLeft, "["+info.GetColumnInfo(1).m_sUnit+"]");
		m_qwtPlot->setAxisTitle(QwtPlot::xBottom, tr("Time"));
	
		m_qwtPlot->setAxisScaleDraw(QwtPlot::xBottom, new TimeScaleDraw(m_start, m_sLabelFormat));
		m_qwtPlot->setAxisScale(QwtPlot::xBottom, m_vX[0], m_vX.back());
		UpdateTimeLabelFormat();
		float fDelta=fMax-fMin;
		fDelta *= 0.05;
//		if ( fDelta<0.001 && info.GetColumnInfo(1).m_sUnit=="C" )
//			fDelta=1;
		if ( fDelta<1e-10 )
			fDelta=1e-10;
		m_qwtPlot->setAxisScale(QwtPlot::yLeft, fMin-fDelta, fMax+fDelta);
	
		//qwtPlot->setAxisLabelRotation(QwtPlot::xBottom, -55.0);
		//qwt06	m_qwtPlot->setAxisLabelFlags(QwtPlot::xBottom, Qt::AlignLeft | Qt::AlignBottom);
	
		QwtText label;
		label.setColor(QColor("blue"));

		if (m_bViewMarkers)
		{
			qDebug() << "EsoVarPlot::Plot - autoplot symbols";
			QwtSymbol symbol;
			symbol.setStyle(GetCurrentMarkerStyle());
//			QColor colorMarker = settings.value("GraphColorMarker", QColor(Qt::red)).value< QColor>();
			symbol.setPen(colorLine);
			
			symbol.setSize(10);
			m_vCrv[iCrvs]->setSymbol(symbol);
			if (m_vY.size() < 13)
				m_vCrv[iCrvs]->setStyle(QwtPlotCurve::Steps);
	
			if (m_vY.size() == 1) //show value label
			{
				qDebug() << "EsoVarPlot::Plot - autoplot values";
				m_vLabelMarker.append(new QwtPlotMarker());
				m_vLabelMarker[iCrvs]->setYValue(m_vY[0]);
				m_vLabelMarker[iCrvs]->setXValue(m_vX[0]);
				label.setText(m_start.toString("MMM dd hh:mm") + QString().sprintf(", %f", m_vY[0])) ;
				m_vLabelMarker[iCrvs]->setLabel(label);
				m_vLabelMarker[iCrvs]->setLabelAlignment(Qt::AlignTop | Qt::AlignRight);
				m_vLabelMarker[iCrvs]->attach(m_qwtPlot);
			}
		} 
	
		QColor colorLineMaxMin = settings.value("GraphLineColorMaxMin", QColor(Qt::green)).value< QColor>();
//		if (viVars.size()>1)
//			colorLineMaxMin = colorLine;
		
		label.setColor(colorLineMaxMin);
		
		//add max
		if (iCurVarPos == iCrvs)
		{
			if (m_bViewMax)
			{
				qDebug("EsoVarPlot::Plot view max");
				m_crvMax = new QwtPlotMarker;
				m_crvMax->setLinePen(QPen(colorLineMaxMin, 0, Qt::DashDotLine));
				m_crvMax->attach(m_qwtPlot);
				m_crvMax->setYValue(m_fMax);
				m_crvMax->setLabelAlignment(Qt::AlignBottom | Qt::AlignLeft);
				m_crvMax->setLineStyle(QwtPlotMarker::HLine);
				label.setText(QString("Maximum=%1").arg(m_fMax));
				m_crvMax->setLabel(label);
			}
	
			//add min
			if (m_bViewMin)
			{
				qDebug("EsoVarPlot::Plot view min");
				m_crvMin = new QwtPlotMarker;
				m_crvMin->setLinePen(QPen(colorLineMaxMin, 0, Qt::DashDotLine));
				m_crvMin->attach(m_qwtPlot);
				m_crvMin->setYValue(m_fMin);
				m_crvMin->setLabelAlignment(Qt::AlignTop | Qt::AlignLeft);
				m_crvMin->setLineStyle(QwtPlotMarker::HLine);
				label.setText(QString("Minimum=%1").arg(m_fMin));
				m_crvMin->setLabel(label);
			}
		}
	}//for all curves
	if (viVars.size() > 1)
		m_qwtPlot->setTitle("");
	else
		m_qwtPlot->setTitle(m_sTitle);



	if (m_bViewGrid)
	{
		qDebug("EsoVarPlot::Plot grid");
		m_qwtGrid = new QwtPlotGrid;
		//m_qwtGrid->enableXMin(true);
		m_qwtGrid->setMajPen(QPen(Qt::gray, 0, Qt::DotLine));
		m_qwtGrid->setMinPen(QPen(Qt::gray, 0, Qt::DotLine));
		m_qwtGrid->attach(m_qwtPlot);
	}    
	// finally, refresh the plot
	m_qwtPlot->replot();
	m_zoomer->setZoomBase();
	m_zoomer->m_startTime = m_start;
	//m_qwtPlot->setUpdatesEnabled(true);
	m_qwtPlot->replot();
}

void EsoVarPlot::pushButtonBack_clicked()
{
	qDebug("EsoVarPlot::pushButtonBack_clicked");
	if (m_iTimeScale == EvViewTotal)
		return;
	QwtDoubleRect rect = m_zoomer->zoomRect(); //returns seconds
	QwtDoubleRect rectB = m_zoomer->zoomBase(); //returns seconds
	qDebug("current: left: %d  right: %d", (int) rect.left(), (int) rect.right());
	qDebug("base:    left: %d  right: %d", (int) rectB.left(), (int) rectB.right());
	QwtDoubleRect rectNew = rect;
	QDateTime tMin;
	QDateTime tMax = m_start.addSecs((int) rect.left());
	if (m_iTimeScale == EvViewHourly)
		tMin = tMax.addSecs(-3600);
	else if (m_iTimeScale == EvViewDaily)
		tMin = tMax.addDays(-1);
	else if (m_iTimeScale == EvViewWeekly)
		tMin = tMax.addDays(-7);
	else if (m_iTimeScale == EvViewMonthly)
		tMin = tMax.addMonths(-1);

	rectNew.setLeft(m_start.secsTo(tMin));
	rectNew.setRight(m_start.secsTo(tMax));
	qDebug("new:     left: %d  right: %d", (int) rectNew.left(), (int) rectNew.right());

	if (rectNew.left() < 0)
	{
		rectNew.setLeft(0);
		rectNew.setRight(tMin.secsTo(tMax));
	}
	if (rectNew.right() > rectB.right())
		rectNew.setRight(rectB.right());
	qDebug("new:     left: %d  right: %d", (int) rectNew.left(), (int) rectNew.right());
	//set zoom
	m_zoomer->zoom(rectNew);
}


void EsoVarPlot::pushButtonForward_clicked()
{
	qDebug("EsoVarPlot::pushButtonForward_clicked");
	if (m_iTimeScale == EvViewTotal)
		return;
	QwtDoubleRect rect = m_zoomer->zoomRect(); //returns seconds
	QwtDoubleRect rectB = m_zoomer->zoomBase(); //returns seconds
	qDebug("current: left: %d  right: %d", (int) rect.left(), (int) rect.right());
	qDebug("base:    left: %d  right: %d", (int) rectB.left(), (int) rectB.right());
	QwtDoubleRect rectNew = rect;
	QDateTime tMin = m_start.addSecs((int) rect.right());
	QDateTime tMax;
	if (m_iTimeScale == EvViewHourly)
		tMax = tMin.addSecs(3600);
	else if (m_iTimeScale == EvViewDaily)
		tMax = tMin.addDays(1);
	else if (m_iTimeScale == EvViewWeekly)
		tMax = tMin.addDays(7);
	else if (m_iTimeScale == EvViewMonthly)
		tMax = tMin.addMonths(1);

	rectNew.setLeft(m_start.secsTo(tMin));
	rectNew.setRight(m_start.secsTo(tMax));
	qDebug("new:     left: %d  right: %d", (int) rectNew.left(), (int) rectNew.right());
	if (rectNew.right() > rectB.right())
	{
		rectNew.setRight(rectB.right());
		rectNew.setLeft(rectB.right() - tMin.secsTo(tMax));
		if (rectNew.left() < 0)
			rectNew.setLeft(0);
	}
	qDebug("new:     left: %d  right: %d", (int) rectNew.left(), (int) rectNew.right());
	//set zoom
	m_zoomer->zoom(rectNew);
}


void EsoVarPlot::setCurrentTimeScale(EvEsoTimeScaleView iTimeScale)
{
	qDebug("EsoVarPlot::setCurrentTimeScale(%d)", iTimeScale);
	m_iTimeScale = iTimeScale;
	//i: hour=0, day=1, week=2, month=3, total=4
	//get current x-min and x-max
	QwtDoubleRect rect = m_zoomer->zoomRect(); //returns seconds
	QwtDoubleRect rectB = m_zoomer->zoomBase(); //returns seconds
	qDebug("current: left: %d  right: %d", (int) rect.left(), (int) rect.right());
	qDebug("base:    left: %d  right: %d", (int) rectB.left(), (int) rectB.right());
	//previous starting point according to selected x-range
	QDateTime tMin = m_start;
	//calculate x-max
	QDateTime tMax;
	if (iTimeScale == EvViewHourly)
		tMax = tMin.addSecs(3600);
	else if (iTimeScale == EvViewDaily)
		tMax = tMin.addDays(1);
	else if (iTimeScale == EvViewWeekly)
		tMax = tMin.addDays(7);
	else if (iTimeScale == EvViewMonthly)
		tMax = tMin.addMonths(1);

	rect.setLeft(0);
	rect.setRight(tMin.secsTo(tMax));
	qDebug("new:     left: %d  right: %d", (int) rect.left(), (int) rect.right());

	//set zoom
	if (iTimeScale == EvViewTotal || rect.right() > rectB.right())
		m_zoomer->zoom(rectB);
	else
		m_zoomer->zoom(rect);
}


void EsoVarPlot::setCurrentEnvironment(int iEnvironmentIndex)
{
	qDebug() << "EsoVarPlot::setCurrentEnvironment "<< iEnvironmentIndex;
	if (m_iEnvironment == iEnvironmentIndex)
	    return;
	m_iEnvironment = iEnvironmentIndex;
	Plot();
}


void EsoVarPlot::viewMax(bool bView)
{
	m_bViewMax = bView;
	Redraw();
}


bool EsoVarPlot::viewMax()
{
	return m_bViewMax;
}


void EsoVarPlot::viewGrid(bool bView)
{
	m_bViewGrid = bView;
	Redraw();
}


bool EsoVarPlot::viewGrid()
{
	return m_bViewGrid;
}


void EsoVarPlot::viewMin(bool bView)
{
	m_bViewMin = bView;
	Redraw();
}


bool EsoVarPlot::viewMin()
{
	return m_bViewMin;
}


void EsoVarPlot::viewMarkers(bool bView)
{
	m_bViewMarkers = bView;
	Redraw();
}


bool EsoVarPlot::viewMarkers()
{
	return m_bViewMarkers;
}


void EsoVarPlot::Redraw()
{
   	m_qwtPlot->setUpdatesEnabled(false);
	QwtDoubleRect rect = m_zoomer->zoomRect();//save zoom
	Plot();
	m_zoomer->zoom(rect); //restore zoom
	m_qwtPlot->setUpdatesEnabled(true);
	m_qwtPlot->replot();
}

QString EsoVarPlot::getDataAsText(bool bIncludeTime)
{
	QLocale locale;
	EsoEnvironment env;
	if (m_iVariable < 0 || !m_parser || m_iEnvironment < 0)
		return "";

	EsoVariableInfo info = m_parser->GetVariableInfo(m_iVariable);
	QString sData;
	if (bIncludeTime)
		sData = "Date/Time\t";
	sData += info.GetColumnInfo(1).m_sName + " " + info.GetColumnInfo(0).m_sName + " [" + info.GetColumnInfo(1).m_sUnit + "]\n";

	QSettings settings(ESO_ORG, ESO_APP);
	QString sDTFormat = settings.value("DateTimeFormatForCopy", "yyyy-MM-dd hh:mm:ss").toString();
	QString sDecimalPoint = settings.value("DecimalPointForCopy", ".").toString();
	QString sColumnSep = settings.value("ColumnSepForCopy", "\t").toString();

	if (sDecimalPoint == ",")
		locale = QLocale("de");
	else
		locale = QLocale("C");

	QDateTime dt0, dt;
	for (unsigned i = 0; i < m_vY.size(); ++i)
	{
		if (bIncludeTime && i < m_vXTimeStruct.size())
		{
			if (i==0)
			{
				dt0 = ConverttoQDateTime(m_vXTimeStruct[i]);
			}
			dt = ConverttoQDateTime(m_vXTimeStruct[i], dt0.date().year());

			sData += dt.toString(sDTFormat) + sColumnSep;
		}
		sData += locale.toString(m_vY[i]) + "\n";
	}
	return sData;
}


QPixmap EsoVarPlot::getPixmap()
{
    return QPixmap::grabWidget( m_qwtPlot );
	//return QPixmap::grabWindow(m_qwtPlot->winId());
}


float EsoVarPlot::getMax() const
{
	return m_fMax;
}


float EsoVarPlot::getMin() const
{
	return m_fMin;
}


float EsoVarPlot::getAvg() const
{
	return m_fAvg;
}


QString EsoVarPlot::getTitle() const
{
	return m_sTitle;
}

void EsoVarPlot::GetStartEndIndex(QwtDoubleRect window, int & iStartIndex, int & iEndIndex) const
{
	iStartIndex = -1;
	iEndIndex = m_vX.size()-1;
	for (int i=0; i< (int) m_vX.size(); ++i)
	{
		if (m_vX[i]>= window.left() && iStartIndex <0)
		{
			iStartIndex = i; 
		}
		if (m_vX[i]>= window.right())
		{
			iEndIndex = i;
			break;
		}
	}
	if (iStartIndex<0)
		iStartIndex=0;
	if (iEndIndex<0)
		iEndIndex=m_vX.size()-1;
}


float EsoVarPlot::getMaxLocal() const
{
	//get start and end time
	int iStartIndex = -1;
	int iEndIndex = -1;
	GetStartEndIndex(GetZoomRect(), iStartIndex, iEndIndex );
	//calculate max.
	if (iStartIndex>=0 && iStartIndex<(int)m_vY.size() && iEndIndex>=0 && iEndIndex<(int)m_vY.size())
		return maxIgnNAN( m_vY, iStartIndex, iEndIndex);
	
	qWarning() << "EsoVarPlot::getMaxLocal Calculation of local maximum failed! iStart:"<<iStartIndex << " iEnd:"<<iEndIndex<<" vector-length:"<<m_vY.size();
	return 0;
}


float EsoVarPlot::getMinLocal() const
{
	//get start and end time
	int iStartIndex = -1;
	int iEndIndex = -1;
	GetStartEndIndex(GetZoomRect(), iStartIndex, iEndIndex );
	//calculate min.
	if (iStartIndex>=0 && iStartIndex<(int)m_vY.size() && iEndIndex>=0 && iEndIndex<(int)m_vY.size())
		return minIgnNAN( m_vY, iStartIndex, iEndIndex);

	qWarning() << "EsoVarPlot::getMinLocal Calculation of local minimum failed! iStart:"<<iStartIndex << " iEnd:"<<iEndIndex<<" vector-length:"<<m_vY.size();
	return 0;
}


float EsoVarPlot::getAvgLocal() const
{
	//get start and end time
	int iStartIndex = -1;
	int iEndIndex = -1;
	GetStartEndIndex(GetZoomRect(), iStartIndex, iEndIndex );
	
	//calculate avg.
	if (iStartIndex>=0 && iStartIndex<(int)m_vY.size() && iEndIndex>=0 && iEndIndex<(int)m_vY.size())
		return avgIgnNAN( m_vY, iStartIndex, iEndIndex);

	qWarning() << "EsoVarPlot::getAvgLocal Calculation of local average failed! iStart:"<<iStartIndex << " iEnd:"<<iEndIndex<<" vector-length:"<<m_vY.size();
	return 0;
}


QString EsoVarPlot::getStartLocal() const
{
	QwtDoubleRect rect = GetZoomRect();
	QDateTime actTime = m_start.addSecs((int) rect.left());
	return ConvertToString(actTime);
}


QString EsoVarPlot::getEndLocal() const
{
	QwtDoubleRect rect = GetZoomRect();
	QDateTime actTime = m_start.addSecs((int) rect.right());
	return ConvertToString(actTime);
}

QString EsoVarPlot::getStart() const
{
	return ConvertToString(m_start);
}


QString EsoVarPlot::getEnd() const
{
	QDateTime actTime = m_start.addSecs((int)m_vX.back());
	return ConvertToString(actTime);
}


void EsoVarPlot::print(QPaintDevice& p, const QwtPlotPrintFilter& f) const
{
	qDebug("EsoVarPlot::print(p,f)");
	m_qwtPlot->replot();
	m_qwtPlot->print(p, f);
}


int EsoVarPlot::getVariable() const
{
	return m_iVariable;
}


EvEsoTimeScaleView EsoVarPlot::getTimeScale() const
{
	return m_iTimeScale;
}


int EsoVarPlot::getEnvironment() const
{
	return m_iEnvironment;
}


QwtDoubleRect EsoVarPlot::GetZoomRect() const
{
	if (m_zoomer != NULL)
		return m_zoomer->zoomRect();
	return QwtDoubleRect();
}


EsoBookmark EsoVarPlot::GetCurrentAsBookmark() const
{
    EsoBookmark bm;
	bm.SetName("-9");
    bm.SetVariable(getVariable());
	bm.SetEnvironment(getEnvironment());
	bm.SetTimeScale(getTimeScale());
	if (m_zoomer != NULL)
		bm.SetZoomRect(m_zoomer->zoomRect());
	return bm;
}


void EsoVarPlot::SetCurrent(EsoBookmark bm)
{
   	m_qwtPlot->setUpdatesEnabled(false);
    setCurrentEnvironment(bm.GetEnvironment());
    setCurrentVariable(bm.GetVariable());
//    setCurrentTimeScale(bm.GetTimeScale());
    if (m_zoomer != NULL)
		m_zoomer->zoom(bm.GetZoomRect());
	m_qwtPlot->setUpdatesEnabled(true);
	m_qwtPlot->replot();
}
