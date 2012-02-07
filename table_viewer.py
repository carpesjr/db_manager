# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                 : DB Manager
Description          : Database manager plugin for QuantumGIS
Date                 : May 23, 2011
copyright            : (C) 2011 by Giuseppe Sucameli
email                : brush.tyler@gmail.com

 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from .db_plugins.plugin import DbError, Table
from .dlg_db_error import DlgDbError

class TableViewer(QTableView):
	def __init__(self, parent=None):
		QTableView.__init__(self, parent)
		self.setSelectionBehavior( QAbstractItemView.SelectRows )
		self.setSelectionMode( QAbstractItemView.ExtendedSelection )
		self.item = None

		# allow to copy results
		copyAction = QAction("copy", self)
		self.addAction( copyAction )
		copyAction.setShortcuts(QKeySequence.Copy)
		QObject.connect(copyAction, SIGNAL("triggered()"), self.copySelectedResults)

		self._clear()

	def refresh(self):
		self.loadData( self.item, True )

	def loadData(self, item, force=False):
		if item == self.item and not force: 
			return
		self._clear()
		if item is None:
			return

		if isinstance(item, Table):
			self._loadTableData( item )
		else:
			return

		self.item = item
		self.connect(self.item, SIGNAL('aboutToChange'), self._clear)
		self.connect(self.item, SIGNAL('changed'), self.refresh)

	def _clear(self):
		if self.item is not None:
			self.disconnect(self.item, SIGNAL('aboutToChange'), self._clear)
			self.disconnect(self.item, SIGNAL('changed'), self.refresh)

		self.item = None

		# delete the old model
		model = self.model()
		self.setModel(None)
		if model: model.deleteLater()

	def _loadTableData(self, table):
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		try:
			# set the new model
			self.setModel( table.tableDataModel(self) )

		except DbError, e:
			QApplication.restoreOverrideCursor()
			DlgDbError.showError(e, self)

		else:
			self.update()
			QApplication.restoreOverrideCursor()


	def copySelectedResults(self):
		if len(self.selectedIndexes()) <= 0:
			return
		model = self.model()

		# convert to string using tab as separator
		text = model.headerToString( "\t" )
		for idx in self.selectionModel().selectedRows():
			text += "\n" + model.rowToString( idx.row(), "\t" )

		QApplication.clipboard().setText( text, QClipboard.Selection )
		QApplication.clipboard().setText( text, QClipboard.Clipboard )


