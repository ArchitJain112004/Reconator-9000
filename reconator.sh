#!/bin/bash
# Reconator 9000 - Elite Recon Script
# Author: Archit

TARGET=$1
WORDLIST="/usr/share/wordlists/dirb/common.txt"
NUCLEI_TEMPLATES="$HOME/nuclei-templates"
OUTDIR="recon_$TARGET"
TIMESTAMP=$(date +%F_%T)

mkdir -p "$OUTDIR"

echo "[+] Recon started on $TARGET at $TIMESTAMP"
echo "[+] Output directory: $OUTDIR"

# Subdomain enumeration
echo "[*] Finding subdomains..."
subfinder -d "$TARGET" -silent > "$OUTDIR/subdomains.txt"

# Port scanning with service detection
echo "[*] Running Nmap scan..."
nmap -sV -T4 "$TARGET" > "$OUTDIR/nmap.txt"

# Header inspection
echo "[*] Fetching HTTP headers..."
curl -sI "https://$TARGET" > "$OUTDIR/headers.txt"

# Directory brute-forcing
echo "[*] Running Gobuster..."
gobuster dir -u "https://$TARGET" -w "$WORDLIST" -l > "$OUTDIR/dirb.txt"

# JavaScript scraping and secrets discovery
echo "[*] Scraping JavaScript files..."
mkdir -p "$OUTDIR/js_files"
wget -r -l2 -nd -A js "https://$TARGET" -P "$OUTDIR/js_files/" 2>/dev/null
grep -iE 'key|token|auth|api|secret' "$OUTDIR/js_files"/*.js > "$OUTDIR/js_secrets.txt" 2>/dev/null

# Nuclei vulnerability scanning
echo "[*] Running nuclei..."
nuclei -u "https://$TARGET" -t "$NUCLEI_TEMPLATES" -o "$OUTDIR/nuclei.txt"

# Archive discovery
if command -v waybackurls &>/dev/null; then
    echo "[*] Pulling Wayback URLs..."
    echo "$TARGET" | waybackurls > "$OUTDIR/wayback.txt"
fi

echo "[+] Recon completed! Results stored in $OUTDIR/"
