#!/usr/bin/env python3
"""
Example usage of the Website Health Checker API

This file demonstrates various ways to use the health checker API
"""

from api import HealthCheckerAPI
import json

def example_single_website():
    """Example: Check a single website"""
    print("="*60)
    print("EXAMPLE 1: Single Website Health Check")
    print("="*60)
    
    api = HealthCheckerAPI()
    
    # Check Google
    result = api.check_website("https://google.com", timeout=10)
    
    print(f"URL: {result['url']}")
    print(f"Status: {result['status_code']}")
    print(f"Healthy: {result['status_healthy']}")
    print(f"Response Time: {result['response_time']:.3f}s")
    print(f"SSL Valid: {result['ssl_valid']}")
    
    if result['ssl_expiry']:
        print(f"SSL Expires: {result['ssl_expiry']}")
        print(f"Days until expiry: {result['ssl_days_until_expiry']}")
    
    if result['error']:
        print(f"Error: {result['error']}")

def example_multiple_websites():
    """Example: Check multiple websites"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Multiple Websites Health Check")
    print("="*60)
    
    api = HealthCheckerAPI()
    
    # List of websites to check
    websites = [
        "https://google.com",
        "https://github.com",
        "https://httpstat.us/200",  # Always returns 200
        "https://httpstat.us/404",  # Always returns 404
        "http://example.com",       # HTTP site (no SSL)
        "https://expired.badssl.com"  # Expired SSL certificate
    ]
    
    print(f"Checking {len(websites)} websites...")
    results = api.check_multiple_websites(websites, timeout=15)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['url']}")
        print(f"   Status: {result['status_code'] or 'FAILED'}")
        print(f"   Healthy: {'✓' if result['status_healthy'] else '✗'}")
        print(f"   Response Time: {result['response_time']:.3f}s" if result['response_time'] else "   Response Time: N/A")
        
        if result['ssl_checked']:
            print(f"   SSL Valid: {'✓' if result['ssl_valid'] else '✗'}")
            if result['ssl_days_until_expiry'] is not None:
                print(f"   SSL Expires in: {result['ssl_days_until_expiry']} days")
        
        if result['error']:
            print(f"   Error: {result['error']}")

def example_with_summary():
    """Example: Get summary statistics"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Health Check with Summary Statistics")
    print("="*60)
    
    api = HealthCheckerAPI()
    
    websites = [
        "https://google.com",
        "https://github.com",
        "https://stackoverflow.com",
        "https://httpstat.us/500",  # Server error
        "https://invalid-url-that-does-not-exist.com"
    ]
    
    results = api.check_multiple_websites(websites)
    summary = api.get_summary(results)
    
    print("SUMMARY STATISTICS:")
    print(f"Total Sites: {summary['total_sites']}")
    print(f"Healthy Sites: {summary['healthy_sites']}")
    print(f"Unhealthy Sites: {summary['unhealthy_sites']}")
    print(f"Health Percentage: {summary['health_percentage']:.1f}%")
    print(f"Average Response Time: {summary['average_response_time']:.3f}s")
    print(f"SSL Sites Checked: {summary['ssl_sites_checked']}")
    print(f"Valid SSL Sites: {summary['ssl_valid_sites']}")
    print(f"Sites with Errors: {summary['sites_with_errors']}")
    
    if summary['fastest_response_time']:
        print(f"Fastest Response: {summary['fastest_response_time']:.3f}s")
    if summary['slowest_response_time']:
        print(f"Slowest Response: {summary['slowest_response_time']:.3f}s")

def example_json_output():
    """Example: Get results as JSON"""
    print("\n" + "="*60)
    print("EXAMPLE 4: JSON Output")
    print("="*60)
    
    api = HealthCheckerAPI()
    
    # Single website as JSON
    json_result = api.check_website_json("https://github.com")
    print("Single website result (JSON):")
    print(json_result)
    
    # Multiple websites as JSON
    websites = ["https://google.com", "https://stackoverflow.com"]
    json_results = api.check_multiple_websites_json(websites)
    print("\nMultiple websites results (JSON):")
    print(json_results)

def example_custom_settings():
    """Example: Custom timeout and redirect settings"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Custom Settings")
    print("="*60)
    
    api = HealthCheckerAPI()
    
    # Custom timeout
    print("Checking with 5-second timeout...")
    result1 = api.check_website("https://httpbin.org/delay/3", timeout=5)
    print(f"Result: {result1['status_healthy']} (Error: {result1.get('error', 'None')})")
    
    # Don't follow redirects
    print("\nChecking without following redirects...")
    result2 = api.check_website("http://github.com", follow_redirects=False)
    print(f"Status Code: {result2['status_code']}")
    print(f"Final URL: {result2['final_url']}")

def main():
    """Run all examples"""
    print("Website Health Checker API - Usage Examples")
    print("=" * 60)
    
    example_single_website()
    # example_multiple_websites()
    example_with_summary()
    example_json_output()
    example_custom_settings()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)

if __name__ == "__main__":
    main()