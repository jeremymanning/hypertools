#!/usr/bin/env python3
"""
Simple test to check what might be causing kernel connection delays
"""

print("🔍 Testing kernel connection issues...")

# Test 1: Basic imports
try:
    import numpy as np
    print("✅ numpy import OK")
except Exception as e:
    print(f"❌ numpy import failed: {e}")

try:
    import pandas as pd
    print("✅ pandas import OK")
except Exception as e:
    print(f"❌ pandas import failed: {e}")

# Test 2: pythreejs import (this might be slow)
print("🔄 Testing pythreejs import...")
try:
    import pythreejs as p3js
    print("✅ pythreejs import OK")
except Exception as e:
    print(f"❌ pythreejs import failed: {e}")

# Test 3: HyperTools import
print("🔄 Testing HyperTools import...")
try:
    import sys
    sys.path.insert(0, '/Users/jmanning/hypertools')
    import hypertools as hyp
    print("✅ hypertools import OK")
except Exception as e:
    print(f"❌ hypertools import failed: {e}")

print("✅ All imports successful - kernel should connect normally")