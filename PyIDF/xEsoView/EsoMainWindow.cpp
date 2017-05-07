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

// $Id: EsoMainWindow.cpp,v 1.21 2008/03/01 20:45:46 cschiefer Exp $

#include <QtGui>
#include <QLocale>
#include <QComboBox>


#include "EsoMainWindow.h"
#include "EsoView.h"
#include "EsoOptions.h"
#include "EsoUtil.h"
#include "EsoBookmark.h"


EsoMainWindow::EsoMainWindow()
{
	qDebug("EsoMainWindow::EsoMainWindow() - start");

	setAcceptDrops(true);
	workspace = new QWorkspace;
	setCentralWidget(workspace);
	connect(workspace, SIGNAL(windowActivated(QWidget *)), this, SLOT(updateMenus()));
	windowMapper = new QSignalMapper(this);
	connect(windowMapper, SIGNAL(mapped(QWidget *)), workspace, SLOT(setActiveWindow(QWidget *)));

	createActions();
	createToolBars();
	createMenus();
	createStatusBar();
	updateMenus();
	readSettings(true);
	updateRecentFileActions();

	setWindowTitle(tr(ESO_APP));
	//restore toolbars
	QSettings settings(ESO_ORG, ESO_APP);
	QByteArray state = settings.value("winState", "").toByteArray();
	restoreState(state);
		
	showReadyMessage();
	qDebug("EsoMainWindow::EsoMainWindow() - end");
}


void EsoMainWindow::closeEvent(QCloseEvent* event)
{
	qDebug("EsoMainWindow::closeEvent(QCloseEvent *event) - start");
	workspace->closeAllWindows();
	if (activeEsoView())
	{
		event->ignore();
	} else
	{
		writeSettings();
		event->accept();
	}
	qDebug("EsoMainWindow::closeEvent(QCloseEvent *event) - end");
}

void EsoMainWindow::open()
{
	qDebug("EsoMainWindow::open() - start");
	QString fileName = QFileDialog::getOpenFileName(this, tr("Select a ESO file"), m_sLastOpenDir,
		"Eso files (*.eso *.xEso)");
	if (!fileName.isEmpty())
	{
		EsoView* existing = findEsoView(fileName);
		if (existing)
		{
			workspace->setActiveWindow(existing);
			//TODO: ask for reloading
			return;
		}
		loadEso(fileName);
	}
	showReadyMessage();
	qDebug("EsoMainWindow::open() - end");
}


void EsoMainWindow::savexEso()
{
	qDebug("EsoMainWindow::savexEso() - start");
	
	QFileInfo defName;
	defName.setFile(activeEsoView()->currentFile());
	QString sDef = defName.dir().path() + "/" + defName.baseName()+".xeso";
	QString fileName = QFileDialog::getSaveFileName(this, tr("Save xEso file"), sDef, "xEso files (*.xeso)");
	if (fileName.isEmpty())
	{
		return;
		qDebug("EsoMainWindow::savexEso() - file name is empty");
	}
	activeEsoView()->savexEso(fileName);
	showReadyMessage();
	qDebug("EsoMainWindow::savexEso() - end");
	return;
}



void EsoMainWindow::loadEso(const QString& sFilename)
{
	qDebug() << "EsoMainWindow::loadEso(" << sFilename << ") - start";
	readSettings(false);
	EsoView* child = createEsoView();
	QFileInfo file(sFilename);
	m_sLastOpenDir = file.absoluteDir().absolutePath();
	bool bxEso=false;

	EvFileType ft = IsxEsoFile(sFilename);
	if (ft == EvFileType_xEso)
	{
		if (child->loadxEso(sFilename))
		{
			statusBar()->showMessage(tr("File loaded"), 2000);
			updateRecentEsoFiles(child->currentFile());
			child->showMaximized();
			bxEso = true;
		}
	}
	else if (ft == EvFileType_Eso)
	{
		if (child->loadFile(sFilename))
		{
			//TODO: check if according xeso is available -> ask user for loading 
			statusBar()->showMessage(tr("File loaded"), 2000);
			updateRecentEsoFiles(child->currentFile());
			child->showMaximized();
		}
	}
	else if (ft == EvFileType_NotFound)
	{
		
		QMessageBox::warning(this, ESO_APP, QString("Can't open file '%1'").arg(sFilename), QMessageBox::Ok, QMessageBox::NoButton);
		child->close();
	}
	else //ft invalid
	{
		QMessageBox::warning(this, ESO_APP, QString("Can't load file '%1' - This is not an valid eso or xEso file.").arg(sFilename), QMessageBox::Ok, QMessageBox::NoButton);
		child->close();
	}
	
	updateMenus();
	showReadyMessage();
	qDebug("EsoMainWindow::loadEso(const QString & sFilename) - end");
}


