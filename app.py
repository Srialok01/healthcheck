import streamlit as st
import time
from health_checker import HealthChecker
from urllib.parse import urlparse
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Website Health Checker",
    page_icon="🔍",
    layout="wide"
)

# Initialize health checker
health_checker = HealthChecker()

# Main title
st.title("🔍 Website Health Checker")
st.markdown("Monitor website status, response times, and SSL certificates")

# Sidebar for configuration
st.sidebar.header("Configuration")
timeout = st.sidebar.slider("Request Timeout (seconds)", 5, 30, 10)
follow_redirects = st.sidebar.checkbox("Follow Redirects", value=True)

# Main input section
st.header("Website URLs to Check")

# Input methods
input_method = st.radio(
    "Choose input method:",
    ["Single URL", "Multiple URLs (bulk)"]
)

urls_to_check = []

if input_method == "Single URL":
    url = st.text_input(
        "Enter website URL:",
        placeholder="https://example.com",
        help="Enter a complete URL including http:// or https://"
    )
    if url:
        urls_to_check = [url]
else:
    urls_text = st.text_area(
        "Enter multiple URLs (one per line):",
        placeholder="https://example.com\nhttps://google.com\nhttps://github.com",
        help="Enter one URL per line"
    )
    if urls_text:
        urls_to_check = [url.strip() for url in urls_text.split('\n') if url.strip()]

# Validation function
def validate_url(url):
    """Validate if URL is properly formatted"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

# Check button and results
if st.button("🚀 Run Health Check", type="primary"):
    if not urls_to_check:
        st.error("Please enter at least one URL to check")
    else:
        # Validate URLs
        valid_urls = []
        invalid_urls = []
        
        for url in urls_to_check:
            if validate_url(url):
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
        
        if invalid_urls:
            st.error(f"Invalid URLs found: {', '.join(invalid_urls)}")
        
        if valid_urls:
            st.success(f"Checking {len(valid_urls)} valid URL(s)...")
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            
            for i, url in enumerate(valid_urls):
                status_text.text(f"Checking {url}...")
                progress_bar.progress((i + 1) / len(valid_urls))
                
                # Perform health check
                result = health_checker.check_website_health(
                    url, 
                    timeout=timeout, 
                    follow_redirects=follow_redirects
                )
                results.append(result)
                
                # Small delay to show progress
                time.sleep(0.1)
            
            status_text.text("Health check completed!")
            
            # Display results
            st.header("📊 Health Check Results")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            healthy_count = sum(1 for r in results if r['status_healthy'])
            avg_response_time = sum(r['response_time'] for r in results if r['response_time'] is not None) / len([r for r in results if r['response_time'] is not None]) if any(r['response_time'] is not None for r in results) else 0
            ssl_valid_count = sum(1 for r in results if r['ssl_valid'])
            ssl_checked_count = sum(1 for r in results if r['ssl_checked'])
            
            with col1:
                st.metric("Healthy Sites", f"{healthy_count}/{len(results)}")
            with col2:
                st.metric("Avg Response Time", f"{avg_response_time:.2f}s" if avg_response_time > 0 else "N/A")
            with col3:
                st.metric("Valid SSL", f"{ssl_valid_count}/{ssl_checked_count}" if ssl_checked_count > 0 else "N/A")
            with col4:
                st.metric("Total Checked", len(results))
            
            # Detailed results
            for result in results:
                with st.expander(f"🌐 {result['url']}", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("HTTP Status")
                        if result['status_healthy']:
                            st.success(f"✅ Status: {result['status_code']}")
                        else:
                            st.error(f"❌ Status: {result['status_code'] or 'Connection Failed'}")
                        
                        if result['response_time']:
                            if result['response_time'] < 1:
                                st.success(f"⚡ Response Time: {result['response_time']:.3f}s")
                            elif result['response_time'] < 3:
                                st.warning(f"⏱️ Response Time: {result['response_time']:.3f}s")
                            else:
                                st.error(f"🐌 Response Time: {result['response_time']:.3f}s")
                        
                        if result['final_url'] != result['url']:
                            st.info(f"🔄 Redirected to: {result['final_url']}")
                    
                    with col2:
                        st.subheader("SSL Certificate")
                        if result['ssl_checked']:
                            if result['ssl_valid']:
                                st.success("✅ SSL Certificate Valid")
                                if result['ssl_expiry']:
                                    st.info(f"📅 Expires: {result['ssl_expiry']}")
                                    if result['ssl_days_until_expiry'] is not None:
                                        if result['ssl_days_until_expiry'] > 30:
                                            st.success(f"⏰ {result['ssl_days_until_expiry']} days until expiry")
                                        elif result['ssl_days_until_expiry'] > 7:
                                            st.warning(f"⚠️ {result['ssl_days_until_expiry']} days until expiry")
                                        else:
                                            st.error(f"🚨 {result['ssl_days_until_expiry']} days until expiry")
                            else:
                                st.error("❌ SSL Certificate Invalid")
                        else:
                            st.info("ℹ️ HTTP site (no SSL)")
                    
                    if result['error']:
                        st.error(f"💥 Error: {result['error']}")

# Example URLs section
st.sidebar.header("Example URLs")
st.sidebar.markdown("""
Try these example URLs:
- https://google.com
- https://github.com
- https://httpstat.us/200
- https://httpstat.us/404
- http://example.com
""")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Monitor your websites' health in real-time")
