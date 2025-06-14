#!/usr/bin/env python3
"""
Test HyperTools Three.js Backend Implementation
"""

import numpy as np
import pandas as pd
import sys
import os

# Add hypertools to path
sys.path.insert(0, '/Users/jmanning/hypertools')

from hypertools.core.threejs_backend import HyperToolsFigure, ThreeJSBackend

def test_2d_scatter():
    """Test 2D scatter plot creation"""
    print("=== TESTING 2D SCATTER PLOT ===")
    
    # Create test data
    n_points = 50
    data = np.random.randn(n_points, 2) * 2
    df = pd.DataFrame(data, columns=['x', 'y'])
    
    print(f"Data shape: {df.shape}")
    print(f"Data preview:\n{df.head()}")
    
    try:
        # Create HyperTools figure
        fig = HyperToolsFigure(df, plot_type='scatter', color='blue', size=0.2)
        
        print(f"✅ Figure created successfully")
        print(f"   - Dimensionality: {fig.dimensionality}")
        print(f"   - Plot type: {fig.plot_type}")
        print(f"   - Renderer type: {type(fig.renderer)}")
        
        # Test figure methods
        renderer = fig.show()
        print(f"✅ show() method works: {type(renderer)}")
        
        return fig
        
    except Exception as e:
        print(f"❌ 2D scatter test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_3d_scatter():
    """Test 3D scatter plot creation"""
    print("\n=== TESTING 3D SCATTER PLOT ===")
    
    # Create test data
    n_points = 50
    data = np.random.randn(n_points, 3) * 2
    df = pd.DataFrame(data, columns=['x', 'y', 'z'])
    
    print(f"Data shape: {df.shape}")
    print(f"Data preview:\n{df.head()}")
    
    try:
        # Create HyperTools figure
        fig = HyperToolsFigure(df, plot_type='scatter', color='red', size=0.15)
        
        print(f"✅ Figure created successfully")
        print(f"   - Dimensionality: {fig.dimensionality}")
        print(f"   - Plot type: {fig.plot_type}")
        print(f"   - Renderer type: {type(fig.renderer)}")
        
        # Test figure methods
        renderer = fig.show()
        print(f"✅ show() method works: {type(renderer)}")
        
        return fig
        
    except Exception as e:
        print(f"❌ 3D scatter test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_2d_line():
    """Test 2D line plot creation"""
    print("\n=== TESTING 2D LINE PLOT ===")
    
    # Create smooth trajectory data
    t = np.linspace(0, 4*np.pi, 100)
    x = np.cos(t) * np.exp(-t/10)
    y = np.sin(t) * np.exp(-t/10)
    
    df = pd.DataFrame({'x': x, 'y': y})
    
    print(f"Data shape: {df.shape}")
    
    try:
        # Create HyperTools figure
        fig = HyperToolsFigure(df, plot_type='line', color='green', linewidth=2)
        
        print(f"✅ Figure created successfully")
        print(f"   - Dimensionality: {fig.dimensionality}")
        print(f"   - Plot type: {fig.plot_type}")
        print(f"   - Renderer type: {type(fig.renderer)}")
        
        # Test figure methods
        renderer = fig.show()
        print(f"✅ show() method works: {type(renderer)}")
        
        return fig
        
    except Exception as e:
        print(f"❌ 2D line test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_3d_line():
    """Test 3D line plot creation"""
    print("\n=== TESTING 3D LINE PLOT ===")
    
    # Create 3D helix data
    t = np.linspace(0, 4*np.pi, 100)
    x = np.cos(t)
    y = np.sin(t)
    z = t / 5
    
    df = pd.DataFrame({'x': x, 'y': y, 'z': z})
    
    print(f"Data shape: {df.shape}")
    
    try:
        # Create HyperTools figure
        fig = HyperToolsFigure(df, plot_type='line', color='purple', linewidth=3)
        
        print(f"✅ Figure created successfully")
        print(f"   - Dimensionality: {fig.dimensionality}")
        print(f"   - Plot type: {fig.plot_type}")
        print(f"   - Renderer type: {type(fig.renderer)}")
        
        # Test figure methods
        renderer = fig.show()
        print(f"✅ show() method works: {type(renderer)}")
        
        return fig
        
    except Exception as e:
        print(f"❌ 3D line test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_backend_api():
    """Test ThreeJSBackend class"""
    print("\n=== TESTING THREEJS BACKEND API ===")
    
    try:
        # Test data
        data = np.random.randn(30, 2)
        
        # Test backend
        backend = ThreeJSBackend()
        fig = backend.plot(data, color='orange')
        
        print(f"✅ Backend API works: {type(fig)}")
        print(f"   - Auto-detected plot type: {fig.plot_type}")
        print(f"   - Dimensionality: {fig.dimensionality}")
        
        return fig
        
    except Exception as e:
        print(f"❌ Backend API test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_auto_detection():
    """Test automatic plot type detection"""
    print("\n=== TESTING AUTO-DETECTION ===")
    
    results = []
    
    # Test small dataset (should be scatter)
    small_data = np.random.randn(10, 2)
    fig1 = HyperToolsFigure(small_data, plot_type='auto')
    print(f"Small dataset (10 points): {fig1.plot_type} (expected: scatter)")
    results.append(('small', fig1.plot_type, 'scatter'))
    
    # Test large dataset (should be line)
    large_data = np.random.randn(200, 2)
    fig2 = HyperToolsFigure(large_data, plot_type='auto')
    print(f"Large dataset (200 points): {fig2.plot_type} (expected: line)")
    results.append(('large', fig2.plot_type, 'line'))
    
    # Test monotonic index (should be line)
    time_data = pd.DataFrame({
        'x': np.arange(50),
        'y': np.random.randn(50)
    })
    fig3 = HyperToolsFigure(time_data, plot_type='auto')
    print(f"Monotonic index: {fig3.plot_type} (expected: line)")
    results.append(('monotonic', fig3.plot_type, 'line'))
    
    return results

def main():
    """Run all tests"""
    print("🚀 TESTING HYPERTOOLS THREE.JS BACKEND")
    print("=" * 50)
    
    # Store test results
    test_results = {}
    
    # Run all tests
    test_results['2d_scatter'] = test_2d_scatter()
    test_results['3d_scatter'] = test_3d_scatter()
    test_results['2d_line'] = test_2d_line()
    test_results['3d_line'] = test_3d_line()
    test_results['backend_api'] = test_backend_api()
    test_results['auto_detection'] = test_auto_detection()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    
    successes = sum(1 for result in test_results.values() if result is not None)
    total = len([k for k in test_results.keys() if k != 'auto_detection'])
    
    print(f"✅ Successful tests: {successes}/{total}")
    
    if successes == total:
        print("🎉 ALL TESTS PASSED - HyperTools Three.js backend is working!")
        print("\nReady for integration with main hypertools.plot() function")
        
        # Return a test figure for potential display
        return test_results['2d_scatter']
    else:
        print("❌ Some tests failed - check errors above")
        return None

if __name__ == "__main__":
    main()