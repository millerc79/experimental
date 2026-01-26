#!/bin/bash
#
# PDF Automation Template Script
#
# SETUP: Copy this file to run_incoming_scans.sh and customize the paths below
# Example: cp run_incoming_scans_template.sh run_incoming_scans.sh
#

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# CUSTOMIZE THESE PATHS FOR YOUR SETUP
# Your source folder (where PDFs arrive)
SCANS_FOLDER="/Users/YOUR_USERNAME/Library/Mobile Documents/com~apple~CloudDocs/Incoming Scans"

# Your destination folder (where PDFs will be organized by year)
FILING_CABINET="/Users/YOUR_USERNAME/Documents/Filing Cabinet"

# Rules file (customize for your needs)
RULES_FILE="pdf_rules_filing_cabinet.json"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  PDF Automation - Incoming Scans${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if folder exists
if [ ! -d "$SCANS_FOLDER" ]; then
    echo -e "${RED}❌ Error: Source folder not found${NC}"
    echo -e "${YELLOW}Expected: $SCANS_FOLDER${NC}"
    echo ""
    echo "Please check that:"
    echo "  1. You've customized the SCANS_FOLDER path in this script"
    echo "  2. The folder exists on your system"
    echo "  3. The path is correct"
    exit 1
fi

# Check if PyPDF2 is installed
if ! python3 -c "import PyPDF2" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  PyPDF2 not installed. Installing now...${NC}"
    pip3 install PyPDF2
    echo -e "${GREEN}✓ PyPDF2 installed${NC}"
    echo ""
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory (where pdf_automation.py is)
cd "$SCRIPT_DIR"

# Determine mode
MODE="${1:-watch}"

case "$MODE" in
    "dry-run")
        echo -e "${YELLOW}🔍 DRY RUN - Checking source folder${NC}"
        echo -e "${YELLOW}No files will be moved${NC}"
        echo -e "${BLUE}Destination: $FILING_CABINET/{year}/...${NC}"
        echo ""
        python3 pdf_automation.py --folder "$SCANS_FOLDER" --rules "$RULES_FILE" --dry-run
        ;;
    "once")
        echo -e "${GREEN}🚀 PROCESSING source folder (one time)${NC}"
        echo -e "${BLUE}Destination: $FILING_CABINET/{year}/...${NC}"
        echo ""
        python3 pdf_automation.py --folder "$SCANS_FOLDER" --rules "$RULES_FILE"
        ;;
    "watch")
        echo -e "${BLUE}👀 WATCHING source folder${NC}"
        echo -e "${BLUE}Will check for new PDFs every 30 seconds${NC}"
        echo -e "${BLUE}Destination: $FILING_CABINET/{year}/...${NC}"
        echo ""
        python3 pdf_automation.py --folder "$SCANS_FOLDER" --rules "$RULES_FILE" --watch --interval 30
        ;;
    *)
        echo -e "${RED}Unknown mode: $MODE${NC}"
        echo ""
        echo "Usage: $0 [mode]"
        echo ""
        echo "Modes:"
        echo "  dry-run  - Preview what would happen (safe)"
        echo "  once     - Process files one time"
        echo "  watch    - Continuously monitor for new files (default)"
        echo ""
        exit 1
        ;;
esac
