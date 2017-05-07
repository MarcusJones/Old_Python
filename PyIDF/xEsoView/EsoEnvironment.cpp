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

// $Id: EsoEnvironment.cpp,v 1.8 2006/11/17 21:48:33 cschiefer Exp $

#include <QDateTime>
#include <QtDebug>
#include <math.h>

#include "EsoEnvironment.h"
#include "EsoUtil.h"

EsoEnvironment::EsoEnvironment()
{
}


EsoEnvironment::~EsoEnvironment()
{
}


// Set the time vector.
void EsoEnvironment::SetTimeVector(const EvReportStep reportStep, std::vector< EvTimeStruct> const & vTime)
{
	switch (reportStep)
	{
		case EvDetailed:
			m_vReportTimeDetailed = vTime;
			break;
		case EvTimeStep:
			m_vReportTimeTimeStep = vTime;
			break;
		case EvHourly:
			m_vReportTimeHourly = vTime;
			break;
		case EvDaily:
			m_vReportTimeDaily = vTime;
			break;
		case EvMonthly:
			m_vReportTimeMonthly = vTime;
			break;
		case EvRunPeriod:
			m_vReportTimeRunPeriod = vTime;
			break;
		default:
			;
			//		wxLogError("EsoEnvironment::SetTimeVector: Invalid reportStep type!");
	}
}


// Get the time vector.
// Returns false if the time vector is empty for the specified report step.
bool EsoEnvironment::GetTimeVector(const EvReportStep reportStep, std::vector< EvTimeStruct>& vTime)
{
	switch (reportStep)
	{
		case EvDetailed:
			vTime = m_vReportTimeDetailed;
			break;
		case EvTimeStep:
			vTime = m_vReportTimeTimeStep;
			break;
		case EvHourly:
			vTime = m_vReportTimeHourly;
			break;
		case EvDaily:
			vTime = m_vReportTimeDaily;
			break;
		case EvMonthly:
			vTime = m_vReportTimeMonthly;
			break;
		case EvRunPeriod:
			vTime = m_vReportTimeRunPeriod;
			break;
		default:
			//wxLogError("EsoEnvironment::SetTimeVector: Invalid reportStep type!");
			return false;
	}
	return !vTime.empty();
}

EvTimeStruct EsoEnvironment::GetStartTime() const
{
	EvTimeStruct start;

	if (!m_vReportTimeDetailed.empty())
		start = m_vReportTimeDetailed.front();

	if (!m_vReportTimeTimeStep.empty() && (start.iMonth == -1 || ConverttoQDateTime(start) > ConverttoQDateTime(m_vReportTimeTimeStep.front())))
		start = m_vReportTimeTimeStep.front();

	if (!m_vReportTimeHourly.empty() && (start.iMonth == -1 || ConverttoQDateTime(start) > ConverttoQDateTime(m_vReportTimeHourly.front())))
		start = m_vReportTimeHourly.front();

	if (!m_vReportTimeDaily.empty() && (start.iMonth == -1 || ConverttoQDateTime(start) > ConverttoQDateTime(m_vReportTimeDaily.front())))
		start = m_vReportTimeDaily.front();

	if (!m_vReportTimeMonthly.empty() && (start.iMonth == -1 || ConverttoQDateTime(start) > ConverttoQDateTime(m_vReportTimeMonthly.front())))
		start = m_vReportTimeMonthly.front();

	if (!m_vReportTimeRunPeriod.empty() && (start.iMonth == -1 || ConverttoQDateTime(start) > ConverttoQDateTime(m_vReportTimeRunPeriod.front())))
		start = m_vReportTimeRunPeriod.front();

	return start;
}


EvTimeStruct EsoEnvironment::GetEndTime(int iYear) const
{
	EvTimeStruct start,end;

	if (!m_vReportTimeDetailed.empty())
		end = m_vReportTimeDetailed.back();

	if (!m_vReportTimeTimeStep.empty() && ConverttoQDateTime(end, iYear) < ConverttoQDateTime(m_vReportTimeTimeStep.back(), iYear))
		end = m_vReportTimeTimeStep.back();

	if (!m_vReportTimeHourly.empty() && ConverttoQDateTime(end, iYear) < ConverttoQDateTime(m_vReportTimeHourly.back(), iYear))
		end = m_vReportTimeHourly.back();

	if (!m_vReportTimeDaily.empty() && ConverttoQDateTime(end, iYear) < ConverttoQDateTime(m_vReportTimeDaily.back(), iYear))
		end = m_vReportTimeDaily.back();

	if (!m_vReportTimeMonthly.empty() && ConverttoQDateTime(end, iYear) < ConverttoQDateTime(m_vReportTimeMonthly.back(), iYear))
		end = m_vReportTimeMonthly.back();

	if (!m_vReportTimeRunPeriod.empty() && ConverttoQDateTime(end, iYear) < ConverttoQDateTime(m_vReportTimeRunPeriod.back(), iYear))
		end = m_vReportTimeRunPeriod.back();

	return end;
}


