"""
PassioGo Data Models

This module contains all data models for the PassioGo API wrapper.
Includes classes for TransportationSystem, Route, Stop, SystemAlert, and Vehicle.

Coordinate System:
    All geographic coordinates use the standard latitude/longitude format:
    - Latitude: Degrees North/South (-90 to +90)
    - Longitude: Degrees East/West (-180 to +180)

Author: PassioGo Contributors
License: See LICENSE file
"""

from typing import Optional, Dict, List


class TransportationSystem:
	"""
	Represents a Passio Go transportation system (university, municipality, airport, etc.).

	A TransportationSystem is the top-level entity that contains routes, stops, and vehicles.
	Use this class to query information about a specific transit agency.

	Attributes:
		id (int): Unique identifier for the transportation system
		name (str, optional): Full name of the transportation system
		username (str, optional): Username/login for the system
		goAgencyName (str, optional): Agency name in Passio Go system
		email (str, optional): Contact email for the system
		goTestMode (bool, optional): Whether system is in test mode
		name2 (bool, optional): Alternative name flag
		homepage (str, optional): System homepage URL
		logo (bool, optional): Whether system has a logo
		goRoutePlannerEnabled (bool, optional): Whether route planner is enabled
		goColor (str, optional): Primary color for the system (hex code)
		goSupportEmail (str, optional): Support email address
		goSharedCode (int, optional): Shared code for system
		goAuthenticationType (bool, optional): Authentication type flag

	Example:
		>>> system = passiogo.getSystemFromID(1270)
		>>> print(system.name)
		'University of Michigan'
		>>> routes = system.getRoutes()
		>>> vehicles = system.getVehicles()
	"""

	def __init__(
		self,
		id: int,
		name: Optional[str] = None,
		username: Optional[str] = None,
		goAgencyName: Optional[str] = None,
		email: Optional[str] = None,
		goTestMode: Optional[bool] = None,
		name2: Optional[bool] = None,
		homepage: Optional[str] = None,
		logo: Optional[bool] = None,
		goRoutePlannerEnabled: Optional[bool] = None,
		goColor: Optional[str] = None,
		goSupportEmail: Optional[str] = None,
		goSharedCode: Optional[int] = None,
		goAuthenticationType: Optional[bool] = None
	):
		"""
		Initialize a TransportationSystem instance.

		Args:
			id: Unique system identifier (required)
			All other parameters are optional system metadata

		Raises:
			AssertionError: If any parameter type is incorrect
		"""
		self.id = id
		self.name = name
		self.username = username
		self.goAgencyName = goAgencyName
		self.email = email
		self.goTestMode = goTestMode
		self.name2 = name2
		self.homepage = homepage
		self.logo = logo
		self.goRoutePlannerEnabled = goRoutePlannerEnabled
		self.goColor = goColor
		self.goSupportEmail = goSupportEmail
		self.goSharedCode = goSharedCode
		self.goAuthenticationType = goAuthenticationType

		self.checkTypes()

	def checkTypes(self):
		"""
		Validates that all instance attributes have correct types.

		Raises:
			AssertionError: If any attribute has an incorrect type
		"""
		# id : int
		assert type(self.id) == int, f"'id' parameter must be an int not {type(self.id)}"

		# name : str or None
		assert (type(self.name) == str or self.name is None), f"'name' parameter must be a str not {type(self.name)}"

		# username : str or None
		assert (type(self.username) == str or self.username is None), f"'username' parameter must be a str not {type(self.username)}"

		# goAgencyName : str or None
		assert (type(self.goAgencyName) == str or self.goAgencyName is None), f"'goAgencyName' parameter must be a str not {type(self.goAgencyName)}"

		# email : str or None
		assert (type(self.email) == str or self.email is None), f"'email' parameter must be a str not {type(self.email)}"

		# goTestMode : bool or None
		assert (type(self.goTestMode) == bool or self.goTestMode is None), f"'goTestMode' parameter must be a bool not {type(self.goTestMode)}"

		# name2 : bool or None
		assert (type(self.name2) == bool or self.name2 is None), f"'name2' parameter must be a bool not {type(self.name2)}"

		# homepage : str or None
		assert (type(self.homepage) == str or self.homepage is None), f"'homepage' parameter must be a str not {type(self.homepage)}"

		# logo : bool or None
		assert (type(self.logo) == bool or self.logo is None), f"'logo' parameter must be a bool not {type(self.logo)}"

		# goRoutePlannerEnabled : bool or None
		assert (type(self.goRoutePlannerEnabled) == bool or self.goRoutePlannerEnabled is None), f"'goRoutePlannerEnabled' parameter must be a bool not {type(self.goRoutePlannerEnabled)}"

		# goColor : str or None
		assert (type(self.goColor) == str or self.goColor is None), f"'goColor' parameter must be a str not {type(self.goColor)}"

		# goSupportEmail : str or None
		assert (type(self.goSupportEmail) == str or self.goSupportEmail is None), f"'goSupportEmail' parameter must be a str not {type(self.goSupportEmail)}"

		# goSharedCode : int or None
		assert (type(self.goSharedCode) == int or self.goSharedCode is None), f"'goSharedCode' parameter must be a int not {type(self.goSharedCode)}"

		# goAuthenticationType : bool or None
		assert (type(self.goAuthenticationType) == bool or self.goAuthenticationType is None), f"'goAuthenticationType' parameter must be a bool not {type(self.goAuthenticationType)}"


