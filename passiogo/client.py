"""
PassioGo API Client

This module handles all HTTP communication with the Passio Go API.
Contains helper functions and the main API request methods.

Author: PassioGo Contributors
License: See LICENSE file
"""

import requests
from typing import Optional, List
from .models import TransportationSystem, Route, Stop, SystemAlert, Vehicle

BASE_URL = "https://passiogo.com"


def toIntInclNone(toInt):
	"""
	Convert a value to integer, preserving None.

	Args:
		toInt: Value to convert (can be int, str, or None)

	Returns:
		int or None: Integer value or None if input was None
	"""
	if toInt == None:
		return toInt
	return(int(toInt))


def sendApiRequest(url: str, body: Optional[dict]) -> Optional[dict]:
	"""
	Send a POST request to the Passio Go API.

	Args:
		url: Full API endpoint URL
		body: JSON body to send (can be None for some endpoints)

	Returns:
		dict: JSON response from the API
		None: If request failed

	Raises:
		Exception: If response cannot be parsed as JSON
		Exception: If API returns an error response

	Example:
		>>> url = "https://passiogo.com/mapGetData.php?getSystems=2&sortMode=1&credentials=1"
		>>> response = sendApiRequest(url, None)
	"""

	# Send Request
	response = requests.post(url, json = body)

	try:
		# Handle JSON Response
		response = response.json()
	except Exception as e:
		raise Exception(f"Error converting API response to JSON! Here is the response received: {response}")
		return None


	# Handle API Error
	if(
		"error" in response and
		response["error"] != ""
	):
		raise Exception(f"Error in Response! Here is the received response: {response}")

	return(response)


def getSystems(
	appVersion: int = 2,
	sortMode: int = 1,
) -> List[TransportationSystem]:
	"""
	Get all available transportation systems.

	Retrieves the complete list of transit agencies available through Passio Go,
	including universities, municipalities, airports, and paratransit services.

	Args:
		appVersion: API version to use (default: 2)
		            - Values < 2: Returns error
		            - Value = 2: Valid response
		sortMode: Sorting mode for results (default: 1)
		          Note: Effect of this parameter is not fully documented

	Returns:
		List of TransportationSystem objects

	Example:
		>>> systems = passiogo.getSystems()
		>>> for system in systems:
		...     print(f"{system.name} (ID: {system.id})")
		'University of Michigan (ID: 1270)'
		'University of Wisconsin-Madison (ID: 567)'
		...
	"""


	# Initialize & Send Request
	url = f"{BASE_URL}/mapGetData.php?getSystems={appVersion}&sortMode={sortMode}&credentials=1"
	systems = sendApiRequest(url, None)


	# Handle Request Error
	if(systems == None):
		return([])


	allSystems = []
	for system in systems["all"]:

		# Convert Empty Strings To None Objects
		for parameter in system.keys():
			if system[parameter] == '':
				system[parameter] = None

		# Check all keys exist
		for key in ["goAgencyName", "email", "email", "goTestMode", "name2", "homepage", "logo", "goRoutePlannerEnabled", "goColor", "goSupportEmail", "goSharedCode", "goAuthenticationType"]:
			if key not in system.keys():
				system[key] = None

		allSystems.append(TransportationSystem(
			id = int(system["id"]),
			name = system["fullname"],
			username = system["username"],
			goAgencyName = system["goAgencyName"],
			email = system["email"],
			goTestMode = bool(int(system["goTestMode"])),
			name2 = bool(int(system["name2"])),
			homepage = system["homepage"],
			logo = bool(int(system["logo"])),
			goRoutePlannerEnabled = bool(int(system["goRoutePlannerEnabled"])),
			goColor = system["goColor"],
			goSupportEmail = system["goSupportEmail"],
			goSharedCode = toIntInclNone(system["goSharedCode"]),
			goAuthenticationType = bool(int(system["goAuthenticationType"])),
		))


	return(allSystems)


