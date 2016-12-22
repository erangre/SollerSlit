# -*- coding: utf8 -*-
# Dioptas - GUI program for fast processing of 2D X-ray data
# Copyright (C) 2014  Clemens Prescher (clemens.prescher@gmail.com)
# GSECARS, University of Chicago
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, print_function

__author__ = 'Clemens Prescher'
import pyqtgraph as pg
import numpy as np
from qtpy import QtCore


class PlotWidget(pg.PlotWidget):
    mouse_moved = QtCore.Signal(float, float)
    mouse_left_clicked = QtCore.Signal(float, float)
    range_changed = QtCore.Signal(list)
    auto_range_status_changed = QtCore.Signal(bool)

    def __init__(self):
        super(PlotWidget, self).__init__()
        self.spectrum_plot = self.getPlotItem()
        self.create_graphics()
        self.create_main_plot()
        self._auto_range = True

    def create_graphics(self):
        self.spectrum_plot.setLabel('bottom', u'2θ', u'°')
        self.spectrum_plot.enableAutoRange(False)
        self.spectrum_plot.buttonsHidden = True
        self.view_box = self.spectrum_plot.vb

    def create_main_plot(self):
        self.plot_item = pg.PlotDataItem(np.linspace(0, 10), np.sin(np.linspace(10, 3)),
                                         pen=pg.mkPen(color=(255, 255, 255), width=2))
        self.fit_item = pg.PlotDataItem(np.linspace(0, 10), np.sin(np.linspace(10, 3)),
                                         pen=pg.mkPen(color=(255, 0, 0), width=2))
        self.vline_item = pg.InfiniteLine(angle=90, movable=False)
        self.hline_item = pg.InfiniteLine(angle=0, movable=False)
        self.spectrum_plot.addItem(self.plot_item)
        self.spectrum_plot.addItem(self.fit_item)
        self.fit_item.hide()
        self.spectrum_plot.addItem(self.vline_item)
        self.spectrum_plot.addItem(self.hline_item)

    @property
    def auto_range(self):
        return self._auto_range

    @auto_range.setter
    def auto_range(self, value):
        if self._auto_range is not value:
            self._auto_range = value
            self.auto_range_status_changed.emit(value)
        if self._auto_range is True:
            self.update_graph_range()

    def plot_data(self, x, y, name=None):
        self.plot_item.setData(x, y)
        self.update_graph_range()

    def plot_fit(self, x, y):
        self.fit_item.setData(x, y)
        self.fit_item.show()

    def update_graph_range(self):
        x_range = list(self.plot_item.dataBounds(0))
        y_range = list(self.plot_item.dataBounds(1))

        if x_range[1] is not None and x_range[0] is not None:
            padding = self.view_box.suggestPadding(0)
            diff = x_range[1] - x_range[0]
            x_range = [x_range[0] - padding * diff,
                       x_range[1] + padding * diff]

            self.view_box.setLimits(xMin=x_range[0], xMax=x_range[1])

            if self.auto_range:
                self.view_box.setRange(xRange=x_range, padding=0)

        if y_range[1] is not None and y_range[0] is not None:
            padding = self.view_box.suggestPadding(1)
            diff = y_range[1] - y_range[0]
            y_range = [y_range[0] - padding * diff,
                       y_range[1] + padding * diff]

            self.view_box.setLimits(yMin=y_range[0], yMax=y_range[1])

            if self.auto_range:
                self.view_box.setRange(yRange=y_range, padding=0)
        self.emit_sig_range_changed()

    def mouseMoved(self, pos):
        pos = self.plot_item.mapFromScene(pos)
        self.mouse_moved.emit(pos.x(), pos.y())

    def modify_mouse_behavior(self):
        # different mouse handlers
        self.view_box.setMouseMode(self.view_box.RectMode)

        self.scene().sigMouseMoved.connect(self.mouseMoved)
        self.view_box.mouseClickEvent = self.myMouseClickEvent
        self.view_box.mouseDragEvent = self.myMouseDragEvent
        self.view_box.mouseDoubleClickEvent = self.myMouseDoubleClickEvent
        self.view_box.wheelEvent = self.myWheelEvent

        # create sigranged changed timer for right click drag
        # if not using the timer the signals are fired too often and
        # the computer becomes slow...
        self.range_changed_timer = QtCore.QTimer()
        self.range_changed_timer.timeout.connect(self.emit_sig_range_changed)
        self.range_changed_timer.setInterval(30)
        self.last_view_range = np.array(self.view_box.viewRange())

    def myMouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton or \
                (ev.button() == QtCore.Qt.LeftButton and
                         ev.modifiers() & QtCore.Qt.ControlModifier):
            view_range = np.array(self.view_box.viewRange()) * 2
            curve_data = self.plot_item.getData()
            x_range = np.max(curve_data[0]) - np.min(curve_data[0])
            if (view_range[0][1] - view_range[0][0]) > x_range:
                self.auto_range = True
            else:
                self.auto_range = False
                self.view_box.scaleBy(2)
            self.emit_sig_range_changed()
        elif ev.button() == QtCore.Qt.LeftButton:
            pos = self.view_box.mapFromScene(ev.pos())
            pos = self.plot_item.mapFromScene(2 * ev.pos() - pos)
            x = pos.x()
            y = pos.y()
            self.mouse_left_clicked.emit(x, y)

    def myMouseDoubleClickEvent(self, ev):
        if (ev.button() == QtCore.Qt.RightButton) or (ev.button() == QtCore.Qt.LeftButton and
                                                              ev.modifiers() & QtCore.Qt.ControlModifier):
            self.auto_range = True
            self.emit_sig_range_changed()

    def myMouseDragEvent(self, ev, axis=None):
        # most of this code is copied behavior mouse drag from the original code
        ev.accept()
        pos = ev.pos()
        lastPos = ev.lastPos()
        dif = pos - lastPos
        dif *= -1

        if ev.button() == QtCore.Qt.RightButton or \
                (ev.button() == QtCore.Qt.LeftButton and
                         ev.modifiers() & QtCore.Qt.ControlModifier):
            # determine the amount of translation
            tr = dif
            tr = self.view_box.mapToView(tr) - self.view_box.mapToView(pg.Point(0, 0))
            x = tr.x()
            y = tr.y()
            self.view_box.translateBy(x=x, y=y)
            if ev.start:
                self.range_changed_timer.start()
            if ev.isFinish():
                self.range_changed_timer.stop()
                self.emit_sig_range_changed()
        else:
            if ev.isFinish():  # This is the final move in the drag; change the view scale now
                self.auto_range = False
                self.view_box.rbScaleBox.hide()
                ax = QtCore.QRectF(pg.Point(ev.buttonDownPos(ev.button())), pg.Point(pos))
                ax = self.view_box.childGroup.mapRectFromParent(ax)
                self.view_box.showAxRect(ax)
                self.view_box.axHistoryPointer += 1
                self.view_box.axHistory = self.view_box.axHistory[:self.view_box.axHistoryPointer] + [ax]
                self.emit_sig_range_changed()
            else:
                # update shape of scale box
                self.view_box.updateScaleBox(ev.buttonDownPos(), ev.pos())

    def emit_sig_range_changed(self):
        new_view_range = np.array(self.view_box.viewRange())
        if not np.array_equal(self.last_view_range, new_view_range):
            self.view_box.sigRangeChangedManually.emit(self.view_box.state['mouseEnabled'])
            self.last_view_range = new_view_range

    def myWheelEvent(self, ev, axis=None, *args):
        if ev.delta() > 0:
            pg.ViewBox.wheelEvent(self.view_box, ev, axis)

            self.auto_range = False
            # axis_range = self.spectrum_plot.viewRange()
            # self.range_changed.emit(axis_range)
            self.emit_sig_range_changed()
        else:
            if self.auto_range is not True:
                view_range = np.array(self.view_box.viewRange())
                curve_data = self.plot_item.getData()
                x_range = np.max(curve_data[0]) - np.min(curve_data[0])
                y_range = np.max(curve_data[1]) - np.min(curve_data[1])
                if (view_range[0][1] - view_range[0][0]) >= x_range and \
                                (view_range[1][1] - view_range[1][0]) >= y_range:
                    self.auto_range = True
                else:
                    self.auto_range = False
                    pg.ViewBox.wheelEvent(self.view_box, ev)
            self.emit_sig_range_changed()
