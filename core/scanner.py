import time
from urllib.parse import urlparse, parse_qs, urlencode
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.http_client import HTTPClient
from core.detector import Detector
from core.database import DatabaseFingerprint
from core.crawler import Crawler
from utils.colors import Colors
from utils.logger import Logger
from utils.helpers import Helpers

class Scanner:
    def __init__(self, options=None):
        self.options = options or {}
        self.logger = Logger()
        self.http = HTTPClient(self.options)
        self.detector = Detector(self.http, self.options)
        self.fingerprinter = DatabaseFingerprint(self.http, self.options)
        self.results = []
        self.total_urls_scanned = 0
        self.total_vulnerabilities_found = 0
    
    def scan_url(self, url, method='GET', data=None):
        self.logger.info(f"Scanning: {Colors.CYAN}{url}{Colors.RESET}")
        
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        if not params and data:
            if isinstance(data, str):
                params = parse_qs(data)
            elif isinstance(data, dict):
                params = data
        
        if not params:
            self.logger.warning(f"No parameters found in URL: {url}")
            return []
        
        self.logger.info(f"Found {Colors.YELLOW}{len(params)}{Colors.RESET} parameter(s) to test")
        
        baseline_response = self.http.get_baseline(url, method, data)
        
        if not baseline_response.success:
            self.logger.error(f"Failed to get baseline response from {url}")
            return []
        
        self.logger.debug(f"Baseline status code: {baseline_response.status_code}")
        self.logger.debug(f"Baseline response time: {baseline_response.elapsed_time:.3f}s")
        
        vulnerabilities = []
        
        for param in params.keys():
            self.logger.info(f"Testing parameter: {Colors.CYAN}{param}{Colors.RESET}")
            
            param_vulns = self.detector.detect_all_types(
                url, param, baseline_response, None
            )
            
            if param_vulns:
                for vuln in param_vulns:
                    vuln['url'] = url
                    vuln['parameter'] = param
                    vuln['method'] = method
                    vulnerabilities.append(vuln)
                    self.total_vulnerabilities_found += 1
                    
                    self.logger.success(f"Vulnerability found in {param}:")
                    self.logger.info(f"  Type: {Colors.RED}{vuln['type']}{Colors.RESET}")
                    self.logger.info(f"  Payload: {Colors.YELLOW}{vuln.get('payload', 'N/A')}{Colors.RESET}")
                    
                    if 'error_message' in vuln:
                        self.logger.info(f"  Error: {Colors.RED}{vuln['error_message'][:100]}...{Colors.RESET}")
            else:
                self.logger.info(f"No vulnerabilities found in {param}")
        
        self.total_urls_scanned += 1
        self.results.extend(vulnerabilities)
        
        return vulnerabilities
    
    def scan_multiple(self, urls):
        all_vulnerabilities = []
        
        self.logger.info(f"Starting batch scan of {Colors.YELLOW}{len(urls)}{Colors.RESET} URLs")
        
        for i, url in enumerate(urls, 1):
            self.logger.info(f"Progress: [{i}/{len(urls)}] {((i-1)/len(urls)*100):.0f}%")
            
            vulns = self.scan_url(url.strip())
            all_vulnerabilities.extend(vulns)
        
        self.logger.success(f"Batch scan complete!")
        self.logger.info(f"Scanned: {self.total_urls_scanned} URLs")
        self.logger.info(f"Vulnerabilities found: {self.total_vulnerabilities_found}")
        
        return all_vulnerabilities
    
    def crawl_and_scan(self, url, depth=2, max_urls=50):
        self.logger.info(f"Starting crawl-and-scan on: {Colors.CYAN}{url}{Colors.RESET}")
        
        crawler_options = self.options.copy()
        crawler_options['crawl_depth'] = depth
        crawler_options['crawl_max'] = max_urls
        
        crawler = Crawler(self.http, crawler_options)
        discovered_urls, discovered_params = crawler.crawl(url)
        
        self.logger.info(f"Found {len(discovered_urls)} URLs with parameters")
        
        all_vulnerabilities = []
        
        for url_with_params in discovered_urls:
            vulns = self.scan_url(url_with_params)
            all_vulnerabilities.extend(vulns)
        
        return all_vulnerabilities
    
    def get_results(self):
        return self.results
    
    def get_summary(self):
        vuln_types = {}
        
        for vuln in self.results:
            vuln_type = vuln.get('type', 'Unknown')
            vuln_types[vuln_type] = vuln_types.get(vuln_type, 0) + 1
        
        return {
            'total_urls_scanned': self.total_urls_scanned,
            'total_vulnerabilities': self.total_vulnerabilities_found,
            'vulnerabilities_by_type': vuln_types,
            'results': self.results
        }
    
    def print_summary(self):
        self.logger.print_header("SCAN SUMMARY")
        
        summary = self.get_summary()
        
        print(f"{Colors.WHITE}URLs Scanned:        {Colors.CYAN}{summary['total_urls_scanned']}{Colors.RESET}")
        print(f"{Colors.WHITE}Vulnerabilities:     {Colors.YELLOW}{summary['total_vulnerabilities']}{Colors.RESET}")
        
        if summary['vulnerabilities_by_type']:
            print(f"\n{Colors.WHITE}Vulnerabilities by Type:{Colors.RESET}")
            for vuln_type, count in summary['vulnerabilities_by_type'].items():
                print(f"  {Colors.RED}•{Colors.RESET} {vuln_type}: {Colors.YELLOW}{count}{Colors.RESET}")
        
        stats = self.http.get_stats()
        print(f"\n{Colors.DIM}Request Statistics:{Colors.RESET}")
        print(f"  Total Requests: {Colors.CYAN}{stats['request_count']}{Colors.RESET}")
        print(f"  Total Time: {Colors.CYAN}{Helpers.format_time(stats['total_time'])}{Colors.RESET}")
        print(f"  Avg Time: {Colors.CYAN}{stats['avg_time']:.3f}s{Colors.RESET}")
        
        print()
    
    def print_results(self):
        if not self.results:
            self.logger.success("No vulnerabilities found!")
            return
        
        self.logger.print_header("VULNERABILITY REPORT")
        
        for i, vuln in enumerate(self.results, 1):
            print(f"{Colors.RED}{'─' * 60}{Colors.RESET}")
            print(f"{Colors.BOLD}[{i}] {vuln.get('type', 'Unknown')} SQL Injection{Colors.RESET}")
            print(f"{Colors.WHITE}URL:{Colors.RESET} {Colors.CYAN}{vuln.get('url', 'N/A')}{Colors.RESET}")
            print(f"{Colors.WHITE}Parameter:{Colors.RESET} {Colors.YELLOW}{vuln.get('parameter', 'N/A')}{Colors.RESET}")
            print(f"{Colors.WHITE}Method:{Colors.RESET} {Colors.MAGENTA}{vuln.get('method', 'GET')}{Colors.RESET}")
            
            if 'payload' in vuln:
                print(f"{Colors.WHITE}Payload:{Colors.RESET} {Colors.RED}{vuln['payload']}{Colors.RESET}")
            
            if 'error_message' in vuln:
                print(f"{Colors.WHITE}Error Message:{Colors.RESET} {Colors.RED}{vuln['error_message'][:150]}...{Colors.RESET}")
            
            if 'db_type' in vuln:
                print(f"{Colors.WHITE}Database Type:{Colors.RESET} {Colors.GREEN}{vuln['db_type']}{Colors.RESET}")
            
            if 'evidence' in vuln:
                print(f"{Colors.WHITE}Evidence:{Colors.RESET} {Colors.LIGHT_YELLOW}{vuln['evidence']}{Colors.RESET}")
            
            print()
    
    def export_results(self, filepath, format='json'):
        import json
        
        summary = self.get_summary()
        
        try:
            with open(filepath, 'w') as f:
                if format == 'json':
                    json.dump(summary, f, indent=4, default=str)
                else:
                    json.dump(summary, f, indent=4, default=str)
            
            self.logger.success(f"Results exported to: {Colors.CYAN}{filepath}{Colors.RESET}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to export results: {e}")
            return False
    
    def close(self):
        self.http.close()
