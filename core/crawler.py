import re
import time
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import Colors
from utils.logger import Logger

class Crawler:
    def __init__(self, http_client, options=None):
        self.http = http_client
        self.options = options or {}
        self.logger = Logger()
        self.max_depth = self.options.get('crawl_depth', 2)
        self.max_urls = self.options.get('crawl_max', 50)
        self.exclude_patterns = self.options.get('exclude', [
            r'\.(jpg|jpeg|png|gif|pdf|css|js|ico|svg|woff|woff2|ttf|eot|csv|zip|tar|gz)$',
            r'logout',
            r'signout',
            r'destroy'
        ])
        self.visited_urls = set()
        self.discovered_urls = []
        self.discovered_params = []
    
    def crawl(self, start_url):
        self.logger.info(f"Starting crawl from: {Colors.CYAN}{start_url}{Colors.RESET}")
        self.logger.info(f"Max depth: {self.max_depth}, Max URLs: {self.max_urls}")
        
        self._crawl_recursive(start_url, depth=0)
        
        self.logger.info(f"Crawl complete. Found {Colors.GREEN}{len(self.discovered_urls)}{Colors.RESET} URLs")
        
        return self.discovered_urls, self.discovered_params
    
    def _crawl_recursive(self, url, depth):
        if depth > self.max_depth or len(self.discovered_urls) >= self.max_urls:
            return
        
        if url in self.visited_urls:
            return
        
        if self._should_exclude(url):
            return
        
        self.visited_urls.add(url)
        
        self.logger.debug(f"Crawling (depth {depth}): {url}")
        
        response = self.http.get(url)
        
        if not response.success:
            return
        
        self._extract_links(response.text, url)
        self._extract_forms(response.text, url)
        
        if depth < self.max_depth and len(self.discovered_urls) < self.max_urls:
            for link in self._get_links(response.text, url):
                if link not in self.visited_urls:
                    self._crawl_recursive(link, depth + 1)
    
    def _extract_links(self, html, base_url):
        try:
            soup = BeautifulSoup(html, 'lxml')
            
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                absolute_url = urljoin(base_url, href)
                
                parsed = urlparse(absolute_url)
                
                if parsed.query:
                    self.discovered_urls.append(absolute_url)
                    
                    params = parse_qs(parsed.query)
                    for param in params.keys():
                        if (param, absolute_url) not in self.discovered_params:
                            self.discovered_params.append((param, absolute_url))
        
        except Exception as e:
            self.logger.debug(f"Error extracting links: {e}")
    
    def _extract_forms(self, html, base_url):
        try:
            soup = BeautifulSoup(html, 'lxml')
            
            for form in soup.find_all('form'):
                action = form.get('action', '')
                method = form.get('method', 'get').upper()
                
                form_url = urljoin(base_url, action) if action else base_url
                
                inputs = form.find_all(['input', 'textarea', 'select'])
                
                for input_tag in inputs:
                    name = input_tag.get('name', '')
                    input_type = input_tag.get('type', 'text').lower()
                    
                    if name and input_type not in ['submit', 'button', 'reset', 'hidden']:
                        if (name, form_url, method) not in self.discovered_params:
                            self.discovered_params.append((name, form_url, method))
        
        except Exception as e:
            self.logger.debug(f"Error extracting forms: {e}")
    
    def _get_links(self, html, base_url):
        links = []
        
        try:
            soup = BeautifulSoup(html, 'lxml')
            
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                absolute_url = urljoin(base_url, href)
                
                parsed_base = urlparse(base_url)
                parsed_link = urlparse(absolute_url)
                
                if parsed_link.netloc == parsed_base.netloc:
                    links.append(absolute_url)
        
        except Exception:
            pass
        
        return links
    
    def _should_exclude(self, url):
        url_lower = url.lower()
        
        for pattern in self.exclude_patterns:
            if re.search(pattern, url_lower):
                return True
        
        return False
    
    def get_urls_with_params(self):
        return self.discovered_urls
    
    def get_params(self):
        return self.discovered_params
    
    def reset(self):
        self.visited_urls = set()
        self.discovered_urls = []
        self.discovered_params = []