def getSystemFromID(
	id: int,
	appVersion: int = 2,
	sortMode: int = 1,
) -> Optional[TransportationSystem]:
	"""
	Get a specific transportation system by its ID.

	Args:
		id: The unique system identifier
		appVersion: API version to use (default: 2)
		sortMode: Sorting mode for results (default: 1)

	Returns:
		TransportationSystem object if found, None otherwise

	Raises:
		AssertionError: If parameter types are incorrect

	Example:
		>>> system = passiogo.getSystemFromID(1270)
		>>> print(system.name)
		'University of Michigan'
	"""

	# Check Input Type
	assert type(id) == int, "`id` must be of type int"

	# Check App Version Type
	assert type(appVersion) == int, "`appVersion` must be of type int"

	# Check sort Mode Type
	assert type(sortMode) == int, "`sortMode` must be of type int"

	systems = getSystems(appVersion,sortMode)

	for system in systems:
		if system.id == id:
			return system
	return None


def printAllSystemsMd(
	includeHtmlBreaks: bool = True
):
	"""
	Print all systems in Markdown format.

	Utility function for generating documentation or lists of available systems.

	Args:
		includeHtmlBreaks: Whether to include <br/> tags after each line (default: True)

	Example:
		>>> passiogo.printAllSystemsMd()
		- University of Michigan (#1270)<br/>
		- University of Wisconsin-Madison (#567)<br/>
		...
	"""
	systems = getSystems()

	for system in systems:
		print(f"- {system.name} (#{system.id}){'<br/>' if includeHtmlBreaks else ''}")


def getRoutes(
	system: TransportationSystem,
	appVersion: int = 1,
	amount: int = 1
) -> List[Route]:
	"""
	Get all routes for a transportation system.

	Args:
		system: The TransportationSystem to query
		appVersion: API version parameter (default: 1)
		amount: Controls which routes are returned:
		        - 1: Returns all routes for the given system (recommended)
		        - 0: Invalid, returns error
		        - >=2: Returns all routes plus potentially unrelated routes

	Returns:
		List of Route objects

	Example:
		>>> system = passiogo.getSystemFromID(1270)
		>>> routes = system.getRoutes()
		>>> for route in routes:
		...     print(f"{route.name}: {len(route.getStops())} stops")
	"""


	# Initialize & Send Request
	url = BASE_URL+f"/mapGetData.php?getRoutes={appVersion}"
	body = {
			"systemSelected0" : str(system.id),
			"amount" : amount
			}
	routes = sendApiRequest(url, body)

	# Handle Request Error
	if(routes == None):
		return(None)


	# Handle Differing Response Format
	if "all" in routes:
		routes = routes["all"]

	allRoutes = []
	for route in routes:
		possibleKeys = ["id", "groupId", "groupColor", "name", "shortName", "nameOrig", "fullname", "myid", "mapApp", "archive", "goPrefixRouteName", "goShowSchedule", "outdated", "distance", "latitude", "longitude", "timezone", "serviceTime", "serviceTimeShort"]

		for possibleKey in possibleKeys:
			if possibleKey not in route.keys():
				route[possibleKey] = None

		allRoutes.append(Route(
			id = route["id"],
			groupId = route["groupId"],
			groupColor = route["groupColor"],
			name = route["name"],
			shortName = route["shortName"],
			nameOrig = route["nameOrig"],
			fullname = route["fullname"],
			myid = route["myid"],
			mapApp = route["mapApp"],
			archive = route["archive"],
			goPrefixRouteName = route["goPrefixRouteName"],
			goShowSchedule = route["goShowSchedule"],
			outdated = route["outdated"],
			distance = route["distance"],
			latitude = route["latitude"],
			longitude = route["longitude"],
			timezone = route["timezone"],
			serviceTime = route["serviceTime"],
			serviceTimeShort = route["serviceTimeShort"],
			systemId = int(route["userId"]),
			system = system
		))

	return(allRoutes)


