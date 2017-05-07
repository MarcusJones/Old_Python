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

// $Id: EsoOptions.cpp,v 1.4 2006/11/17 21:48:33 cschiefer Exp $

#include "EsoOptions.h"
#include <QLocale>
#include <QSettings>
#include <QRegExpValidator>
#include <QColorDialog>
#include "EsoUtil.h"
#include "qwt_symbol.h"
#include <QColorGroup>

EsoOptions::EsoOptions(QWidget* parent) 
	: QDialog(parent)
{
	uiOptions.setupUi(this);

	//	QLocale locale;
	//	int iSel = uiOptions.comboBoxLocale->findText(locale.name());
	//	uiOptions.comboBoxLocale->setCurrentIndex(iSel);
	//	setLocale(iSel);
	QSettings settings(ESO_ORG, ESO_APP);
	uiOptions.lineEditDateFormat->setText(settings.value("DateTimeFormatForCopy", "yyyy-MM-dd hh:mm:ss").toString());

	QRegExp decPointRe("^.$");
	QRegExpValidator* decPointVal = new QRegExpValidator(decPointRe, NULL);
	uiOptions.lineEditDecimalPoint->setValidator(decPointVal);
	uiOptions.lineEditDecimalPoint->setText(settings.value("DecimalPointForCopy", ".").toString());

	uiOptions.lineEditColumnSep->setText(settings.value("ColumnSepForCopy", "\t").toString());

	connect(uiOptions.pushButtonColorBackground, SIGNAL(clicked()), this, SLOT(setBackgroundColor()));
	QColor colorBg = settings.value("GraphBackgroundColor", QColor(Qt::white)).value< QColor>();
	QPalette palette; 
	palette.setColor(QPalette::Background, colorBg);
	uiOptions.frame_BackgroundColor->setPalette(palette);
	
	connect(uiOptions.pushButtonLineColor, SIGNAL(clicked()), this, SLOT(setLineColor()));
	QColor color = settings.value("GraphLineColor", QColor(Qt::blue)).value< QColor>();
	palette.setColor(QPalette::Foreground, color);
	uiOptions.lineColor->setPalette(palette);

	connect(uiOptions.pushButtonLineColorMaxMin, SIGNAL(clicked()), this, SLOT(setLineColorMaxMin()));
	QColor colorMaxMin = settings.value("GraphLineColorMaxMin", QColor(Qt::green)).value< QColor>();
	palette.setColor(QPalette::Foreground, colorMaxMin);
	uiOptions.lineColorMaxMin->setPalette(palette);

	connect(uiOptions.pushButtonColorMarker, SIGNAL(clicked()), this, SLOT(setColorMarker()));
	QColor colorMarker = settings.value("GraphColorMarker", QColor(Qt::red)).value< QColor>();
	palette.setColor(QPalette::Foreground, colorMarker);
	uiOptions.lineColorMarker->setPalette(palette);


	int iStyle = settings.value("ApplicationStyle", GetCurrentAppStyle()).toInt();
	QStringList styleList = QStyleFactory::keys();
	uiOptions.comboBoxAppStyle->setMaxCount(styleList.size());
	uiOptions.comboBoxAppStyle->addItems(styleList);
	uiOptions.comboBoxAppStyle->setCurrentIndex(iStyle);

	//QwtSymbol sym;
	static const QChar unicodeEllipse[] =
	{
		0x006F
	}; //{0x25CB};
	static const QChar unicodeRect[] =
	{
		0x25A1
	};
	static const QChar unicodeDiamond[] =
	{
		0x25CA
	};
	static const QChar unicodeTriangleD[] =
	{
		0x2207
	};
	static const QChar unicodeTriangleU[] =
	{
		0x2206
	};
	static const QChar unicodeTriangleL[] =
	{
		0x22B3
	};
	static const QChar unicodeTriangleR[] =
	{
		0x22B2
	};
	static const QChar unicodeCross[] =
	{
		0x002B
	};
	static const QChar unicodeXCross[] =
	{
		0x00D7
	};

	QFont font = uiOptions.comboBoxMarkerStyle->font();
	font.setFamily("Lucida Sans Unicode");
	font.setPixelSize(font.pixelSize() * 2);
	uiOptions.comboBoxMarkerStyle->setFont(font);
	uiOptions.comboBoxMarkerStyle->addItem(QString::fromRawData(unicodeEllipse, 1));
	uiOptions.comboBoxMarkerStyle->addItem(QString::fromRawData(unicodeRect, 1));
	uiOptions.comboBoxMarkerStyle->addItem(QString::fromRawData(unicodeDiamond, 1));
	uiOptions.comboBoxMarkerStyle->addItem(QString::fromRawData(unicodeTriangleD, 1));
	uiOptions.comboBoxMarkerStyle->addItem(QString::fromRawData(unicodeTriangleU, 1));
	uiOptions.comboBoxMarkerStyle->addItem(QString::fromRawData(unicodeTriangleL, 1));
	uiOptions.comboBoxMarkerStyle->addItem(QString::fromRawData(unicodeTriangleR, 1));
	uiOptions.comboBoxMarkerStyle->addItem(QString::fromRawData(unicodeCross, 1));
	uiOptions.comboBoxMarkerStyle->addItem(QString::fromRawData(unicodeXCross, 1));

	int iMarkerStyle = settings.value("GraphMarkerStyle", 7).toInt();
	comboBoxMarkerStyleToolTip(iMarkerStyle);
	uiOptions.comboBoxMarkerStyle->setCurrentIndex(iMarkerStyle);
	connect(uiOptions.comboBoxMarkerStyle, SIGNAL(currentIndexChanged(int)), this, SLOT(comboBoxMarkerStyleToolTip(int)));
}


