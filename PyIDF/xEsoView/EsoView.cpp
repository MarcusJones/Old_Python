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

// $Id: EsoView.cpp,v 1.28 2008/03/01 21:02:55 cschiefer Exp $

#include <QtGui>
#include <QListView>
#include <QPrinter>
#include <QTreeWidgetItem>
#include <QString>
#include <QTextStream>

#include "EsoView.h"
#include "ui_esoform.h"
#include "EsoParser.h"
#include "EsoVarPlot.h"
#include "EsoUtil.h"
#include "EsoBookmark.h"
#include "EsoMainWindow.h"


EsoView::EsoView(QWidget* parent) 
	: QWidget(parent)
{
	qDebug("EsoView::EsoView(QWidget *parent) - start");
	setAttribute(Qt::WA_DeleteOnClose);

	qDebug("EsoView::EsoView(QWidget *parent) - setup ui");
	ui.setupUi(this);

	qDebug("EsoView::EsoView(QWidget *parent) - init qwt plot window");
	m_varPlot = new EsoVarPlot(parent, ui.qwtPlot);

	qDebug("EsoView::EsoView(QWidget *parent) - create new parser");
	m_Parser = new EsoParser();
	m_varPlot->SetParser(m_Parser);
	m_workspace = NULL;
	m_mainWindow = NULL;
	m_bCopyOptionIncludeTime = true;

	qDebug("EsoView::EsoView(QWidget *parent) - add comboBoxTimeAxis items");
	ui.comboBoxTimeAxis->setMaxCount(5);
	ui.comboBoxTimeAxis->insertItem(EvViewHourly, tr("hour"));
	ui.comboBoxTimeAxis->insertItem(EvViewDaily, tr("day"));
	ui.comboBoxTimeAxis->insertItem(EvViewWeekly, tr("week"));
	ui.comboBoxTimeAxis->insertItem(EvViewMonthly, tr("month"));
	ui.comboBoxTimeAxis->insertItem(EvViewTotal, tr("total"));

	qDebug("EsoView::EsoView(QWidget *parent) - set time axis");
	ui.comboBoxTimeAxis->setCurrentIndex(EvViewTotal);//total

	connect(this, SIGNAL(environmentSelectionChanged(int)), m_varPlot, SLOT(setCurrentEnvironment(int)));
	connect(this, SIGNAL(variableSelectionChanged(int)), m_varPlot, SLOT(setCurrentVariable(int)));
	connect(this, SIGNAL(timeScaleSelectionChanged(EvEsoTimeScaleView)), m_varPlot, SLOT(setCurrentTimeScale(EvEsoTimeScaleView)));
	connect(m_varPlot, SIGNAL(updateVarInfo()), this, SLOT(setVarInfo()));
	connect(m_varPlot, SIGNAL(redraw()), this, SLOT(setVarInfoLocal()));

	connect(ui.treeWidget->header(), SIGNAL(sectionClicked(int)),this, SLOT(setCurrentItemVisible()));

	connect(ui.treeWidget, SIGNAL(itemSelectionChanged()), this, SLOT(setCurrentVariable()));
	connect(ui.comboBoxEnvironment, SIGNAL(activated(int)), this, SLOT(setCurrentEnvironment(int)));
	connect(ui.comboBoxTimeAxis, SIGNAL(highlighted(int)), this, SLOT(setCurrentTimeScale(int)));
	connect(ui.pushButtonPrevious, SIGNAL(clicked()), m_varPlot, SLOT(pushButtonBack_clicked()));
	connect(ui.pushButtonNext, SIGNAL(clicked()), m_varPlot, SLOT(pushButtonForward_clicked()));

	connect(ui.lineEditFilterName, SIGNAL(returnPressed()), this, SLOT(filterChanged()));
	connect(ui.lineEditFilterArea, SIGNAL(returnPressed()), this, SLOT(filterChanged()));
	connect(ui.lineEditFilterTimestep, SIGNAL(returnPressed()), this, SLOT(filterChanged()));
	connect(ui.lineEditFilterUnit, SIGNAL(returnPressed()), this, SLOT(filterChanged()));
	connect(ui.pushButtonFilter, SIGNAL(clicked()), this, SLOT(filterChanged()));
	connect(ui.pushButtonClearFilter, SIGNAL(clicked()), this, SLOT(resetFilter()));

	m_bViewVariableList = true;
	m_bViewFilter = true;
	m_bViewVarInfo = true;
	m_bViewInfo = true;
	
	qDebug("EsoView::EsoView(QWidget *parent) - add header");
	QStringList header;
	//Selection, Bookmark, Id, Name, Area, Unit, Timestep
	header << "" << "" << "Id" << "Name" << "Area" << "Unit" << "Timestep" << "";
	ui.treeWidget->setHeaderLabels(header);
	ui.treeWidget->setSortingEnabled(true);  //enable sorting
	ui.treeWidget->sortItems(iIdColumn, Qt::AscendingOrder);
	ui.treeWidget->setRootIsDecorated(false);//hide tree lines
	ui.treeWidget->setColumnHidden(iMarkerColumn, true);
	qDebug("EsoView::EsoView(QWidget *parent) - end");


	ui.labelMax->setText("");
	ui.labelMin->setText("");
	ui.labelAvg->setText("");
	m_clipboard = QApplication::clipboard();
	m_iCurrentBookmark=-1;

	qDebug("EsoView::EsoView(QWidget *parent) - end");
}