def getStops(
	system: TransportationSystem,
	appVersion: int = 2,
	sA: int = 1,
	raw: bool = False
) -> List[Stop]:
	"""
	Get all stops for a transportation system.

	Args:
		system: The TransportationSystem to query
		appVersion: API version parameter (default: 2)
		            Note: Effect of this parameter is not fully documented
		sA: Controls which stops are returned:
		    - 0: Returns error
		    - 1: Returns all stops for the given system (recommended)
		    - >=2: Returns all stops plus potentially unrelated stops
		raw: If True, returns raw API response dict instead of Stop objects

	Returns:
		List of Stop objects, or dict if raw=True

	Example:
		>>> system = passiogo.getSystemFromID(1270)
		>>> stops = system.getStops()
		>>> for stop in stops:
		...     print(f"{stop.name}: ({stop.latitude}, {stop.longitude})")
		...     print(f"  Served by routes: {list(stop.routesAndPositions.keys())}")
	"""


	# Initialize & Send Request
	url = BASE_URL+"/mapGetData.php?getStops="+str(appVersion)
	body = {
		"s0" : str(system.id),
		"sA" : sA
	}
	stops = sendApiRequest(url, body)

	# Return Raw Response
	if raw:
		return(stops)

	# Handle Request Error
	if(stops == None):
		return(None)

	# Handle Empty Routes
	if stops["routes"] == []:
		stops["routes"] = {}

	# Handle Empty Stops
	if stops["stops"] == []:
		stops["stops"] = {}


	# Create Route & Stops Dictionary
	# {routeid -> [stopid, stopid]}
	routesAndStops = {}
	for routeId, route in stops["routes"].items():
		routesAndStops[routeId] = []
		for stop in route[2:]:
			if stop == 0:
				continue
			routesAndStops[routeId].append(stop[1])


	# Create Each Stop Object
	allStops = []
	for id, stop in stops["stops"].items():

		# Create Route & Positions Dictionary
		# {routeid -> [position]}
		routesAndPositions = {}
		for routeId in routesAndStops.keys():
			if stop["id"] not in routesAndStops[routeId]:
				continue
			routesAndPositions[routeId] = [i for i,x in enumerate(routesAndStops[routeId]) if x == stop["id"]]


		keys = ["userId", "radius"]
		for key in keys:
			if key not in stop:
				stop[key] = None

		allStops.append(Stop(
			id = stop["id"],
			routesAndPositions = routesAndPositions,
			systemId = None if stop["userId"] is None else int(stop["userId"]),
			name = stop["name"],
			latitude = stop["latitude"],
			longitude = stop["longitude"],
			radius = stop["radius"],
			system = system,
		))

	return(allStops)


def getSystemAlerts(
	system: TransportationSystem,
	appVersion: int = 1,
	amount: int = 1,
	routesAmount: int = 0
) -> List[SystemAlert]:
	"""
	Get all active alerts for a transportation system.

	Alerts include service notifications, route changes, delays, and other
	important information for riders.

	Args:
		system: The TransportationSystem to query
		appVersion: API version parameter (default: 1)
		            - 0: Returns error
		            - >=1: Valid
		amount: Number of alerts to retrieve (default: 1)
		routesAmount: Route filtering parameter (default: 0)

	Returns:
		List of SystemAlert objects

	Example:
		>>> system = passiogo.getSystemFromID(1270)
		>>> alerts = system.getSystemAlerts()
		>>> for alert in alerts:
		...     print(f"{alert.name}")
		...     print(f"  {alert.html}")
		...     print(f"  Active: {alert.dateTimeFrom} to {alert.dateTimeTo}")
	"""


	# Initialize & Send Request
	url = BASE_URL+f"/goServices.php?getAlertMessages={appVersion}"
	body = {
		"systemSelected0" : str(system.id),
		"amount" : amount,
		"routesAmount":routesAmount
	}
	errorMsgs = sendApiRequest(url, body)

	# Handle Request Error
	if(errorMsgs == None):
		return(None)

	# Create SystemAlert Objects
	allAlerts = []
	for errorMsg in errorMsgs["msgs"]:
		allAlerts.append(SystemAlert(
			id = errorMsg["id"],
			systemId = errorMsg["userId"],
			system = system,
			routeId = errorMsg["routeId"],
			name = errorMsg["name"],
			html = errorMsg["html"],
			archive = errorMsg["archive"],
			important = errorMsg["important"],
			dateTimeCreated = errorMsg["created"],
			dateTimeFrom = errorMsg["from"],
			dateTimeTo = errorMsg["to"],
			asPush = errorMsg["asPush"],
			gtfs = errorMsg["gtfs"],
			gtfsAlertCauseId = errorMsg["gtfsAlertCauseId"],
			gtfsAlertEffectId = errorMsg["gtfsAlertEffectId"],
			gtfsAlertUrl = errorMsg["gtfsAlertUrl"],
			gtfsAlertHeaderText = errorMsg["gtfsAlertHeaderText"],
			gtfsAlertDescriptionText = errorMsg["gtfsAlertDescriptionText"],
			routeGroupId = errorMsg["routeGroupId"],
			createdUtc = errorMsg["createdUtc"],
			authorId = errorMsg["authorId"],
			author = errorMsg["author"],
			updated = errorMsg["updated"],
			updateAuthorId = errorMsg["updateAuthorId"],
			updateAuthor = errorMsg["updateAuthor"],
			createdF = errorMsg["createdF"],
			fromF = errorMsg["fromF"],
			fromOk = errorMsg["fromOk"],
			toOk = errorMsg["toOk"],
		))

	return(allAlerts)


