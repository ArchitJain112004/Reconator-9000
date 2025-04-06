#!/bin/bash
# Author: Archit
TARGET=$1
WORDLIST="/usr/share/wordlists/dirb/common.txt"
NUCLEI_TEMPLATES="$HOME/nuclei-templates"
OUTDIR="recon_$TARGET"

mkdir -p $OUTDIR

echo "[+] Starting Recon on $TARGET"
echo "[+] Output Directory: $OUTDIR"

echo "[+] Finding Subdomains..."
subfinder -d $TARGET -silent | tee $OUTDIR/subdomains.txt

echo "[+] Running Nmap..."
nmap -sV -T4 $TARGET | tee $OUTDIR/nmap.txt

echo "[+] Fetching Headers..."
curl -I https://$TARGET > $OUTDIR/headers.txt

echo "[+] Brute-forcing directories..."
gobuster dir -u https://$TARGET -w $WORDLIST -l | tee $OUTDIR/dirb.txt

echo "[+] Scraping JS files..."
wget -r -l2 -nd -A js https://$TARGET -P $OUTDIR/js_files/ 2>/dev/null
grep -iE 'key|token|auth|api|secret' $OUTDIR/js_files/*.js > $OUTDIR/js_secrets.txt

echo "[+] Running nuclei scan..."
nuclei -u https://$TARGET -t $NUCLEI_TEMPLATES -o $OUTDIR/nuclei.txt

echo "[+] Pulling waybackurls (if installed)..."
command -v waybackurls &> /dev/null && echo $TARGET | waybackurls > $OUTDIR/wayback.txt

echo "[+] Recon Complete! All results saved in $OUTDIR/"