void EsoMainWindow::updateRecentEsoFiles(const QString& fileName)
{
	qDebug("EsoMainWindow::updateRecentEsoFiles( const QString& fileName ) - start");
	int iCurPos=-1;
	for (int i=0; i<m_vRecentFiles.size(); ++i)
	{
		if ( m_vRecentFiles.at(i) == fileName )
		{
			iCurPos=i;
			break;
		}
	}
	if (iCurPos>=0) //file already in list - move to front
	{
		m_vRecentFiles.remove(iCurPos);
		m_vRecentFiles.prepend(fileName);
	}
	else //add to front
	{
		m_vRecentFiles.prepend(fileName);
	}

	while (m_vRecentFiles.size() > MAX_RECENTFILES)
		m_vRecentFiles.remove(MAX_RECENTFILES-1);

	SetRecentfiles( m_vRecentFiles );
	
	foreach(QWidget * widget, QApplication::topLevelWidgets())
	{
		EsoMainWindow* mainWin = qobject_cast< EsoMainWindow*>(widget);
		if (mainWin)
			mainWin->updateRecentFileActions();
	}
	qDebug("EsoMainWindow::updateRecentEsoFiles( const QString& fileName ) - end");
}



void EsoMainWindow::openRecentEsoFile()
{
	qDebug("EsoMainWindow::openRecentEsoFile() - start");
	QAction* action = qobject_cast< QAction*>(sender());
	if (action)
	{
		loadEso(action->data().toString());
	}
	showReadyMessage();
	qDebug("EsoMainWindow::openRecentEsoFile() - end");
}

void EsoMainWindow::about()
{
	qDebug("EsoMainWindow::about() - start");
	 QMessageBox::about( this, "About xEsoView",
					tr("<p><H1 ALIGN=\"center\">xEsoView 0.3.2</H1>"
					"<P>is a file viewer for <A HREF=\"http://www.eere.energy.gov/buildings/energyplus/\">EnergyPlus</A> eso output files.<BR>"
					"Homepage: <A HREF \"http://xesoview.sourceforge.net\">http://xesoview.sourceforge.net</P>"
					"<P>Copyright Dr. Christian Schiefer<BR>"
					"Vienna - Austria<BR>"
					"Apr. 2008</P>"
					"<P>Feedback is welcome and can be sent to <A HREF=\"mailto:cschiefer@users.sourceforge.net?subject=xEsoview\">"
					"cschiefer@users.sourceforge.net</A>.</P>"
					"<P>xEsoView is based on the work of "
					"<A HREF=\"http://qwt.sf.net\">Qwt</A> and <A HREF=\"http://www.trolltech.com\">Qt</A>.</P>"
					));
	qDebug("EsoMainWindow::about() - end");
}

void EsoMainWindow::options()
{
	qDebug("EsoMainWindow::options() - start");
	EsoOptions dialog(this);
	if (dialog.exec() == QDialog::Accepted)
	{
		QSettings settings(ESO_ORG, ESO_APP);
		settings.setValue("DateTimeFormatForCopy", dialog.uiOptions.lineEditDateFormat->text());
		if (dialog.uiOptions.lineEditDecimalPoint->text() == "," || dialog.uiOptions.lineEditDecimalPoint->text() == ".")
			settings.setValue("DecimalPointForCopy", dialog.uiOptions.lineEditDecimalPoint->text());
		settings.setValue("ColumnSepForCopy", dialog.uiOptions.lineEditColumnSep->text());
		settings.setValue("GraphBackgroundColor", dialog.uiOptions.frame_BackgroundColor->palette().color(QPalette::Background));
		settings.setValue("GraphLineColor", dialog.uiOptions.lineColor->palette().color(QPalette::Foreground));
		settings.setValue("GraphLineColorMaxMin", dialog.uiOptions.lineColorMaxMin->palette().color(QPalette::Foreground));
		settings.setValue("GraphColorMarker", dialog.uiOptions.lineColorMarker->palette().color(QPalette::Foreground));
		settings.setValue("ApplicationStyle", dialog.uiOptions.comboBoxAppStyle->currentIndex());
		settings.setValue("GraphMarkerStyle", dialog.uiOptions.comboBoxMarkerStyle->currentIndex());
	}
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->Redraw();
}


