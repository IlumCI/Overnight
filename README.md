## Overview
The **Overnight recon tool** is an automated reconnaissance and vulnerability assessment script designed for ethical hacking and Capture The Flag (CTF) challenges. It integrates various Kali Linux tools to perform tasks such as subdomain enumeration, web probing, directory brute-forcing, API fuzzing, parameter discovery, JWT attacks, GraphQL exploitation, and SSRF testing.

## Features
- **Subdomain Enumeration**: Uses `subfinder` to identify subdomains of a target.
- **Web Probing**: Uses `httpx` to check the status, title, and technologies of found subdomains.
- **Directory Brute-Forcing**: Uses `ffuf` to discover hidden directories.
- **API Fuzzing**: Uses `ffuf` to find potential API endpoints.
- **Parameter Discovery**: Uses `ffuf` to enumerate GET parameters.
- **JWT Token Bruteforce**: Uses `jwt_tool` to attempt JWT token attacks.
- **GraphQL Exploitation**: Uses `GraphQLmap` to analyze GraphQL endpoints.
- **SSRF Testing**: Uses `interactsh` to detect Server-Side Request Forgery vulnerabilities.
- **Automated Installation**: Checks for required tools and installs missing ones.
- **Logging and Output**: Saves results in JSON format within the `results/` directory.

---

## Configuration Options
The script allows for easy customization via variables and wordlists. Below are key configuration points:

### Target Configuration
Modify the `TARGET` variable to specify the domain you want to test:
```python
TARGET = "example.com"  # Change this to your target
```

### Output Directory
All results are stored in the `OUTPUT_DIR` directory. You can change this path:
```python
OUTPUT_DIR = "./results"
```

### Wordlists
The script uses pre-defined wordlists for different tasks. You can modify or replace these:
```python
WORDLISTS = {
    "subdomains": "subdomains.txt",
    "directories": "directories.txt",
    "params": "params.txt",
    "api_fuzz": "api_fuzz.txt",
    "jwt_secrets": "jwt_secrets.txt"
}
```
To add a new wordlist, create a file in `./wordlists` and update the `WORDLISTS` dictionary.

### Tool Installation
The script checks for necessary tools and installs missing ones. The `TOOLS` dictionary defines which tools are used:
```python
TOOLS = {
    "subfinder": "subfinder",
    "httpx": "httpx",
    "nuclei": "nuclei",
    "ffuf": "ffuf",
    "jwt_tool": "https://github.com/ticarpi/jwt_tool",
    "graphqlmap": "https://github.com/swisskyrepo/GraphQLmap",
    "interactsh": "https://github.com/projectdiscovery/interactsh",
    "dalfox": "https://github.com/hahwul/dalfox"
}
```
You can add more tools or modify installation methods by editing the `install_tools()` function.

---

## Customizing the Script

### Adding New Functionalities
To add a new scanning feature, define a new function and integrate it into the `main()` function. Example:
```python
def custom_scan():
    result = run_command(["nmap", "-A", TARGET])
    return result
```
Then, call this function inside `main()`:
```python
custom_scan()
```

### Modifying Scan Parameters
Each function uses predefined command-line arguments. You can tweak these for better performance:
```python
def dir_fuzz():
    result = run_command(["ffuf", "-w", os.path.join(WORDLIST_DIR, WORDLISTS["directories"]),
                          "-u", f"https://{TARGET}/FUZZ", "-recursion", "-fc", "403,404",
                          "-mc", "200,301,302", "-o", os.path.join(OUTPUT_DIR, "dirs.json")])
    return result
```
To change HTTP response codes to filter (`-fc`, `-mc`), modify their values.

---

## Running the Script
Ensure you have **Python 3** installed and execute:
```sh
chmod +x ov.py
./ov.py
```
If encountering permission issues, use:
```sh
python3 ov.py
```

### Dependencies
- Ensure you are running Kali Linux.
- Install missing dependencies manually if needed:
```sh
sudo apt update && sudo apt install -y subfinder httpx nuclei ffuf
```

---

## Conclusion
The Kali Multitool provides an automated solution for reconnaissance and vulnerability assessment. By modifying the configuration variables and adjusting command parameters, users can tailor the script to their specific needs. Future enhancements could include parallel execution and advanced output formatting.

