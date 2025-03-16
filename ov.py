#!/usr/bin/env python3
import os
import subprocess
import json
import time
from datetime import datetime

# Configuration
TARGET = "example.com"  # Change this to your target
OUTPUT_DIR = "./results"
WORDLIST_DIR = "./wordlists"
TOOLS_DIR = "./tools"
LOG_FILE = os.path.join(OUTPUT_DIR, "log.txt")

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(WORDLIST_DIR, exist_ok=True)
os.makedirs(TOOLS_DIR, exist_ok=True)

# Wordlists
WORDLISTS = {
    "subdomains": "subdomains.txt",
    "directories": "directories.txt",
    "params": "params.txt",
    "api_fuzz": "api_fuzz.txt",
    "jwt_secrets": "jwt_secrets.txt"
}

# Tools to install if not in Kali repo
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

# Function to check wordlists
def check_wordlists():
    for key, filename in WORDLISTS.items():
        path = os.path.join(WORDLIST_DIR, filename)
        if not os.path.exists(path):
            print(f"[!] Missing {key} wordlist: {path}")

# Function to install tools
def install_tools():
    for tool, package in TOOLS.items():
        if subprocess.run(["which", tool], capture_output=True).returncode != 0:
            if package.startswith("http"):
                tool_path = os.path.join(TOOLS_DIR, tool)
                if not os.path.exists(tool_path):
                    subprocess.run(["git", "clone", package, tool_path], check=True)
                    print(f"Installed {tool} from source")
            else:
                subprocess.run(["sudo", "apt", "install", "-y", package], check=True)
                print(f"Installed {tool} from Kali repo")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def run_command(command):
    log(f"Running: {' '.join(command)}")
    try:
        output = subprocess.run(command, capture_output=True, text=True, check=True)
        return output.stdout
    except subprocess.CalledProcessError as e:
        log(f"Error: {e}")
        return ""

# Subdomain enumeration
def subdomain_enum():
    subdomains_file = os.path.join(OUTPUT_DIR, "subdomains.json")
    result = run_command(["subfinder", "-d", TARGET, "-all", "-oJ", subdomains_file])
    return result

# Web Probing
def web_probe():
    web_alive_file = os.path.join(OUTPUT_DIR, "web_alive.json")
    result = run_command(["httpx", "-l", os.path.join(OUTPUT_DIR, "subdomains.json"), "-status-code", "-title", "-tech-detect", "-oJ", web_alive_file])
    return result

# Directory brute-force
def dir_fuzz():
    result = run_command(["ffuf", "-w", os.path.join(WORDLIST_DIR, WORDLISTS["directories"]), "-u", f"https://{TARGET}/FUZZ", "-recursion", "-fc", "403,404", "-mc", "200,301,302", "-o", os.path.join(OUTPUT_DIR, "dirs.json")])
    return result

# API fuzzing
def api_fuzz():
    result = run_command(["ffuf", "-w", os.path.join(WORDLIST_DIR, WORDLISTS["api_fuzz"]), "-u", f"https://{TARGET}/api/FUZZ", "-recursion", "-fc", "403,404", "-mc", "200,201,202,301,302", "-o", os.path.join(OUTPUT_DIR, "api.json")])
    return result

# Parameter discovery
def param_fuzz():
    result = run_command(["ffuf", "-w", os.path.join(WORDLIST_DIR, WORDLISTS["params"]), "-u", f"https://{TARGET}/?FUZZ=1", "-mc", "200,302", "-o", os.path.join(OUTPUT_DIR, "params.json")])
    return result

# JWT Token Bruteforce
def jwt_attack():
    jwt_file = os.path.join(OUTPUT_DIR, "jwt_results.json")
    result = run_command(["jwt_tool", "-t", f"https://{TARGET}", "-brute", "-o", jwt_file])
    return result

# GraphQL Exploitation
def graphql_attack():
    gql_file = os.path.join(OUTPUT_DIR, "graphql.json")
    result = run_command(["python3", os.path.join(TOOLS_DIR, "graphqlmap", "graphqlmap.py"), "-u", f"https://{TARGET}/graphql", "--json", gql_file])
    return result

# SSRF Testing
def ssrf_attack():
    ssrf_file = os.path.join(OUTPUT_DIR, "ssrf.json")
    result = run_command(["interactsh-client", "-json", "-o", ssrf_file])
    return result

# Main execution
def main():
    install_tools()
    check_wordlists()
    subdomain_enum()
    web_probe()
    dir_fuzz()
    api_fuzz()
    param_fuzz()
    jwt_attack()
    graphql_attack()
    ssrf_attack()
    print("\n[+] Scan Complete. Check results in the results/ folder.")

if __name__ == "__main__":
    main()