void EsoMainWindow::updateMenus()
{
	qDebug("EsoMainWindow::updateMenus() - start");
	bool hasEsoView = (activeEsoView() != 0);
	savexEsoAct->setEnabled(hasEsoView);
	closeAct->setEnabled(hasEsoView);
	closeAllAct->setEnabled(hasEsoView);
	tileAct->setEnabled(hasEsoView);
	cascadeAct->setEnabled(hasEsoView);
	nextAct->setEnabled(hasEsoView);
	previousAct->setEnabled(hasEsoView);
	separatorAct->setVisible(hasEsoView);
	viewMaxAct->setEnabled(hasEsoView);
	viewMinAct->setEnabled(hasEsoView);
	viewMarkersAct->setEnabled(hasEsoView);
	viewFilterAct->setEnabled(hasEsoView);
	viewInfoAct->setEnabled(hasEsoView);
	viewVarInfoAct->setEnabled(hasEsoView);
	viewGridAct->setEnabled(hasEsoView);
	viewVariableListAct->setEnabled(hasEsoView);
	reloadAct->setEnabled(hasEsoView);
	copyDataToClipboardAct->setEnabled(hasEsoView);
	copyOptionIncludeTimeAct->setEnabled(hasEsoView);
	copyPicToClipboardAct->setEnabled(hasEsoView);
	copyFileInfoAct->setEnabled(hasEsoView);
	copyVarInfoAct->setEnabled(hasEsoView);
	printAct->setEnabled(hasEsoView);
	printPDFAct->setEnabled(hasEsoView);
	addBookmarkAct->setEnabled(hasEsoView);
	if (hasEsoView)
	{
		deleteBookmarkAct->setEnabled( activeEsoView()->GetNumberOfBookmarks()>0);
		nextBookmarkAct->setEnabled(activeEsoView()->GetNumberOfBookmarks()>0);
		prevBookmarkAct->setEnabled(activeEsoView()->GetNumberOfBookmarks()>0);
		gotoBookmarkAct->setEnabled(activeEsoView()->GetNumberOfBookmarks()>0);
		m_BMcombo->setEnabled(activeEsoView()->GetNumberOfBookmarks()>0);
		
		activeEsoView()->InitBookmarkCombo();//clear Bookmark combo and initialize
		viewMaxAct->setChecked(activeEsoView()->viewMax());
		viewMinAct->setChecked(activeEsoView()->viewMin());
		viewMarkersAct->setChecked(activeEsoView()->viewMarkers());
		viewGridAct->setChecked(activeEsoView()->viewGrid());
		viewFilterAct->setChecked(activeEsoView()->viewFilter());
		viewVariableListAct->setChecked(activeEsoView()->viewVariableList());
		viewInfoAct->setChecked(activeEsoView()->viewInfo());
		viewVarInfoAct->setChecked(activeEsoView()->viewVarInfo());
		copyOptionIncludeTimeAct->setChecked(activeEsoView()->copyOptionIncludeTime());
	}
	else
	{
		deleteBookmarkAct->setEnabled(false);
		nextBookmarkAct->setEnabled(false);
		prevBookmarkAct->setEnabled(false);
		gotoBookmarkAct->setEnabled(false);
		m_BMcombo->setEnabled(false);
	}
	qDebug("EsoMainWindow::updateMenus() - end");
}

void EsoMainWindow::updateWindowMenu()
{
	qDebug("EsoMainWindow::updateWindowMenu() - start");
	windowMenu->clear();
	windowMenu->addAction(savexEsoAct);
	windowMenu->addAction(closeAct);
	windowMenu->addAction(closeAllAct);
	windowMenu->addSeparator();
	windowMenu->addAction(tileAct);
	windowMenu->addAction(cascadeAct);
	windowMenu->addSeparator();
	windowMenu->addAction(nextAct);
	windowMenu->addAction(previousAct);
	windowMenu->addAction(separatorAct);

	QList< QWidget*> windows = workspace->windowList();
	separatorAct->setVisible(!windows.isEmpty());

	for (int i = 0; i < windows.size(); ++i)
	{
		EsoView* child = qobject_cast< EsoView*>(windows.at(i));
		QString text;
		if (i < 9)
		{
			text = tr("&%1. %2").arg(i + 1).arg(child->userFriendlyCurrentFile());
		} else
		{
		  	text = tr("%1. %2").arg(i + 1).arg(child->userFriendlyCurrentFile());
		}
		QAction* action = windowMenu->addAction(text);
		action->setCheckable(true);
		action ->setChecked(child == activeEsoView());
		connect(action, SIGNAL(triggered()), windowMapper, SLOT(map()));
		windowMapper->setMapping(action, child);
	}
	qDebug("EsoMainWindow::updateWindowMenu() - end");
}


EsoView* EsoMainWindow::createEsoView()
{
	qDebug("EsoMainWindow::createEsoView() - start");
	EsoView* child = new EsoView(workspace);
	workspace->addWindow(child);
	child->setWorkspace(workspace);
	child->setMainWindow(this);
	connect(child, SIGNAL(setMessage(const QString &)), this, SLOT(showMessage(const QString &)));
	qDebug("EsoMainWindow::createEsoView() - end");
	return child;
}