EsoView::~EsoView()
{
	//write bookmarks
	SetFlag("viewMin", m_sCurEsoFile, viewMin());
	SetFlag("viewMax", m_sCurEsoFile, viewMax());
	SetFlag("viewGrid", m_sCurEsoFile, viewGrid());
	SetFlag("viewMarkers", m_sCurEsoFile, viewMarkers());
	
	SetFlag("viewFilter", m_sCurEsoFile, viewFilter());	
	SetFlag("viewInfo", m_sCurEsoFile, viewInfo());
	SetFlag("viewVarInfo", m_sCurEsoFile, viewVarInfo());
	SetFlag("viewVarList", m_sCurEsoFile, viewVariableList());
	SetCurrent( m_sCurEsoFile, GetCurrentAsBookmark());
	SetBookmarks(m_sCurEsoFile, m_vBookmarks);
	m_mainWindow->getBookmarkCombo()->clear();
}

void EsoView::resetFilter()
{
	ui.treeWidget->setUpdatesEnabled(false);
	QList< QTreeWidgetItem*> all = ui.treeWidget->findItems("", Qt::MatchContains);
	//make all visible
	foreach(QTreeWidgetItem * item, all)
		ui.treeWidget->setItemHidden(item, false);
	//clear filter edits
	ui.lineEditFilterName->clear();
	ui.lineEditFilterArea->clear();
	ui.lineEditFilterUnit->clear();
	ui.lineEditFilterTimestep->clear();
	ui.groupBoxFilter->setToolTip("");
	ui.treeWidget->setUpdatesEnabled(true);
	if (ui.treeWidget->currentItem() != NULL)
		ui.treeWidget->scrollToItem(ui.treeWidget->currentItem());
	ui.treeWidget->repaint();
	showMessage(tr("Ready"));
}


void EsoView::filterChanged()
{
	qDebug() << "EsoView::filterChanged - start";
	qDebug() << "EsoView::filterChanged - name " << ui.lineEditFilterName->text();
	qDebug() << "EsoView::filterChanged - area " << ui.lineEditFilterArea->text();
	qDebug() << "EsoView::filterChanged - timestep " << ui.lineEditFilterTimestep->text();
	qDebug() << "EsoView::filterChanged - unit " << ui.lineEditFilterUnit->text();
	showMessage(tr("Filter ..."));
	ui.treeWidget->setUpdatesEnabled(false);
	QList< QTreeWidgetItem*> found;
	QList< QTreeWidgetItem*> all = ui.treeWidget->findItems("", Qt::MatchContains);
	QSet< QTreeWidgetItem*> allfound = QSet< QTreeWidgetItem*>::fromList(all);

	//make all hidden
	foreach(QTreeWidgetItem * item, all)
		ui.treeWidget->setItemHidden(item, true);

	bool bReset = true;
	//name
	if (!ui.lineEditFilterName->text().isEmpty())
	{
		found = ui.treeWidget->findItems(ui.lineEditFilterName->text(), Qt::MatchContains, iNameColumn);
		allfound.intersect(QSet< QTreeWidgetItem*>::fromList(found));
		bReset = false;
	}

	//area
	if (!ui.lineEditFilterArea->text().isEmpty())
	{
		found = ui.treeWidget->findItems(ui.lineEditFilterArea->text(), Qt::MatchContains, iAreaColumn);
		allfound.intersect(QSet< QTreeWidgetItem*>::fromList(found));
		bReset = false;
	}

	//unit
	if (!ui.lineEditFilterUnit->text().isEmpty())
	{
		found = ui.treeWidget->findItems(ui.lineEditFilterUnit->text(), Qt::MatchContains, iUnitColumn);
		allfound.intersect(QSet< QTreeWidgetItem*>::fromList(found));
		bReset = false;
	}

	//area
	if (!ui.lineEditFilterTimestep->text().isEmpty())
	{
		found = ui.treeWidget->findItems(ui.lineEditFilterTimestep->text(), Qt::MatchContains, iTimeStepColumn);
		allfound.intersect(QSet< QTreeWidgetItem*>::fromList(found));
		bReset = false;
	}

	QString sTip;
	if (bReset)
	{
		resetFilter();
		showMessage(tr("Ready"));
		ui.groupBoxFilter->setToolTip("");
	} else
	{
	  	//show found items
	  	foreach(QTreeWidgetItem * item, allfound)
	  		ui.treeWidget->setItemHidden(item, false);

		if (allfound.isEmpty())
		{
			sTip = tr("Nothing found");
			showMessage(sTip);
		} else
		{
	  	  	sTip = tr("Filtered out %1 from %2").arg(allfound.count()).arg(all.count());
	  	  	showMessage(sTip);
		}
	}
	ui.groupBoxFilter->setToolTip(sTip);
	ui.treeWidget->setUpdatesEnabled(true);
	if (ui.treeWidget->currentItem() != NULL && ! ui.treeWidget->isItemHidden(ui.treeWidget->currentItem()) )
		ui.treeWidget->scrollToItem(ui.treeWidget->currentItem());
	ui.treeWidget->repaint();
	qDebug() << "EsoView::filterChanged - end";
}


void EsoView::setWorkspace(QWorkspace* ws)
{
	m_workspace = ws;
}



void EsoView::setMainWindow(EsoMainWindow* mw)
{
	m_mainWindow = mw;
}


