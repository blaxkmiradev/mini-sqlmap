import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import Colors

class HTMLWriter:
    def __init__(self, filepath):
        self.filepath = filepath
    
    def write(self, data, summary=None):
        try:
            html_content = self._generate_html(data, summary)
            
            with open(self.filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return True
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to write HTML: {e}")
            return False
    
    def _generate_html(self, data, summary):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        vuln_rows = ""
        for i, vuln in enumerate(data, 1):
            vuln_rows += f"""
            <tr>
                <td>{i}</td>
                <td><code>{vuln.get('type', 'Unknown')}</code></td>
                <td><a href="{vuln.get('url', '#')}">{vuln.get('url', 'N/A')[:50]}...</a></td>
                <td><code>{vuln.get('parameter', 'N/A')}</code></td>
                <td><code>{vuln.get('method', 'GET')}</code></td>
                <td><code class="payload">{vuln.get('payload', 'N/A')}</code></td>
                <td>{vuln.get('db_type', 'Unknown')}</td>
            </tr>
            """
        
        if not vuln_rows:
            vuln_rows = "<tr><td colspan='7' style='text-align:center;'>No vulnerabilities found</td></tr>"
        
        vuln_count = len(data)
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini SQLMap - Vulnerability Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            padding: 20px;
            color: #e0e0e0;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 30px;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            color: #00d9ff;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(0,217,255,0.3);
        }}
        
        .header p {{
            color: #888;
            font-size: 1.1em;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-card h3 {{
            color: #888;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        
        .stat-card .value {{
            font-size: 2em;
            font-weight: bold;
        }}
        
        .stat-card.vulnerabilities .value {{
            color: #ff4757;
        }}
        
        .stat-card.safe .value {{
            color: #2ed573;
        }}
        
        .stat-card.time .value {{
            color: #ffa502;
        }}
        
        .section {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .section h2 {{
            color: #00d9ff;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(0,217,255,0.3);
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        th {{
            background: rgba(0,217,255,0.1);
            color: #00d9ff;
            padding: 15px 10px;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 12px 10px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        
        tr:hover {{
            background: rgba(255,255,255,0.03);
        }}
        
        code {{
            background: rgba(0,0,0,0.3);
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        code.payload {{
            color: #ff6b6b;
            word-break: break-all;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .badge-danger {{
            background: rgba(255,71,87,0.2);
            color: #ff4757;
        }}
        
        .badge-warning {{
            background: rgba(255,165,2,0.2);
            color: #ffa502;
        }}
        
        .badge-info {{
            background: rgba(0,217,255,0.2);
            color: #00d9ff;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}
        
        .footer a {{
            color: #00d9ff;
            text-decoration: none;
        }}
        
        .disclaimer {{
            background: rgba(255,71,87,0.1);
            border: 1px solid rgba(255,71,87,0.3);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        
        .disclaimer strong {{
            color: #ff4757;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🕵️ Mini SQLMap Report</h1>
            <p>Vulnerability Scan Report - {timestamp}</p>
        </div>
        
        <div class="disclaimer">
            <strong>⚠️ DISCLAIMER:</strong> This report is for authorized security testing only. 
            Unauthorized scanning is illegal.
        </div>
        
        <div class="stats">
            <div class="stat-card vulnerabilities">
                <h3>Vulnerabilities Found</h3>
                <div class="value">{vuln_count}</div>
            </div>
            <div class="stat-card safe">
                <h3>Status</h3>
                <div class="value">{'VULNERABLE' if vuln_count > 0 else 'SAFE'}</div>
            </div>
            <div class="stat-card time">
                <h3>Generated</h3>
                <div class="value">{timestamp.split()[1]}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 Vulnerability Details</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Type</th>
                        <th>URL</th>
                        <th>Parameter</th>
                        <th>Method</th>
                        <th>Payload</th>
                        <th>Database</th>
                    </tr>
                </thead>
                <tbody>
                    {vuln_rows}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Generated by <a href="https://github.com/blaxkmiradev/mini-sqlmap">Mini SQLMap</a></p>
            <p>Version 1.0.0 | By Rikixz (@blaxkmiradev)</p>
        </div>
    </div>
</body>
</html>
        """
        return html
