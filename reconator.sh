#!/bin/bash
# Reconator 9000 Elite - GUI Frontend
# Author: Archit
# Description: PyQt5-based interface for running recon tools using reconator.sh
# Version: 1.0


TARGET=$1
OUTDIR=$2
shift 2
TOOLS=("$@")

mkdir -p "$OUTDIR"

for tool in "${TOOLS[@]}"; do
    case "$tool" in
        subfinder)
            subfinder -d "$TARGET" -o "$OUTDIR/subfinder.txt"
            ;;
        nmap)
            nmap -T4 -A "$TARGET" -oN "$OUTDIR/nmap_scan.txt"
            ;;
        whatweb)
            whatweb "$TARGET" > "$OUTDIR/whatweb_results.txt"
            ;;
        dirb)
            gobuster dir -u "http://$TARGET" -w /usr/share/wordlists/dirb/common.txt -o "$OUTDIR/directory_scan.txt"
            ;;
        traceroute)
            traceroute "$TARGET" > "$OUTDIR/traceroute.txt"
            ;;
        waf)
            wafw00f "$TARGET" > "$OUTDIR/waf_detection.txt"
            ;;
        all)
            # Optional: run all of the above
            ;;
        *)
            echo "Unknown tool: $tool"
            ;;
    esac
done