bool EsoView::loadFile(const QString& fileName)
{
	qDebug() << "EsoView::loadFile(" << fileName << ") - start";

	if (!m_workspace)
	{
		qDebug("EsoView::loadFile Workspace not set!");
		return false;
	}
	if (!m_mainWindow)
	{
		qDebug("EsoView::loadFile main window not set!");
		return false;
	}
	QApplication::setOverrideCursor(Qt::WaitCursor);

	//load eso
	QProgressBar* progress = new QProgressBar();
	connect(m_Parser, SIGNAL(setParseProgress(int)), progress, SLOT(setValue(int)));
	connect(m_Parser, SIGNAL(setTotalParseSteps(int)), progress, SLOT(setMaximum(int)));

	m_mainWindow->statusBar()->addPermanentWidget(progress);
	setCurrentFile(fileName);
	showMessage(tr("Parsing file "));
	QString sErrorMessage;
	if (!m_Parser->Parse(fileName, sErrorMessage))
	{
		QApplication::restoreOverrideCursor();
		QMessageBox::warning(this, ESO_APP, sErrorMessage, QMessageBox::Ok, QMessageBox::NoButton);
		delete progress;
		progress = NULL;
		return false;
	}
	qDebug("EsoView::loadFile - finished parsing");

	//add environements to
	showMessage(tr("Set environments"));
	qDebug("EsoView::loadFile - set environments");
	qApp->processEvents();
	int iNumEnv = m_Parser->GetNumberOfEnvironments();
	EsoEnvironment* env = NULL;
	ui.comboBoxEnvironment->clear();
	for (int i = 0; i < iNumEnv; ++i)
	{
		env = m_Parser->GetEnvironmentPtr(i);
		if (env != NULL)
		{
			if (i == 0)
				ui.comboBoxEnvironment->setToolTip(env->GetInfo(false));
			ui.comboBoxEnvironment->insertItem(i, env->GetInfo(true));
		}
	}
	//select first environment
	int iEnvironment = 0;
	ui.comboBoxEnvironment->setCurrentIndex(iEnvironment);
	environmentSelectionChanged(iEnvironment);


	//set info
	qDebug("EsoView::loadFile - set file info");
	showMessage(tr("Set file info"));
	qApp->processEvents();
	QFileInfo fi(m_Parser->GetESOFile());
	QString sInfo = fi.absoluteFilePath() + "\n" + m_Parser->GetEPVersion() + "\n" + m_Parser->GetSimulationTime();
	ui.labelFileInfo->setText(sInfo);
	ui.labelFileInfo->setWordWrap(true);
	ui.labelFileInfo->setToolTip(sInfo);

	m_mainWindow->statusBar()->removeWidget(progress);
	delete progress;
	progress = NULL;
	qApp->processEvents();

	//fill list
	showMessage(tr("Fill variable list"));
	qApp->processEvents();
	int iNumVars = FillList();
	
	//select first variable
	qDebug() << "EsoView::loadFile - select first variable";
	ui.treeWidget->setCurrentItem(ui.treeWidget->topLevelItem(0));
	ui.treeWidget->scrollToItem(ui.treeWidget->currentItem());

	showMessage(tr("Init plot"));
	qApp->processEvents();
//	m_varPlot->GetQwtPlot()->setCanvasBackground(QColor("white"));

	//read bookmarks from config file
	QList<EsoBookmark> vBookmarks = GetRecentBookmarks( m_sCurEsoFile );
	
	//read view flags from config file
	viewMin(GetFlag("viewMin", m_sCurEsoFile));
	viewMax(GetFlag("viewMax", m_sCurEsoFile));
	viewGrid(GetFlag("viewGrid", m_sCurEsoFile));	
	viewMarkers(GetFlag("viewMarkers", m_sCurEsoFile));	
	viewFilter(GetFlag("viewFilter", m_sCurEsoFile));	
	viewInfo(GetFlag("viewInfo", m_sCurEsoFile));
	viewVarInfo(GetFlag("viewVarInfo", m_sCurEsoFile));
	viewVariableList(GetFlag("viewVarList", m_sCurEsoFile));
	
	//add bookmarks
	for (int i=0; i<vBookmarks.size(); ++i)
		AddToBookmarks(vBookmarks[i]);
	
	InitBookmarkCombo();
	
	//read current view from config
	EsoBookmark bm = GetCurrent(m_sCurEsoFile);
	//select timescale
	EvEsoTimeScaleView timescale = bm.GetTimeScale();
	qDebug() << "EsoView::loadFile() - set time scale to " << timescale;
	ui.comboBoxTimeAxis->setCurrentIndex( (int)timescale );
	
	if ( IsValidEnvironment(bm.GetEnvironment()) && IsValidVariable(bm.GetVariable()) )	
	{
		qDebug("EsoView::loadFile - select current view");
		gotoBookmark( bm );
	}
	else
	{
		qDebug("EsoView::loadFile - select first variable");
		ui.treeWidget->setCurrentItem(ui.treeWidget->topLevelItem(0));
	}


	if (iNumVars == 0)
	{
		QMessageBox::warning(this, ESO_APP, "No variable data found!\n", QMessageBox::Ok, QMessageBox::NoButton);
	}

	QApplication::restoreOverrideCursor();
	qDebug("EsoView::loadFile(const QString &fileName) - end");
	return true;
}


bool EsoView::IsValidEnvironment(int iEnvironment)
{
	if (m_Parser==NULL)
		return false;
	return (m_Parser->GetEnvironmentPtr( iEnvironment ) != NULL);
}


bool EsoView::IsValidVariable(int iVariable)
{
	if (m_Parser==NULL)
		return false;
	EsoVariableInfo info = m_Parser->GetVariableInfo( iVariable );
	if (iVariable>=0 && (int)info.GetIndex() == iVariable )
		return true;
	return false; 
}


void EsoView::showMessage(const QString& sMessage)
{
	emit setMessage(sMessage);
}


