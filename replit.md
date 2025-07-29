# Website Health Checker

## Overview

This is a Streamlit-based web application that provides comprehensive website health monitoring capabilities. The application allows users to check website status, response times, SSL certificate validity, and other health metrics for single or multiple URLs. It features a clean, user-friendly interface with configurable options for timeout settings and redirect handling.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple two-tier architecture:

**Frontend Layer**: Streamlit web interface that provides user interaction and data visualization
**Backend Layer**: Python-based health checking logic encapsulated in a dedicated class

This architecture was chosen for its simplicity and rapid development capabilities, making it ideal for a focused utility application. The monolithic approach eliminates complexity while providing all necessary functionality.

## Key Components

### 1. Streamlit Frontend (app.py)
- **Purpose**: User interface and application orchestration
- **Features**: 
  - Single URL and bulk URL input methods
  - Configurable timeout and redirect settings
  - Real-time results display
- **Design Choice**: Streamlit was selected for rapid prototyping and built-in web interface capabilities

### 2. Health Checker Module (health_checker.py)
- **Purpose**: Core health checking functionality
- **Capabilities**:
  - HTTP status code verification
  - Response time measurement
  - SSL certificate validation and expiry checking
  - Redirect handling
- **Design Choice**: Separate class-based module for modularity and potential reuse

### 3. Configuration Management
- **Timeout Settings**: Configurable request timeouts (5-30 seconds)
- **Redirect Handling**: Optional redirect following
- **User Agent**: Default user agent to prevent blocking

## Data Flow

1. **Input Collection**: Users provide URLs through either single input or bulk text area
2. **Configuration**: Users set timeout and redirect preferences via sidebar
3. **Health Checking**: URLs are processed through the HealthChecker class
4. **Results Processing**: Health check results are formatted and displayed
5. **Data Presentation**: Results shown in structured format with status indicators

The flow is designed to be synchronous and immediate, providing real-time feedback to users.

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for the user interface
- **Requests**: HTTP library for making web requests and handling responses
- **Pandas**: Data manipulation and presentation (implied from import)

### Standard Library Dependencies
- **ssl**: SSL certificate validation
- **socket**: Network operations
- **urllib.parse**: URL parsing and validation
- **datetime**: Timestamp generation
- **time**: Performance timing measurements

**Rationale**: Minimal external dependencies were chosen to reduce complexity and ensure reliability. The requests library provides robust HTTP handling, while Streamlit offers rapid web UI development.

## Deployment Strategy

The application is designed for simple deployment scenarios:

### Local Development
- Direct Python execution with Streamlit server
- No database or complex infrastructure requirements
- Self-contained application with minimal setup

### Production Considerations
- Can be deployed on any platform supporting Python and Streamlit
- No persistent storage requirements (stateless operation)
- Horizontal scaling possible through load balancing
- Container-friendly architecture

**Design Rationale**: The stateless, self-contained design ensures easy deployment and maintenance while avoiding infrastructure complexity for this utility application.

## Key Architectural Decisions

### 1. Stateless Design
- **Problem**: Need for simple, reliable health checking
- **Solution**: Stateless application with no data persistence
- **Benefits**: Easy deployment, no database management, improved reliability

### 2. Session-based HTTP Handling
- **Problem**: Efficient handling of multiple requests
- **Solution**: Reusable requests session with default headers
- **Benefits**: Connection reuse, consistent headers, better performance

### 3. Modular Health Checking
- **Problem**: Separation of concerns between UI and business logic
- **Solution**: Dedicated HealthChecker class
- **Benefits**: Testability, reusability, clean code organization

### 4. Flexible Input Methods
- **Problem**: Supporting both single and bulk URL checking
- **Solution**: Radio button selection between input methods
- **Benefits**: User flexibility, efficient bulk operations