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

// $Id: EsoVariableInfo.h,v 1.3 2006/11/17 21:48:33 cschiefer Exp $

#ifndef EVESOVARIABLEINFO_H
#define EVESOVARIABLEINFO_H

//Includes
#include <QString>
#include <vector>

enum EvReportStep
{
	EvDetailed = 0, //detailed - lists every instance (i.e. HVAC variable timesteps)
	EvTimeStep = 1, //timestep - refers to the zone timestep/timestep in hour value
	EvHourly = 2,
	EvDaily = 3,
	EvMonthly = 4,
	EvRunPeriod = 5 //runperiod, environment, and annual are synonymous
};


/** Stores name and unit of one column from the variable declaration lines. */
struct EvColumnInfo
{
	QString m_sName;	/**< Column name. */
	QString m_sUnit;  /**< Part of the variable name enclosed with '[' ']'. */
	void Clear()
	{
		m_sName.clear();
		m_sUnit.clear();
	}
	/** Comparison operator equal. */
	friend bool operator==(EvColumnInfo const & colInfo1, EvColumnInfo const & colInfo2);
};

//! Stores the info for one variable from the EnergyPlus 'eso' output file.
class EsoVariableInfo
{
	//Methods
public:
	/** Constructor.		*/
	EsoVariableInfo();

	/** Copy constructor.	*/
	EsoVariableInfo(EsoVariableInfo const & other);

	/** Get the variable info comment. */
	QString GetComment() const;

	/** Set the variable info comment. */
	void SetComment(QString const & sComment);

	/** Get the variable index number. */
	unsigned GetIndex() const;

	/** Set the report step. */
	void SetReportStep(EvReportStep const reportStep);

	/** Get the report step. */
	EvReportStep GetReportStep() const;

	/** Set the variable index number. */
	void SetIndex(unsigned iIndex);

	/** Get the column infos. */
	std::vector< EvColumnInfo> const & GetColumnInfos() const;

	/** Get the column info of the specified column. */
	EvColumnInfo const & GetColumnInfo(unsigned iColumnIndex) const;

	/** Add column info. */
	void AddColumnInfo(EvColumnInfo const & columnInfo);

	/** Assignment operator. */
	EsoVariableInfo& operator =(EsoVariableInfo const & other);

	/** Comparison operator equal. */
	friend bool operator==(EsoVariableInfo const & varInfo1, EsoVariableInfo const & varInfo2);

	/** clear content. */
	void Clear();

	/** Destructor.			*/
	~EsoVariableInfo();

private:

	//Members
public:

private:
	unsigned m_iIndex;							/**< Variable index number (first value in the variable declaration line.) */
	std::vector< EvColumnInfo> m_vColumnNames;
	QString m_sComment; 					/**< Text after the '!' in the variable declaration line */
	EvReportStep m_ReportStep;					/**< Report step for variable. */
};


#endif
