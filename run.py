#!/usr/bin/env python3
import sys
from src.cli.main import main
from src.utils.colors import Colors

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test-colors":
        Colors.test_colors()
    else:
        main() 