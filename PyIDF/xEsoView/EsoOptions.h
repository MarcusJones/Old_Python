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

// $Id: EsoOptions.h,v 1.3 2006/11/17 21:48:33 cschiefer Exp $

#ifndef ESOOPTIONS_H
#define ESOOPTIONS_H
#include "ui_options.h"

class EsoOptions : public QDialog
{
	Q_OBJECT
public:
	EsoOptions(QWidget* parent = 0);
	Ui::DialogOptions uiOptions;

private slots:
	void setBackgroundColor();
	void setLineColor();
	void setLineColorMaxMin();
	void setColorMarker();
	void comboBoxMarkerStyleToolTip(int iStyle);
};

#endif