void EsoMainWindow::createActions()
{
	qDebug("EsoMainWindow::createActions() - start");
	openAct = new QAction(QIcon(":/images/open.png"), tr("&Open..."), this);
	openAct->setShortcut(Qt::CTRL + Qt::Key_O);
	openAct->setStatusTip(tr("Open an existing file"));
	connect(openAct, SIGNAL(triggered()), this, SLOT(open()));

	savexEsoAct = new QAction(QIcon(":/images/save.png"), tr("&Save xEso..."), this);
	savexEsoAct->setShortcut(Qt::CTRL + Qt::Key_S);
	savexEsoAct->setStatusTip(tr("Save xEso file (Bookmarks, current view, ...)"));
	connect(savexEsoAct, SIGNAL(triggered()), this, SLOT(savexEso()));

	reloadAct = new QAction(QIcon(":/images/reload.png"), tr("&Reload file"), this);
	reloadAct->setShortcut(Qt::CTRL + Qt::Key_R);
	reloadAct->setStatusTip(tr("Reload eso file"));
	connect(reloadAct, SIGNAL(triggered()), this, SLOT(reloadEso()));

	printAct = new QAction(QIcon(":/images/print.png"), tr("&Print graphic"), this);
	printAct->setShortcut(Qt::CTRL + Qt::Key_P);
	printAct->setStatusTip(tr("Print graphic"));
	connect(printAct, SIGNAL(triggered()), this, SLOT(print()));

	printPDFAct = new QAction(QIcon(":/images/exportpdf.png"), tr("&Export graphic in PDF format"), this);
	printPDFAct->setShortcut(Qt::CTRL + Qt::Key_D);
	printPDFAct->setStatusTip(tr("Export graphic"));
	connect(printPDFAct, SIGNAL(triggered()), this, SLOT(printPDF()));

	optionsAct = new QAction(tr("Preferences"), this);
	optionsAct->setStatusTip(tr("Edit application preferences"));
	connect(optionsAct, SIGNAL(triggered()), this, SLOT(options()));

	exitAct = new QAction(tr("E&xit"), this);
	exitAct->setShortcut(Qt::CTRL + Qt::Key_Q);
	exitAct->setStatusTip(tr("Exit the application"));
	connect(exitAct, SIGNAL(triggered()), qApp, SLOT(closeAllWindows()));

	closeAct = new QAction(tr("Cl&ose"), this);
	closeAct->setShortcut(Qt::CTRL + Qt::Key_F4);
	closeAct->setStatusTip(tr("Close the active window"));
	connect(closeAct, SIGNAL(triggered()), workspace, SLOT(closeActiveWindow()));

	closeAllAct = new QAction(tr("Close &All"), this);
	closeAllAct->setStatusTip(tr("Close all the windows"));
	connect(closeAllAct, SIGNAL(triggered()), workspace, SLOT(closeAllWindows()));

	QIcon icoViewMax(":/images/viewMax.png");
	icoViewMax.addFile(":/images/viewMax_on.png", QSize(32, 32), QIcon::Normal, QIcon::On);
	viewMaxAct = new QAction(icoViewMax, tr("View maximum"), this);
	viewMaxAct->setStatusTip(tr("Show line at maximum"));
	viewMaxAct->setCheckable(true);
	connect(viewMaxAct, SIGNAL(triggered()), this, SLOT(viewMax()));

	QIcon icoViewMin(":/images/viewMin.png");
	icoViewMin.addFile(":/images/viewMin_on.png", QSize(32, 32), QIcon::Normal, QIcon::On);
	viewMinAct = new QAction(icoViewMin, tr("View minimum"), this);
	viewMinAct->setStatusTip(tr("Show line at mimimum"));
	viewMinAct->setCheckable(true);
	connect(viewMinAct, SIGNAL(triggered()), this, SLOT(viewMin()));

	QIcon icoViewMarkers(":/images/viewMarkers.png");
	icoViewMarkers.addFile(":/images/viewMarkers_on.png", QSize(32, 32), QIcon::Normal, QIcon::On);
	viewMarkersAct = new QAction(icoViewMarkers, tr("View markers"), this); ;
	viewMarkersAct->setStatusTip(tr("Show markers at each value"));
	viewMarkersAct->setCheckable(true);
	connect(viewMarkersAct, SIGNAL(triggered()), this, SLOT(viewMarkers()));

	QIcon icoViewFilter(":/images/filter.png");
	icoViewFilter.addFile(":/images/filter_on.png", QSize(32, 32), QIcon::Normal, QIcon::On);
	viewFilterAct = new QAction(icoViewFilter, tr("View filter"), this);
	viewFilterAct->setStatusTip(tr("View variable filter"));
	viewFilterAct->setCheckable(true);
	connect(viewFilterAct, SIGNAL(triggered()), this, SLOT(viewFilter()));

	QIcon icoViewInfo(":/images/info.png");
	icoViewInfo.addFile(":/images/info_on.png", QSize(32, 32), QIcon::Normal, QIcon::On);
	viewInfoAct = new QAction(icoViewInfo, tr("View file information"), this); ;
	viewInfoAct->setStatusTip(tr("View file information"));
	viewInfoAct->setCheckable(true);
	connect(viewInfoAct, SIGNAL(triggered()), this, SLOT(viewInfo()));

	QIcon icoViewVarInfo(":/images/varinfo.png");
	icoViewVarInfo.addFile(":/images/varinfo_on.png", QSize(32, 32), QIcon::Normal, QIcon::On);
	viewVarInfoAct = new QAction(icoViewVarInfo, tr("View variable information"), this); ;
	viewVarInfoAct->setStatusTip(tr("View variable information"));
	viewVarInfoAct->setCheckable(true);
	connect(viewVarInfoAct, SIGNAL(triggered()), this, SLOT(viewVarInfo()));

	QIcon icoViewGrid(":/images/viewGrid.png");
	icoViewGrid.addFile(":/images/viewGrid_on.png", QSize(32, 32), QIcon::Normal, QIcon::On);
	viewGridAct = new QAction(icoViewGrid, tr("View grid"), this); ;
	viewGridAct->setStatusTip(tr("View grid"));
	viewGridAct->setCheckable(true);
	connect(viewGridAct, SIGNAL(triggered()), this, SLOT(viewGrid()));

	QIcon icoViewVariableList(":/images/viewVariableList.png");
	icoViewVariableList.addFile(":/images/viewVariableList_on.png", QSize(32, 32), QIcon::Normal, QIcon::On);
	viewVariableListAct = new QAction(icoViewVariableList, tr("View variable list"), this); ;
	viewVariableListAct->setStatusTip(tr("View variable list"));
	viewVariableListAct->setCheckable(true);
	connect(viewVariableListAct, SIGNAL(triggered()), this, SLOT(viewVariableList()));

	copyDataToClipboardAct = new QAction(QIcon(":/images/copy.png"), tr("Copy variable data"), this);
	copyDataToClipboardAct->setStatusTip(tr("Copy current selected variable data to clipboard"));
	connect(copyDataToClipboardAct, SIGNAL(triggered()), this, SLOT(copyDataToClipboard()));
	copyDataToClipboardAct->setShortcut(tr("Ctrl+C"));

	copyPicToClipboardAct = new QAction(QIcon(":/images/copyGraph.png"), tr("Copy graphic"), this);
	copyPicToClipboardAct->setStatusTip(tr("Copy current graphic to clipboard"));
	connect(copyPicToClipboardAct, SIGNAL(triggered()), this, SLOT(copyPicToClipboard()));
	copyPicToClipboardAct->setShortcut(tr("Ctrl+Shift+C"));

	copyOptionIncludeTimeAct = new QAction("Copy include time data", this);
	copyOptionIncludeTimeAct->setStatusTip(tr("Copy of variable data will include time data"));
	connect(copyOptionIncludeTimeAct, SIGNAL(triggered()), this, SLOT(copyOptionIncludeTime()));
	copyOptionIncludeTimeAct->setCheckable(true);

	copyFileInfoAct = new QAction(QIcon(":/images/copy.png"), tr("Copy file information"), this);
	copyFileInfoAct->setStatusTip(tr("Copy current file information to clipboard"));
	connect(copyFileInfoAct, SIGNAL(triggered()), this, SLOT(copyFileInfoToClipboard()));
	
	copyVarInfoAct = new QAction(QIcon(":/images/copy.png"), tr("Copy variable information"), this);
	copyVarInfoAct->setStatusTip(tr("Copy current variable information to clipboard"));
	connect(copyVarInfoAct, SIGNAL(triggered()), this, SLOT(copyVarInfoToClipboard()));
	

	tileAct = new QAction(tr("&Tile"), this);
	tileAct->setStatusTip(tr("Tile the windows"));
	connect(tileAct, SIGNAL(triggered()), workspace, SLOT(tile()));

	cascadeAct = new QAction(tr("&Cascade"), this);
	cascadeAct->setStatusTip(tr("Cascade the windows"));
	connect(cascadeAct, SIGNAL(triggered()), workspace, SLOT(cascade()));

	nextAct = new QAction(tr("Ne&xt"), this);
	nextAct->setShortcut(tr("Ctrl+F6"));
	nextAct->setStatusTip(tr("Move the focus to the next window"));
	connect(nextAct, SIGNAL(triggered()), workspace, SLOT(activateNextWindow()));

	previousAct = new QAction(tr("Pre&vious"), this);
	previousAct->setShortcut(tr("Ctrl+Shift+F6"));
	previousAct->setStatusTip(tr("Move the focus to the previous window"));
	connect(previousAct, SIGNAL(triggered()), workspace, SLOT(activatePreviousWindow()));


	addBookmarkAct = new QAction(QIcon(":/images/addBookmark.png"), tr("&Add bookmark"), this);
	addBookmarkAct->setStatusTip(tr("Add current graphic as bookmark"));
	connect(addBookmarkAct, SIGNAL(triggered()), this, SLOT(addCurrentToBookmarks()));

	deleteBookmarkAct = new QAction(QIcon(":/images/deleteBookmark.png"), tr("&Delete bookmark"), this);
	deleteBookmarkAct->setStatusTip(tr("Delete current bookmark"));
	connect(deleteBookmarkAct, SIGNAL(triggered()), this, SLOT(deleteBookmark()));

	nextBookmarkAct = new QAction(QIcon(":/images/nextBookmark.png"), tr("&Next bookmark"), this);
	nextBookmarkAct->setStatusTip(tr("Go to next bookmark"));
	connect(nextBookmarkAct, SIGNAL(triggered()), this, SLOT(nextBookmark()));

	m_BMcombo = new QComboBox();
	gotoBookmarkAct = new QAction(m_BMcombo);
	m_BMcombo->setToolTip(tr("Jump to bookmark"));
	m_BMcombo->setStatusTip(tr("Jump to bookmark"));
	connect(m_BMcombo, SIGNAL(currentIndexChanged(const QString &)), this, SLOT(gotoBookmark(const QString &)));

	prevBookmarkAct = new QAction(QIcon(":/images/previousBookmark.png"), tr("&Previous bookmark"), this);
	prevBookmarkAct->setStatusTip(tr("Go to previous bookmark"));
	connect(prevBookmarkAct, SIGNAL(triggered()), this, SLOT(prevBookmark()));


	for (int i = 0; i < MAX_RECENTFILES; ++i)
	{
		recentFileActs[i] = new QAction(this);
		recentFileActs[i]->setVisible(false);
		connect(recentFileActs[i], SIGNAL(triggered()), this, SLOT(openRecentEsoFile()));
	}

	separatorAct = new QAction(this);
	separatorAct->setSeparator(true);

	aboutAct = new QAction(tr("&About"), this);
	aboutAct->setStatusTip(tr("Show the application's About box"));
	connect(aboutAct, SIGNAL(triggered()), this, SLOT(about()));
	
	qDebug("EsoMainWindow::createActions() - end");
}