int EsoView::FillList()
{
	qDebug("EsoView::FillList() - start");
	QProgressBar* progress = new QProgressBar(this->parentWidget());
	ui.treeWidget->clear();
	ui.treeWidget->setUpdatesEnabled(false);

	//get current environement
	EsoEnvironment env;
	qDebug("EsoView::FillList() - get environment");
	m_Parser->GetEnvironment(ui.comboBoxEnvironment->currentIndex(), env);

	//fill table
	std::map< int,EsoVariableInfo>::const_iterator iter;
	std::map< int,EsoVariableInfo>::const_iterator iterBegin;
	std::map< int,EsoVariableInfo>::const_iterator iterEnd;
	qDebug("EsoView::FillList() - get variable info");
	m_Parser->GetVariableInfo(iterBegin, iterEnd);
	int iNumVars = (int) std::distance(iterBegin, iterEnd);
	progress->setMaximum(iNumVars);
	qDebug("EsoView::FillList() - number of variables: %d", iNumVars);

	qDebug("EsoView::FillList() - fill list start");
	int i = 0;
	QString sTip, sId;
	QTextStream streamId(&sId);
	streamId.setFieldWidth(6);
	streamId.setFieldAlignment(QTextStream::AlignRight);
	for (iter = iterBegin; iter != iterEnd; ++iter, ++i)
	{
		progress->setValue(i);
		qApp->processEvents();
		if (env.IsEmpty(iter->first))
		{
			qDebug() << "Skipping variable without data: " << iter->second.GetColumnInfo(0).m_sName;
			continue;
		}
		QTreeWidgetItem* row = new QTreeWidgetItem(ui.treeWidget);
		sTip = "Id:  \t" + QString("%1").arg(iter->first) + "\n" +
			"Name:\t" +	iter->second.GetColumnInfo(1).m_sName + "\n" +
			"Area:\t" + iter->second.GetColumnInfo(0).m_sName + "\n" +
			"Unit:\t" + iter->second.GetColumnInfo(1).m_sUnit + "\n" +
			"TimeStep:\t" + ConvertToString(iter->second.GetReportStep());
		
		QCheckBox * cb = new QCheckBox(ui.treeWidget);
		
		cb->setCheckState(Qt::Unchecked);
		ui.treeWidget->setItemWidget(row,iSelectionColumn ,cb);

		connect(ui.treeWidget->itemWidget(row, iSelectionColumn), SIGNAL(stateChanged(int)), this, SLOT(selectVar(int)));

		row->setText(iMarkerColumn, ""); /*marker*/
		
		sId = "";
		streamId << iter->first << " ";
		row->setTextAlignment(iIdColumn, Qt::AlignRight);
		row->setText(iIdColumn, sId); /*variable number*/
		row->setToolTip(iIdColumn, sTip);
		
		cb->setObjectName(sId);
		
		row->setText(iNameColumn, iter->second.GetColumnInfo(1).m_sName+" "); /*name*/
		row->setToolTip(iNameColumn, sTip);

		row->setText(iAreaColumn, iter->second.GetColumnInfo(0).m_sName+" "); /*area*/
		row->setToolTip(iAreaColumn, sTip);

		row->setText(iUnitColumn, iter->second.GetColumnInfo(1).m_sUnit+" "); /*Unit*/
		row->setToolTip(iUnitColumn, sTip);

		row->setText(iTimeStepColumn, ConvertToString(iter->second.GetReportStep())+" "); /*TimeStep*/
		row->setToolTip(iTimeStepColumn, sTip);
	}
	ui.treeWidget->setUpdatesEnabled(true);
	for (int i = 0; i< ui.treeWidget->columnCount(); ++i)
	{
		if (i==iMarkerColumn || i == iIdColumn || i == iUnitColumn || i == iTimeStepColumn)
			ui.treeWidget->resizeColumnToContents(i);
		qDebug() << "EsoView::FillList() - width=" << ui.treeWidget->columnWidth(i) << " for column "<<i;
	}

	//filter - make sure that list is filtered after switching of environment
	filterChanged();

	//select variable - make sure that variable is selected after switching of environment
	if (m_varPlot != NULL)
	{
	    int iVar = m_varPlot->getVariable();
	    qDebug() << "EsoView::FillList() - select variable " << iVar;
	    if (iVar>0)
	    {
			QTreeWidgetItem * curItem = getItem(iVar);
			if (curItem != NULL)
			{
				ui.treeWidget->setCurrentItem(curItem);
		    	variableSelectionChanged(iVar);
			}
		}
	}

	delete progress;
	progress = NULL;
	qDebug("EsoView::FillList() - end");
	return iNumVars;
}


void EsoView::selectVar(int iVal)
{
	QString sId = "-1"; 
	
	qDebug() << "EsoView::selectVar - Start";
	QCheckBox * cb = qobject_cast< QCheckBox*>(sender());
	if (cb)
	{
		int iVar = cb->objectName().toInt(); /*variable number*/
		bool bSel = iVal==0 ? false : true;
		qDebug() << "EsoView::selectVar: Var " << iVar << (bSel ? " selected" : " unselected");
		QTreeWidgetItem * currentItem = getItem(iVar);
		ui.treeWidget->setCurrentItem(currentItem);
		m_varPlot->setSelection(iVar, bSel);
	}
	qDebug() << "EsoView::selectVar - End";
}

QString EsoView::userFriendlyCurrentFile()
{
	return QFileInfo(m_sCurEsoFile).absoluteFilePath();
}


void EsoView::closeEvent(QCloseEvent* event)
{
	if (true /*maybeSave()*/)
	{
		event->accept();
	} else
	{
		event->ignore();
	}
}


void EsoView::setCurrentFile(const QString& fileName)
{
	QFileInfo info(fileName);
	if (info.exists())
	{
		m_sCurEsoFile = info.canonicalFilePath();
		setWindowModified(false);
		setWindowTitle(m_sCurEsoFile);
	}
}

QTreeWidgetItem* EsoView::getItem(int iId)
{
	qDebug() << "EsoView::getItem(" << iId << ")";
	QString sId;
	QTextStream streamId(&sId);
	streamId.setFieldWidth(6);
	streamId.setFieldAlignment(QTextStream::AlignRight);
	streamId << iId  << " ";
	QList< QTreeWidgetItem*> cur = ui.treeWidget->findItems( sId, Qt::MatchExactly, iIdColumn);
	if (cur.size() == 1)
	    return cur[0];
	return NULL;
}


