import os
import sys
import random

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    LIGHT_BLACK = '\033[90m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    LIGHT_BLUE = '\033[94m'
    LIGHT_MAGENTA = '\033[95m'
    LIGHT_CYAN = '\033[96m'
    LIGHT_WHITE = '\033[97m'
    
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    @staticmethod
    def remove_colors(text):
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
    
    @staticmethod
    def supports_color():
        if os.getenv('NO_COLOR'):
            return False
        if sys.platform in ('win32', 'cygwin') and 'TERM' not in os.environ:
            try:
                import colorama
                colorama.init()
                return True
            except ImportError:
                return False
        return True
    
    @classmethod
    def enable(cls):
        cls.RESET = '\033[0m'
        cls.BOLD = '\033[1m'
        cls.DIM = '\033[2m'
        cls.ITALIC = '\033[3m'
        cls.UNDERLINE = '\033[4m'
        cls.BLACK = '\033[30m'
        cls.RED = '\033[31m'
        cls.GREEN = '\033[32m'
        cls.YELLOW = '\033[33m'
        cls.BLUE = '\033[34m'
        cls.MAGENTA = '\033[35m'
        cls.CYAN = '\033[36m'
        cls.WHITE = '\033[37m'
        cls.LIGHT_BLACK = '\033[90m'
        cls.LIGHT_RED = '\033[91m'
        cls.LIGHT_GREEN = '\033[92m'
        cls.LIGHT_YELLOW = '\033[93m'
        cls.LIGHT_BLUE = '\033[94m'
        cls.LIGHT_MAGENTA = '\033[95m'
        cls.LIGHT_CYAN = '\033[96m'
        cls.LIGHT_WHITE = '\033[97m'
        cls.BG_BLACK = '\033[40m'
        cls.BG_RED = '\033[41m'
        cls.BG_GREEN = '\033[42m'
        cls.BG_YELLOW = '\033[43m'
        cls.BG_BLUE = '\033[44m'
        cls.BG_MAGENTA = '\033[45m'
        cls.BG_CYAN = '\033[46m'
        cls.BG_WHITE = '\033[47m'
    
    @classmethod
    def disable(cls):
        cls.RESET = ''
        cls.BOLD = ''
        cls.DIM = ''
        cls.ITALIC = ''
        cls.UNDERLINE = ''
        cls.BLACK = ''
        cls.RED = ''
        cls.GREEN = ''
        cls.YELLOW = ''
        cls.BLUE = ''
        cls.MAGENTA = ''
        cls.CYAN = ''
        cls.WHITE = ''
        cls.LIGHT_BLACK = ''
        cls.LIGHT_RED = ''
        cls.LIGHT_GREEN = ''
        cls.LIGHT_YELLOW = ''
        cls.LIGHT_BLUE = ''
        cls.LIGHT_MAGENTA = ''
        cls.LIGHT_CYAN = ''
        cls.LIGHT_WHITE = ''
        cls.BG_BLACK = ''
        cls.BG_RED = ''
        cls.BG_GREEN = ''
        cls.BG_YELLOW = ''
        cls.BG_BLUE = ''
        cls.BG_MAGENTA = ''
        cls.BG_CYAN = ''
        cls.BG_WHITE = ''

class BANNER:
    ASCII_ART = f"""
{Colors.CYAN}{Colors.BOLD}
    _   _ _   _ _______          _____ _    _       _   _                  
   | \ | | \ | |__   __|        / ____| |  | |     | \ | |                 
   |  \| |  \| |  | |  ______ | (___ | |__| | __ _|  \| | _____      __  
   | . ` | . ` |  | | |______| \___ \|  __  |/ _` | . ` |/ _ \ \ /\ / /  
   | |\  | |\  |  | |         ____) | |  | | (_| | |\  |  __/\ V  V /   
   |_| \_|_| \_|  |_|        |_____/|_|  |_|\__,_|_| \_|\___| \_/\_/    
                                                                            
{Colors.LIGHT_CYAN}    ========================================================================
                              SQL INJECTION SCANNER
                          Bug Hunter's Vulnerability Scanner
                                                                              
                               FOR AUTHORIZED USE ONLY
    ========================================================================
{Colors.LIGHT_MAGENTA}                                Version: 1.0.0
                                    Author: {Colors.CYAN}Rikixz{Colors.LIGHT_MAGENTA} (@blaxkmiradev)
{Colors.RESET}
"""

class ProgressBar:
    def __init__(self, total, prefix='Progress', length=50, fill='#'):
        self.total = total
        self.prefix = prefix
        self.length = length
        self.fill = fill
        self.current = 0
    
    def update(self, current=None):
        if current is not None:
            self.current = current
        else:
            self.current += 1
        
        percent = self.current / self.total
        filled = int(self.length * percent)
        bar = self.fill * filled + '░' * (self.length - filled)
        
        print(f'\r{self.prefix} |{Colors.CYAN}{bar}{Colors.RESET}| {percent:.0%} ({self.current}/{self.total})', end='', flush=True)
        
        if self.current >= self.total:
            print()
    
    def reset(self):
        self.current = 0

class Spinner:
    def __init__(self, message="Loading"):
        self.message = message
        self.frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.running = False
    
    def start(self):
        self.running = True
        import threading
        self.thread = threading.Thread(target=self._spin)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join(timeout=0.1)
        print('\r' + ' ' * (len(self.message) + 20), end='\r')
    
    def _spin(self):
        i = 0
        while self.running:
            frame = self.frames[i % len(self.frames)]
            print(f'\r{Colors.CYAN}{frame}{Colors.RESET} {self.message}...', end='', flush=True)
            i += 1
            import time
            time.sleep(0.1)
