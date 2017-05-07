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

// $Id: EsoView.h,v 1.17 2007/02/27 21:18:22 cschiefer Exp $

#ifndef ESOVIEW_H
#define ESOVIEW_H
#include "ui_esoform.h"
#include "EsoUtil.h"
#include "EsoBookmark.h"


class EsoParser;
class EsoVarPlot;
class QWorkspace;
class QMainWindow;
class EsoMainWindow;


class EsoView : public QWidget
{
	Q_OBJECT
public:
	EsoView(QWidget* parent = 0);
	~EsoView();

	bool loadFile(const QString& fileName);
	bool loadxEso(const QString& fileName);
	QString userFriendlyCurrentFile();
	QString currentFile()
	{
		return m_sCurEsoFile;
	}
	bool savexEso(const QString& fileName);
	int FillList();
	void viewMax(bool bView);
	bool viewMax();
	void viewMin(bool bView);
	bool viewMin();
	void viewMarkers(bool bView);
	bool viewMarkers();
	void viewFilter(bool bView);
	bool viewFilter();
	void viewInfo(bool bView);
	bool viewInfo();
	void viewVarInfo(bool bView);
	bool viewVarInfo();
	void viewGrid(bool bView);
	bool viewGrid();
	void viewVariableList(bool bView);
	bool viewVariableList();
	void reloadEso();
	void setWorkspace(QWorkspace*);
	void setMainWindow(EsoMainWindow*);
	void copyDataToClipboard();
	void copyPicToClipboard();
	void copyOptionIncludeTime(bool bIncludeTime);
	bool copyOptionIncludeTime();
	void copyFileInfoToClipboard();
	void copyVarInfoToClipboard();
	void print();
	void printPDF();
	void Redraw();
	QTreeWidgetItem* getItem(int iId);
	QString gotoBookmark(EsoBookmark bm);
	EsoBookmark deleteBookmark(); //returns name of deleted bookmark
	QString nextBookmark();
	QString prevBookmark();
	void gotoBookmark(QString sBM);
	EsoBookmark GetCurrentAsBookmark() const;
	EsoBookmark AddCurrentToBookmarks();
	void AddToBookmarks(EsoBookmark & bm);
	int GetNumberOfBookmarks() const;
	QList<EsoBookmark> GetBookmarks() const;
	void InitBookmarkCombo();
	int GetNextAvailableBookmark();
	bool IsValidEnvironment(int iEnvironment);
	bool IsValidVariable(int iVariable);
	
protected:
	void closeEvent(QCloseEvent* event);

public slots:
	void filterChanged();
	void resetFilter();
	void setVarInfoLocal();
	void selectVar(int iVal);
	
signals:
	void setMessage(const QString& sMessage);
	void environmentSelectionChanged(int iEnvironmentIndex);
	void variableSelectionChanged(int iVariableIndex);
	void timeScaleSelectionChanged(EvEsoTimeScaleView iTimeScale);

private:
	QWorkspace* m_workspace;
	EsoMainWindow* m_mainWindow;
	QClipboard* m_clipboard;
	void showMessage(const QString& sMessage);
	void setCurrentFile(const QString& fileName);
	void print(bool bToPDF);

	QString m_sCurEsoFile;
	bool isUntitled;
	EsoParser* m_Parser;
	EsoVarPlot* m_varPlot;
	Ui::EsoForm ui;
	bool m_bCopyOptionIncludeTime;

	QList<EsoBookmark> m_vBookmarks;
	int m_iCurrentBookmark;
	bool m_bViewVariableList;
	bool m_bViewFilter;
	bool m_bViewVarInfo;
	bool m_bViewInfo;

private slots:
	void setCurrentEnvironment(int iEnvironmentIndex);
	void setCurrentTimeScale(int iTimeScale);
	void setCurrentVariable();
	void setVarInfo();
	void setCurrentItemVisible();
};


#endif
