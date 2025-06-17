#!/usr/bin/env python3
"""
Complete test of the plot.py fix and Three.js backend functionality
"""

import numpy as np
import sys
sys.path.insert(0, '/Users/jmanning/hypertools')
import hypertools as hyp

def test_plot_fix():
    """Test that plot.py returns HyperToolsFigure correctly"""
    print("🔧 TESTING COMPLETE PLOT FIX")
    print("=" * 50)
    
    # Create test data with clear Y positioning
    test_data = np.array([
        [0, 4],    # Top point
        [1, 2],    # Upper middle
        [2, 0],    # Center
        [3, -2],   # Lower middle  
        [4, -4]    # Bottom point
    ])
    
    print("Test data (X, Y):")
    for i, (x, y) in enumerate(test_data):
        print(f"  Point {i+1}: ({x:2.0f}, {y:2.0f})")
    
    print(f"\nY range: {test_data[:, 1].min()} to {test_data[:, 1].max()}")
    
    # Test 1: Command line environment (should return HyperToolsFigure)
    print("\n📊 Testing in command line environment...")
    fig = hyp.plot(test_data, 'ro', markersize=12)
    
    print(f"✅ Figure type: {type(fig).__name__}")
    
    if hasattr(fig, 'dimensionality'):
        print(f"✅ Dimensionality: {fig.dimensionality}")
        print(f"✅ Camera position: {fig.camera.position}")
        print(f"✅ Controls target: {fig.controls[0].target}")
        
        # Verify data positioning
        positions = fig._data_to_positions(fig.datasets[0])
        positions_3d = positions.reshape(-1, 3)
        print(f"\n🎯 Data Positioning Verification:")
        print(f"Input Y values:    {test_data[:, 1]}")
        print(f"Three.js Y values: {[p[1] for p in positions_3d]}")
        
        # Check if data matches
        input_y = test_data[:, 1]
        threejs_y = [p[1] for p in positions_3d]
        matches = np.allclose(input_y, threejs_y)
        print(f"✅ Y positions match: {matches}")
        
        if not matches:
            print("❌ ERROR: Y positions don't match input data!")
            return False
            
    else:
        print("❌ ERROR: Got wrong object type!")
        return False
    
    # Test 2: Matplotlib conversion
    print(f"\n📈 Testing matplotlib conversion...")
    try:
        matplotlib_fig = fig.to_matplotlib()
        print("✅ Matplotlib conversion successful")
    except Exception as e:
        print(f"❌ Matplotlib conversion failed: {e}")
        return False
    
    # Test 3: Different format strings
    print(f"\n🎨 Testing different format strings...")
    
    test_formats = ['ro', 'b-', 'g--', 'k:', 'mo-']
    for fmt in test_formats:
        try:
            test_fig = hyp.plot(test_data, fmt, markersize=8)
            print(f"✅ Format '{fmt}': {type(test_fig).__name__}")
        except Exception as e:
            print(f"❌ Format '{fmt}' failed: {e}")
            return False
    
    print(f"\n" + "=" * 50)
    print("✅ ALL TESTS PASSED - Plot fix working correctly!")
    print("✅ Ready for Jupyter testing with fixed behavior")
    print("=" * 50)
    
    return True, fig

def test_jupyter_simulation():
    """Simulate Jupyter auto-display behavior"""
    print("\n🪐 TESTING JUPYTER SIMULATION")
    print("=" * 30)
    
    # Mock IPython environment
    class MockIPython:
        def __init__(self):
            self.kernel = True
    
    import sys
    sys.modules['IPython'] = type(sys)('IPython')
    sys.modules['IPython'].get_ipython = lambda: MockIPython()
    
    # Test with mocked Jupyter environment
    test_data = np.array([[0, 1], [1, 2], [2, 0]])
    
    try:
        result = hyp.plot(test_data, 'bo')
        print(f"✅ Jupyter mode result type: {type(result).__name__}")
        if hasattr(result, 'dimensionality'):
            print("✅ Returns HyperToolsFigure (not Renderer)")
            return True
        else:
            print("❌ Still returns wrong type in Jupyter mode")
            return False
    except Exception as e:
        print(f"❌ Jupyter simulation failed: {e}")
        return False

if __name__ == "__main__":
    success, fig = test_plot_fix()
    
    if success:
        # Run Jupyter simulation
        jupyter_success = test_jupyter_simulation()
        
        if jupyter_success:
            print("\n🎉 COMPLETE SUCCESS!")
            print("Ready to test in actual Jupyter notebook")
        else:
            print("\n⚠️  Jupyter mode needs additional fixes")
    else:
        print("\n❌ Basic plot fix failed - needs more work")