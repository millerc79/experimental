#!/bin/bash
# Wrapper script to run PDF automation with the correct Python environment

# Use the system Python3 which has access to user-installed packages
/usr/bin/python3 pdf_automation.py "$@"
