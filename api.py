#!/usr/bin/env python3
"""
Website Health Checker API

A Python utility that performs comprehensive health checks on websites including:
- HTTP status code verification
- Response time measurement  
- SSL certificate validation and expiry checking
- Redirect handling
- Comprehensive logging to .log files

Usage:
    from api import HealthCheckerAPI
    
    # Create API instance
    api = HealthCheckerAPI()
    
    # Check single website
    result = api.check_website("https://google.com")
    print(result)
    
    # Check multiple websites
    results = api.check_multiple_websites([
        "https://google.com",
        "https://github.com", 
        "https://httpstat.us/404"
    ])
    
    # Get summary statistics
    summary = api.get_summary(results)
    print(summary)
"""

from health_checker import HealthChecker
import json
import logging
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

class HealthCheckerAPI:
    """
    API wrapper for website health checking functionality with logging
    """
    
    def __init__(self, log_file: Optional[str] = None, enable_console_logging: bool = True):
        """
        Initialize the health checker API with logging
        
        Args:
            log_file (str): Path to log file. If None, defaults to 'health_checker_YYYYMMDD.log'
            enable_console_logging (bool): Whether to also log to console (default: True)
        """
        self.health_checker = HealthChecker()
        self.setup_logging(log_file, enable_console_logging)
        
        # Log initialization
        self.logger.info("=" * 60)
        self.logger.info("Health Checker API initialized")
        self.logger.info(f"Timestamp: {datetime.now().isoformat()}")
        self.logger.info("=" * 60)
    
    def setup_logging(self, log_file: Optional[str] = None, enable_console_logging: bool = True):
        """
        Set up logging configuration
        
        Args:
            log_file (str): Path to log file
            enable_console_logging (bool): Whether to also log to console
        """
        # Create logger
        self.logger = logging.getLogger('HealthCheckerAPI')
        self.logger.setLevel(logging.INFO)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Set up file handler
        if log_file is None:
            timestamp = datetime.now().strftime('%Y%m%d')
            log_file = f'health_checker_{timestamp}.log'
        
        self.log_file = log_file
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Set up console handler if enabled
        if enable_console_logging:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        self.logger.info(f"Logging initialized - Log file: {log_file}")
    
    def log_result(self, result: Dict[str, Any], operation: str = "health_check"):
        """
        Log health check result details
        
        Args:
            result (dict): Health check result
            operation (str): Operation type for logging context
        """
        self.logger.info(f"--- {operation.upper()} RESULT ---")
        self.logger.info(f"URL: {result['url']}")
        self.logger.info(f"Status Code: {result.get('status_code', 'N/A')}")
        self.logger.info(f"Healthy: {result['status_healthy']}")
        self.logger.info(f"Response Time: {result.get('response_time', 'N/A')}s")
        self.logger.info(f"Final URL: {result.get('final_url', 'N/A')}")
        
        if result.get('ssl_checked'):
            self.logger.info(f"SSL Valid: {result['ssl_valid']}")
            if result.get('ssl_expiry'):
                self.logger.info(f"SSL Expires: {result['ssl_expiry']}")
                self.logger.info(f"Days Until Expiry: {result.get('ssl_days_until_expiry', 'N/A')}")
        
        if result.get('error'):
            self.logger.error(f"Error: {result['error']}")
        
        self.logger.info("-" * 40)
    
    def check_website(self, url: str, timeout: int = 10, follow_redirects: bool = True) -> Dict[str, Any]:
        """
        Check the health of a single website
        
        Args:
            url (str): Website URL to check
            timeout (int): Request timeout in seconds (default: 10)
            follow_redirects (bool): Whether to follow redirects (default: True)
            
        Returns:
            dict: Health check results containing:
                - url: Original URL
                - timestamp: Check timestamp
                - status_code: HTTP status code
                - status_healthy: Boolean indicating if site is healthy
                - response_time: Response time in seconds
                - final_url: Final URL after redirects
                - ssl_checked: Whether SSL was checked
                - ssl_valid: SSL certificate validity
                - ssl_expiry: SSL certificate expiry date
                - ssl_days_until_expiry: Days until SSL expires
                - error: Error message if any
        """
        self.logger.info(f"Starting health check for URL: {url}")
        self.logger.info(f"Config - Timeout: {timeout}s, Follow Redirects: {follow_redirects}")
        
        if not self._validate_url(url):
            error_result = {
                'url': url,
                'error': 'Invalid URL format',
                'status_healthy': False,
                'timestamp': None,
                'status_code': None,
                'response_time': None,
                'final_url': url,
                'ssl_checked': False,
                'ssl_valid': False,
                'ssl_expiry': None,
                'ssl_days_until_expiry': None
            }
            self.logger.error(f"Invalid URL format: {url}")
            self.log_result(error_result, "validation_error")
            return error_result
        
        result = self.health_checker.check_website_health(url, timeout, follow_redirects)
        self.log_result(result, "single_check")
        return result
    
    def check_multiple_websites(self, urls: List[str], timeout: int = 10, follow_redirects: bool = True) -> List[Dict[str, Any]]:
        """
        Check the health of multiple websites
        
        Args:
            urls (list): List of website URLs to check
            timeout (int): Request timeout in seconds (default: 10)
            follow_redirects (bool): Whether to follow redirects (default: True)
            
        Returns:
            list: List of health check results for each URL
        """
        self.logger.info(f"Starting bulk health check for {len(urls)} URLs")
        self.logger.info(f"URLs to check: {', '.join(urls)}")
        
        results = []
        for i, url in enumerate(urls, 1):
            self.logger.info(f"Checking URL {i}/{len(urls)}: {url}")
            result = self.check_website(url, timeout, follow_redirects)
            results.append(result)
        
        self.logger.info(f"Bulk health check completed for {len(urls)} URLs")
        return results
    
    def get_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary statistics from health check results
        
        Args:
            results (list): List of health check results
            
        Returns:
            dict: Summary statistics including:
                - total_sites: Total number of sites checked
                - healthy_sites: Number of healthy sites
                - unhealthy_sites: Number of unhealthy sites
                - health_percentage: Percentage of healthy sites
                - average_response_time: Average response time
                - ssl_sites_checked: Number of sites with SSL checked
                - ssl_valid_sites: Number of sites with valid SSL
                - ssl_invalid_sites: Number of sites with invalid SSL
                - sites_with_errors: Number of sites with errors
                - fastest_response_time: Fastest response time
                - slowest_response_time: Slowest response time
        """
        self.logger.info("Generating summary statistics")
        summary = self.health_checker.get_health_summary(results)
        
        # Log summary details
        self.logger.info("--- SUMMARY STATISTICS ---")
        self.logger.info(f"Total Sites: {summary.get('total_sites', 0)}")
        self.logger.info(f"Healthy Sites: {summary.get('healthy_sites', 0)}")
        self.logger.info(f"Unhealthy Sites: {summary.get('unhealthy_sites', 0)}")
        self.logger.info(f"Health Percentage: {summary.get('health_percentage', 0):.1f}%")
        self.logger.info(f"Average Response Time: {summary.get('average_response_time', 0):.3f}s")
        self.logger.info(f"SSL Sites Checked: {summary.get('ssl_sites_checked', 0)}")
        self.logger.info(f"Valid SSL Sites: {summary.get('ssl_valid_sites', 0)}")
        self.logger.info(f"Sites with Errors: {summary.get('sites_with_errors', 0)}")
        
        if summary.get('fastest_response_time'):
            self.logger.info(f"Fastest Response: {summary['fastest_response_time']:.3f}s")
        if summary.get('slowest_response_time'):
            self.logger.info(f"Slowest Response: {summary['slowest_response_time']:.3f}s")
        
        self.logger.info("-" * 30)
        return summary
    
    def check_website_json(self, url: str, timeout: int = 10, follow_redirects: bool = True) -> str:
        """
        Check website health and return results as JSON string
        
        Args:
            url (str): Website URL to check
            timeout (int): Request timeout in seconds (default: 10)
            follow_redirects (bool): Whether to follow redirects (default: True)
            
        Returns:
            str: JSON formatted health check results
        """
        result = self.check_website(url, timeout, follow_redirects)
        return json.dumps(result, indent=2)
    
    def check_multiple_websites_json(self, urls: List[str], timeout: int = 10, follow_redirects: bool = True) -> str:
        """
        Check multiple websites and return results as JSON string
        
        Args:
            urls (list): List of website URLs to check
            timeout (int): Request timeout in seconds (default: 10)
            follow_redirects (bool): Whether to follow redirects (default: True)
            
        Returns:
            str: JSON formatted health check results
        """
        results = self.check_multiple_websites(urls, timeout, follow_redirects)
        return json.dumps(results, indent=2)
    
    def _validate_url(self, url: str) -> bool:
        """
        Validate if URL is properly formatted
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if URL is valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

