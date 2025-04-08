#!/bin/bash

# ░█▀▄░█▀▀░█▀▀░█▀▀░█▄█░▀█▀░█▀▀
# ░█▀▄░█▀▀░█▀▀░█▀▀░█░█░░█░░▀▀█
# ░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀
#         Reconator 9000 - Elite Recon Suite

TARGET=$1
if [ -z "$TARGET" ]; then
    echo "[!] Usage: $0 <domain>"
    exit 1
fi

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
OUTDIR="recon_${TARGET}_${TIMESTAMP}"
mkdir -p "$OUTDIR" "$OUTDIR/js_files"

WORDLIST="/usr/share/wordlists/dirb/common.txt"
NUCLEI_TEMPLATES="$HOME/nuclei-templates"
SUMMARY="$OUTDIR/_SUMMARY.txt"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

log_summary() {
    echo -e "$1" >> "$SUMMARY"
}

check_tool() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}[!] $1 not installed. Skipping...${NC}"
        log_summary "[!] $1 not installed."
        return 1
    fi
    return 0
}

smart_protocol() {
    echo -e "${GREEN}[+] Detecting protocol...${NC}"
    if curl --head --silent --fail "https://$TARGET" > /dev/null; then
        echo "https"
    else
        echo "http"
    fi
}

echo -e "${GREEN}[+] Starting Reconator 9000 on $TARGET${NC}"
log_summary "🔍 Recon started on $TARGET"
log_summary "🕒 Timestamp: $TIMESTAMP"

# 1. Subdomains
if check_tool subfinder; then
    echo -e "${GREEN}[+] Running subfinder...${NC}"
    subfinder -d "$TARGET" -silent | tee "$OUTDIR/subdomains.txt"
    log_summary "✅ Subfinder run successfully"
fi

# 2. Nmap
if check_tool nmap; then
    echo -e "${GREEN}[+] Running Nmap...${NC}"
    nmap -sV -T4 "$TARGET" | tee "$OUTDIR/nmap.txt"
    log_summary "✅ Nmap completed"
fi

# 3. Header Info
PROTO=$(smart_protocol)
if check_tool curl; then
    echo -e "${GREEN}[+] Fetching HTTP headers...${NC}"
    curl -I "$PROTO://$TARGET" > "$OUTDIR/headers.txt"
    log_summary "✅ Headers fetched using $PROTO"
fi

# 4. Dirbusting
if check_tool gobuster; then
    echo -e "${GREEN}[+] Brute-forcing directories...${NC}"
    gobuster dir -u "$PROTO://$TARGET" -w "$WORDLIST" -l | tee "$OUTDIR/dirb.txt"
    log_summary "✅ Directory scan done"
fi

# 5. JavaScript & Secrets
if check_tool wget; then
    echo -e "${GREEN}[+] Downloading JS files...${NC}"
    wget -r -l2 -nd -A js "$PROTO://$TARGET" -P "$OUTDIR/js_files" 2>/dev/null
    echo -e "${GREEN}[+] Searching for secrets in JS files...${NC}"
    grep -iE 'key|token|auth|api|secret' "$OUTDIR/js_files"/*.js 2>/dev/null > "$OUTDIR/js_secrets.txt"
    log_summary "✅ JS scraping done"
fi

# 6. Nuclei
if check_tool nuclei; then
    echo -e "${GREEN}[+] Running nuclei scan...${NC}"
    nuclei -u "$PROTO://$TARGET" -t "$NUCLEI_TEMPLATES" -o "$OUTDIR/nuclei.txt"
    log_summary "✅ Nuclei scan completed"
fi

# 7. Wayback
if check_tool waybackurls; then
    echo -e "${GREEN}[+] Pulling Wayback URLs...${NC}"
    echo "$TARGET" | waybackurls > "$OUTDIR/wayback.txt"
    log_summary "✅ Wayback URLs collected"
fi

# Final Summary
echo -e "\n${GREEN}[+] Recon complete! All data saved in: $OUTDIR/${NC}"
log_summary "✅ Reconator 9000 complete!"
log_summary "📁 All outputs in: $OUTDIR"
