/***************************************************************************
 *   Copyright (C) 2005 	Christian Schiefer, Vienna, Austria 		   *
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

// $Id: EsoScrollbar.h,v 1.3 2006/04/25 20:41:04 cschiefer Exp $

#ifndef ESOSCROLLBAR_H
#define ESOSCROLLBAR_H

#include <QScrollBar>

class EsoScrollBar : public QScrollBar
{
	Q_OBJECT

public:
	EsoScrollBar(QWidget* parent = NULL);
	EsoScrollBar(Qt::Orientation, QWidget* parent = NULL);
	EsoScrollBar(float minBase, float maxBase, Qt::Orientation o, QWidget* parent = NULL);

	void setInverted(bool);
	bool isInverted() const;

	float minBaseValue() const;
	float maxBaseValue() const;

	float minSliderValue() const;
	float maxSliderValue() const;

	int extent() const;

signals:
	void sliderMoved(Qt::Orientation, float, float);
	void valueChanged(Qt::Orientation, float, float);

public slots:
	virtual void setBase(float min, float max);
	virtual void moveSlider(float min, float max);

protected:
	void sliderRange(int value, float& min, float& max) const;
	int mapToTick(float) const;
	float mapFromTick(int) const;

private slots:
	void catchValueChanged(int value);
	void catchSliderMoved(int value);

private:
	void init();

	bool d_inverted;
	float d_minBase;
	float d_maxBase;
	int d_baseTicks;
};

#endif
