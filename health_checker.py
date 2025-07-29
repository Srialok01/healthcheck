import requests
import ssl
import socket
from datetime import datetime, timezone
from urllib.parse import urlparse
import time

class HealthChecker:
    """Website health checker class that performs comprehensive health checks"""
    
    def __init__(self):
        self.session = requests.Session()
        # Set a default user agent to avoid blocking
        self.session.headers.update({
            'User-Agent': 'Website Health Checker 1.0'
        })
    
    def check_website_health(self, url, timeout=10, follow_redirects=True):
        """
        Perform comprehensive health check on a website
        
        Args:
            url (str): Website URL to check
            timeout (int): Request timeout in seconds
            follow_redirects (bool): Whether to follow redirects
            
        Returns:
            dict: Health check results
        """
        result = {
            'url': url,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status_code': None,
            'status_healthy': False,
            'response_time': None,
            'final_url': url,
            'ssl_checked': False,
            'ssl_valid': False,
            'ssl_expiry': None,
            'ssl_days_until_expiry': None,
            'error': None
        }
        
        try:
            # Start timing
            start_time = time.time()
            
            # Make HTTP request
            response = self.session.get(
                url,
                timeout=timeout,
                allow_redirects=follow_redirects,
                verify=True  # Verify SSL certificates
            )
            
            # Calculate response time
            end_time = time.time()
            result['response_time'] = end_time - start_time
            
            # Record status code and final URL
            result['status_code'] = response.status_code
            result['final_url'] = response.url
            
            # Check if status is healthy (2xx or 3xx)
            result['status_healthy'] = 200 <= response.status_code < 400
            
            # Check SSL certificate if HTTPS
            parsed_url = urlparse(result['final_url'])
            if parsed_url.scheme == 'https':
                ssl_info = self._check_ssl_certificate(parsed_url.hostname, parsed_url.port or 443)
                result.update(ssl_info)
            
        except requests.exceptions.SSLError as e:
            result['error'] = f"SSL Error: {str(e)}"
            result['ssl_checked'] = True
            result['ssl_valid'] = False
            
        except requests.exceptions.ConnectionError as e:
            result['error'] = f"Connection Error: {str(e)}"
            
        except requests.exceptions.Timeout as e:
            result['error'] = f"Timeout Error: Request took longer than {timeout} seconds"
            
        except requests.exceptions.TooManyRedirects as e:
            result['error'] = "Too Many Redirects: The request exceeded the maximum number of redirects"
            
        except requests.exceptions.RequestException as e:
            result['error'] = f"Request Error: {str(e)}"
            
        except Exception as e:
            result['error'] = f"Unexpected Error: {str(e)}"
        
        return result
    
    def _check_ssl_certificate(self, hostname, port=443):
        """
        Check SSL certificate validity and expiration
        
        Args:
            hostname (str): Hostname to check
            port (int): Port number (default 443)
            
        Returns:
            dict: SSL certificate information
        """
        ssl_result = {
            'ssl_checked': True,
            'ssl_valid': False,
            'ssl_expiry': None,
            'ssl_days_until_expiry': None
        }
        
        try:
            # Create SSL context
            context = ssl.create_default_context()
            
            # Connect to the server
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    # Get certificate
                    cert = ssock.getpeercert()
                    
                    # Certificate is valid if we got here without exception
                    ssl_result['ssl_valid'] = True
                    
                    # Parse expiry date
                    if 'notAfter' in cert:
                        expiry_str = cert['notAfter']
                        # Parse the date format: 'MMM DD HH:MM:SS YYYY GMT'
                        expiry_date = datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')
                        expiry_date = expiry_date.replace(tzinfo=timezone.utc)
                        
                        ssl_result['ssl_expiry'] = expiry_date.strftime('%Y-%m-%d %H:%M:%S UTC')
                        
                        # Calculate days until expiry
                        now = datetime.now(timezone.utc)
                        days_until_expiry = (expiry_date - now).days
                        ssl_result['ssl_days_until_expiry'] = days_until_expiry
                        
                        # If certificate is expired, mark as invalid
                        if days_until_expiry < 0:
                            ssl_result['ssl_valid'] = False
                            
        except ssl.SSLError as e:
            ssl_result['ssl_valid'] = False
            
        except socket.gaierror as e:
            ssl_result['ssl_valid'] = False
            
        except Exception as e:
            ssl_result['ssl_valid'] = False
        
        return ssl_result
    
    def check_multiple_websites(self, urls, timeout=10, follow_redirects=True):
        """
        Check multiple websites
        
        Args:
            urls (list): List of URLs to check
            timeout (int): Request timeout in seconds
            follow_redirects (bool): Whether to follow redirects
            
        Returns:
            list: List of health check results
        """
        results = []
        for url in urls:
            result = self.check_website_health(url, timeout, follow_redirects)
            results.append(result)
        return results
    
    def get_health_summary(self, results):
        """
        Generate summary statistics from health check results
        
        Args:
            results (list): List of health check results
            
        Returns:
            dict: Summary statistics
        """
        if not results:
            return {}
        
        total_sites = len(results)
        healthy_sites = sum(1 for r in results if r['status_healthy'])
        
        # Calculate average response time for successful requests
        response_times = [r['response_time'] for r in results if r['response_time'] is not None]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # SSL statistics
        ssl_checked = sum(1 for r in results if r['ssl_checked'])
        ssl_valid = sum(1 for r in results if r['ssl_valid'])
        
        # Sites with errors
        error_count = sum(1 for r in results if r['error'] is not None)
        
        return {
            'total_sites': total_sites,
            'healthy_sites': healthy_sites,
            'unhealthy_sites': total_sites - healthy_sites,
            'health_percentage': (healthy_sites / total_sites * 100) if total_sites > 0 else 0,
            'average_response_time': avg_response_time,
            'ssl_sites_checked': ssl_checked,
            'ssl_valid_sites': ssl_valid,
            'ssl_invalid_sites': ssl_checked - ssl_valid,
            'sites_with_errors': error_count,
            'fastest_response_time': min(response_times) if response_times else None,
            'slowest_response_time': max(response_times) if response_times else None
        }