void EsoMainWindow::updateRecentFileActions()
{
	qDebug("EsoMainWindow::updateRecentFileActions() - start");
	int numRecentFiles = qMin(m_vRecentFiles.size(), (int) MAX_RECENTFILES);

	for (int i = 0; i < numRecentFiles; ++i)
	{
		QString text = tr("&%1 %2").arg(i + 1).arg(m_vRecentFiles[i]);
		recentFileActs[i]->setText(text);
		recentFileActs[i]->setData(m_vRecentFiles[i]);
		recentFileActs[i]->setVisible(true);
	}
	for (int j = numRecentFiles; j < MAX_RECENTFILES; ++j)
		recentFileActs[j]->setVisible(false);
	qDebug("EsoMainWindow::updateRecentFileActions() - end");
}


void EsoMainWindow::createMenus()
{
	qDebug("EsoMainWindow::createMenus() - start");
	fileMenu = menuBar()->addMenu(tr("&File"));
	fileMenu->addAction(openAct);
	recentMenu = fileMenu->addMenu(tr("&Recently opened files"));
	for (int i = 0; i < MAX_RECENTFILES; ++i)
		recentMenu->addAction(recentFileActs[i]);
	fileMenu->addAction(savexEsoAct);
	fileMenu->addAction(reloadAct);
	fileMenu->addAction(printAct);
	fileMenu->addAction(printPDFAct);
	fileMenu->addAction(optionsAct);
	fileMenu->addSeparator();
	fileMenu->addAction(exitAct);

	viewMenu = menuBar()->addMenu(tr("&View"));
	viewMenu->addAction(viewMaxAct);
	viewMenu->addAction(viewMinAct);
	viewMenu->addAction(viewMarkersAct);
	viewMenu->addAction(viewGridAct);
	viewMenu->addSeparator();
	viewMenu->addAction(viewFilterAct);
	viewMenu->addAction(viewInfoAct);
	viewMenu->addAction(viewVarInfoAct);
	viewMenu->addAction(viewVariableListAct);
	viewMenu->addSeparator();
	
	viewsMenu = viewMenu->addMenu(tr("&Toolbars"));
	viewToolBar->toggleViewAction()->setStatusTip(tr("Toggle toolbar 'View'"));
	viewsMenu->addAction(viewToolBar->toggleViewAction());
	fileToolBar->toggleViewAction()->setStatusTip(tr("Toggle toolbar 'File'"));
	viewsMenu->addAction(fileToolBar->toggleViewAction());
	bookmarkToolBar->toggleViewAction()->setStatusTip(tr("Toggle toolbar 'Bookmark'"));
	viewsMenu->addAction(bookmarkToolBar->toggleViewAction());
	
	copyMenu = menuBar()->addMenu(tr("&Copy"));
	copyMenu->addAction(copyPicToClipboardAct);
	copyMenu->addSeparator();
	copyMenu->addAction(copyDataToClipboardAct);
	copyMenu->addAction(copyOptionIncludeTimeAct);
	copyMenu->addSeparator();
	copyMenu->addAction(copyFileInfoAct);
	copyMenu->addAction(copyVarInfoAct);

	bookMarkMenu =menuBar()->addMenu(tr("&Bookmark"));
	bookMarkMenu->addAction(addBookmarkAct);
	bookMarkMenu->addAction(deleteBookmarkAct);
	bookMarkMenu->addAction(prevBookmarkAct);
	bookMarkMenu->addAction(nextBookmarkAct);

	windowMenu = menuBar()->addMenu(tr("&Window"));
	connect(windowMenu, SIGNAL(aboutToShow()), this, SLOT(updateWindowMenu()));

	menuBar()->addSeparator();

	helpMenu = menuBar()->addMenu(tr("&Help"));
	helpMenu->addAction(aboutAct);
	qDebug("EsoMainWindow::createMenus() - end");
}


