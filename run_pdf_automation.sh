#!/bin/bash
#
# PDF Automation Tool Runner
# Simple script to run PDF automation with common settings
#

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  PDF Automation Tool${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if PyPDF2 is installed
if ! python3 -c "import PyPDF2" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  PyPDF2 not installed. Installing now...${NC}"
    pip3 install PyPDF2
    echo -e "${GREEN}✓ PyPDF2 installed${NC}"
    echo ""
fi

# Default settings
FOLDER="${1:-.}"  # First argument or current directory
MODE="${2:-interactive}"  # Second argument or interactive mode

case "$MODE" in
    "dry-run")
        echo -e "${YELLOW}🔍 Running in DRY RUN mode (no files will be moved)${NC}"
        python3 pdf_automation.py --folder "$FOLDER" --dry-run
        ;;
    "auto")
        echo -e "${GREEN}🚀 Running in AUTOMATIC mode${NC}"
        python3 pdf_automation.py --folder "$FOLDER"
        ;;
    "watch")
        echo -e "${BLUE}👀 Running in WATCH mode (monitoring for new PDFs)${NC}"
        python3 pdf_automation.py --folder "$FOLDER" --watch
        ;;
    *)
        echo -e "${BLUE}📋 Running in INTERACTIVE mode${NC}"
        python3 pdf_automation.py
        ;;
esac

echo ""
echo -e "${GREEN}✅ Done!${NC}"