bool EsoEnvironment::IsEmpty(int const iVariableId)
{
	std::map< int,std::vector< float> >::const_iterator iter(m_mapData.find(iVariableId));
	if (iter != m_mapData.end())
	{
		return iter->second.empty();
	}
	return true;
}


// Get the data vector.
// Returns false if the data vector does not exist for the specified variable id.
bool EsoEnvironment::GetDataVector(int const iVariableId, std::vector< float>& vData)
{
	std::map< int,std::vector< float> >::const_iterator iter(m_mapData.find(iVariableId));
	if (iter != m_mapData.end())
	{
		vData = iter->second;
		return true;
	}
	//wxLogError("EsoEnvironment::GetDataVector: Specified variable id not in store!");
	return false;
}


// Set the data vector.
void EsoEnvironment::SetDataVector(int const iVariableId, std::vector< float> const & vData)
{
	//TODO: check if id is already in map!
	m_mapData.insert(std::make_pair(iVariableId, vData));
}


// Add data to the specified variable.
void EsoEnvironment::AddDataInit(int const iVariableId)
{
	std::map< int,std::vector< float> >::iterator iterData(m_mapData.find(iVariableId));
	if (iterData == m_mapData.end())
	{
		std::vector< float> vec;
		std::pair< std::map< int,std::vector< float> >::iterator,bool> resPair;
		resPair = m_mapData.insert(std::make_pair(iVariableId, vec));
		iterData = resPair.first;
	}
	iterData->second.push_back(ESONAN /*NAN*/);
}


void EsoEnvironment::AddData(int const iVariableId, float const & fData)
{
	std::map< int,std::vector< float> >::iterator iterData(m_mapData.find(iVariableId));
	if (iterData == m_mapData.end())
	{
		qCritical() << "EsoEnvironment::AddData - variable id " << iVariableId << " not yet initialized!";
		AddDataInit(iVariableId);
		iterData = m_mapData.find(iVariableId);
	}
	iterData->second.back() = fData;
}


// Add time to the specified report step.
void EsoEnvironment::AddTime(const EvReportStep reportStep, EvTimeStruct const & time)
{
	switch (reportStep)
	{
		case EvDetailed:
			m_vReportTimeDetailed.push_back(time);
			break;
		case EvTimeStep:
			m_vReportTimeTimeStep.push_back(time);
			break;
		case EvHourly:
			m_vReportTimeHourly.push_back(time);
			break;
		case EvDaily:
			m_vReportTimeDaily.push_back(time);
			break;
		case EvMonthly:
			m_vReportTimeMonthly.push_back(time);
			break;
		case EvRunPeriod:
			m_vReportTimeRunPeriod.push_back(time);
			break;
		default:
			;
			//wxLogError("EsoEnvironment::SetTimeVector: Invalid reportStep type!");
	}
}

void EsoEnvironment::SetInfo(QVector< EvEnvInfoVar> vsInfo)
{
	m_vsInfo = vsInfo;
}

// Get concatenated info.
QString EsoEnvironment::GetInfo(bool bShort) const
{
	QString sInfo;
	QVector< EvEnvInfoVar>::const_iterator iter;
	QVector< EvEnvInfoVar>::const_iterator iterEnd(m_vsInfo.end());
	for (iter = m_vsInfo.begin(); iter != iterEnd; ++iter)
	{
		if (bShort)
		{
			return (*iter).sValue;
		} else
		{
			sInfo += (*iter).sTitle + " ";
			if ((*iter).sUnit != "[]")
				sInfo += (*iter).sUnit;
			sInfo += ": " + (*iter).sValue + "\n";
		}
	}
	QDateTime start = ConverttoQDateTime(GetStartTime(), -1);
	sInfo += "Start time: " + start.toString("ddd MMM dd hh:mm") + "\n";
	sInfo += "End time: " + ConverttoQDateTime(GetEndTime(start.date().year()), start.date().year()).toString("ddd MMM dd hh:mm") + "\n";
	return sInfo;
}


int EsoEnvironment::GetNumberOfVariables() const
{
	return (int) m_mapData.size();
}