def getVehicles(
	system: TransportationSystem,
	appVersion: int = 2
) -> List[Vehicle]:
	"""
	Get all currently active vehicles for a transportation system.

	Returns real-time vehicle positions, routes, and status information.

	Args:
		system: The TransportationSystem to query
		appVersion: API version parameter (default: 2)
		            - 0: Returns error
		            - >=1: Valid

	Returns:
		List of Vehicle objects with real-time positions

	Note:
		Vehicle coordinates use the standard latitude/longitude format:
		- latitude: North/South position (-90 to +90)
		- longitude: East/West position (-180 to +180)

	Example:
		>>> system = passiogo.getSystemFromID(1270)
		>>> vehicles = system.getVehicles()
		>>> for vehicle in vehicles:
		...     print(f"Vehicle {vehicle.name} on route {vehicle.routeName}")
		...     print(f"  Location: ({vehicle.latitude}, {vehicle.longitude})")
		...     print(f"  Heading: {vehicle.calculatedCourse}°")
		...     print(f"  Passenger load: {vehicle.paxLoad}%")
	"""


	# Initialize & Send Request
	url = BASE_URL+"/mapGetData.php?getBuses="+str(appVersion)
	body = {
		"s0" : str(system.id),
		"sA" : 1
	}
	vehicles = sendApiRequest(url, body)

	# Handle Request Error
	if(vehicles == None):
		return(None)

	allVehicles = []
	for vehicleId, vehicle in vehicles["buses"].items():
		if vehicleId == '-1':
			continue

		vehicle = vehicle[0]

		for key in ["busId", "busName", "busType", "calculatedCourse", "routeId", "route", "color", "created", "latitude", "longitude", "speed", "paxLoad100", "outOfService", "more", "tripId"]:
			if key not in vehicle:
				vehicle[key] = None


		allVehicles.append(Vehicle(
			id = vehicle["busId"],
			name = vehicle["busName"],
			type = vehicle["busType"],
			system = system,
			calculatedCourse = vehicle["calculatedCourse"],
			routeId = vehicle["routeId"],
			routeName = vehicle["route"],
			color = vehicle["color"],
			created = vehicle["created"],
			latitude = vehicle["latitude"],
			longitude = vehicle["longitude"],
			speed = vehicle["speed"],
			paxLoad = vehicle["paxLoad100"],
			outOfService = vehicle["outOfService"],
			more = vehicle["more"],
			tripId = vehicle["tripId"],
		))

	return(allVehicles)


# Attach methods to TransportationSystem class
TransportationSystem.getRoutes = getRoutes
TransportationSystem.getStops = getStops
TransportationSystem.getSystemAlerts = getSystemAlerts
TransportationSystem.getVehicles = getVehicles
