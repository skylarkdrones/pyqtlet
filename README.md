# pyqtlet

---

### NOTE:
This repository is no longer in active development. To follow a fork that is being updated, please follow https://github.com/JaWeilBaum/pyqtlet2.

---

pyqtlet is a wrapper for Leaflet maps in PyQt5. In construction and design, it mimics the [official leaflet api](http://leafletjs.com/reference-1.3.0.html) as much as possible.

pyqtlet is currently in v0.3.0. To get started, visit the [Getting Started page](http://pyqtlet.readthedocs.io/en/latest/getting-started.html)

Further details about implementation, API docs etc can also be found on the [pyqtlet site](http://pyqtlet.readthedocs.io/en/latest/index.html)

## Installation

``` bash
pip3 install PyQt5
pip3 install pyqtlet
```

``` bash
# To test whether it is successfully working
python3 
>>> from pyqtlet import L, MapWidget
>>> # No errors
```

## Usage

``` python
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from pyqtlet import L, MapWidget


class MapWindow(QWidget):
    def __init__(self):
        # Setting up the widgets and layout
        super().__init__()
        self.mapWidget = MapWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.mapWidget)
        self.setLayout(self.layout)

        # Working with the maps with pyqtlet
        self.map = L.map(self.mapWidget)
        self.map.setView([12.97, 77.59], 10)
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(self.map)
        self.marker = L.marker([12.934056, 77.610029])
        self.marker.bindPopup('Maps are a treasure.')
        self.map.addLayer(self.marker)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MapWindow()
    sys.exit(app.exec_())
```

## Using Unimplemented Leaflet Features
At this time, there is noone actively adding features to pyqtlet. This means that there
are a lot of Leaflet features that are not implemented in pyqtlet. However, there is still
a way to access these features via the `runJavaScript` api. This allows arbitrary code to
be run within the map window.

For example, if we want to change the marker icon in the above example, add the following
2 lines of code after the `self.map.addLayer(self.marker)` statement.

``` python
        # Create a icon called markerIcon in the js runtime.
        self.map.runJavaScript('var markerIcon = L.icon({iconUrl: "https://leafletjs.com/examples/custom-icons/leaf-red.png"});')
        # Edit the existing python object by accessing it's jsName property
        self.map.runJavaScript(f'{self.marker.jsName}.setIcon(markerIcon);')
```

This technique will allow users to use all the features available in leaflet.

## Contributing
In terms of contributing, there is a lot of work that still needs to be done. 
Specifically, there are a lot of leaflet features that need to be ported into pyqtlet. All contributions welcome.
For further details, visit the [contributing page](http://pyqtlet.readthedocs.io/en/latest/contributing.html).
