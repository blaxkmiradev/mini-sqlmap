#!/usr/bin/env python3

import sys
import argparse
import os
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.colors import Colors, BANNER
from utils.logger import Logger
from utils.helpers import Helpers
from core.scanner import Scanner
from output.json_writer import JSONWriter
from output.html_writer import HTMLWriter
from output.csv_writer import CSVWriter

class MiniSQLMap:
    def __init__(self):
        self.logger = Logger()
        self.args = None
        self.scanner = None
    
    def parse_arguments(self):
        parser = argparse.ArgumentParser(
            description='Mini SQLMap - SQL Injection Vulnerability Scanner',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''
Examples:
  python mini_sqlmap.py -u "http://target.com/page?id=1"
  python mini_sqlmap.py -u "http://target.com/page?id=1" --risk=2
  python mini_sqlmap.py -m urls.txt -o results.json
  python mini_sqlmap.py -u "http://target.com/page?id=1" --cookie="PHPSESSID=abc"
            '''
        )
        
        parser.add_argument('-u', '--url', help='Target URL to scan')
        parser.add_argument('-m', '--mass', help='File containing multiple URLs to scan')
        parser.add_argument('-d', '--data', help='POST data to send with the request')
        parser.add_argument('--method', default='GET', help='HTTP method (GET or POST)')
        
        parser.add_argument('--cookie', help='Cookie string to use')
        parser.add_argument('--user-agent', help='Custom User-Agent')
        parser.add_argument('-H', '--header', action='append', help='Custom header (format: "Name: Value")')
        
        parser.add_argument('--dbms', choices=['MySQL', 'PostgreSQL', 'MSSQL', 'Oracle', 'SQLite'], 
                          help='Force database type')
        parser.add_argument('--risk', type=int, default=1, choices=[1, 2, 3],
                          help='Risk level (1-3, default: 1)')
        parser.add_argument('-v', '--verbosity', type=int, default=1, choices=[0, 1, 2, 3, 4, 5, 6],
                          help='Verbosity level (0-6, default: 1)')
        
        parser.add_argument('--proxy', help='HTTP proxy URL')
        parser.add_argument('--delay', type=float, default=0, help='Delay between requests in seconds')
        parser.add_argument('--timeout', type=int, default=30, help='Request timeout in seconds')
        parser.add_argument('--retries', type=int, default=3, help='Number of retries on failure')
        
        parser.add_argument('--crawl', type=int, metavar='DEPTH', help='Crawl website to discover URLs')
        parser.add_argument('--crawl-max', type=int, default=50, help='Maximum URLs to crawl')
        
        parser.add_argument('-o', '--output', help='Output file for results')
        parser.add_argument('--format', choices=['json', 'html', 'csv'], default='json',
                          help='Output format (default: json)')
        
        parser.add_argument('--batch', action='store_true', help='Run in batch mode (no prompts)')
        parser.add_argument('--colors', action='store_true', default=True, help='Enable colored output')
        parser.add_argument('--no-colors', action='store_true', help='Disable colored output')
        parser.add_argument('--threads', type=int, default=1, help='Number of concurrent threads (future)')
        
        parser.add_argument('--version', action='store_true', help='Show version information')
        parser.add_argument('--list-payloads', action='store_true', help='List all available payloads')
        
        return parser.parse_args()
    
    def setup(self):
        if not Colors.supports_color() or self.args.no_colors:
            Colors.disable()
        
        if self.args.verbosity >= 2:
            self.logger.set_level('DEBUG')
        elif self.args.verbosity == 1:
            self.logger.set_level('INFO')
        else:
            self.logger.set_level('WARNING')
    
    def validate_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def load_urls_from_file(self, filepath):
        urls = []
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        urls.append(line)
            return urls
        except Exception as e:
            self.logger.error(f"Failed to load URLs from file: {e}")
            return []
    
    def create_scanner_options(self):
        options = {
            'timeout': self.args.timeout,
            'delay': self.args.delay,
            'proxy': self.args.proxy,
            'risk': self.args.risk,
            'retries': self.args.retries
        }
        
        if self.args.cookie:
            options['cookies'] = Helpers.parse_cookies(self.args.cookie)
        
        if self.args.user_agent:
            options['user_agent'] = self.args.user_agent
        
        if self.args.header:
            headers = {}
            for header in self.args.header:
                if ':' in header:
                    key, value = header.split(':', 1)
                    headers[key.strip()] = value.strip()
            options['headers'] = headers
        
        return options
    
    def run_single_scan(self):
        if not self.args.url:
            self.logger.error("URL is required. Use -u or --url to specify target.")
            return False
        
        if not self.validate_url(self.args.url):
            self.logger.error(f"Invalid URL: {self.args.url}")
            return False
        
        self.logger.info(f"Starting scan on: {Colors.CYAN}{self.args.url}{Colors.RESET}")
        
        options = self.create_scanner_options()
        self.scanner = Scanner(options)
        
        if self.args.crawl:
            self.logger.info(f"Starting crawl scan (depth: {self.args.crawl})")
            vulnerabilities = self.scanner.crawl_and_scan(
                self.args.url, 
                depth=self.args.crawl,
                max_urls=self.args.crawl_max
            )
        else:
            vulnerabilities = self.scanner.scan_url(
                self.args.url,
                method=self.args.method,
                data=self.args.data
            )
        
        self.display_results(vulnerabilities)
        
        if self.args.output:
            self.save_results(vulnerabilities)
        
        self.scanner.close()
        return len(vulnerabilities) > 0
    
    def run_batch_scan(self):
        if not self.args.mass:
            self.logger.error("File with URLs is required for batch scan. Use -m or --mass.")
            return False
        
        urls = self.load_urls_from_file(self.args.mass)
        
        if not urls:
            self.logger.error("No valid URLs found in file.")
            return False
        
        self.logger.info(f"Loaded {len(urls)} URLs from {self.args.mass}")
        
        options = self.create_scanner_options()
        self.scanner = Scanner(options)
        
        for i, url in enumerate(urls, 1):
            self.logger.info(f"Scanning [{i}/{len(urls)}]: {Colors.CYAN}{url}{Colors.RESET}")
            
            if not self.validate_url(url):
                self.logger.warning(f"Invalid URL: {url}, skipping...")
                continue
            
            try:
                self.scanner.scan_url(url)
            except Exception as e:
                self.logger.error(f"Scan failed for {url}: {e}")
        
        vulnerabilities = self.scanner.get_results()
        self.display_results(vulnerabilities)
        
        if self.args.output:
            self.save_results(vulnerabilities)
        
        self.scanner.close()
        return len(vulnerabilities) > 0
    
    def display_results(self, vulnerabilities):
        self.logger.print_header("SCAN RESULTS")
        
        if vulnerabilities:
            self.logger.warning(f"Found {len(vulnerabilities)} vulnerability(ies)!")
            
            for i, vuln in enumerate(vulnerabilities, 1):
                print(f"\n{Colors.RED}{'-' * 60}{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.RED}[{i}] {vuln.get('type', 'SQL Injection')}{Colors.RESET}")
                print(f"{Colors.WHITE}URL: {Colors.CYAN}{vuln.get('url', 'N/A')}{Colors.RESET}")
                print(f"{Colors.WHITE}Parameter: {Colors.YELLOW}{vuln.get('parameter', 'N/A')}{Colors.RESET}")
                print(f"{Colors.WHITE}Method: {Colors.MAGENTA}{vuln.get('method', 'GET')}{Colors.RESET}")
                
                if 'payload' in vuln:
                    print(f"{Colors.WHITE}Payload: {Colors.RED}{vuln['payload']}{Colors.RESET}")
                
                if 'error_message' in vuln:
                    print(f"{Colors.WHITE}Error: {Colors.RED}{vuln['error_message'][:100]}...{Colors.RESET}")
                
                if 'db_type' in vuln:
                    print(f"{Colors.WHITE}Database: {Colors.GREEN}{vuln['db_type']}{Colors.RESET}")
        else:
            self.logger.success("No vulnerabilities found.")
        
        if self.scanner:
            self.scanner.print_summary()
    
    def save_results(self, vulnerabilities):
        if not self.args.output:
            return
        
        try:
            if self.args.format == 'json':
                writer = JSONWriter(self.args.output)
            elif self.args.format == 'html':
                writer = HTMLWriter(self.args.output)
            elif self.args.format == 'csv':
                writer = CSVWriter(self.args.output)
            else:
                writer = JSONWriter(self.args.output)
            
            writer.write(vulnerabilities)
            self.logger.success(f"Results saved to: {Colors.CYAN}{self.args.output}{Colors.RESET}")
            
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
    
    def list_payloads(self):
        from payloads.blind import BOOLEAN_PAYLOADS
        from payloads.error import ERROR_PAYLOADS
        from payloads.time import TIME_PAYLOADS
        from payloads.union import UNION_PAYLOADS
        from payloads.stacked import STACKED_PAYLOADS
        
        self.logger.print_header("AVAILABLE PAYLOADS")
        
        categories = [
            ("Boolean-based Blind", BOOLEAN_PAYLOADS),
            ("Error-based", ERROR_PAYLOADS),
            ("Time-based Blind", TIME_PAYLOADS),
            ("Union-based", UNION_PAYLOADS),
            ("Stacked Queries", STACKED_PAYLOADS)
        ]
        
        for name, payloads in categories:
            print(f"\n{Colors.YELLOW}{name} ({len(payloads)} payloads){Colors.RESET}")
            print(f"{Colors.YELLOW}{'-' * 40}{Colors.RESET}")
            for i, payload in enumerate(payloads[:10], 1):
                print(f"  {Colors.CYAN}{i}.{Colors.RESET} {Colors.RED}{payload}{Colors.RESET}")
            if len(payloads) > 10:
                print(f"  {Colors.DIM}... and {len(payloads) - 10} more{Colors.RESET}")
    
    def show_version(self):
        print(f"{Colors.CYAN}Mini SQLMap{Colors.RESET} v1.0.0")
        print(f"{Colors.DIM}SQL Injection Vulnerability Scanner{Colors.RESET}")
        print(f"{Colors.DIM}Author: Rikixz (@blaxkmiradev){Colors.RESET}")
        print(f"{Colors.DIM}https://github.com/blaxkmiradev/mini-sqlmap{Colors.RESET}")
    
    def show_disclaimer(self):
        disclaimer = """
+=====================================================================+
|                    LEGAL DISCLAIMER                                 |
+=====================================================================+
|                                                                     |
|  This tool is for EDUCATIONAL and AUTHORIZED SECURITY TESTING      |
|  PURPOSES ONLY.                                                     |
|                                                                     |
|  - Only scan URLs you have explicit permission to test             |
|  - Unauthorized scanning is ILLEGAL in most jurisdictions          |
|  - The developers are NOT responsible for misuse                    |
|  - Always obtain written permission before security testing         |
|                                                                     |
|  By using this tool, you agree to these terms.                      |
|                                                                     |
+=====================================================================+
        """
        print(f"{Colors.YELLOW}{disclaimer}{Colors.RESET}")
    
    def run(self):
        self.args = self.parse_arguments()
        
        if self.args.version:
            self.show_version()
            return
        
        if self.args.list_payloads:
            self.list_payloads()
            return
        
        print(BANNER.ASCII_ART)
        self.show_disclaimer()
        
        if not self.args.url and not self.args.mass:
            print(f"\n{Colors.YELLOW}Usage: python mini_sqlmap.py -u \"http://target.com/page?id=1\"{Colors.RESET}\n")
            print(f"{Colors.CYAN}Run with --help for more options{Colors.RESET}\n")
            return
        
        self.setup()
        
        if self.args.batch or self.args.mass:
            self.run_batch_scan()
        else:
            self.run_single_scan()

def main():
    try:
        app = MiniSQLMap()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[*] Scan interrupted by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR]{Colors.RESET} {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
