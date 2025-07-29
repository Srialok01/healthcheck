# Website Health Checker API

A comprehensive Python utility that performs health checks on websites, providing detailed information about HTTP status, response times, SSL certificates, and more.

## Features

- **HTTP Status Monitoring**: Check HTTP status codes and response health
- **Response Time Measurement**: Accurate timing of website responses
- **SSL Certificate Validation**: Verify SSL certificates and check expiry dates
- **Redirect Handling**: Optional following of HTTP redirects
- **Bulk Checking**: Support for checking multiple websites at once
- **Summary Statistics**: Generate comprehensive health summaries
- **JSON Output**: Export results in JSON format
- **Command Line Interface**: Easy-to-use CLI for quick checks

## Installation

This utility requires Python 3.6+ and the `requests` library:

```bash
pip install requests
```

## Quick Start

### Basic Usage

```python
from api import HealthCheckerAPI

# Create API instance
api = HealthCheckerAPI()

# Check a single website
result = api.check_website("https://google.com")
print(f"Status: {result['status_code']}")
print(f"Response Time: {result['response_time']:.3f}s")
print(f"SSL Valid: {result['ssl_valid']}")
```

### Check Multiple Websites

```python
websites = [
    "https://google.com",
    "https://github.com", 
    "https://stackoverflow.com"
]

results = api.check_multiple_websites(websites)
summary = api.get_summary(results)

print(f"Healthy sites: {summary['healthy_sites']}/{summary['total_sites']}")
print(f"Average response time: {summary['average_response_time']:.3f}s")
```

### Command Line Usage

```bash
# Check single website
python api.py https://google.com

# Check multiple websites
python api.py https://google.com https://github.com https://stackoverflow.com

# With custom timeout and summary
python api.py https://google.com https://github.com --timeout 15 --summary

# JSON output
python api.py https://google.com --json

# Don't follow redirects
python api.py http://github.com --no-redirects
```

## API Reference

### HealthCheckerAPI Class

#### Methods

##### `check_website(url, timeout=10, follow_redirects=True)`

Check the health of a single website.

**Parameters:**
- `url` (str): Website URL to check
- `timeout` (int): Request timeout in seconds (default: 10)
- `follow_redirects` (bool): Whether to follow redirects (default: True)

**Returns:**
Dictionary containing:
- `url`: Original URL
- `timestamp`: Check timestamp
- `status_code`: HTTP status code
- `status_healthy`: Boolean indicating if site is healthy (2xx or 3xx status)
- `response_time`: Response time in seconds
- `final_url`: Final URL after redirects
- `ssl_checked`: Whether SSL was checked
- `ssl_valid`: SSL certificate validity
- `ssl_expiry`: SSL certificate expiry date
- `ssl_days_until_expiry`: Days until SSL expires
- `error`: Error message if any

##### `check_multiple_websites(urls, timeout=10, follow_redirects=True)`

Check the health of multiple websites.

**Parameters:**
- `urls` (list): List of website URLs to check
- `timeout` (int): Request timeout in seconds (default: 10) 
- `follow_redirects` (bool): Whether to follow redirects (default: True)

**Returns:**
List of health check result dictionaries.

##### `get_summary(results)`

Generate summary statistics from health check results.

**Parameters:**
- `results` (list): List of health check results

**Returns:**
Dictionary containing summary statistics:
- `total_sites`: Total number of sites checked
- `healthy_sites`: Number of healthy sites
- `unhealthy_sites`: Number of unhealthy sites
- `health_percentage`: Percentage of healthy sites
- `average_response_time`: Average response time
- `ssl_sites_checked`: Number of sites with SSL checked
- `ssl_valid_sites`: Number of sites with valid SSL
- `ssl_invalid_sites`: Number of sites with invalid SSL
- `sites_with_errors`: Number of sites with errors
- `fastest_response_time`: Fastest response time
- `slowest_response_time`: Slowest response time

##### `check_website_json(url, timeout=10, follow_redirects=True)`

Check website health and return results as JSON string.

##### `check_multiple_websites_json(urls, timeout=10, follow_redirects=True)`

Check multiple websites and return results as JSON string.

## Examples

### Example 1: Basic Health Check

```python
from api import HealthCheckerAPI

api = HealthCheckerAPI()
result = api.check_website("https://google.com")

print(f"URL: {result['url']}")
print(f"Status: {result['status_code']}")
print(f"Healthy: {result['status_healthy']}")
print(f"Response Time: {result['response_time']:.3f}s")
print(f"SSL Valid: {result['ssl_valid']}")
```

### Example 2: Monitor Multiple Sites

```python
websites = [
    "https://google.com",
    "https://github.com",
    "https://stackoverflow.com",
    "https://httpstat.us/404"  # This will return 404
]

api = HealthCheckerAPI()
results = api.check_multiple_websites(websites, timeout=15)

for result in results:
    status = "✓" if result['status_healthy'] else "✗"
    print(f"{status} {result['url']} - {result['status_code']}")
```

### Example 3: SSL Certificate Monitoring

```python
api = HealthCheckerAPI()
result = api.check_website("https://google.com")

if result['ssl_checked']:
    if result['ssl_valid']:
        days_left = result['ssl_days_until_expiry']
        if days_left < 30:
            print(f"⚠️  SSL certificate expires in {days_left} days!")
        else:
            print(f"✓ SSL certificate valid ({days_left} days remaining)")
    else:
        print("❌ SSL certificate is invalid!")
```

### Example 4: Performance Monitoring

```python
api = HealthCheckerAPI()
results = api.check_multiple_websites([
    "https://google.com",
    "https://github.com",
    "https://stackoverflow.com"
])

summary = api.get_summary(results)

print(f"Average response time: {summary['average_response_time']:.3f}s")
print(f"Fastest site: {summary['fastest_response_time']:.3f}s")
print(f"Slowest site: {summary['slowest_response_time']:.3f}s")
```

## Command Line Interface

The API includes a built-in CLI for quick health checks:

```bash
# Basic usage
python api.py https://google.com

# Multiple sites with summary
python api.py https://google.com https://github.com --summary

# Custom timeout
python api.py https://slow-site.com --timeout 30

# JSON output
python api.py https://google.com --json

# Don't follow redirects
python api.py http://github.com --no-redirects
```

## Error Handling

The API handles various error conditions gracefully:

- **Connection errors**: Network connectivity issues
- **Timeout errors**: Requests that exceed the timeout limit
- **SSL errors**: Invalid or expired SSL certificates
- **HTTP errors**: Non-2xx status codes
- **Redirect errors**: Too many redirects

All errors are captured in the `error` field of the result dictionary.

## Use Cases

- **Website Monitoring**: Regular health checks of production websites
- **SSL Certificate Monitoring**: Track SSL certificate expiry dates
- **Performance Testing**: Measure and compare response times
- **Uptime Monitoring**: Automated checking of website availability
- **Load Balancer Health Checks**: Verify backend server health
- **DevOps Integration**: Include in CI/CD pipelines for deployment verification

## Files

- `api.py`: Main API implementation and CLI
- `health_checker.py`: Core health checking functionality
- `example_usage.py`: Comprehensive usage examples
- `README.md`: This documentation

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this utility.

## License

This project is open source and available under the MIT License.