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

// $Id: EsoVariableInfo.cpp,v 1.3 2006/11/17 21:48:33 cschiefer Exp $

#include "EsoVariableInfo.h"


EsoVariableInfo::EsoVariableInfo()
{
	m_iIndex = 0;
	m_ReportStep = EvHourly;
}


/* Copy constructor.	*/
EsoVariableInfo::EsoVariableInfo(EsoVariableInfo const & other)
{
	*this = other;
}


/* Assignment operator. */
EsoVariableInfo& EsoVariableInfo::operator =(EsoVariableInfo const & other)
{
	if (this == &other)
		return *this;

	m_iIndex = other.m_iIndex;
	m_sComment = other.m_sComment;
	m_vColumnNames = other.m_vColumnNames;
	m_ReportStep = other.m_ReportStep;

	return *this;
}

void EsoVariableInfo::Clear()
{
	m_iIndex = 0;
	m_sComment.clear();
	m_vColumnNames.clear();
	m_ReportStep = EvHourly;
}


/* Get the variable info comment. */
QString EsoVariableInfo::GetComment() const
{
	return m_sComment;
}


/* Set the variable info comment. */
void EsoVariableInfo::SetComment(QString const & sComment)
{
	m_sComment = sComment;
}


/* Get the variable index number. */
unsigned EsoVariableInfo::GetIndex() const
{
	return m_iIndex;
}


/* Set the variable index number. */
void EsoVariableInfo::SetIndex(unsigned iIndex)
{
	m_iIndex = iIndex;
}


EvReportStep EsoVariableInfo::GetReportStep() const
{
	return m_ReportStep;
}


void EsoVariableInfo::SetReportStep(EvReportStep const reportStep)
{
	m_ReportStep = reportStep;
}


/* Get the column infos. */
std::vector< EvColumnInfo> const & EsoVariableInfo::GetColumnInfos() const
{
	return m_vColumnNames;
}


/* Get the column info of the specified column. */
EvColumnInfo const & EsoVariableInfo::GetColumnInfo(unsigned iColumnIndex) const
{
	if (iColumnIndex >= m_vColumnNames.size())
	{
		EvColumnInfo* colEmpty = new EvColumnInfo;
		return *colEmpty;
	}
	return m_vColumnNames[iColumnIndex];
}


/* Add column info. */
void EsoVariableInfo::AddColumnInfo(EvColumnInfo const & columnInfo)
{
	m_vColumnNames.push_back(columnInfo);
}


EsoVariableInfo::~EsoVariableInfo()
{
}


bool operator==(EvColumnInfo const & colInfo1, EvColumnInfo const & colInfo2)
{
	return (colInfo1.m_sName == colInfo2.m_sName && colInfo1.m_sUnit == colInfo2.m_sUnit);
}


/* Comparison operator equal. */
bool operator==(EsoVariableInfo const & varInfo1, EsoVariableInfo const & varInfo2)
{
	return (varInfo1.m_iIndex == varInfo2.m_iIndex && varInfo1.m_sComment == varInfo2.m_sComment && varInfo1.m_vColumnNames == varInfo2.m_vColumnNames && varInfo1.m_ReportStep == varInfo2.m_ReportStep);
}
