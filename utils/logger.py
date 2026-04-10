import sys
import datetime
import os
from .colors import Colors

class Logger:
    LOG_LEVELS = {
        'DEBUG': 0,
        'INFO': 1,
        'SUCCESS': 2,
        'WARNING': 3,
        'ERROR': 4,
        'CRITICAL': 5
    }
    
    def __init__(self, name="MiniSQLMap", level='INFO'):
        self.name = name
        self.level = level
        self.log_file = None
        self.log_to_file = False
    
    def set_level(self, level):
        self.level = level.upper()
    
    def set_log_file(self, filepath):
        self.log_file = filepath
        self.log_to_file = True
        try:
            with open(filepath, 'a') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"Log started at {self._get_timestamp()}\n")
                f.write(f"{'='*60}\n")
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to create log file: {e}")
    
    def _get_timestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _log(self, level, message, *args, **kwargs):
        if self.LOG_LEVELS.get(level, 0) < self.LOG_LEVELS.get(self.level, 1):
            return
        
        timestamp = self._get_timestamp()
        prefix = kwargs.get('prefix', '')
        
        colors = {
            'DEBUG': Colors.LIGHT_BLACK,
            'INFO': Colors.CYAN,
            'SUCCESS': Colors.GREEN,
            'WARNING': Colors.YELLOW,
            'ERROR': Colors.RED,
            'CRITICAL': Colors.RED + Colors.BOLD
        }
        
        color = colors.get(level, Colors.WHITE)
        symbol = {
            'DEBUG': '[D]',
            'INFO': '[*]',
            'SUCCESS': '[+]',
            'WARNING': '[!]',
            'ERROR': '[-]',
            'CRITICAL': '[!CRITICAL!]'
        }.get(level, '[]')
        
        formatted_message = f"{Colors.DIM}{timestamp}{Colors.RESET} {color}{symbol}{Colors.RESET} {prefix}{message}"
        
        if args:
            formatted_message = formatted_message.format(*args)
        
        print(formatted_message)
        
        if self.log_to_file and self.log_file:
            clean_message = Colors.remove_colors(formatted_message)
            try:
                with open(self.log_file, 'a') as f:
                    f.write(f"{clean_message}\n")
            except Exception:
                pass
    
    def debug(self, message, *args, **kwargs):
        self._log('DEBUG', message, *args, **kwargs)
    
    def info(self, message, *args, **kwargs):
        self._log('INFO', message, *args, **kwargs)
    
    def success(self, message, *args, **kwargs):
        self._log('SUCCESS', message, *args, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        self._log('WARNING', message, *args, **kwargs)
    
    def error(self, message, *args, **kwargs):
        self._log('ERROR', message, *args, **kwargs)
    
    def critical(self, message, *args, **kwargs):
        self._log('CRITICAL', message, *args, **kwargs)

    @staticmethod
    def banner():
        from .colors import BANNER
        print(BANNER.ASCII_ART)
    
    @staticmethod
    def print_box(text, color=Colors.CYAN):
        lines = text.split('\n')
        max_len = max(len(line) for line in lines)
        
        print(f"{color}+{'-' * (max_len + 2)}+{Colors.RESET}")
        for line in lines:
            padding = max_len - len(line)
            print(f"{color}|{Colors.RESET} {line}{' ' * padding} {color}|{Colors.RESET}")
        print(f"{color}+{'-' * (max_len + 2)}+{Colors.RESET}")
    
    @staticmethod
    def print_header(text):
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{text.center(60)}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")
    
    @staticmethod
    def print_section(title):
        print(f"\n{Colors.YELLOW}{Colors.BOLD}{title}{Colors.RESET}")
        print(f"{Colors.YELLOW}{'-' * len(title)}{Colors.RESET}\n")

logger = Logger()
