# Changelog


## 0.2.3 (2025-10-16)

### Fixed

- **CRITICAL**: Fixed latitude/longitude swap bug in `Vehicle` class `__init__()` method
  - Previous versions assigned `latitude` parameter to `self.longitude` attribute
  - Missing assignment for `self.latitude` attribute
  - This caused all vehicle coordinates to be incorrect
  - **Action Required**: If you're using vehicle coordinates from versions 0.2.2 or earlier, you may need to swap them

### Changed

- Reorganized codebase into modular structure:
  - Created `passiogo/models.py` for all data model classes
  - Created `passiogo/client.py` for API communication
  - Updated `passiogo/__init__.py` to export from modules
  - Maintains full backward compatibility
- Improved documentation throughout codebase:
  - Added comprehensive docstrings to all classes and methods
  - Documented coordinate system (latitude: -90 to +90, longitude: -180 to +180)
  - Added type hints with `Optional` for better IDE support

### Added

- Created detailed examples documentation (`docs/examples.md`) with practical use cases:
  - Getting started examples
  - Working with systems, routes, and stops
  - Vehicle tracking examples
  - Service alerts
  - Geographic operations (distance calculations, GeoJSON export)
  - Advanced usage patterns (dashboards, error handling, coordinate validation)
- Created architecture documentation (`docs/ARCHITECTURE.md`):
  - Module structure explanation
  - Data flow diagrams
  - Class hierarchy documentation
  - Coordinate system specification
  - Design decisions and rationale
- Package metadata: Added `__version__` and `__all__` to `__init__.py`


## 0.2.2 (Date Unknown)

### Fixed

- Fixed Getting Systems Bug


## 0.2.1 (2024-08-18)

### Added

- Testing for every transportation system
- `Vehicle` object
- `TransportationSystem.getVehicles()` which returns a list of `Vehicle` objects

### Changed

- Fixed `AttributeError: 'list' object has no attribute 'items'` error thrown in `TransportationSystem.getRoutes()`

### Removed


## 0.2.0 (2024-07-31)

### Added

- `TransportationSystem` class with the following methods: `getRoutes()`, `getStops()`, `getSystemAlerts()`
- `Route` class with the following method: `getStops()`
- `Stop` class
- `getSystems()`
- `getSystemsFromID()`
- `printAllSystemsMd()`

### Changed

### Removed


## 0.1.2 (2024-07-14)

### Added

- Added License

### Changed

- Fixed Documentation Build
- All 
- Fixed PyPi long description type
- `printAllSystemsMd()` has the new parameter `includeHtml` with a default of `True` to render HTML breaks after each line

### Removed

- Removed obsolete `debug` parameters


## 0.1.1 (2024-07-12)

### Added

- Create Documentation With ReadTheDocs.io
- Create Changelog
- New `getSystems()` Method
- New `printAllSystemsMd()` Method
- Added PyPi Project Links

### Changed

- Change Project Description

### Removed

- None


## 0.1.0 (2024-07-12)

- Initial Commit