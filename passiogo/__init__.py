"""
PassioGo - Unofficial Python API Wrapper for Passio Go Transit Systems

This package provides a Python interface to the Passio Go API, enabling access
to real-time transit data for hundreds of universities, municipalities, airports,
and paratransit services.

Basic Usage:
    >>> import passiogo
    >>>
    >>> # Get all available systems
    >>> systems = passiogo.getSystems()
    >>>
    >>> # Get a specific system by ID
    >>> umich = passiogo.getSystemFromID(1270)
    >>>
    >>> # Get routes, stops, and vehicles
    >>> routes = umich.getRoutes()
    >>> stops = umich.getStops()
    >>> vehicles = umich.getVehicles()
    >>> alerts = umich.getSystemAlerts()

Coordinate System:
    All geographic coordinates use the standard latitude/longitude format:
    - Latitude: Degrees North/South (-90 to +90)
    - Longitude: Degrees East/West (-180 to +180)

Author: PassioGo Contributors
License: See LICENSE file
"""

# Import models
from .models import (
	TransportationSystem,
	Route,
	Stop,
	SystemAlert,
	Vehicle
)

# Import client functions
from .client import (
	getSystems,
	getSystemFromID,
	printAllSystemsMd,
	BASE_URL
)

# For backward compatibility, also import websocket placeholder
import json
import websocket


### Live Timings ###
## Not Yet Supported! ##

# Launch WebSocket
def launchWS():
	"""
	Launch WebSocket connection for live vehicle tracking.

	WARNING: This feature is not yet fully implemented.

	The WebSocket functionality is planned for future releases to provide
	real-time streaming updates of vehicle positions.
	"""
	uri = "wss://passio3.com/"


	websocket.enableTrace(False) # For Debugging
	wsapp = websocket.WebSocketApp(
		uri,
		on_open = subscribeWS,
		#on_message = ...,
		on_error = handleWsError,
		on_close = handleWsClose
	)
	wsapp.run_forever(
		ping_interval = 5,
		ping_timeout = 3,
	)


def handleWsError(wsapp, error):
	"""Handle WebSocket errors (not yet implemented)."""
	...


def handleWsClose(wsapp, close_status_code, close_msg):
	"""Handle WebSocket close events (not yet implemented)."""
	wsapp.close()


def subscribeWS(
	wsapp,
	userId
):
	"""
	Subscribe to vehicle location updates via WebSocket.

	WARNING: This feature is not yet fully implemented.

	Args:
		wsapp: WebSocket app instance
		userId: Transportation system ID to subscribe to
	"""

	subscriptionMsg = {
		"subscribe":"location",
		"userId":[userId],
		"field":[
			"busId",
			"latitude",
			"longitude",
			"course",
			"paxLoad",
			"more"
		]
	}
	wsapp.send(json.dumps(subscriptionMsg))


# Package metadata
__version__ = "0.2.3"
__all__ = [
	# Models
	"TransportationSystem",
	"Route",
	"Stop",
	"SystemAlert",
	"Vehicle",
	# Functions
	"getSystems",
	"getSystemFromID",
	"printAllSystemsMd",
	# WebSocket (not yet supported)
	"launchWS",
	"subscribeWS",
	# Constants
	"BASE_URL",
]
