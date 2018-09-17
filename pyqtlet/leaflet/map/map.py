import json
import logging
import os
import time

from PyQt5.QtCore import pyqtSlot, pyqtSignal

from ... import mapwidget
from ..core import Evented

class Map(Evented):
    '''
    .. module:: pyqtlet

    pyqtlet equivalent of L.map

    Map element has to be the first pyqtlet object to be initiated.

    .. note::
        Further documentation can be found at the official leaflet API.

    :param pyqtlet.MapWidget mapWidget: The mapwidget object
        Should only be sent once, when the first object is being 
        initialised.

    :param dict options: Options for initiation (optional)
    '''
   
    clicked = pyqtSignal(dict)
    zoom = pyqtSignal(dict)
    drawCreated = pyqtSignal(dict)
    # mapId is a static variable shared between all layers
    # It is used to give unique names to layers
    mapId = 0

    @property
    def layers(self):
        """
        Instead of L.map.eachLayer
        """
        return self._layers

    @property
    def jsName(self):
        '''
        Name of the Leaflet element
        '''
        return self._jsName

    @pyqtSlot(dict)
    def _onClick(self, event):
        self._logger.debug('map clicked. event: {event}'.format(event=event))
        self.clicked.emit(event)

    @pyqtSlot(dict)
    def _onDrawCreated(self, event):
        self._logger.debug('draw created. event: {event}'.format(event=event))
        self.drawCreated.emit(event)

    @pyqtSlot(dict)
    def _onZoom(self, event):
        self._logger.debug('map zoom. event: {event}'.format(event=event))
        self.zoom.emit(event)

    def __init__(self, mapWidget, options=None):
        '''
        pyqtlet equivalent of L.map

        Map element has to be the first pyqtlet object to be initiated.

        :param pyqtlet.MapWidget mapWidget: The mapwidget object
            Should only be sent once, when the first object is being 
            initialised.

        :param dict options: Options for initiation (optional)

        .. note
            Further documentation can be found at the official leaflet API.
        '''

        super().__init__(mapWidget)
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(9)
        self.options = options
        self._layers = []
        self._controls = []
        self._jsName = self._getNewMapName()
        self._initJs(mapWidget)
        self._connectEventToSignal('click', '_onClick')
        self._connectEventToSignal('zoom', '_onZoom')
        self._connectEventToSignal('draw:created', '_onDrawCreated')

    def _getNewMapName(self):
        mapName = 'map{}'.format(self.mapId)
        Map.mapId += 1
        return mapName

    def _initJs(self, mapWidget):
        # First we need to create a new map object in the html
        js = ('var {mapName}_el = document.getElementById("map");'
              '{mapName}_el.setAttribute("id", "{mapName}");'
              '{mapName}_el.style.width = "100vw";'
              '{mapName}_el.style.height = "100vh";').format(mapName=self.jsName)
        # self.runJavaScript(js)
        jsObject = 'L.map("{mapName}"'.format(mapName=mapWidget.mapId)
        if self.options:
            jsObject += ', {options}'.format(options=self._stringifyForJs(self.options))
        jsObject += ')'
        self._createJsObject(jsObject)
        self.runJavaScript('{mapName}.setView([12.97, 77.59], 10);'.format(mapName=self.jsName))

    def setView(self, latLng, zoom=None, options=None):
        js = '{mapName}.setView({latLng}'.format(mapName=self.jsName, latLng=latLng);
        if zoom:
            js += ', {zoom}'.format(zoom=zoom)
        if options:
            js += ', {options}'.format(options=options)
        js += ');'
        self.runJavaScript(js)

    def addLayer(self, layer):
        self._layers.append(layer)
        layer.map = self
        js = '{mapName}.addLayer({layerName})'.format(mapName=self.jsName, layerName=layer.layerName)
        self.runJavaScript(js)

    def removeLayer(self, layer):
        if layer not in self._layers:
            # TODO Should we raise a ValueError here? Or just return
            return
        self._layers.remove(layer)
        layer.map = None
        js = '{mapName}.removeLayer({layerName})'.format(mapName=self.jsName, layerName=layer.layerName)
        self.runJavaScript(js)

    def addControl(self, control):
        self._controls.append(control)
        control.map = self
        js = '{mapName}.addControl({controlName})'.format(mapName=self.jsName, controlName=control.controlName)
        self.runJavaScript(js)

    def removeControl(self, control):
        if control not in self._controls:
            # TODO Should we raise a ValueError here? Or just return
            return
        self._controls.remove(control)
        control.map = None
        js = '{mapName}.removeControl({controlName})'.format(mapName=self.jsName, controlName=control.controlName)
        self.runJavaScript(js)

    def getBounds(self, callback):
        return self.getJsResponse('{mapName}.getBounds()'.format(mapName=self.jsName), callback)

    def getCenter(self, callback):
        return self.getJsResponse('{mapName}.getCenter()'.format(mapName=self.jsName), callback)

    def getZoom(self, callback):
        return self.getJsResponse('{mapName}.getZoom()'.format(mapName=self.jsName), callback)

    def getState(self, callback):
        return self.getJsResponse('getMapState({jsmap})'.format(jsmap=self.jsName), callback)

    def hasLayer(self, layer):
        return layer in self._layers

    def setZoom(self, zoom, options=None):
        js = '{mapName}.setZoom({zoom}'.format(mapName=self.jsName, zoom=zoom)
        if options:
            js += ', {options}'.format(options=options)
        js += ');'
        self.runJavaScript(js)

    def setMaxBounds(self, bounds):
        js = '{mapName}.setMaxBounds({bounds})'.format(mapName=self.jsName, bounds=bounds)
        self.runJavaScript(js)
       
    def fitBounds(self, bounds):
        js = '{mapName}.fitBounds({bounds})'.format(mapName=self.jsName, bounds=bounds)
        self.runJavaScript(js)

    def setMaxZoom(self, zoom):
        js = '{mapName}.setMaxZoom({zoom})'.format(mapName=self.jsName, zoom=zoom)
        self.runJavaScript(js)

    def setMinZoom(self, zoom):
        js = '{mapName}.setMinZoom({zoom})'.format(mapName=self.jsName, zoom=zoom)
        self.runJavaScript(js)

    def panTo(self, latLng, options=None):
        js = '{mapName}.panTo({latLng}'.format(mapName=self.jsName, latLng=latLng);
        if options:
            js += ', {options}'.format(options=options)
        js += ');'
        self.runJavaScript(js)

    def flyTo(self, latLng, zoom=None, options=None):
        js = '{mapName}.flyTo({latLng}'.format(mapName=self.jsName, latLng=latLng);
        if zoom:
            js += ', {zoom}'.format(zoom=zoom)
        if options:
            js += ', {options}'.format(options=options)
        js += ');'
        self.runJavaScript(js)