class Route:
	"""
	Represents a transit route within a transportation system.

	A Route is a defined path that vehicles follow, connecting multiple stops.
	Routes have schedules, colors, and service times.

	Attributes:
		id (int): Unique route identifier
		groupId (int, optional): Group identifier for route grouping
		groupColor (str, optional): Color for the route group (hex code)
		name (str, optional): Route name
		shortName (str, optional): Abbreviated route name
		nameOrig (str, optional): Original route name
		fullname (str, optional): Full route name
		myid (int, optional): Alternative route ID
		mapApp (bool, optional): Whether route appears in map app
		archive (bool, optional): Whether route is archived
		goPrefixRouteName (bool, optional): Whether to prefix route name
		goShowSchedule (bool, optional): Whether to show schedule
		outdated (bool, optional): Whether route data is outdated
		distance (int, optional): Route distance in meters
		latitude (float, optional): Route center latitude (-90 to +90)
		longitude (float, optional): Route center longitude (-180 to +180)
		timezone (str, optional): Timezone for route (e.g., "America/New_York")
		serviceTime (str, optional): Service time description
		serviceTimeShort (str, optional): Abbreviated service time
		systemId (int, optional): ID of parent transportation system
		system (TransportationSystem, optional): Parent system object reference

	Example:
		>>> routes = system.getRoutes()
		>>> for route in routes:
		...     print(f"{route.name}: {route.latitude}, {route.longitude}")
		...     stops = route.getStops()
	"""

	def __init__(
		self,
		id: int,
		groupId: Optional[int] = None,
		groupColor: Optional[str] = None,
		name: Optional[str] = None,
		shortName: Optional[str] = None,
		nameOrig: Optional[str] = None,
		fullname: Optional[str] = None,
		myid: Optional[int] = None,
		mapApp: Optional[bool] = None,
		archive: Optional[bool] = None,
		goPrefixRouteName: Optional[bool] = None,
		goShowSchedule: Optional[bool] = None,
		outdated: Optional[bool] = None,
		distance: Optional[int] = None,
		latitude: Optional[float] = None,
		longitude: Optional[float] = None,
		timezone: Optional[str] = None,
		serviceTime: Optional[str] = None,
		serviceTimeShort: Optional[str] = None,
		systemId: Optional[int] = None,
		system: Optional["TransportationSystem"] = None,
	):
		"""
		Initialize a Route instance.

		Args:
			id: Unique route identifier (required)
			latitude: Route center latitude in degrees (-90 to +90)
			longitude: Route center longitude in degrees (-180 to +180)
			All other parameters are optional route metadata
		"""
		self.id = id
		self.groupId = groupId
		self.groupColor = groupColor
		self.name = name
		self.shortName = shortName
		self.nameOrig = nameOrig
		self.fullname = fullname
		self.myid = myid
		self.mapApp = mapApp
		self.archive = archive
		self.goPrefixRouteName = goPrefixRouteName
		self.goShowSchedule = goShowSchedule
		self.outdated = outdated
		self.distance = distance
		self.latitude = latitude
		self.longitude = longitude
		self.serviceTime = serviceTime
		self.serviceTimeShort = serviceTimeShort
		self.systemId = systemId
		self.system = system


	def getStops(self) -> List["Stop"]:
		"""
		Gets all stops served by this route.

		Returns:
			List of Stop objects that this route visits

		Example:
			>>> route = routes[0]
			>>> stops = route.getStops()
			>>> print(f"Route {route.name} has {len(stops)} stops")
		"""
		stopsForRoute = []
		allStops = self.system.getStops()

		for stop in allStops:
			if \
				self.myid in list(stop.routesAndPositions.keys()) or \
				self.id in list(stop.routesAndPositions.keys()) or \
				self.groupId in list(stop.routesAndPositions.keys()):
				stopsForRoute.append(stop)

		return(stopsForRoute)