void EsoMainWindow::createToolBars()
{
	qDebug("EsoMainWindow::createToolBars() - start");
	fileToolBar = addToolBar(tr("File toolbar"));
	fileToolBar->setObjectName("File");
	fileToolBar->addAction(openAct);
	fileToolBar->addAction(savexEsoAct);
	fileToolBar->addAction(reloadAct);
	fileToolBar->addAction(printAct);
	fileToolBar->addAction(printPDFAct);

	
	viewToolBar = addToolBar(tr("View toolbar"));
	viewToolBar->setObjectName("View");
	viewToolBar->addAction(viewMaxAct);
	viewToolBar->addAction(viewMinAct);
	viewToolBar->addAction(viewMarkersAct);
	viewToolBar->addAction(viewGridAct);
	viewToolBar->addSeparator();
	viewToolBar->addAction(viewFilterAct);
	viewToolBar->addAction(viewInfoAct);
	viewToolBar->addAction(viewVarInfoAct);
	viewToolBar->addAction(viewVariableListAct);

	
	bookmarkToolBar = addToolBar(tr("Bookmark toolbar"));
	bookmarkToolBar->setObjectName("Bookmark");
	bookmarkToolBar->addAction(addBookmarkAct);
	bookmarkToolBar->addAction(deleteBookmarkAct);
	bookmarkToolBar->addAction(prevBookmarkAct);
	bookmarkToolBar->addWidget( m_BMcombo);
	bookmarkToolBar->addAction(nextBookmarkAct);

	qDebug("EsoMainWindow::createToolBars() - end");
}