void EsoView::setCurrentVariable()
{
	QTreeWidgetItem * curItem = ui.treeWidget->currentItem();
	if (curItem == NULL)
	{
		qCritical() << "EsoView::setCurrentVariable -  current item == NULL";
		return;
	}
	int i = curItem->text(iIdColumn).toInt();
	qDebug("EsoView::setCurrentVariable(%d)", i);
	QTreeWidgetItem* currentItem = getItem(i);
	int iPrev = m_varPlot->getVariable();
	
	//make sure that only one variable is selected
	QList<QTreeWidgetItem *> selctedItems = ui.treeWidget->selectedItems();
	if (selctedItems.size()>1)
	{
		for (int i = 0; i < selctedItems.size(); ++i)
		{
			if (currentItem!=selctedItems[i])
	        	ui.treeWidget->setItemSelected(selctedItems[i], false);
		}
	}

	if (iPrev != i) //replot only if selection changed
	{
		emit variableSelectionChanged(i);
	}
	ui.treeWidget->setItemSelected(currentItem, true);

}


void EsoView::setVarInfo()
{
	qDebug("EsoView::setVarInfo");
	if (m_Parser==NULL)
		 return;
	ui.groupBoxVariableInfo->setTitle(QString("Variable Information - %1").arg( m_Parser->GetVariableTitle( m_varPlot->getVariable() )) );
	ui.groupBoxVarInfo->setTitle(QString("Total: %1 - %2").arg(m_varPlot->getStart(), m_varPlot->getEnd()));
	ui.labelMax->setText(ConvertToString(m_varPlot->getMax()));
	ui.labelMin->setText(ConvertToString(m_varPlot->getMin()));
	ui.labelAvg->setText(ConvertToString(m_varPlot->getAvg()));
}


void EsoView::setVarInfoLocal()
{
	qDebug("EsoView::setVarInfoLocal");
	QString str;
	ui.groupBoxVarInfoLocal->setTitle(QString("Visible: %1 - %2").arg(m_varPlot->getStartLocal(), m_varPlot->getEndLocal()));
	ui.labelMaxLocal->setText(ConvertToString(m_varPlot->getMaxLocal()));
	ui.labelMinLocal->setText(ConvertToString(m_varPlot->getMinLocal()));
	ui.labelAvgLocal->setText(ConvertToString(m_varPlot->getAvgLocal()));
}


void EsoView::setCurrentEnvironment(int iEnvironmentIndex)
{
	qDebug("EsoView::setCurrentEnvironment(%d)", iEnvironmentIndex);
	if (m_varPlot->getEnvironment() == iEnvironmentIndex)
	    return;
	EsoEnvironment* env = m_Parser->GetEnvironmentPtr(iEnvironmentIndex);
	if (env != NULL)
		ui.comboBoxEnvironment->setToolTip(env->GetInfo(false));
	emit environmentSelectionChanged(iEnvironmentIndex);

	//FillList();

	//this is a workaround to force redrawing of the time axis
	m_varPlot->GetQwtPlot()->setUpdatesEnabled(false);
	EvEsoTimeScaleView iTimeScale = m_varPlot->getTimeScale();
	if ((int)iTimeScale == 0)
		setCurrentTimeScale((EvEsoTimeScaleView)1);
	else
		setCurrentTimeScale((EvEsoTimeScaleView)0);
	setCurrentTimeScale(iTimeScale);
	
	m_varPlot->GetQwtPlot()->setUpdatesEnabled(true);
	setCurrentItemVisible();
}


void EsoView::setCurrentTimeScale(int iTimeScale)
{
	//0=hour, 1=daily, 2=weekly, 3=monthly, 4=total,
	qDebug("EsoView::setCurrentTimeScale(%d)", iTimeScale);
	emit timeScaleSelectionChanged((EvEsoTimeScaleView) iTimeScale);
}

void EsoView::viewMax(bool bView)
{
	m_varPlot->viewMax(bView);
}


bool EsoView::viewMax()
{
	return m_varPlot->viewMax();
}


void EsoView::viewMin(bool bView)
{
	m_varPlot->viewMin(bView);
}


bool EsoView::viewMin()
{
	return m_varPlot->viewMin();
}


void EsoView::viewGrid(bool bView)
{
	m_varPlot->viewGrid(bView);
}


bool EsoView::viewGrid()
{
	return m_varPlot->viewGrid();
}


void EsoView::Redraw()
{
	m_varPlot->Redraw();	
}


void EsoView::print()
{
	print(false);
}

void EsoView::print(bool bToPDF)
{
	qDebug("EsoView::print()");
	QPrinter printer(QPrinter::HighResolution);
	printer.setDocName(m_varPlot->getTitle());
	printer.setCreator(ESO_APP);
	printer.setOrientation(QPrinter::Landscape);
	
	if (bToPDF)
	{
		QString fileName = QFileDialog::getSaveFileName(this, "Export PDF", QString(), "*.pdf");
		if (fileName.isEmpty())
			return;
		printer.setOutputFormat(QPrinter::PdfFormat);
		printer.setOutputFileName(fileName);
		m_varPlot->print(printer);
	} else
	{
	  	QPrintDialog dialog(&printer);
		if (dialog.exec())
		{
			QwtPlotPrintFilter filter;
	  		//  		  filter.setOptions(QwtPlotPrintFilter::PrintAll);
			if (printer.colorMode() == QPrinter::GrayScale)
			{
	  			filter.setOptions(QwtPlotPrintFilter::PrintAll & ~QwtPlotPrintFilter::PrintCanvasBackground);
			}
	  		m_varPlot->print(printer, filter);
		} else
			qDebug("EsoView::print() - user canceled");
	}
}


void EsoView::printPDF()
{
	print(true);
}


void EsoView::viewMarkers(bool bView)
{
	m_varPlot->viewMarkers(bView);
}


bool EsoView::viewMarkers()
{
	return m_varPlot->viewMarkers();
}


void EsoView::viewFilter(bool bView)
{
	ui.groupBoxFilter->setVisible(bView);
	ui.groupBoxFilter->setChecked(bView);
	m_bViewFilter = bView;
}