class Stop:
	"""
	Represents a transit stop/station within a transportation system.

	A Stop is a physical location where vehicles pick up and drop off passengers.
	Stops can be served by multiple routes.

	Attributes:
		id (str): Unique stop identifier
		routesAndPositions (dict): Mapping of route IDs to positions on each route
		                           Format: {routeId: [position1, position2, ...]}
		systemId (int, optional): ID of parent transportation system
		name (str, optional): Stop name/description
		latitude (float, optional): Stop latitude in degrees (-90 to +90)
		longitude (float, optional): Stop longitude in degrees (-180 to +180)
		radius (int, optional): Stop coverage radius in meters
		system (TransportationSystem, optional): Parent system object reference

	Example:
		>>> stops = system.getStops()
		>>> for stop in stops:
		...     print(f"{stop.name}: {stop.latitude}, {stop.longitude}")
		...     print(f"Served by routes: {list(stop.routesAndPositions.keys())}")
	"""

	def __init__(
		self,
		id: str,
		routesAndPositions: Optional[Dict[str, List[int]]] = None,
		systemId: Optional[int] = None,
		name: Optional[str] = None,
		latitude: Optional[float] = None,
		longitude: Optional[float] = None,
		radius: Optional[int] = None,
		system: Optional[TransportationSystem] = None,
	):
		"""
		Initialize a Stop instance.

		Args:
			id: Unique stop identifier (required)
			latitude: Stop latitude in degrees (-90 to +90)
			longitude: Stop longitude in degrees (-180 to +180)
			routesAndPositions: Dictionary mapping route IDs to positions
			All other parameters are optional stop metadata
		"""
		if routesAndPositions is None:
			routesAndPositions = {}

		self.id = id
		self.routesAndPositions = routesAndPositions
		self.systemId = systemId
		self.name = name
		self.latitude = latitude
		self.longitude = longitude
		self.radius = radius
		self.system = system


class SystemAlert:
	"""
	Represents a service alert or notification for a transportation system.

	SystemAlerts notify riders of service changes, delays, route closures,
	or other important information. Supports GTFS real-time alert format.

	Attributes:
		id (int): Unique alert identifier
		systemId (int, optional): ID of affected transportation system
		system (TransportationSystem, optional): System object reference
		routeId (int, optional): ID of affected route (if route-specific)
		name (str, optional): Alert title/name
		html (str, optional): Alert content in HTML format
		archive (bool, optional): Whether alert is archived
		important (bool, optional): Whether alert is marked as important
		dateTimeCreated (str, optional): Alert creation timestamp
		dateTimeFrom (str, optional): Alert effective start time
		dateTimeTo (str, optional): Alert effective end time
		asPush (bool, optional): Whether alert was pushed as notification
		gtfs (bool, optional): Whether alert is GTFS-formatted
		gtfsAlertCauseId (int, optional): GTFS alert cause code
		gtfsAlertEffectId (int, optional): GTFS alert effect code
		gtfsAlertUrl (str, optional): URL with more information
		gtfsAlertHeaderText (str, optional): GTFS alert header
		gtfsAlertDescriptionText (str, optional): GTFS alert description
		routeGroupId (int, optional): Affected route group ID
		createdUtc (str, optional): Creation time in UTC
		authorId (int, optional): Alert author ID
		author (str, optional): Alert author name
		updated (str, optional): Last update timestamp
		updateAuthorId (int, optional): Last updater ID
		updateAuthor (str, optional): Last updater name
		createdF (str, optional): Formatted creation time
		fromF (str, optional): Formatted start time
		fromOk (bool, optional): Whether start time is valid
		toOk (bool, optional): Whether end time is valid

	Example:
		>>> alerts = system.getSystemAlerts()
		>>> for alert in alerts:
		...     print(f"{alert.name}: {alert.html}")
		...     print(f"Active from {alert.dateTimeFrom} to {alert.dateTimeTo}")
	"""

	def __init__(
		self,
		id: int,
		systemId: Optional[int] = None,
		system: Optional[TransportationSystem] = None,
		routeId: Optional[int] = None,
		name: Optional[str] = None,
		html: Optional[str] = None,
		archive: Optional[bool] = None,
		important: Optional[bool] = None,
		dateTimeCreated: Optional[str] = None,
		dateTimeFrom: Optional[str] = None,
		dateTimeTo: Optional[str] = None,
		asPush: Optional[bool] = None,
		gtfs: Optional[bool] = None,
		gtfsAlertCauseId: Optional[int] = None,
		gtfsAlertEffectId: Optional[int] = None,
		gtfsAlertUrl: Optional[str] = None,
		gtfsAlertHeaderText: Optional[str] = None,
		gtfsAlertDescriptionText: Optional[str] = None,
		routeGroupId: Optional[int] = None,
		createdUtc: Optional[str] = None,
		authorId: Optional[int] = None,
		author: Optional[str] = None,
		updated: Optional[str] = None,
		updateAuthorId: Optional[int] = None,
		updateAuthor: Optional[str] = None,
		createdF: Optional[str] = None,
		fromF: Optional[str] = None,
		fromOk: Optional[bool] = None,
		toOk: Optional[bool] = None,
	):
		"""
		Initialize a SystemAlert instance.

		Args:
			id: Unique alert identifier (required)
			All other parameters are optional alert metadata
		"""
		self.id = id
		self.systemId = systemId
		self.system = system
		self.routeId = routeId
		self.name = name
		self.html = html
		self.archive = archive
		self.important = important
		self.dateTimeCreated = dateTimeCreated
		self.dateTimeFrom = dateTimeFrom
		self.dateTimeTo = dateTimeTo
		self.asPush = asPush
		self.gtfs = gtfs
		self.gtfsAlertCauseId = gtfsAlertCauseId
		self.gtfsAlertEffectId = gtfsAlertEffectId
		self.gtfsAlertUrl = gtfsAlertUrl
		self.gtfsAlertHeaderText = gtfsAlertHeaderText
		self.gtfsAlertDescriptionText = gtfsAlertDescriptionText
		self.routeGroupId = routeGroupId
		self.createdUtc = createdUtc
		self.authorId = authorId
		self.author = author
		self.updated = updated
		self.updateAuthorId = updateAuthorId
		self.updateAuthor = updateAuthor
		self.createdF = createdF
		self.fromF = fromF
		self.fromOk = fromOk
		self.toOk = toOk