void EsoMainWindow::createStatusBar()
{
	qDebug("EsoMainWindow::createStatusBar() - start");
	showMessage(tr("Ready"));
	qDebug("EsoMainWindow::createStatusBar() - end");
}


void EsoMainWindow::readSettings(bool bInit)
{
	qDebug("EsoMainWindow::readSettings() - start");
	QSettings settings(ESO_ORG, ESO_APP);
	if (bInit)
	{
		QPoint pos = settings.value("pos", QPoint(200, 200)).toPoint();
		QSize size = settings.value("size", QSize(400, 400)).toSize();
		move(pos);
		resize(size);
		m_sLastOpenDir = settings.value("lastOpenDir", QDir::homePath()).toString();
	}
	m_vRecentFiles.clear();
	m_vRecentFiles = GetRecentfiles();
	
	qDebug("EsoMainWindow::readSettings() - end");
}


void EsoMainWindow::writeSettings()
{
	qDebug("EsoMainWindow::writeSettings() - start");
	QSettings settings(ESO_ORG, ESO_APP);
	settings.setValue("pos", pos());
	settings.setValue("size", size());
	settings.setValue("lastOpenDir", m_sLastOpenDir);
	settings.setValue("winState", saveState());
		
//  	settings.setValue("toolbarBookmarkPos", bookmarkToolBar->pos());
//  	settings.setValue("toolbarViewPos", viewToolBar->pos());
//  	settings.setValue("toolbarFilePos", fileToolBar->pos());

	qDebug("EsoMainWindow::writeSettings() - end");
}