bool EsoView::viewFilter()
{
	return m_bViewFilter;
}


void EsoView::viewInfo(bool bView)
{
	ui.groupBoxFileInfo->setVisible(bView);
	ui.groupBoxFileInfo->setChecked(bView);
	m_bViewInfo = bView;
}


bool EsoView::viewInfo()
{
	return m_bViewInfo;
}


void EsoView::viewVarInfo(bool bView)
{
	ui.groupBoxVariableInfo->setVisible(bView);
	ui.groupBoxVariableInfo->setChecked(bView);
	m_bViewVarInfo = bView;
}


bool EsoView::viewVarInfo()
{
	return m_bViewVarInfo;
}


void EsoView::viewVariableList(bool bView)
{
	ui.frameVariableList->setVisible(bView);
	m_bViewVariableList = bView;
}


bool EsoView::viewVariableList()
{
	return m_bViewVariableList;
}


void EsoView::reloadEso()
{
	EsoBookmark bm;
	bm = GetCurrentAsBookmark();
	SetCurrent(m_sCurEsoFile, bm);
	loadFile(m_sCurEsoFile);
	filterChanged();
}


void EsoView::copyDataToClipboard()
{
	qDebug("EsoView::copyDataToClipboard()");
	if (ui.treeWidget->currentItem())
	{
		m_clipboard->setText(m_varPlot->getDataAsText(m_bCopyOptionIncludeTime));
	}
}


void EsoView::copyPicToClipboard()
{
	qDebug("EsoView::copyPicToClipboard()");
	if (ui.treeWidget->currentItem())
	{
		m_clipboard->setPixmap(m_varPlot->getPixmap());
	}
}


void EsoView::copyFileInfoToClipboard()
{
	qDebug("EsoView::copyFileInfoToClipboard()");
	if (ui.treeWidget->currentItem())
	{
		m_clipboard->setText(
				"Filename\t" + m_sCurEsoFile + "\n" +
				"Program Version\t" + m_Parser->GetEPVersion() + "\n" +
				"Simulation time\t" + m_Parser->GetSimulationTime() + "\n"); 
	}
}


void EsoView::copyVarInfoToClipboard()
{
	qDebug("EsoView::copyVarInfoToClipboard()");
	QLocale locale;
	if (ui.treeWidget->currentItem())
	{
		m_clipboard->setText(
				QString("Variable Id\t") + QString("%1").arg(m_varPlot->getVariable()) + "\n" +
				"Variable Name\t" + m_varPlot->getTitle() + "\n" +
				"Total Start Time\t" + m_varPlot->getStart() + "\n" +
				"Total End Time\t" + m_varPlot->getEnd() + "\n" +
				"Total Maximum\t" + ConvertToString(m_varPlot->getMax()) + "\n" +
				"Total Minimum\t" + ConvertToString(m_varPlot->getMin()) + "\n" +
				"Total Average\t" + ConvertToString(m_varPlot->getAvg()) + "\n" +
				"Local Start Time\t" + m_varPlot->getStartLocal() + "\n" +
				"Local End Time\t" + m_varPlot->getEndLocal() + "\n" +
				"Local Maximum\t" + ConvertToString(m_varPlot->getMaxLocal()) + "\n" +
				"Local Minimum\t" + ConvertToString(m_varPlot->getMinLocal()) + "\n" +
				"Local Average\t" + ConvertToString(m_varPlot->getAvgLocal()) + "\n");
	}
}


bool EsoView::copyOptionIncludeTime()
{
	return m_bCopyOptionIncludeTime;
}


void EsoView::copyOptionIncludeTime(bool bIncludeTime)
{
	m_bCopyOptionIncludeTime = bIncludeTime;
}


void EsoView::setCurrentItemVisible()
{
   	qDebug() << "EsoView::setCurrentItemVisible()" ;
	QTreeWidgetItem * currentItem = ui.treeWidget->currentItem();
	ui.treeWidget->scrollToItem(currentItem);
    ui.treeWidget->setItemSelected(currentItem, true);
}


bool EsoView::savexEso(const QString& fileName)
{
	EsoBookmark curBm;
	curBm = m_varPlot->GetCurrentAsBookmark();
	
	QFile file(fileName);
    if (!file.open(QIODevice::WriteOnly))
    {
    	qDebug() << "EsoView::savexEso: Can't open file "<< fileName;
    	return false;
	}
    QDataStream out(&file);

    // Write a header with a "magic number" xEso and a version 0.3
    out << (quint32)0x7845736F; //xEso
    out << (qint32)3; 			//version 0.3
    out.setVersion(QDataStream::Qt_4_1);

    //eso filename
    out << m_sCurEsoFile;

    // Write the data
    //general - maker, grid, max/min line toggles,...
    out << viewMax();       //1
    out << viewMin();       //2
    out << viewMarkers();	//3
    out << viewFilter();	//4
    out << viewInfo();		//5
    out << viewVarInfo();	//6
    out << viewGrid();		//7
    out << viewVariableList();//8
    //first current - environment, time-scale, id, zoom - as bookmark
    out << curBm;           //9

	//all other bookmarks 
	out << (qint32)m_vBookmarks.size(); //10
	for (int i=0; i<m_vBookmarks.size(); ++i)
		out << m_vBookmarks[i];
	
    //include eso file ?
    file.close();
    return true;
}