# Command line interface
def main():
    """Command line interface for the health checker API"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Website Health Checker API')
    parser.add_argument('urls', nargs='+', help='Website URLs to check')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout in seconds (default: 10)')
    parser.add_argument('--no-redirects', action='store_true', help='Do not follow redirects')
    parser.add_argument('--summary', action='store_true', help='Show summary statistics')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    parser.add_argument('--log-file', type=str, help='Custom log file path (default: health_checker_YYYYMMDD.log)')
    parser.add_argument('--no-console-log', action='store_true', help='Disable console logging (log only to file)')
    
    args = parser.parse_args()
    
    # Create API instance with logging configuration
    api = HealthCheckerAPI(
        log_file=args.log_file,
        enable_console_logging=not args.no_console_log
    )
    
    # Check websites
    if len(args.urls) == 1:
        result = api.check_website(args.urls[0], args.timeout, not args.no_redirects)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print_single_result(result)
    else:
        results = api.check_multiple_websites(args.urls, args.timeout, not args.no_redirects)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_multiple_results(results)
            
        if args.summary:
            summary = api.get_summary(results)
            print("\n" + "="*50)
            print("SUMMARY STATISTICS")
            print("="*50)
            print_summary(summary)

def print_single_result(result: Dict[str, Any]):
    """Print formatted single result"""
    print(f"\nHealth Check Results for: {result['url']}")
    print("-" * 50)
    print(f"Status Code: {result['status_code'] or 'N/A'}")
    print(f"Healthy: {'✓' if result['status_healthy'] else '✗'}")
    print(f"Response Time: {result['response_time']:.3f}s" if result['response_time'] else "N/A")
    print(f"Final URL: {result['final_url']}")
    
    if result['ssl_checked']:
        print(f"SSL Valid: {'✓' if result['ssl_valid'] else '✗'}")
        if result['ssl_expiry']:
            print(f"SSL Expires: {result['ssl_expiry']}")
            if result['ssl_days_until_expiry'] is not None:
                print(f"Days Until Expiry: {result['ssl_days_until_expiry']}")
    
    if result['error']:
        print(f"Error: {result['error']}")

def print_multiple_results(results: List[Dict[str, Any]]):
    """Print formatted multiple results"""
    print(f"\nHealth Check Results for {len(results)} websites:")
    print("=" * 80)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['url']}")
        print(f"   Status: {result['status_code'] or 'FAILED'} | "
              f"Healthy: {'✓' if result['status_healthy'] else '✗'} | "
              f"Time: {result['response_time']:.3f}s" if result['response_time'] else "Time: N/A")
        
        if result['ssl_checked']:
            ssl_status = '✓' if result['ssl_valid'] else '✗'
            print(f"   SSL: {ssl_status}", end="")
            if result['ssl_days_until_expiry'] is not None:
                print(f" (expires in {result['ssl_days_until_expiry']} days)")
            else:
                print()
        
        if result['error']:
            print(f"   Error: {result['error']}")

def print_summary(summary: Dict[str, Any]):
    """Print formatted summary statistics"""
    print(f"Total Sites: {summary['total_sites']}")
    print(f"Healthy: {summary['healthy_sites']} ({summary['health_percentage']:.1f}%)")
    print(f"Unhealthy: {summary['unhealthy_sites']}")
    print(f"Average Response Time: {summary['average_response_time']:.3f}s")
    
    if summary['ssl_sites_checked'] > 0:
        print(f"SSL Sites Checked: {summary['ssl_sites_checked']}")
        print(f"Valid SSL: {summary['ssl_valid_sites']}")
        print(f"Invalid SSL: {summary['ssl_invalid_sites']}")
    
    print(f"Sites with Errors: {summary['sites_with_errors']}")
    
    if summary['fastest_response_time']:
        print(f"Fastest Response: {summary['fastest_response_time']:.3f}s")
    if summary['slowest_response_time']:
        print(f"Slowest Response: {summary['slowest_response_time']:.3f}s")

if __name__ == "__main__":
    main()