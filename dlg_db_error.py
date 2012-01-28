# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                 : DB Manager
Description          : Database manager plugin for QuantumGIS
Date                 : May 23, 2011
copyright            : (C) 2011 by Giuseppe Sucameli
email                : brush.tyler@gmail.com

The content of this file is based on 
- PG_Manager by Martin Dobias (GPLv2 license)
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

from ui.DlgDbError_ui import Ui_DlgDbError
from .db_plugins.plugin import DbError

class DlgDbError(QDialog, Ui_DlgDbError):
	def __init__(self, e, parent=None):
		QDialog.__init__(self, parent)
		self.setupUi(self)

		def sanitize(txt):
			return "" if txt == None else "<pre>" + txt.replace('<','&lt;') + "</pre>"

		if isinstance(e, DbError) and hasattr(e.query):
			self.setQueryMessage( sanitize(e.message), sanitize(e.query) )
		else:
			self.setMessage( sanitize(e.message) )

	def setMessage(self, msg):
		self.txtErrorMsg.setHtml(msg)
		self.stackedWidget.setCurrentIndex(0)

	def setQueryMessage(self, msg, query):
		self.txtQueryErrorMsg.setHtml(msg)
		self.txtQuery.setHtml(query)
		self.stackedWidget.setCurrentIndex(1)


	@staticmethod
	def showError(e, parent=None):
		dlg = DlgDbError(e, parent)
		dlg.exec_()