void EsoMainWindow::copyDataToClipboard()
{
	qDebug("EsoMainWindow::copyDataToClipboardAct()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->copyDataToClipboard();
	showReadyMessage();
}


void EsoMainWindow::copyPicToClipboard()
{
	qDebug("EsoMainWindow::copyPicToClipboardAct()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->copyPicToClipboard();
	showReadyMessage();
}


void EsoMainWindow::copyFileInfoToClipboard()
{
	qDebug("EsoMainWindow::copyFileInfoToClipboard()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->copyFileInfoToClipboard();
	showReadyMessage();

}


void EsoMainWindow::copyVarInfoToClipboard()
{
	qDebug("EsoMainWindow::copyVarInfoToClipboard()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->copyVarInfoToClipboard();
	showReadyMessage();
}


void EsoMainWindow::viewMin()
{
	qDebug("EsoMainWindow::viewMin()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->viewMin(viewMinAct->isChecked());
	showReadyMessage();
}


void EsoMainWindow::viewMax()
{
	qDebug("EsoMainWindow::viewMax()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->viewMax(viewMaxAct->isChecked());
	showReadyMessage();
}


void EsoMainWindow::viewMarkers()
{
	qDebug("EsoMainWindow::viewMarkers()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->viewMarkers(viewMarkersAct->isChecked());
	showReadyMessage();
}


void EsoMainWindow::viewFilter()
{
	qDebug("EsoMainWindow::viewFilter()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->viewFilter(viewFilterAct->isChecked());
	showReadyMessage();
}


void EsoMainWindow::viewInfo()
{
	qDebug("EsoMainWindow::viewInfo()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->viewInfo(viewInfoAct->isChecked());
	showReadyMessage();
}


void EsoMainWindow::viewVarInfo()
{
	qDebug("EsoMainWindow::viewVarInfo()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->viewVarInfo(viewVarInfoAct->isChecked());
	showReadyMessage();
}


void EsoMainWindow::viewGrid()
{
	qDebug("EsoMainWindow::viewGrid()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->viewGrid(viewGridAct->isChecked());
	showReadyMessage();
}


void EsoMainWindow::viewVariableList()
{
	qDebug("EsoMainWindow::viewVariableList()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->viewVariableList(viewVariableListAct->isChecked());
	showReadyMessage();
}

void EsoMainWindow::reloadEso()
{
	qDebug("EsoMainWindow::reloadEso()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->reloadEso();
	showReadyMessage();
}


EsoView* EsoMainWindow::activeEsoView()
{
//	qDebug("EsoMainWindow::activeEsoView()");
	return qobject_cast< EsoView*>(workspace->activeWindow());
}


EsoView* EsoMainWindow::findEsoView(const QString& fileName)
{
	qDebug("EsoMainWindow::findEsoView(const QString &fileName) - start");
	QString canonicalFilePath = QFileInfo(fileName).canonicalFilePath();

	foreach(QWidget * window, workspace->windowList())
	{
		EsoView* child = qobject_cast< EsoView*>(window);
		if (child->currentFile() == canonicalFilePath)
			return child;
	}
	qDebug("EsoMainWindow::findEsoView(const QString &fileName) - end");
	return 0;
}


void EsoMainWindow::showMessage(const QString& sMessage)
{
	statusBar()->showMessage(sMessage);
}

void EsoMainWindow::showReadyMessage()
{
	statusBar()->showMessage(tr("Ready"));
}

void EsoMainWindow::dragEnterEvent(QDragEnterEvent* event)
{
	qDebug() << "EsoMainWindow::dragEnterEvent " << event->mimeData()->formats();
	if (event->mimeData()->hasFormat("text/uri-list"))
		event->acceptProposedAction();
}


void EsoMainWindow::dropEvent(QDropEvent* event)
{
	//load eso
	qDebug() << "EsoMainWindow::dropEvent " << event->mimeData()->urls();
	event->acceptProposedAction();
	QList< QUrl> files;
	foreach(QUrl url, event->mimeData()->urls())
	{
		QString sFileName = url.toLocalFile();
		qDebug() << "EsoMainWindow::dropEvent " << sFileName;
		loadEso(sFileName);
	}    
	showReadyMessage();
	qDebug("EsoMainWindow::dropEvent() - end");
}


void EsoMainWindow::copyOptionIncludeTime()
{
	qDebug("EsoMainWindow::copyOptionIncludeTime()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->copyOptionIncludeTime(copyOptionIncludeTimeAct->isChecked());
	showReadyMessage();
}


void EsoMainWindow::print()
{
	qDebug("EsoMainWindow::print()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->print();
	showReadyMessage();
}


void EsoMainWindow::printPDF()
{
	qDebug("EsoMainWindow::printPDF()");
	if (workspace->activeWindow() != NULL)
		qobject_cast< EsoView*>(workspace->activeWindow())->printPDF();
	showReadyMessage();
}


int EsoMainWindow::GetRecentIndex(QString sFilename)
{
	for (int i=0; i< m_vRecentFiles.size(); ++i)
	{
		if (m_vRecentFiles[i] == sFilename)
			return i;
	}
	return -1;
}


// void EsoMainWindow::addBookmark(EsoBookmark bm, bool bAddToRecent)
// {
// 	qDebug("EsoMainWindow::addBookmark()");
// 	if (workspace->activeWindow() != NULL)
// 	{
// 		EsoView* curView = qobject_cast< EsoView*>(workspace->activeWindow());
// 		if (curView == NULL)
// 			return;
// 		int iRecInd = GetRecentIndex(curView->currentFile());
// 		if (iRecInd<0)
// 			qDebug() << "EsoMainWindow::addCurentToBookmarks - Can't find current file in recent file list!! '";
// 		else if (bAddToRecent)
// 			m_vRecentFiles[iRecInd].vBookmarks.push_back(bm);
// 		curView->(bm);
// 		updateMenus();
// 	}
// }


QComboBox * EsoMainWindow::getBookmarkCombo()
{
	return m_BMcombo;
}


void EsoMainWindow::addCurrentToBookmarks()
{
	qDebug("EsoMainWindow::addCurentToBookmarks()");
	if (workspace->activeWindow() != NULL)
	{
		EsoView* curView = qobject_cast< EsoView*>(workspace->activeWindow());
		if (curView == NULL)
			return;
		EsoBookmark bm = curView->AddCurrentToBookmarks();
		updateMenus();
	}
}

int EsoMainWindow::GetNumRecent()
{
	return m_vRecentFiles.size();
}

void EsoMainWindow::deleteBookmark()
{
	qDebug("EsoMainWindow::deleteBookmark()");
	if (workspace->activeWindow() != NULL)
	{
        EsoView* curView = qobject_cast< EsoView*>(workspace->activeWindow());
        if (curView == NULL)
            return;
		EsoBookmark bm = curView->deleteBookmark();
	}
	updateMenus();
}


void EsoMainWindow::nextBookmark()
{
	qDebug("EsoMainWindow::nextBookmark()");
	if (workspace->activeWindow() != NULL)
	{
        EsoView* curView = qobject_cast< EsoView*>(workspace->activeWindow());
        if (curView == NULL)
            return;
		QString sBM = curView->nextBookmark();
		int iBM = m_BMcombo->findText(sBM);
		qDebug() << "EsoMainWindow::nextBookmark - iBM=" << iBM ;
		m_BMcombo->blockSignals(true);
		m_BMcombo->setCurrentIndex(iBM);
		m_BMcombo->blockSignals(false);
	}
}


void EsoMainWindow::prevBookmark()
{
	qDebug("EsoMainWindow::prevBookmark()");
	if (workspace->activeWindow() != NULL)
	{
        EsoView* curView = qobject_cast< EsoView*>(workspace->activeWindow());
        if (curView == NULL)
            return;
		QString sBM = curView->prevBookmark();
		int iBM = m_BMcombo->findText(sBM);
		qDebug() << "EsoMainWindow::prevBookmark - iBM=" << iBM ;
		m_BMcombo->blockSignals(true);
		m_BMcombo->setCurrentIndex(iBM);
		m_BMcombo->blockSignals(false);

	}
}


void EsoMainWindow::gotoBookmark(const QString &sBM)
{
	qDebug() << "EsoMainWindow::gotoBookmark(" << sBM << ")";
	if (workspace->activeWindow() != NULL)
	{
		EsoView* curView = qobject_cast< EsoView*>(workspace->activeWindow());
		if (curView == NULL)
			return;
		curView->gotoBookmark(sBM);
	}
}