bool EsoView::loadxEso(const QString& fileName)
{
    QFile file(fileName);
    if (!file.open(QIODevice::ReadOnly))
    {
    	qDebug() << "EsoView::loadEso: Can't open file "<< fileName;
    	return false;
	}
    QDataStream in(&file);

	quint32 iMagic;
    in >> iMagic;
    if (iMagic != 0x7845736F) //xEso
    {
    	qDebug() << "EsoView::loadEso: Bad magic number - not a xEso file: "<< fileName;
    	file.close();
        return false;
	}

    qint32 iVersion;
    in >> iVersion;
    if (iVersion != 3) //version 0.3
    {
    	qDebug() << "EsoView::loadEso: Bad xEso file version: "<< iVersion;
    	file.close();
        return false;
	}

    QString sTemp;
    bool bMax, bMin, bMarkers, bFilter, bVarInfo, bInfo, bGrid, bVariableList;

    //eso filename
    in >> m_sCurEsoFile;
    in >> bMax;    		//1
    in >> bMin;    		//2
    in >> bMarkers;		//3
    in >> bFilter; 		//4
    in >> bInfo;   		//5
    in >> bVarInfo;		//6
    in >> bGrid;   		//7
    in >> bVariableList;//8

	//first current - environment, time-scale, id, zoom - as bookmark
    EsoBookmark curBm;
    in >> curBm;        //9
	
	qDebug() << "EsoView::loadxEso() - current: sName" << curBm.GetName();
	qDebug() << "EsoView::loadxEso() - current: iEnv" << curBm.GetEnvironment();
	qDebug() << "EsoView::loadxEso() - current: iVar"  << curBm.GetVariable();
	qDebug() << "EsoView::loadxEso() - current: zoom l="  << curBm.GetZoomRect().left() << ", r=" << curBm.GetZoomRect().right()<< ", t=" << curBm.GetZoomRect().top()<< ", b=" << curBm.GetZoomRect().bottom();

	//number of bookmarks
	qint32 iNumBM=0;
	std::vector<EsoBookmark> vBm;
	in >> iNumBM;
	for (int i=0; i<iNumBM; ++i)
	{
		EsoBookmark  otherBM;
		in >> otherBM;
		vBm.push_back(otherBM);
	}
	
	file.close();
	
	bool bRet = loadFile(m_sCurEsoFile); //this will also read settings from config file
	if (!bRet)
	{
		qDebug() << "EsoView::loadxEso() - loading of eso file failed.";
		return bRet;
	}
	
	//now overwrite settings from config file with values from xeso file
	viewMarkers(bMarkers);
	viewFilter(bFilter);
	viewInfo(bInfo);
    viewVarInfo(bVarInfo);
    viewGrid(bGrid);
    viewMax(bMax);
    viewMin(bMin);
    viewVariableList(bVariableList);
	
	m_vBookmarks.clear();
	InitBookmarkCombo();
	
	for (unsigned i=0; i< vBm.size(); ++i)
		AddToBookmarks(vBm[i]);
	InitBookmarkCombo();
	if (curBm.GetTimeScale()>=0)
	{
		qDebug() << "EsoView::loadxEso() - set time scale to " << curBm.GetTimeScale();
		ui.comboBoxTimeAxis->setCurrentIndex((int)curBm.GetTimeScale() );
	}
	
	if (curBm.GetEnvironment()>=0 && curBm.GetVariable()>=0)
	{
		//m_varPlot->Plot(); //force replot
		gotoBookmark(curBm);
	}	
	else
		ui.treeWidget->setCurrentItem(ui.treeWidget->topLevelItem(0));

    return bRet;
}


void EsoView::InitBookmarkCombo()
{
	qDebug() << "EsoView::InitBookmarkCombo - start";
	m_mainWindow->getBookmarkCombo()->blockSignals(true);
	m_mainWindow->getBookmarkCombo()->clear();
	for (int i=0; i<m_vBookmarks.size();++i )
	{
		m_mainWindow->getBookmarkCombo()->addItem( QString("%1").arg(m_vBookmarks[i].GetName()) );
	}
	if ( m_iCurrentBookmark>=0 && m_iCurrentBookmark<m_vBookmarks.size() )
	{
		int iPos = m_mainWindow->getBookmarkCombo()->findText(m_vBookmarks[m_iCurrentBookmark].GetName());
		m_mainWindow->getBookmarkCombo()->setCurrentIndex(iPos);
	}
	m_mainWindow->getBookmarkCombo()->blockSignals(false);
	qDebug() << "EsoView::InitBookmarkCombo - end";
}


void EsoView::AddToBookmarks(EsoBookmark & bm)
{
	qDebug() << "EsoView::AddToBookmarks() - sName" << bm.GetName();
	qDebug() << "EsoView::AddToBookmarks() - iEnv" << bm.GetEnvironment();
	qDebug() << "EsoView::AddToBookmarks() - iVar"  << bm.GetVariable();
	qDebug() << "EsoView::AddToBookmarks() - zoom l="  << bm.GetZoomRect().left() << ", r=" << bm.GetZoomRect().right()<< ", t=" << bm.GetZoomRect().top()<< ", b=" << bm.GetZoomRect().bottom();
	
	m_vBookmarks.append(bm);
	m_mainWindow->getBookmarkCombo()->addItem(QString("%1").arg(bm.GetName()));

	QTreeWidgetItem* item = getItem(bm.GetVariable());
	if (item != NULL)
	{
		item->setIcon(iMarkerColumn,QIcon(":/images/bookmark.png"));
		QStringList sList;
		if (!item->text(iMarkerColumn).isEmpty())
			sList = item->text(iMarkerColumn).trimmed().split(", ");
		sList << bm.GetName();
		item->setText(iMarkerColumn, sList.join(", "));
	}
	if (!m_vBookmarks.empty())
	{
		ui.treeWidget->setColumnHidden(iMarkerColumn, false);
		ui.treeWidget->resizeColumnToContents(iMarkerColumn);
	}
}

EsoBookmark EsoView::AddCurrentToBookmarks()
{
	qDebug() << "EsoView::AddCurrentToBookmarks()";
    EsoBookmark bm = GetCurrentAsBookmark();
	m_iCurrentBookmark = GetNextAvailableBookmark();
	QString sName;
	sName.setNum(m_iCurrentBookmark);
	bm.SetName(sName);
	qDebug() << "EsoView::AddCurrentToBookmarks() - iCurr" << m_iCurrentBookmark;
	AddToBookmarks(bm);
	return bm;
}

