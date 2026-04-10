# 🕵️ Mini SQLMap - Bug Hunter's SQL Injection Scanner

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-red.svg)

**⚠️ DISCLAIMER: FOR AUTHORIZED SECURITY TESTING ONLY ⚠️**

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Examples](#-examples)
- [Project Structure](#-project-structure)
- [Detection Techniques](#-detection-techniques)
- [Contributing](#-contributing)
- [License](#-license)
- [Credits](#-credits)

---

## ✨ Features

### Core Scanning
- **SQL Injection Detection** - Detects multiple SQL injection types:
  - Boolean-based blind
  - Error-based
  - Time-based blind
  - Union-based
  - Stacked queries
  - Out-of-band

### Database Support
- MySQL
- PostgreSQL
- Microsoft SQL Server
- Oracle
- SQLite
- MariaDB

### Scanning Modes
- Single URL scan
- Multiple URLs from file
- Crawl target website
- Test specific parameters

### Output Options
- Console output with colors
- JSON report
- HTML report
- XML report
- CSV export

### Advanced Features
- Cookie support
- Custom headers
- User-Agent spoofing
- Proxy support
- Rate limiting
- Request delay
- Timeout configuration
- Random User-Agents

---

## 🔧 Installation

### Requirements
```
Python 3.8+
requests
colorama
beautifulsoup4
lxml
```

### Quick Install

```bash
# Clone the repository
git clone https://github.com/blaxkmiradev/mini-sqlmap.git
cd mini-sqlmap

# Install dependencies
pip install -r requirements.txt

# Run
python mini_sqlmap.py --help
```

### Using Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
python mini_sqlmap.py --help
```

---

## 📖 Usage

### Basic Usage

```bash
# Single URL scan
python mini_sqlmap.py -u "http://target.com/page?id=1"

# Scan with cookies
python mini_sqlmap.py -u "http://target.com/page?id=1" --cookie="PHPSESSID=abc123"

# Scan with custom headers
python mini_sqlmap.py -u "http://target.com/page?id=1" -H "Authorization: Bearer token"

# Batch scan from file
python mini_sqlmap.py -m urls.txt

# Verbose output
python mini_sqlmap.py -u "http://target.com/page?id=1" -v 3
```

### Advanced Options

```bash
# Set database type to test
python mini_sqlmap.py -u "http://target.com/page?id=1" --dbms=MySQL

# Set risk level (1-3)
python mini_sqlmap.py -u "http://target.com/page?id=1" --risk=2

# Set verbosity level (0-6)
python mini_sqlmap.py -u "http://target.com/page?id=1" -v 4

# Use proxy
python mini_sqlmap.py -u "http://target.com/page?id=1" --proxy="http://127.0.0.1:8080"

# Random delay between requests
python mini_sqlmap.py -u "http://target.com/page?id=1" --delay=1

# Set timeout
python mini_sqlmap.py -u "http://target.com/page?id=1" --timeout=30

# Crawl website
python mini_sqlmap.py -u "http://target.com/" --crawl=3

# Save output to file
python mini_sqlmap.py -u "http://target.com/page?id=1" -o results.json

# Output format
python mini_sqlmap.py -u "http://target.com/page?id=1" --format=html -o report.html
```

---

## 💡 Examples

### Example 1: Basic Scan
```bash
python mini_sqlmap.py -u "http://testphp.vulnweb.com/listproducts.php?cat=1"
```

### Example 2: Authenticated Scan
```bash
python mini_sqlmap.py -u "http://target.com/admin/search" \
    --cookie="session=eyJ..." \
    --data="search=term"
```

### Example 3: Full Scan with Report
```bash
python mini_sqlmap.py -u "http://target.com/page?id=1" \
    --risk=2 \
    --verbosity=3 \
    --format=json \
    -o vulnerability_report.json
```

### Example 4: Batch Scanning
```bash
# Create urls.txt with one URL per line
echo "http://target1.com/page?id=1" > urls.txt
echo "http://target2.com/product?id=5" >> urls.txt

python mini_sqlmap.py -m urls.txt --format=csv -o batch_results.csv
```

---

## 📁 Project Structure

```
mini-sqlmap/
├── mini_sqlmap.py          # Main entry point
├── core/
│   ├── __init__.py
│   ├── scanner.py          # Main scanning engine
│   ├── detector.py         # Vulnerability detection
│   ├── payloads.py         # SQL injection payloads
│   ├── http_client.py      # HTTP request handler
│   ├── database.py         # Database fingerprinting
│   └── crawler.py          # Website crawler
├── payloads/
│   ├── __init__.py
│   ├── blind.py            # Boolean-based payloads
│   ├── error.py            # Error-based payloads
│   ├── time.py             # Time-based payloads
│   ├── union.py            # Union-based payloads
│   └── stacked.py          # Stacked queries payloads
├── output/
│   ├── __init__.py
│   ├── console.py          # Console output with colors
│   ├── json_writer.py      # JSON report generator
│   ├── html_writer.py      # HTML report generator
│   └── csv_writer.py       # CSV export
├── utils/
│   ├── __init__.py
│   ├── colors.py           # Color definitions
│   ├── logger.py           # Logging utilities
│   └── helpers.py          # Helper functions
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── LICENSE                # MIT License
```

---

## 🔍 Detection Techniques

### 1. Boolean-Based Blind SQL Injection
Tests if True/False queries produce different responses.

**Example Payload:**
```sql
' OR '1'='1
' AND '1'='2
```

### 2. Error-Based SQL Injection
Triggers database errors that reveal information.

**Example Payload:**
```sql
' AND EXTRACTVALUE(1,CONCAT(0x7e,version()))--
```

### 3. Time-Based Blind SQL Injection
Uses sleep/delay functions to infer results.

**Example Payload:**
```sql
' AND SLEEP(5)--
' OR (SELECT CASE WHEN 1=1 THEN SLEEP(3) ELSE 0 END)--
```

### 4. Union-Based SQL Injection
Uses UNION to extract data from other tables.

**Example Payload:**
```sql
' UNION SELECT NULL--
' UNION SELECT username,password FROM users--
```

### 5. Stacked Queries
Executes multiple statements.

**Example Payload:**
```sql
'; DROP TABLE users--
'; SELECT * FROM users--
```

---

## 🎨 Output Colors

| Color | Meaning |
|-------|---------|
| 🔴 Red | Critical/Vulnerable |
| 🟡 Yellow | Warning/Medium Risk |
| 🟢 Green | Safe/No Issues |
| 🔵 Blue | Information |
| 🟣 Purple | Debug/Dev Info |
| ⚪ White | Normal Output |
| ⚫ Gray | Verbose Details |

---

## 📊 Risk Levels

| Level | Name | Description |
|-------|------|-------------|
| 1 | Low | Safe payloads, minimal impact |
| 2 | Medium | More aggressive, may modify data |
| 3 | High | Potentially destructive, use with caution |

---

## 🤝 Contributing

Contributions are welcome! Please read the guidelines first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ⚠️ Legal Disclaimer

**THIS TOOL IS FOR EDUCATIONAL AND AUTHORIZED SECURITY TESTING PURPOSES ONLY.**

- Only scan URLs you have permission to test
- Unauthorized scanning is illegal and punishable by law
- The authors are not responsible for misuse of this tool
- Always obtain written permission before security testing
- Use responsibly and ethically

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Made with ❤️ by [Rikixz](https://github.com/blaxkmiradev)**

[![GitHub](https://img.shields.io/badge/GitHub-blaxkmiradev-333?style=flat&logo=github)](https://github.com/blaxkmiradev)

---

## ⭐ Show Your Support

If this project helped you, please give it a ⭐!

---

<div align="center">

**Happy Hunting! 🎯**

</div>
