# test_imports.py
try:
    import pandas as pd
    print("✓ pandas imported successfully")
except ImportError:
    print("✗ pandas not found")

try:
    import openpyxl
    print("✓ openpyxl imported successfully")
except ImportError:
    print("✗ openpyxl not found")

try:
    from datetime import datetime
    print("✓ datetime imported successfully")
except ImportError:
    print("✗ datetime not found")

print("Setup test complete!")
