#!/bin/bash

# Author: Archit Jain | Reconator 9000 Elite
# Purpose: Perform a full recon on a target

TARGET=$1
WORDLIST="/usr/share/wordlists/dirb/common.txt"
NUCLEI_TEMPLATES="$HOME/nuclei-templates"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
OUTDIR="recon_${TARGET}_${TIMESTAMP}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Tool Check
check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}[!] Tool $1 is not installed. Skipping...${NC}"
        return 1
    fi
    return 0
}

# Create output directory
mkdir -p "$OUTDIR"
echo -e "${GREEN}[+] Starting Recon on $TARGET${NC}"
echo "[+] Output Directory: $OUTDIR"

# Subdomain Enumeration
if check_tool subfinder; then
    echo -e "${GREEN}[+] Finding Subdomains...${NC}"
    subfinder -d "$TARGET" -silent | tee "$OUTDIR/subdomains.txt"
fi

# Nmap Scan
if check_tool nmap; then
    echo -e "${GREEN}[+] Running Nmap...${NC}"
    nmap -sV -T4 "$TARGET" | tee "$OUTDIR/nmap.txt"
fi

# HTTP/HTTPS check
PROTOCOL="https"
curl --head --silent --fail "$PROTOCOL://$TARGET" > /dev/null || PROTOCOL="http"

# Header Fetch
if check_tool curl; then
    echo -e "${GREEN}[+] Fetching Headers using $PROTOCOL...${NC}"
    curl -I "$PROTOCOL://$TARGET" > "$OUTDIR/headers.txt"
fi

# Directory Brute Force
if check_tool gobuster; then
    echo -e "${GREEN}[+] Brute-forcing directories...${NC}"
    gobuster dir -u "$PROTOCOL://$TARGET" -w "$WORDLIST" -l | tee "$OUTDIR/dirb.txt"
fi

# JS Scraping
if check_tool wget; then
    echo -e "${GREEN}[+] Scraping JS files...${NC}"
    mkdir -p "$OUTDIR/js_files"
    wget -r -l2 -nd -A js "$PROTOCOL://$TARGET" -P "$OUTDIR/js_files/" 2>/dev/null
    grep -iE 'key|token|auth|api|secret' "$OUTDIR/js_files/"*.js > "$OUTDIR/js_secrets.txt" 2>/dev/null
fi

# Nuclei Scan
if check_tool nuclei; then
    echo -e "${GREEN}[+] Running Nuclei Scan...${NC}"
    nuclei -u "$PROTOCOL://$TARGET" -t "$NUCLEI_TEMPLATES" -o "$OUTDIR/nuclei.txt"
fi

# Wayback URLs
if check_tool waybackurls; then
    echo -e "${GREEN}[+] Pulling Wayback URLs...${NC}"
    echo "$TARGET" | waybackurls > "$OUTDIR/wayback.txt"
fi

echo -e "${GREEN}[+] Recon Complete! All results saved in $OUTDIR/${NC}"
