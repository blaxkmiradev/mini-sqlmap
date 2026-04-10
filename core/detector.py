import time
import random
import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import Colors
from utils.logger import Logger
from utils.helpers import Helpers

class Detector:
    def __init__(self, http_client, options=None):
        self.http = http_client
        self.options = options or {}
        self.logger = Logger()
        self.risk_level = self.options.get('risk', 1)
        
    def detect_boolean_blind(self, url, param, baseline_response, payload):
        response = self.http.test_payload(url, param, payload, technique='append')
        
        if not response.success:
            return False, None
        
        is_diff, msg = Helpers.is_vulnerable_response(
            response.text, 
            baseline_response.text
        )
        
        if is_diff:
            true_payload = payload.replace('false', 'true')
            false_payload = payload.replace('true', 'false')
            
            response_true = self.http.test_payload(url, param, true_payload, technique='append')
            response_false = self.http.test_payload(url, param, false_payload, technique='append')
            
            true_diff, _ = Helpers.is_vulnerable_response(response_true.text, baseline_response.text)
            false_diff, _ = Helpers.is_vulnerable_response(response_false.text, baseline_response.text)
            
            if true_diff and not false_diff:
                return True, {
                    'type': 'Boolean-based Blind',
                    'payload': payload,
                    'true_response': response_true.text[:200],
                    'false_response': response_false.text[:200] if response_false.success else None
                }
        
        return False, None
    
    def detect_error_based(self, url, param, baseline_response, payload, db_type=None):
        response = self.http.test_payload(url, param, payload, technique='append')
        
        if not response.success:
            return False, None
        
        error_msg = Helpers.extract_error_message(response.text, db_type)
        
        if error_msg:
            detected_db = Helpers.detect_db_type(error_msg)
            return True, {
                'type': 'Error-based',
                'payload': payload,
                'error_message': error_msg,
                'db_type': detected_db,
                'vulnerable': True
            }
        
        return False, None
    
    def detect_time_based(self, url, param, baseline_response, payload, sleep_time=5):
        response = self.http.test_payload(url, param, payload, technique='append')
        
        if not response.success:
            return False, None
        
        if response.elapsed_time >= sleep_time:
            return True, {
                'type': 'Time-based Blind',
                'payload': payload,
                'delay': response.elapsed_time,
                'expected_delay': sleep_time,
                'evidence': f"Response delayed by {response.elapsed_time:.2f}s"
            }
        
        return False, None
    
    def detect_union_based(self, url, param, baseline_response, payloads):
        for payload in payloads:
            response = self.http.test_payload(url, param, payload, technique='replace')
            
            if not response.success:
                continue
            
            if self._check_union_response(response, baseline_response):
                return True, {
                    'type': 'Union-based',
                    'payload': payload,
                    'evidence': 'Union query executed successfully'
                }
        
        return False, None
    
    def _check_union_response(self, response, baseline):
        if not response.success:
            return False
        
        if response.status_code == 500:
            return True
        
        if 'sql' in response.text.lower() or 'union' in response.text.lower():
            return True
        
        baseline_words = set(re.findall(r'\w+', baseline.text.lower()))
        response_words = set(re.findall(r'\w+', response.text.lower()))
        
        unique_in_response = response_words - baseline_words
        if len(unique_in_response) > 0:
            for word in unique_in_response:
                if any(keyword in word for keyword in ['version', 'user', 'database', 'table', 'column', 'admin']):
                    return True
        
        return False
    
    def detect_stacked_queries(self, url, param, baseline_response, payloads):
        for payload in payloads:
            response = self.http.test_payload(url, param, payload, technique='append')
            
            if not response.success:
                continue
            
            if response.status_code == 200:
                diff, _ = Helpers.is_vulnerable_response(response.text, baseline_response.text)
                if diff:
                    return True, {
                        'type': 'Stacked Queries',
                        'payload': payload,
                        'evidence': 'Additional query executed'
                    }
        
        return False, None
    
    def detect_all_types(self, url, param, baseline_response, payloads):
        vulnerabilities = []
        
        from payloads.blind import BOOLEAN_PAYLOADS
        from payloads.error import ERROR_PAYLOADS
        from payloads.time import TIME_PAYLOADS
        from payloads.union import UNION_PAYLOADS
        from payloads.stacked import STACKED_PAYLOADS
        
        self.logger.info(f"Testing {Colors.CYAN}{param}{Colors.RESET} parameter...")
        
        if self.risk_level >= 1:
            for payload in BOOLEAN_PAYLOADS[:5]:
                vulnerable, result = self.detect_boolean_blind(url, param, baseline_response, payload)
                if vulnerable:
                    vulnerabilities.append(result)
                    self.logger.success(f"Found: {Colors.GREEN}Boolean-based Blind SQLi{Colors.RESET}")
                    break
        
        for payload in ERROR_PAYLOADS[:5]:
            vulnerable, result = self.detect_error_based(url, param, baseline_response, payload)
            if vulnerable:
                vulnerabilities.append(result)
                self.logger.success(f"Found: {Colors.GREEN}Error-based SQLi{Colors.RESET}")
                break
        
        if self.risk_level >= 2:
            for payload in TIME_PAYLOADS[:5]:
                vulnerable, result = self.detect_time_based(url, param, baseline_response, payload, sleep_time=3)
                if vulnerable:
                    vulnerabilities.append(result)
                    self.logger.success(f"Found: {Colors.GREEN}Time-based Blind SQLi{Colors.RESET}")
                    break
            
            for payload in UNION_PAYLOADS[:3]:
                vulnerable, result = self.detect_union_based(url, param, baseline_response, [payload])
                if vulnerable:
                    vulnerabilities.append(result)
                    self.logger.success(f"Found: {Colors.GREEN}Union-based SQLi{Colors.RESET}")
                    break
        
        if self.risk_level >= 3:
            for payload in STACKED_PAYLOADS[:3]:
                vulnerable, result = self.detect_stacked_queries(url, param, baseline_response, [payload])
                if vulnerable:
                    vulnerabilities.append(result)
                    self.logger.success(f"Found: {Colors.GREEN}Stacked Queries SQLi{Colors.RESET}")
                    break
        
        return vulnerabilities
