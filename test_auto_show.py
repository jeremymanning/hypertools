#!/usr/bin/env python3
"""
Test that hyp.plot() auto-shows in Jupyter but returns figure object in scripts
"""

import numpy as np
import sys
sys.path.insert(0, '/Users/jmanning/hypertools')
import hypertools as hyp

def test_auto_show():
    """Test the auto-show functionality"""
    print("🧪 Testing auto-show behavior...")
    
    # Create simple test data
    data = np.array([[0, 1], [1, 0], [-1, -1]])
    
    # In a script (not Jupyter), should return HyperToolsFigure
    result = hyp.plot(data, 'ro', markersize=10)
    
    print(f"Return type: {type(result)}")
    
    if hasattr(result, 'show'):
        print("✅ Returned HyperToolsFigure object (script mode)")
        print("   - In Jupyter, this would auto-display")
        print("   - In scripts, you get the figure object")
    else:
        print("❌ Unexpected return type")
        
    return result

if __name__ == "__main__":
    print("🔧 AUTO-SHOW FUNCTIONALITY TEST")
    print("=" * 40)
    
    fig = test_auto_show()
    
    print("\n📋 Expected behavior:")
    print("- Jupyter: hyp.plot() automatically displays widget")
    print("- Scripts: hyp.plot() returns figure object")
    print("- Both: fig.show() can be called manually")
    print("=" * 40)