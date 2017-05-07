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

// $Id: EsoParser.h,v 1.6 2007/02/27 21:18:22 cschiefer Exp $

#ifndef EVESOPARSER_H
#define EVESOPARSER_H

//Includes
#include <vector>
#include <QObject>
class QTextStream;
class QFile;

#include "EsoVariableInfo.h"
#include "EsoEnvironment.h"


//! Parse EnergyPlus 'eso' output file and store values.
class EsoParser : public QObject
{
	Q_OBJECT

public:
	//! Constructor.
	EsoParser();

	//! Get the eso file names
	QString GetESOFile() const;

	//! Get the EnergyPlus version.
	QString GetEPVersion() const;

	//! Get the simulation date and time.
	QString GetSimulationTime() const;

	//! Get the number of simulation environments.
	int GetNumberOfEnvironments() const;

	//! Get the specified environment. Returns false if index is invalid.
	bool GetEnvironment(int iIndex, EsoEnvironment& environment) const;

	//! Get the specified environment. Returns 0 if index is invalid.
	EsoEnvironment* GetEnvironmentPtr(int iIndex);

	//! Parse the file.
	bool Parse(QString const & sFileName, QString& sErrorMessage);

	//! Get variable info.
	EsoVariableInfo GetVariableInfo(int iIndex) const;

	void GetVariableInfo(std::map< int,EsoVariableInfo>::const_iterator& iterBegin, std::map< int,EsoVariableInfo>::const_iterator& iterEnd);

	//! Return list of variables with specified time step.
	void GetVariableIds(EvReportStep, std::vector<int> & vVariableIds);

	//! Get variable title
	QString GetVariableTitle(int iVar);
	
	//Clear parser.
	void Clear();

	//!Destructor.
	virtual ~EsoParser();

signals:
	void setParseProgress(int);
	void setTotalParseSteps(int);

private:
	///! Set the EnergyPlus version.
	void SetEPVersion(QString const & sEPVersion);

	//! Set the EnergyPlus version.
	void SetSimulationTime(QString const & sSimulationTime);

	//!* Add the specified environment.
	void AddEnvironment(EsoEnvironment const & environment);

	//! Parse all environments
	bool ParseEnvironments(QTextStream& inputStream);

	//! Read variable names.
	bool ParseVariableNames(QTextStream& inputStream);

	//! Parse the header line and set members for version and simulationtime.
	bool ParseHeaderLine(QTextStream& inputStream);

	//! Copy constructor not allowed.
	EsoParser(EsoParser const & other);

	//! Assignment operator not allowed.
	EsoParser& operator =(EsoParser const & other);

	void ProgressNextLine();
	int GetNumLines(QFile & file, QString& sErrorMessage);

	//! Comparison operator equal not allowed.
	//friend bool operator==(EsoParser const & varInfo1, EsoParser const & varInfo2);

	std::map< int,EsoVariableInfo> m_mapVariableInfos;	//!< Variablenames.
	std::vector< EsoEnvironment> m_vEnvironments;		//!< Environments with simulation data.
	QString m_sVersion; 							//!< EnergyPlus version.
	QString m_sSimulationTime; 						//!< Date and time of simulation.
	QString m_sESOFileName;							//!< File name of the input file to parse.
	int m_iVariableIndexOfEnvironment;					//!< Variable index of environments.
	int m_iVariableIndexOfTime;							//!< Variable index of time.
	EsoVariableInfo m_emptyVariableInfo;
	int m_iCurrentLine;
	int m_iTotalLines;
};



#endif
