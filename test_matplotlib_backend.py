"""
Test script for matplotlib backend implementation.

This script tests basic functionality of the new matplotlib backend
to ensure plots render correctly.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add hypertools to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

try:
    import hypertools as hyp
    print("✓ Successfully imported hypertools")
    
    # Test importing the specific plot function
    from hypertools.plot.plot import plot as hyp_plot
    print("✓ Successfully imported plot function")
except ImportError as e:
    print(f"✗ Failed to import hypertools: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def test_basic_2d_plot():
    """Test basic 2D scatter plot."""
    print("\nTesting basic 2D scatter plot...")
    
    # Generate simple 2D data
    np.random.seed(42)
    data = np.random.randn(100, 2)
    
    try:
        fig = hyp_plot(data, save_path='test_2d_scatter.png')
        print("✓ 2D scatter plot successful")
        plt.close(fig)
        return True
    except Exception as e:
        print(f"✗ 2D scatter plot failed: {e}")
        return False

def test_basic_3d_plot():
    """Test basic 3D scatter plot."""
    print("\nTesting basic 3D scatter plot...")
    
    # Generate simple 3D data
    np.random.seed(42)
    data = np.random.randn(100, 3)
    
    try:
        fig = hyp_plot(data, save_path='test_3d_scatter.png')
        print("✓ 3D scatter plot successful")
        plt.close(fig)
        return True
    except Exception as e:
        print(f"✗ 3D scatter plot failed: {e}")
        return False

def test_format_strings():
    """Test matplotlib format strings."""
    print("\nTesting format strings...")
    
    # Generate simple data
    np.random.seed(42)
    data = np.random.randn(50, 2)
    
    try:
        # Test different format strings
        fig = hyp_plot(data, 'ro-', save_path='test_format_strings.png')
        print("✓ Format string 'ro-' successful")
        plt.close(fig)
        return True
    except Exception as e:
        print(f"✗ Format string test failed: {e}")
        return False

def test_multiple_datasets():
    """Test plotting multiple datasets."""
    print("\nTesting multiple datasets...")
    
    # Generate multiple datasets
    np.random.seed(42)
    data1 = np.random.randn(50, 2) + [0, 0]
    data2 = np.random.randn(50, 2) + [3, 3]
    data = [data1, data2]
    
    try:
        fig = hyp_plot(data, save_path='test_multiple_datasets.png')
        print("✓ Multiple datasets plot successful")
        plt.close(fig)
        return True
    except Exception as e:
        print(f"✗ Multiple datasets test failed: {e}")
        return False

def test_line_plot():
    """Test line plot mode."""
    print("\nTesting line plot...")
    
    # Generate trajectory data
    t = np.linspace(0, 4*np.pi, 100)
    data = pd.DataFrame({
        'x': np.cos(t) + 0.1*np.random.randn(100),
        'y': np.sin(t) + 0.1*np.random.randn(100)
    })
    
    try:
        fig = hyp_plot(data, mode='lines', save_path='test_line_plot.png')
        print("✓ Line plot successful")
        plt.close(fig)
        return True
    except Exception as e:
        print(f"✗ Line plot failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing matplotlib backend implementation...")
    
    # Set matplotlib to non-interactive backend
    plt.ioff()
    
    tests = [
        test_basic_2d_plot,
        test_basic_3d_plot,
        test_format_strings,
        test_multiple_datasets,
        test_line_plot
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Matplotlib backend is working.")
    else:
        print("✗ Some tests failed. Check implementation.")
    
    # Clean up test files
    import glob
    for f in glob.glob('test_*.png'):
        try:
            os.remove(f)
            print(f"Cleaned up {f}")
        except:
            pass

if __name__ == "__main__":
    main()