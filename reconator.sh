#!/bin/bash

# Author: Archit Jain
# Project: Reconator 9000 🚀

TARGET=$1
WORDLIST="/usr/share/wordlists/dirb/common.txt"
NUCLEI_TEMPLATES="$HOME/nuclei-templates"
OUTDIR="recon_$TARGET"

# Colors
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
CYAN="\033[0;36m"
RESET="\033[0m"

# Header
echo -e "${CYAN}╔════════════════════════════╗"
echo -e "║   Starting Reconator 9000  ║"
echo -e "╚════════════════════════════╝${RESET}"

# Check for target
if [ -z "$TARGET" ]; then
    echo -e "${RED}[!] Usage: $0 <target-domain>${RESET}"
    exit 1
fi

mkdir -p "$OUTDIR"
echo -e "${GREEN}[+] Target: $TARGET"
echo -e "[+] Output Directory: $OUTDIR${RESET}"

# Function to check if tool exists
check_tool() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}[!] Tool $1 not found! Skipping...${RESET}"
        return 1
    fi
}

# Subfinder
check_tool subfinder && {
    echo -e "${YELLOW}[+] Finding Subdomains...${RESET}"
    subfinder -d "$TARGET" -silent | tee "$OUTDIR/subdomains.txt"
}

# Nmap
check_tool nmap && {
    echo -e "${YELLOW}[+] Running Nmap...${RESET}"
    nmap -sV -T4 "$TARGET" | tee "$OUTDIR/nmap.txt"
}

# Headers
check_tool curl && {
    echo -e "${YELLOW}[+] Fetching Headers...${RESET}"
    curl -I "https://$TARGET" > "$OUTDIR/headers.txt"
}

# Gobuster
check_tool gobuster && {
    echo -e "${YELLOW}[+] Brute-forcing Directories...${RESET}"
    gobuster dir -u "https://$TARGET" -w "$WORDLIST" -l | tee "$OUTDIR/dirb.txt"
}

# JS File Scraping
check_tool wget && {
    echo -e "${YELLOW}[+] Scraping JavaScript Files...${RESET}"
    mkdir -p "$OUTDIR/js_files"
    wget -r -l2 -nd -A js "https://$TARGET" -P "$OUTDIR/js_files/" 2>/dev/null
    grep -iE 'key|token|auth|api|secret' "$OUTDIR/js_files/"*.js > "$OUTDIR/js_secrets.txt" 2>/dev/null
}

# Nuclei
check_tool nuclei && {
    echo -e "${YELLOW}[+] Running Nuclei Scan...${RESET}"
    nuclei -u "https://$TARGET" -t "$NUCLEI_TEMPLATES" -o "$OUTDIR/nuclei.txt"
}

# Waybackurls
check_tool waybackurls && {
    echo -e "${YELLOW}[+] Pulling Wayback URLs...${RESET}"
    echo "$TARGET" | waybackurls > "$OUTDIR/wayback.txt"
}

echo -e "${GREEN}[✓] Recon Complete!"
echo -e "[✓] All results saved in $OUTDIR/"
echo -e "[✓] Time: $(date)${RESET}"
