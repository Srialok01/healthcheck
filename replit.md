# Website Health Checker API

## Overview

This project has been transformed from a Streamlit web application into a comprehensive Python API utility for website health monitoring. The API provides programmatic access to health checking capabilities including HTTP status verification, response time measurement, SSL certificate validation, and redirect handling. It supports both single and bulk URL checking with detailed reporting and summary statistics.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a clean API-first architecture:

**API Layer**: Python API wrapper (HealthCheckerAPI) that provides programmatic access to health checking functionality
**Core Layer**: Health checking logic encapsulated in the HealthChecker class with comprehensive error handling
**CLI Layer**: Command-line interface for direct usage and testing

This architecture was redesigned to eliminate web dependencies and focus on programmatic access, making it ideal for integration into monitoring systems, CI/CD pipelines, and other automation tools.

## Key Components

### 1. API Wrapper (api.py)
- **Purpose**: Main API interface and command-line tool
- **Features**: 
  - Single and multiple URL health checking
  - JSON output support
  - Command-line interface with configurable options
  - URL validation and error handling
- **Design Choice**: API-first approach enables integration with various systems and automation tools

### 2. Health Checker Module (health_checker.py)
- **Purpose**: Core health checking functionality
- **Capabilities**:
  - HTTP status code verification with comprehensive error handling
  - Precise response time measurement
  - SSL certificate validation and expiry date calculation
  - Configurable redirect handling
  - Summary statistics generation
- **Design Choice**: Enhanced with better error handling and type safety for robust API usage

### 3. Example Usage (example_usage.py)
- **Purpose**: Comprehensive examples demonstrating API usage
- **Capabilities**:
  - Single and multiple website checking examples
  - JSON output demonstrations
  - Custom configuration examples
  - Summary statistics usage
- **Design Choice**: Provides clear usage patterns for developers integrating the API

## Data Flow

1. **API Input**: URLs provided via Python method calls or command-line arguments
2. **URL Validation**: Input URLs validated for proper format before processing
3. **Health Checking**: URLs processed through HealthChecker class with configurable options
4. **Results Processing**: Comprehensive health check data collected including SSL information
5. **Output Generation**: Results returned as Python dictionaries or JSON strings
6. **Summary Statistics**: Optional aggregated statistics calculated from multiple results

The flow is designed for programmatic integration while maintaining synchronous operation for immediate feedback.

## External Dependencies

### Core Libraries
- **Requests**: HTTP library for making web requests and handling responses
- **JSON**: Built-in library for JSON serialization and output formatting

### Standard Library Dependencies
- **ssl**: SSL certificate validation
- **socket**: Network operations
- **urllib.parse**: URL parsing and validation
- **datetime**: Timestamp generation
- **time**: Performance timing measurements

**Rationale**: Minimal external dependencies were chosen to reduce complexity and ensure reliability. The requests library provides robust HTTP handling, while standard library modules handle data processing and CLI functionality.

## Deployment Strategy

The application is designed for simple deployment scenarios:

### Local Development
- Direct Python execution as API or CLI tool
- No database or complex infrastructure requirements
- Self-contained utility with minimal setup

### Production Considerations
- Can be integrated into any Python-based system
- No persistent storage requirements (stateless operation)
- Suitable for monitoring systems, CI/CD pipelines, and automation tools
- Container-friendly and serverless-compatible architecture

**Design Rationale**: The API-first, stateless design ensures easy integration and maintenance while providing maximum flexibility for different use cases and deployment scenarios.

## Key Architectural Decisions

### 1. API-First Architecture
- **Problem**: Need for programmatic access to health checking functionality
- **Solution**: Clean API wrapper with CLI support
- **Benefits**: Easy integration, automation-friendly, multiple interface options

### 2. Enhanced Error Handling
- **Problem**: Robust handling of network and SSL errors
- **Solution**: Comprehensive exception handling with detailed error messages
- **Benefits**: Reliable operation, clear debugging information, graceful degradation

### 3. Modular Design
- **Problem**: Separation of concerns between API interface and core functionality
- **Solution**: Dedicated HealthChecker class with API wrapper
- **Benefits**: Testability, reusability, clean code organization

### 4. Flexible Output Formats
- **Problem**: Supporting different integration requirements
- **Solution**: Python dictionaries, JSON strings, and formatted CLI output
- **Benefits**: Multiple integration options, easy data processing, human-readable results

### 5. Type Safety and Validation
- **Problem**: Handling various SSL certificate formats and edge cases
- **Solution**: Enhanced type checking and null safety in SSL validation
- **Benefits**: Improved reliability, better error handling, fewer runtime issues

## Recent Changes (July 29, 2025)

✓ Transformed from Streamlit web application to Python API utility
✓ Created comprehensive API wrapper (api.py) with CLI support
✓ Enhanced error handling and type safety in SSL certificate validation
✓ Added example usage file with comprehensive demonstrations
✓ Implemented JSON output capabilities for easy integration
✓ Created detailed README documentation with usage examples
✓ Removed web interface dependencies for cleaner deployment