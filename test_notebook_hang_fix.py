#!/usr/bin/env python3
"""
Test if the camera fix also resolves the notebook hanging issue
"""

import numpy as np
import sys
import time
sys.path.insert(0, '/Users/jmanning/hypertools')
import hypertools as hyp

def test_rendering_speed():
    """Test if rendering is now fast and non-blocking"""
    print("⏱️  TESTING RENDERING PERFORMANCE")
    print("=" * 40)
    
    # Test multiple figure creation (simulating notebook cells)
    start_time = time.time()
    
    figures = []
    for i in range(3):
        print(f"Creating figure {i+1}...")
        
        # Create different types of plots
        if i == 0:
            data = np.random.randn(20, 2)
            fig = hyp.plot(data, 'ro', markersize=8)
        elif i == 1:
            t = np.linspace(0, 2*np.pi, 50)
            data = np.column_stack([np.cos(t), np.sin(t)])
            fig = hyp.plot(data, 'b-', linewidth=2)
        else:
            data = np.random.randn(15, 2) * 1.5
            fig = hyp.plot(data, 'g^', markersize=10)
        
        figures.append(fig)
        
        # Check if renderer creation is blocking
        try:
            renderer = fig.show()
            print(f"  ✅ Figure {i+1} renderer created successfully")
        except Exception as e:
            print(f"  ❌ Figure {i+1} failed: {e}")
    
    total_time = time.time() - start_time
    print(f"\n⏱️  Total time: {total_time:.2f} seconds")
    
    if total_time < 5.0:  # Should be very fast
        print("✅ Rendering performance looks good")
    else:
        print("⚠️  Rendering seems slower than expected")
    
    return figures

def test_widget_creation():
    """Test widget creation doesn't block"""
    print("\n🔧 TESTING WIDGET CREATION")
    print("=" * 40)
    
    try:
        # Simple test case
        data = np.array([[0, 1], [1, 0], [-1, -1]])
        fig = hyp.plot(data, 'ko', markersize=12)
        
        # Try to access widget properties
        renderer = fig.show()
        
        print(f"Widget type: {type(renderer)}")
        print(f"Widget width: {renderer.width}")
        print(f"Widget height: {renderer.height}")
        
        # Check if widget has proper attributes
        if hasattr(renderer, 'scene') and hasattr(renderer, 'camera'):
            print("✅ Widget properly initialized")
            return True
        else:
            print("❌ Widget missing attributes")
            return False
            
    except Exception as e:
        print(f"❌ Widget creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 NOTEBOOK HANG FIX TEST")
    print("=" * 50)
    
    # Test 1: Rendering performance
    figures = test_rendering_speed()
    
    # Test 2: Widget creation
    widget_ok = test_widget_creation()
    
    print("\n" + "=" * 50)
    print("📋 SUMMARY:")
    print(f"- Created {len(figures)} figures successfully")
    print(f"- Widget creation: {'✅ OK' if widget_ok else '❌ FAILED'}")
    print("- Ready for Jupyter notebook testing")
    print("=" * 50)