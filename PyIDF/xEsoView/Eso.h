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

// $Id: Eso.h,v 1.5 2007/02/27 21:18:22 cschiefer Exp $
//! General definitions.

#ifndef ESO_H
#define ESO_H

#define ESO_ORG "Christian Schiefer"
#define ESO_APP "xEsoView"

const float ESONAN = -1111111.1l;
const int iSelectionColumn 	= 0;
const int iMarkerColumn 	= 1;
const int iIdColumn 		= 2;
const int iNameColumn 		= 3;
const int iAreaColumn 		= 4;
const int iUnitColumn 		= 5;
const int iTimeStepColumn 	= 6;

enum EvDayType
{
	EvSunday 			= 0,
	EvMonday 			= 1,
	EvTuesday 			= 2,
	EvWednesday 		= 3,
	EvThursday 			= 4,
	EvFriday 			= 5,
	EvSaturday 			= 6,
	EvSummerdesignday 	= 7,
	EvWinterdesignday 	= 8,
	EvHoliday 			= 9,
	EvCustomday1 		= 10,
	EvCustomday2 		= 11
};

enum EvEsoTimeScaleView
{
	EvViewHourly = 0,
	EvViewDaily = 1,
	EvViewWeekly = 2,
	EvViewMonthly = 3,
	EvViewTotal = 4
};




struct EvTimeStruct
{
	int iDayofSimulation;
	int iMonth;
	int iDayOfMonth;
	bool bDST_Indicator; 		// [1=yes 0=no]
	int iHour;
	int iStartMinute;
	int iEndMinute;
	EvDayType iDayType;
	EvTimeStruct()
	{
		iMonth = -1; //indicates invalid date
	}
};


enum EvFileType
{
	EvFileType_NotFound,
	EvFileType_Invalid,
	EvFileType_Eso,
	EvFileType_xEso
};

#endif