class Vehicle:
	"""
	Represents a transit vehicle (bus, shuttle, etc.) in a transportation system.

	Vehicles have real-time location data, route assignments, and operational status.
	This is the primary class for tracking live vehicle positions.

	Attributes:
		id (str, optional): Unique vehicle identifier
		name (str, optional): Vehicle name/number
		type (str, optional): Vehicle type (e.g., "bus", "shuttle")
		system (TransportationSystem, optional): Parent system object reference
		calculatedCourse (int, optional): Vehicle heading in degrees (0-359)
		routeId (str, optional): ID of route vehicle is currently serving
		routeName (str, optional): Name of route vehicle is currently serving
		color (str, optional): Route color (hex code)
		created (str, optional): Timestamp when vehicle data was created
		latitude (float, optional): Current vehicle latitude in degrees (-90 to +90)
		longitude (float, optional): Current vehicle longitude in degrees (-180 to +180)
		speed (float, optional): Current vehicle speed
		paxLoad (float, optional): Passenger load percentage (0-100)
		outOfService (bool, optional): Whether vehicle is out of service
		more (str, optional): Additional vehicle information
		tripId (str, optional): Current trip identifier

	Note:
		The latitude and longitude fields represent the vehicle's real-time position.
		These coordinates follow the standard geographic coordinate system:
		- Latitude: North/South position (-90° to +90°)
		- Longitude: East/West position (-180° to +180°)

	Example:
		>>> vehicles = system.getVehicles()
		>>> for vehicle in vehicles:
		...     print(f"Vehicle {vehicle.name} on route {vehicle.routeName}")
		...     print(f"Location: {vehicle.latitude}, {vehicle.longitude}")
		...     print(f"Speed: {vehicle.speed}, Load: {vehicle.paxLoad}%")
	"""

	def __init__(
		self,
		id: Optional[str] = None,
		name: Optional[str] = None,
		type: Optional[str] = None,
		system: Optional[TransportationSystem] = None,
		calculatedCourse: Optional[int] = None,
		routeId: Optional[str] = None,
		routeName: Optional[str] = None,
		color: Optional[str] = None,
		created: Optional[str] = None,
		latitude: Optional[float] = None,
		longitude: Optional[float] = None,
		speed: Optional[float] = None,
		paxLoad: Optional[float] = None,
		outOfService: Optional[bool] = None,
		more: Optional[str] = None,
		tripId: Optional[str] = None,
	):
		"""
		Initialize a Vehicle instance.

		Args:
			id: Unique vehicle identifier
			latitude: Current vehicle latitude in degrees (-90 to +90)
			longitude: Current vehicle longitude in degrees (-180 to +180)
			calculatedCourse: Vehicle heading in degrees (0-359)
			paxLoad: Passenger load percentage (0-100)
			All other parameters are optional vehicle metadata

		Note:
			Previous versions of this library had a bug where latitude and longitude
			were swapped. This has been fixed in version 0.2.3+.
		"""
		self.id = id
		self.name = name
		self.type = type
		self.system = system
		self.calculatedCourse = calculatedCourse
		self.routeId = routeId
		self.routeName = routeName
		self.color = color
		self.created = created
		self.latitude = latitude
		self.longitude = longitude
		self.speed = speed
		self.paxLoad = paxLoad
		self.outOfService = outOfService
		self.more = more
		self.tripId = tripId
