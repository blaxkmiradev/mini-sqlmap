import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import Colors, BANNER, ProgressBar, Spinner

class ConsoleOutput:
    COLORS = Colors
    
    @staticmethod
    def print_banner():
        print(BANNER.ASCII_ART)
    
    @staticmethod
    def print_scan_start(url):
        print(f"\n{Colors.CYAN}{'─' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.WHITE}  Starting scan on: {Colors.CYAN}{url}{Colors.RESET}")
        print(f"{Colors.CYAN}{'─' * 60}{Colors.RESET}\n")
    
    @staticmethod
    def print_scan_complete(vulns_found):
        print(f"\n{Colors.CYAN}{'─' * 60}{Colors.RESET}")
        if vulns_found > 0:
            print(f"{Colors.GREEN}{Colors.BOLD}  Scan complete! Found {vulns_found} vulnerability(ies){Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}{Colors.BOLD}  Scan complete. No vulnerabilities found{Colors.RESET}")
        print(f"{Colors.CYAN}{'─' * 60}{Colors.RESET}\n")
    
    @staticmethod
    def print_vulnerability(vuln, index=1):
        print(f"\n{Colors.RED}{'─' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.RED}[{index}] {vuln.get('type', 'SQL Injection')}{Colors.RESET}")
        print(f"{Colors.LIGHT_WHITE}URL: {Colors.CYAN}{vuln.get('url', 'N/A')}{Colors.RESET}")
        print(f"{Colors.LIGHT_WHITE}Parameter: {Colors.YELLOW}{vuln.get('parameter', 'N/A')}{Colors.RESET}")
        print(f"{Colors.LIGHT_WHITE}Method: {Colors.MAGENTA}{vuln.get('method', 'GET')}{Colors.RESET}")
        
        if 'payload' in vuln:
            print(f"{Colors.LIGHT_WHITE}Payload: {Colors.RED}{vuln['payload']}{Colors.RESET}")
        
        if 'error_message' in vuln:
            print(f"{Colors.LIGHT_WHITE}Error: {Colors.RED}{vuln['error_message'][:150]}...{Colors.RESET}")
        
        if 'db_type' in vuln:
            print(f"{Colors.LIGHT_WHITE}Database: {Colors.GREEN}{vuln['db_type']}{Colors.RESET}")
        
        print()
    
    @staticmethod
    def print_progress(current, total, prefix='Progress'):
        pb = ProgressBar(total, prefix)
        pb.update(current)
    
    @staticmethod
    def print_info(message):
        print(f"{Colors.CYAN}[*]{Colors.RESET} {message}")
    
    @staticmethod
    def print_success(message):
        print(f"{Colors.GREEN}[+]{Colors.RESET} {message}")
    
    @staticmethod
    def print_warning(message):
        print(f"{Colors.YELLOW}[!]{Colors.RESET} {message}")
    
    @staticmethod
    def print_error(message):
        print(f"{Colors.RED}[-]{Colors.RESET} {message}")
    
    @staticmethod
    def print_debug(message):
        print(f"{Colors.LIGHT_BLACK}[D]{Colors.RESET} {message}")
    
    @staticmethod
    def print_table(headers, rows):
        col_widths = [len(h) for h in headers]
        
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        separator = "+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"
        
        print(f"\n{Colors.CYAN}{separator}{Colors.RESET}")
        
        header_row = "|" + "|".join([f" {h:<{col_widths[i]}} " for i, h in enumerate(headers)]) + "|"
        print(f"{Colors.BOLD}{header_row}{Colors.RESET}")
        print(f"{Colors.CYAN}{separator}{Colors.RESET}")
        
        for row in rows:
            data_row = "|" + "|".join([f" {str(cell):<{col_widths[i]}} " for i, cell in enumerate(row)]) + "|"
            print(f"{data_row}")
        
        print(f"{Colors.CYAN}{separator}{Colors.RESET}\n")
    
    @staticmethod
    def print_box(message, color=Colors.CYAN):
        lines = message.split('\n')
        max_len = max(len(line) for line in lines)
        
        print(f"\n{color}┌{'─' * (max_len + 2)}┐{Colors.RESET}")
        for line in lines:
            padding = max_len - len(line)
            print(f"{color}│{Colors.RESET} {line}{' ' * padding} {color}│{Colors.RESET}")
        print(f"{color}└{'─' * (max_len + 2)}┘{Colors.RESET}\n")