void EsoOptions::comboBoxMarkerStyleToolTip(int iMarkerStyle)
{
	switch (iMarkerStyle)
	{
		case 0:
			uiOptions.comboBoxMarkerStyle->setToolTip("Circle");
			break;
		case 1:
			uiOptions.comboBoxMarkerStyle->setToolTip("Rectangle");
			break;
		case 2:
			uiOptions.comboBoxMarkerStyle->setToolTip("Diamond");
			break;
		case 3:
			uiOptions.comboBoxMarkerStyle->setToolTip("Triangle pointing downwards");
			break;
		case 4:
			uiOptions.comboBoxMarkerStyle->setToolTip("Triangle pointing upwards");
			break;
		case 5:
			uiOptions.comboBoxMarkerStyle->setToolTip("Triangle pointing left");
			break;
		case 6:
			uiOptions.comboBoxMarkerStyle->setToolTip("Triangle pointing right");
			break;
		case 7:
			uiOptions.comboBoxMarkerStyle->setToolTip("Cross");
			break;
		case 8:
			uiOptions.comboBoxMarkerStyle->setToolTip("Diagonal cross");
			break;
		default:
			uiOptions.comboBoxMarkerStyle->setToolTip("");
	}
}


void EsoOptions::setBackgroundColor()
{
	QPalette palette = uiOptions.frame_BackgroundColor->palette();
	QColor color = QColorDialog::getColor(palette.color(QPalette::Background), this);
	if (color.isValid())
	{
		palette.setColor(QPalette::Background, color);
		uiOptions.frame_BackgroundColor->setPalette(palette);
	}
}


void EsoOptions::setLineColor()
{
	QPalette palette = uiOptions.lineColor->palette();
	QColor color = QColorDialog::getColor(palette.color(QPalette::Foreground), this);
	if (color.isValid())
	{
		palette.setColor(QPalette::Foreground, color);
		uiOptions.lineColor->setPalette(palette);
	}
}


void EsoOptions::setLineColorMaxMin()
{
	QPalette palette = uiOptions.lineColorMaxMin->palette();
	QColor color = QColorDialog::getColor(palette.color(QPalette::Foreground), this);
	if (color.isValid())
	{
		palette.setColor(QPalette::Foreground, color);
		uiOptions.lineColorMaxMin->setPalette(palette);
	}
}


void EsoOptions::setColorMarker()
{
	QPalette palette = uiOptions.lineColorMarker->palette();
	QColor color = QColorDialog::getColor(palette.color(QPalette::Foreground), this);
	if (color.isValid())
	{
		palette.setColor(QPalette::Foreground, color);
		uiOptions.lineColorMarker->setPalette(palette);
	}
}

