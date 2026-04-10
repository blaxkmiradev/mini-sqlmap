import csv
import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import Colors

class CSVWriter:
    def __init__(self, filepath):
        self.filepath = filepath
    
    def write(self, data):
        try:
            with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
                if not data:
                    writer = csv.writer(f)
                    writer.writerow(['No vulnerabilities found'])
                    return True
                
                fieldnames = ['url', 'parameter', 'type', 'payload', 'method', 'db_type', 'error_message', 'evidence']
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for vuln in data:
                    row = {
                        'url': vuln.get('url', ''),
                        'parameter': vuln.get('parameter', ''),
                        'type': vuln.get('type', ''),
                        'payload': vuln.get('payload', ''),
                        'method': vuln.get('method', 'GET'),
                        'db_type': vuln.get('db_type', ''),
                        'error_message': vuln.get('error_message', ''),
                        'evidence': vuln.get('evidence', '')
                    }
                    writer.writerow(row)
            
            return True
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to write CSV: {e}")
            return False
