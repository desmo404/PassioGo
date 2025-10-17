
# Examples

This page provides practical examples of how to use the PassioGo API wrapper.

## Table of Contents

- [Getting Started](#getting-started)
- [Working with Systems](#working-with-systems)
- [Routes and Stops](#routes-and-stops)
- [Vehicle Tracking](#vehicle-tracking)
- [Service Alerts](#service-alerts)
- [Geographic Operations](#geographic-operations)
- [Advanced Usage](#advanced-usage)

---

## Getting Started

### Installation

```bash
pip install passiogo
```

### Basic Import

```python
import passiogo

# Get all available transportation systems
systems = passiogo.getSystems()
print(f"Found {len(systems)} transit systems")
```

---

## Working with Systems

### List All Available Systems

```python
import passiogo

# Get all systems
systems = passiogo.getSystems()

# Print system names and IDs
for system in systems[:10]:  # First 10 systems
    print(f"{system.name} (ID: {system.id})")
```

Output:
```
University of Michigan (ID: 1270)
University of Wisconsin-Madison (ID: 567)
...
```

### Get a Specific System by ID

```python
import passiogo

# Get University of Michigan transit system
umich = passiogo.getSystemFromID(1270)

print(f"System Name: {umich.name}")
print(f"System ID: {umich.id}")
print(f"Homepage: {umich.homepage}")
print(f"Support Email: {umich.goSupportEmail}")
```

### Search for Systems by Name

```python
import passiogo

# Find systems matching a search term
search_term = "University"
systems = passiogo.getSystems()

matching_systems = [s for s in systems if search_term.lower() in s.name.lower()]

for system in matching_systems[:5]:
    print(f"{system.name} (ID: {system.id})")
```

---

## Routes and Stops

### Get All Routes for a System

```python
import passiogo

# Get a transportation system
system = passiogo.getSystemFromID(1270)

# Get all routes
routes = system.getRoutes()

print(f"Found {len(routes)} routes")

# Print route details
for route in routes:
    print(f"\nRoute: {route.name}")
    print(f"  ID: {route.id}")
    print(f"  Short Name: {route.shortName}")
    print(f"  Color: {route.groupColor}")
    print(f"  Service Time: {route.serviceTimeShort}")
```

### Get All Stops for a System

```python
import passiogo

system = passiogo.getSystemFromID(1270)
stops = system.getStops()

print(f"Found {len(stops)} stops")

# Print stop details
for stop in stops[:10]:  # First 10 stops
    print(f"\nStop: {stop.name}")
    print(f"  ID: {stop.id}")
    print(f"  Location: ({stop.latitude}, {stop.longitude})")
    print(f"  Served by {len(stop.routesAndPositions)} routes")
```

### Get Stops for a Specific Route

```python
import passiogo

system = passiogo.getSystemFromID(1270)
routes = system.getRoutes()

# Get first route
route = routes[0]
stops = route.getStops()

print(f"Route '{route.name}' has {len(stops)} stops:")

for i, stop in enumerate(stops, 1):
    print(f"{i}. {stop.name} - ({stop.latitude}, {stop.longitude})")
```

### Find Routes Serving a Specific Stop

```python
import passiogo

system = passiogo.getSystemFromID(1270)
stops = system.getStops()

# Get first stop
stop = stops[0]

print(f"Stop: {stop.name}")
print(f"Served by routes:")

for route_id in stop.routesAndPositions.keys():
    print(f"  Route ID: {route_id}")
```

---

## Vehicle Tracking

### Get All Active Vehicles

```python
import passiogo

system = passiogo.getSystemFromID(1270)
vehicles = system.getVehicles()

print(f"Found {len(vehicles)} active vehicles")

for vehicle in vehicles:
    print(f"\nVehicle: {vehicle.name}")
    print(f"  Route: {vehicle.routeName}")
    print(f"  Location: ({vehicle.latitude}, {vehicle.longitude})")
    print(f"  Heading: {vehicle.calculatedCourse}°")
    print(f"  Speed: {vehicle.speed}")
    print(f"  Passenger Load: {vehicle.paxLoad}%")
    print(f"  In Service: {not vehicle.outOfService}")
```

### Track Vehicles on a Specific Route

```python
import passiogo

system = passiogo.getSystemFromID(1270)
vehicles = system.getVehicles()
routes = system.getRoutes()

# Get a specific route (e.g., first route)
target_route = routes[0]

# Filter vehicles on this route
route_vehicles = [v for v in vehicles if v.routeId == str(target_route.id)]

print(f"Route: {target_route.name}")
print(f"Active vehicles: {len(route_vehicles)}")

for vehicle in route_vehicles:
    print(f"\n  {vehicle.name}")
    print(f"    Position: ({vehicle.latitude}, {vehicle.longitude})")
    print(f"    Load: {vehicle.paxLoad}%")
```

### Real-Time Vehicle Monitoring Loop

```python
import passiogo
import time

system = passiogo.getSystemFromID(1270)

# Monitor vehicles every 30 seconds
while True:
    vehicles = system.getVehicles()

    print(f"\n=== Update at {time.strftime('%H:%M:%S')} ===")
    print(f"Active vehicles: {len(vehicles)}")

    for vehicle in vehicles:
        print(f"{vehicle.name} on {vehicle.routeName}: ({vehicle.latitude}, {vehicle.longitude})")

    time.sleep(30)  # Wait 30 seconds before next update
```

---

## Service Alerts

### Get All Active Alerts

```python
import passiogo

system = passiogo.getSystemFromID(1270)
alerts = system.getSystemAlerts()

print(f"Found {len(alerts)} active alerts")

for alert in alerts:
    print(f"\n{'='*60}")
    print(f"Alert: {alert.name}")
    print(f"Important: {'Yes' if alert.important else 'No'}")
    print(f"Active: {alert.dateTimeFrom} to {alert.dateTimeTo}")
    print(f"\n{alert.html}")
```

### Filter Important Alerts

```python
import passiogo

system = passiogo.getSystemFromID(1270)
alerts = system.getSystemAlerts()

important_alerts = [a for a in alerts if a.important]

print(f"Found {len(important_alerts)} important alerts:")

for alert in important_alerts:
    print(f"\n{alert.name}")
    print(f"  {alert.gtfsAlertDescriptionText or alert.html}")
```

---

## Geographic Operations

### Calculate Distance Between Stop and Vehicle

```python
import passiogo
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points
    on Earth using the Haversine formula.

    Returns distance in meters.
    """
    R = 6371000  # Earth radius in meters

    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c

# Get system data
system = passiogo.getSystemFromID(1270)
vehicles = system.getVehicles()
stops = system.getStops()

# Find closest vehicle to first stop
target_stop = stops[0]

print(f"Finding vehicles near: {target_stop.name}")
print(f"Stop location: ({target_stop.latitude}, {target_stop.longitude})")

distances = []
for vehicle in vehicles:
    if vehicle.latitude and vehicle.longitude:
        dist = haversine_distance(
            target_stop.latitude, target_stop.longitude,
            vehicle.latitude, vehicle.longitude
        )
        distances.append((vehicle, dist))

# Sort by distance
distances.sort(key=lambda x: x[1])

# Show closest 5 vehicles
print(f"\nClosest vehicles:")
for vehicle, dist in distances[:5]:
    print(f"  {vehicle.name} on {vehicle.routeName}: {dist:.0f}m away")
```

### Find Stops Within a Geographic Area

```python
import passiogo

# Define bounding box (latitude/longitude range)
min_lat, max_lat = 42.27, 42.30
min_lon, max_lon = -83.75, -83.73

system = passiogo.getSystemFromID(1270)
stops = system.getStops()

# Filter stops within bounding box
nearby_stops = [
    s for s in stops
    if s.latitude and s.longitude
    and min_lat <= s.latitude <= max_lat
    and min_lon <= s.longitude <= max_lon
]

print(f"Found {len(nearby_stops)} stops in area:")
for stop in nearby_stops:
    print(f"  {stop.name}: ({stop.latitude}, {stop.longitude})")
```

### Export Route to GeoJSON

```python
import passiogo
import json

system = passiogo.getSystemFromID(1270)
routes = system.getRoutes()
route = routes[0]
stops = route.getStops()

# Create GeoJSON feature collection
geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Add stops as point features
for stop in stops:
    if stop.latitude and stop.longitude:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [stop.longitude, stop.latitude]  # GeoJSON uses [lon, lat]
            },
            "properties": {
                "name": stop.name,
                "id": stop.id,
                "route": route.name
            }
        }
        geojson["features"].append(feature)

# Save to file
with open(f"route_{route.id}.geojson", "w") as f:
    json.dump(geojson, f, indent=2)

print(f"Exported {len(geojson['features'])} stops to GeoJSON")
```

---

## Advanced Usage

### Compare Multiple Transit Systems

```python
import passiogo

# Compare several university transit systems
system_ids = [1270, 567, 123]  # Example IDs

for sys_id in system_ids:
    system = passiogo.getSystemFromID(sys_id)
    if system:
        routes = system.getRoutes()
        vehicles = system.getVehicles()
        stops = system.getStops()

        print(f"\n{system.name}:")
        print(f"  Routes: {len(routes)}")
        print(f"  Stops: {len(stops)}")
        print(f"  Active Vehicles: {len(vehicles)}")
```

### Build a Simple Dashboard

```python
import passiogo
import time
from datetime import datetime

def print_dashboard(system_id):
    """Print a simple real-time dashboard for a transit system."""
    system = passiogo.getSystemFromID(system_id)

    while True:
        # Clear screen (platform-specific)
        print("\033[2J\033[H")  # ANSI escape codes

        # Header
        print("="*70)
        print(f"{system.name} - Live Dashboard".center(70))
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(70))
        print("="*70)

        # Get data
        vehicles = system.getVehicles()
        alerts = system.getSystemAlerts()

        # Vehicles by route
        print("\nACTIVE VEHICLES BY ROUTE:")
        print("-"*70)

        route_counts = {}
        for v in vehicles:
            route_counts[v.routeName] = route_counts.get(v.routeName, 0) + 1

        for route, count in sorted(route_counts.items()):
            print(f"  {route}: {count} vehicle(s)")

        # Alerts
        if alerts:
            print(f"\nACTIVE ALERTS ({len(alerts)}):")
            print("-"*70)
            for alert in alerts[:5]:  # Show max 5
                important = " [IMPORTANT]" if alert.important else ""
                print(f"  • {alert.name}{important}")

        print("\n" + "="*70)
        print("Refreshing in 30 seconds... (Ctrl+C to exit)")

        time.sleep(30)

# Run dashboard
print_dashboard(1270)
```

### Error Handling

```python
import passiogo

def get_system_safely(system_id):
    """Safely get a system with error handling."""
    try:
        system = passiogo.getSystemFromID(system_id)
        if system is None:
            print(f"System ID {system_id} not found")
            return None
        return system
    except Exception as e:
        print(f"Error getting system: {e}")
        return None

def get_vehicles_with_retry(system, max_retries=3):
    """Get vehicles with retry logic."""
    for attempt in range(max_retries):
        try:
            vehicles = system.getVehicles()
            return vehicles
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retry
            else:
                print("Max retries reached")
                return []

# Usage
system = get_system_safely(1270)
if system:
    vehicles = get_vehicles_with_retry(system)
    print(f"Retrieved {len(vehicles)} vehicles")
```

### Coordinate Validation

```python
import passiogo

def is_valid_coordinate(lat, lon):
    """
    Validate geographic coordinates.

    Args:
        lat: Latitude (-90 to +90)
        lon: Longitude (-180 to +180)

    Returns:
        bool: True if coordinates are valid
    """
    return (
        lat is not None and
        lon is not None and
        -90 <= lat <= 90 and
        -180 <= lon <= 180
    )

# Check vehicle coordinates
system = passiogo.getSystemFromID(1270)
vehicles = system.getVehicles()

valid_vehicles = [
    v for v in vehicles
    if is_valid_coordinate(v.latitude, v.longitude)
]

print(f"Total vehicles: {len(vehicles)}")
print(f"Vehicles with valid coordinates: {len(valid_vehicles)}")
print(f"Invalid: {len(vehicles) - len(valid_vehicles)}")
```

---

## Notes

### Coordinate System

All geographic coordinates in PassioGo use the standard latitude/longitude format:

- **Latitude**: Degrees North/South (-90 to +90)
- **Longitude**: Degrees East/West (-180 to +180)

Example valid coordinates:
- University of Michigan: (42.278, -83.738)
- New York City: (40.7128, -74.0060)
- London: (51.5074, -0.1278)

### API Rate Limiting

While the Passio Go API doesn't have documented rate limits, it's good practice to:

- Cache results when possible
- Avoid polling more frequently than every 15-30 seconds
- Implement exponential backoff for retries
- Handle errors gracefully

### Data Freshness

- **Vehicle data**: Updated in real-time, typically every 15-30 seconds
- **Routes/Stops**: Generally static, can be cached for hours/days
- **Alerts**: Check every few minutes for important updates

### Need Help?

- [API Reference](api.md)
- [GitHub Issues](https://github.com/athuler/PassioGo/issues)
- [Main Documentation](index.md)