int EsoView::GetNextAvailableBookmark()
{
	int iMax=0;
	int iTemp=0;
	for (int i=0; i<m_vBookmarks.size(); ++i)
	{
		iTemp = m_vBookmarks[i].GetName().toInt();
		if (iTemp>iMax)
			iMax = iTemp;
	}
	if (!m_vBookmarks.empty())
		++iMax;
	return iMax;
}

EsoBookmark EsoView::deleteBookmark()
{
	qDebug() << "EsoView::deleteBookmark() - start";
	EsoBookmark bm;
	
	if (m_vBookmarks.isEmpty())
	    return bm;
	
	QString sName = m_mainWindow->getBookmarkCombo()->currentText();
	qDebug() << "EsoView::deleteBookmark() - current name:" << sName;
	if (sName.isEmpty())
		return bm;
	
	int iCurBM=-1;
	for (int i=0; i<m_vBookmarks.size();++i)
	{
		if (m_vBookmarks[i].GetName() == sName)
		{
			iCurBM=i;
			break;
		}
	}
	
	if (iCurBM>=0 && iCurBM<m_vBookmarks.size())
	{
		bm = m_vBookmarks[iCurBM];
		sName=m_vBookmarks.at(iCurBM).GetName();
        m_vBookmarks.removeAt(iCurBM);
		m_iCurrentBookmark=-1;

		QTreeWidgetItem* item = getItem(bm.GetVariable());
		if (item != NULL)
		{
	   		QString sBM = item->text(iMarkerColumn);
	   		QStringList sBML = sBM.split(", ");
 	   		for (int i=0; i<sBML.size();++i)
 	  		    qDebug() << "EsoView::deleteBookmark - bm list["<<i<<"]=" << sBML[i];
	   		int iToDel = sBML.indexOf(sName);
	   		sBML.removeAt(iToDel);
	   		if (sBML.isEmpty())
	   		{
				item->setIcon(iMarkerColumn, QIcon());
				item->setText(iMarkerColumn, "");
			}
			else
				item->setText(iMarkerColumn, sBML.join(", "));
		}
		int iPos = m_mainWindow->getBookmarkCombo()->findText(sName);
		qDebug() << "EsoView::deleteBookmark() - Index in combo: " << iPos;
		if (iPos>=0)
		{
			m_mainWindow->getBookmarkCombo()->blockSignals(true);
			m_mainWindow->getBookmarkCombo()->removeItem(iPos);
			m_mainWindow->getBookmarkCombo()->blockSignals(false);
		}

	}
	else
	{
	   	qWarning() << "EsoView::deleteBookmark() - did not find current bm!";
		return bm;
	}
	ui.treeWidget->resizeColumnToContents(iMarkerColumn);
	if (m_vBookmarks.empty()) 
		ui.treeWidget->setColumnHidden(iMarkerColumn, true);
   	qDebug() << "EsoView::DeleteBookmark() - end";
	return bm;
}


QString EsoView::nextBookmark()
{
   	if (m_vBookmarks.isEmpty())
	    return "";
	++m_iCurrentBookmark;
	if (m_iCurrentBookmark<0 || m_iCurrentBookmark>=m_vBookmarks.size())
		m_iCurrentBookmark=0;
   	qDebug() << "EsoView::nextBookmark() - current:" << m_iCurrentBookmark;
	return gotoBookmark(m_vBookmarks.at(m_iCurrentBookmark));
}


QString EsoView::prevBookmark()
{
	if (m_vBookmarks.isEmpty())
	    return ""; 
	--m_iCurrentBookmark;
	if (m_iCurrentBookmark<0 || m_iCurrentBookmark>=m_vBookmarks.size())
		m_iCurrentBookmark=m_vBookmarks.size()-1;
   	qDebug() << "EsoView::prevBookmark() - current:" << m_iCurrentBookmark;
	return gotoBookmark(m_vBookmarks.at(m_iCurrentBookmark));
}


void EsoView::gotoBookmark(QString sBM)
{
	for (int i=0; i<m_vBookmarks.size(); ++i)
	{
		if (m_vBookmarks[i].GetName() == sBM)
		{
			gotoBookmark(m_vBookmarks.at(i));
			return;
		}
	}
	
}


EsoBookmark EsoView::GetCurrentAsBookmark() const
{
	return m_varPlot->GetCurrentAsBookmark();
}


QList<EsoBookmark> EsoView::GetBookmarks() const
{
	return m_vBookmarks;
}


int EsoView::GetNumberOfBookmarks() const
{
	return m_vBookmarks.size();
}
	
	
QString EsoView::gotoBookmark(EsoBookmark bm)
{
   	qDebug() << "EsoView::gotoBookmark() - current: sName" << bm.GetName();
   	qDebug() << "EsoView::gotoBookmark() - current: iEnv" << bm.GetEnvironment();
   	qDebug() << "EsoView::gotoBookmark() - current: iVar"  << bm.GetVariable();
	qDebug() << "EsoView::gotoBookmark() - current: zoom l="  << bm.GetZoomRect().left() << ", r=" << bm.GetZoomRect().right()<< ", t=" << bm.GetZoomRect().top()<< ", b=" << bm.GetZoomRect().bottom();
	//set environment
	ui.comboBoxEnvironment->setCurrentIndex( bm.GetEnvironment() );
	setCurrentEnvironment( bm.GetEnvironment() );
	//set time scale drop down
	ui.comboBoxTimeAxis->setCurrentIndex((int)bm.GetTimeScale() );

	m_varPlot->SetCurrent(bm);
	QTreeWidgetItem * currentItem = getItem(m_varPlot->getVariable());
	ui.treeWidget->setCurrentItem(currentItem);
	setCurrentItemVisible();	
	return bm.GetName();
}
