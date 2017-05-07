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

// $Id: EsoScrollbar.cpp,v 1.3 2006/04/25 20:41:04 cschiefer Exp $

#include <qstyle.h>
#if QT_VERSION >= 0x040000
#include <qstyleoption.h>
#endif
#include "EsoScrollbar.h"

EsoScrollBar::EsoScrollBar(QWidget* parent)
	: QScrollBar(parent)
{
	init();
}

EsoScrollBar::EsoScrollBar(Qt::Orientation o, QWidget* parent)
	: QScrollBar(o, parent)
{
	init();
}

EsoScrollBar::EsoScrollBar(float minBase, float maxBase, Qt::Orientation o, QWidget* parent)
	: QScrollBar(o, parent)
{
	init();
	setBase(minBase, maxBase);
	moveSlider(minBase, maxBase);
}

void EsoScrollBar::init()
{
	d_inverted = orientation() == Qt::Vertical;
	d_baseTicks = 1000000;
	d_minBase = 0.0;
	d_maxBase = 1.0;
	moveSlider(d_minBase, d_maxBase);

	connect(this, SIGNAL(sliderMoved(int)), SLOT(catchSliderMoved(int)));
	connect(this, SIGNAL(valueChanged(int)), SLOT(catchValueChanged(int)));
}

void EsoScrollBar::setInverted(bool inverted)
{
	if (d_inverted != inverted)
	{
		d_inverted = inverted;
		moveSlider(minSliderValue(), maxSliderValue());
	}
}

bool EsoScrollBar::isInverted() const
{
	return d_inverted;
}

void EsoScrollBar::setBase(float min, float max)
{
	if (min != d_minBase || max != d_maxBase)
	{
		d_minBase = min;
		d_maxBase = max;

		moveSlider(minSliderValue(), maxSliderValue());
	}
}

void EsoScrollBar::moveSlider(float min, float max)
{
	const int sliderTicks = qRound((max - min) / (d_maxBase - d_minBase) * d_baseTicks);

	// setRange initiates a valueChanged of the scrollbars
	// in some situations. So we block
	// and unblock the signals.

	blockSignals(true);

	setRange(sliderTicks / 2, d_baseTicks - sliderTicks / 2);
	int steps = sliderTicks / 200;
	if (steps <= 0)
		steps = 1;

#if QT_VERSION < 0x040000
	setSteps(steps, sliderTicks);
#else
	setSingleStep(steps);
	setPageStep(sliderTicks);
#endif

	int tick = mapToTick(min + (max - min) / 2);
	if (isInverted())
		tick = d_baseTicks - tick;

#if QT_VERSION < 0x040000
	directSetValue(tick);
	rangeChange();
#else
	setSliderPosition(tick);
#endif
	blockSignals(false);
}

float EsoScrollBar::minBaseValue() const
{
	return d_minBase;
}

float EsoScrollBar::maxBaseValue() const
{
	return d_maxBase;
}

void EsoScrollBar::sliderRange(int value, float& min, float& max) const
{
	if (isInverted())
		value = d_baseTicks - value;

	const int visibleTicks = pageStep();

	min = mapFromTick(value - visibleTicks / 2);
	max = mapFromTick(value + visibleTicks / 2);
}

float EsoScrollBar::minSliderValue() const
{
	float min, dummy;
	sliderRange(value(), min, dummy);

	return min;
}

float EsoScrollBar::maxSliderValue() const
{
	float max, dummy;
	sliderRange(value(), dummy, max);

	return max;
}

int EsoScrollBar::mapToTick(float v) const
{
	return (int) ((v - d_minBase) / (d_maxBase - d_minBase) * d_baseTicks);
}

float EsoScrollBar::mapFromTick(int tick) const
{
	return d_minBase + (d_maxBase - d_minBase) * tick / d_baseTicks;
}

void EsoScrollBar::catchValueChanged(int value)
{
	float min, max;
	sliderRange(value, min, max);
	emit valueChanged(orientation(), min, max);
}

void EsoScrollBar::catchSliderMoved(int value)
{
	float min, max;
	sliderRange(value, min, max);
	emit sliderMoved(orientation(), min, max);
}

int EsoScrollBar::extent() const
{
#if QT_VERSION < 0x040000
	return style().pixelMetric(QStyle::PM_ScrollBarExtent, this);
#else
	QStyleOptionSlider opt;
	opt.init(this);
	opt.subControls = QStyle::SC_None;
	opt.activeSubControls = QStyle::SC_None;
	opt.orientation = orientation();
	opt.minimum = minimum();
	opt.maximum = maximum();
	opt.sliderPosition = sliderPosition();
	opt.sliderValue = value();
	opt.singleStep = singleStep();
	opt.pageStep = pageStep();
	opt.upsideDown = invertedAppearance();
	if (orientation() == Qt::Horizontal)
		opt.state |= QStyle::State_Horizontal;
	return style()->pixelMetric(QStyle::PM_ScrollBarExtent, &opt, this);
#endif
}
