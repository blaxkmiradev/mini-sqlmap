import requests
import time
import random
from urllib.parse import urlparse, parse_qs, urlencode
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import Colors
from utils.logger import Logger
from utils.helpers import Helpers

class HTTPClient:
    DEFAULT_USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    ]
    
    def __init__(self, options=None):
        self.options = options or {}
        self.session = requests.Session()
        self.logger = Logger()
        
        self.timeout = self.options.get('timeout', 30)
        self.delay = self.options.get('delay', 0)
        self.proxy = self.options.get('proxy', None)
        self.user_agent = self.options.get('user_agent', random.choice(self.DEFAULT_USER_AGENTS))
        self.cookies = self.options.get('cookies', {})
        self.headers = self.options.get('headers', {})
        self.verify_ssl = self.options.get('verify_ssl', True)
        
        self.request_count = 0
        self.total_time = 0
    
    def _build_headers(self, additional_headers=None):
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1'
        }
        
        if self.cookies:
            cookie_str = '; '.join([f"{k}={v}" for k, v in self.cookies.items()])
            headers['Cookie'] = cookie_str
        
        headers.update(self.headers)
        
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    def _apply_delay(self):
        if self.delay > 0:
            time.sleep(self.delay)
    
    def request(self, method, url, **kwargs):
        self._apply_delay()
        
        method = method.upper()
        
        headers = kwargs.pop('headers', {})
        headers.update(self._build_headers())
        
        req_kwargs = {
            'headers': headers,
            'timeout': kwargs.pop('timeout', self.timeout),
            'allow_redirects': kwargs.pop('allow_redirects', True),
            'verify': kwargs.pop('verify', self.verify_ssl)
        }
        
        if self.proxy:
            req_kwargs['proxies'] = {
                'http': self.proxy,
                'https': self.proxy
            }
        
        req_kwargs.update(kwargs)
        
        start_time = time.time()
        
        try:
            response = self.session.request(method, url, **req_kwargs)
            elapsed = time.time() - start_time
            
            self.request_count += 1
            self.total_time += elapsed
            
            response.elapsed_time = elapsed
            response.success = True
            response.error = None
            
            return response
            
        except requests.exceptions.Timeout as e:
            elapsed = time.time() - start_time
            self.request_count += 1
            self.total_time += elapsed
            
            error_response = requests.Response()
            error_response.status_code = 0
            error_response.success = False
            error_response.error = f"Timeout: {str(e)}"
            error_response.elapsed_time = elapsed
            error_response.text = ""
            return error_response
            
        except requests.exceptions.ConnectionError as e:
            elapsed = time.time() - start_time
            self.request_count += 1
            self.total_time += elapsed
            
            error_response = requests.Response()
            error_response.status_code = 0
            error_response.success = False
            error_response.error = f"Connection Error: {str(e)}"
            error_response.elapsed_time = elapsed
            error_response.text = ""
            return error_response
            
        except requests.exceptions.RequestException as e:
            elapsed = time.time() - start_time
            self.request_count += 1
            self.total_time += elapsed
            
            error_response = requests.Response()
            error_response.status_code = 0
            error_response.success = False
            error_response.error = f"Request Error: {str(e)}"
            error_response.elapsed_time = elapsed
            error_response.text = ""
            return error_response
    
    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)
    
    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)
    
    def head(self, url, **kwargs):
        return self.request('HEAD', url, **kwargs)
    
    def options_request(self, url, **kwargs):
        return self.request('OPTIONS', url, **kwargs)
    
    def get_baseline(self, url, method='GET', data=None):
        if method.upper() == 'POST':
            return self.post(url, data=data)
        return self.get(url, params=data)
    
    def test_payload(self, url, param, payload, method='GET', data=None, technique='append'):
        if method.upper() == 'POST':
            if data:
                if isinstance(data, str):
                    params = parse_qs(data)
                else:
                    params = data.copy()
            else:
                params = {}
            
            params[param] = [params.get(param, [''])[0] + payload]
            
            if isinstance(data, str):
                new_data = urlencode(params, doseq=True)
            else:
                new_data = params
            
            return self.post(url, data=new_data)
        else:
            return self.inject_and_get(url, param, payload, technique)
    
    def inject_and_get(self, url, param, payload, technique='append'):
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        
        if param in query_params:
            if technique == 'replace':
                query_params[param] = [payload]
            elif technique == 'append':
                query_params[param] = [str(query_params[param][0]) + payload]
            elif technique == 'quote':
                query_params[param] = [f"'{payload}'"]
        
        new_query = urlencode(query_params, doseq=True)
        new_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if new_query:
            new_url += f"?{new_query}"
        
        return self.get(new_url)
    
    def set_cookie(self, name, value):
        self.cookies[name] = value
    
    def set_cookies(self, cookies):
        if isinstance(cookies, dict):
            self.cookies.update(cookies)
        elif isinstance(cookies, str):
            self.cookies.update(Helpers.parse_cookies(cookies))
    
    def set_header(self, name, value):
        self.headers[name] = value
    
    def clear_cookies(self):
        self.cookies = {}
        self.session.cookies.clear()
    
    def get_stats(self):
        return {
            'request_count': self.request_count,
            'total_time': self.total_time,
            'avg_time': self.total_time / self.request_count if self.request_count > 0 else 0
        }
    
    def reset_stats(self):
        self.request_count = 0
        self.total_time = 0
    
    def close(self):
        self.session.close()
