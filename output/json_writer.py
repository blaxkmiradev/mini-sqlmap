import json
import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import Colors

class JSONWriter:
    def __init__(self, filepath):
        self.filepath = filepath
    
    def write(self, data):
        try:
            output = {
                'scan_info': {
                    'timestamp': datetime.datetime.now().isoformat(),
                    'tool': 'Mini SQLMap',
                    'version': '1.0.0'
                },
                'results': data
            }
            
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4, default=str)
            
            return True
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to write JSON: {e}")
            return False
    
    @staticmethod
    def format_vulnerability(vuln):
        return {
            'url': vuln.get('url'),
            'parameter': vuln.get('parameter'),
            'type': vuln.get('type'),
            'payload': vuln.get('payload'),
            'method': vuln.get('method'),
            'db_type': vuln.get('db_type'),
            'error_message': vuln.get('error_message'),
            'evidence': vuln.get('evidence')
        }
