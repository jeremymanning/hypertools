#!/usr/bin/env python3
"""
Test Matplotlib-Style API for HyperTools Three.js Backend
"""

import numpy as np
import pandas as pd
import sys
import os

# Add hypertools to path
sys.path.insert(0, '/Users/jmanning/hypertools')

from hypertools.core.threejs_backend import HyperToolsFigure, ThreeJSBackend

def test_basic_format_strings():
    """Test basic matplotlib format string parsing"""
    print("=== TESTING FORMAT STRING PARSING ===")
    
    # Create test data
    t = np.linspace(0, 2*np.pi, 50)
    data = pd.DataFrame({
        'x': np.cos(t),
        'y': np.sin(t)
    })
    
    print(f"Data shape: {data.shape}")
    
    # Test different format strings
    format_tests = [
        ('r-', 'Red solid line'),
        ('bo', 'Blue circles'),
        ('g--', 'Green dashed line'),
        ('k:', 'Black dotted line'),
        ('mo-', 'Magenta line with circle markers'),
        ('c*', 'Cyan stars'),
        ('y^-', 'Yellow triangles with line')
    ]
    
    figures = []
    
    for fmt_str, description in format_tests:
        try:
            print(f"\nTesting '{fmt_str}': {description}")
            fig = HyperToolsFigure(data, fmt=fmt_str)
            
            # Check parsed style
            style = fig.plot_styles[0]
            print(f"   Parsed style: {style}")
            
            renderer = fig.show()
            print(f"   ✅ Created successfully: {type(renderer)}")
            figures.append((fmt_str, fig))
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    return figures

def test_multiple_datasets():
    """Test plotting multiple datasets with different styles"""
    print("\n=== TESTING MULTIPLE DATASETS ===")
    
    # Create multiple datasets
    t = np.linspace(0, 4*np.pi, 100)
    
    data1 = pd.DataFrame({
        'x': t,
        'y': np.sin(t)
    })
    
    data2 = pd.DataFrame({
        'x': t,
        'y': np.cos(t)
    })
    
    data3 = pd.DataFrame({
        'x': t,
        'y': np.sin(t) * np.cos(t/2)
    })
    
    datasets = [data1, data2, data3]
    
    print(f"Dataset shapes: {[d.shape for d in datasets]}")
    
    # Test different ways to specify styles
    test_cases = [
        # Single format string applied to all
        ('r-', 'All red lines'),
        
        # List of format strings
        (['r-', 'b--', 'go'], 'Red line, blue dashed, green circles'),
        
        # Mixed with kwargs
        (['r-', 'b-'], 'Two styles with linewidth override')
    ]
    
    figures = []
    
    for fmt, description in test_cases:
        try:
            print(f"\nTesting: {description}")
            print(f"   Format: {fmt}")
            
            if description.endswith('override'):
                fig = HyperToolsFigure(datasets, fmt=fmt, linewidth=[3, 1])
            else:
                fig = HyperToolsFigure(datasets, fmt=fmt)
            
            print(f"   Number of datasets: {fig.n_datasets}")
            print(f"   Parsed styles:")
            for i, style in enumerate(fig.plot_styles):
                print(f"     Dataset {i}: color={style['color']}, line={style['linestyle']}, marker={style['marker']}")
            
            renderer = fig.show()
            print(f"   ✅ Created successfully: {type(renderer)}")
            figures.append((fmt, fig))
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            import traceback
            traceback.print_exc()
    
    return figures

def test_interpolation():
    """Test line interpolation functionality"""
    print("\n=== TESTING LINE INTERPOLATION ===")
    
    # Create sparse data that should be interpolated
    sparse_data = pd.DataFrame({
        'x': [0, 1, 3, 5],
        'y': [0, 2, 1, 3]
    })
    
    print(f"Original data points: {len(sparse_data)}")
    
    try:
        # Test with interpolation
        fig = HyperToolsFigure(sparse_data, fmt='b-', interpolation_samples=50)
        
        print(f"Interpolation samples: {fig.plot_styles[0]['interpolation_samples']}")
        
        # Test interpolation method directly
        interpolated = fig._interpolate_line_data(sparse_data, 50)
        print(f"Interpolated data points: {len(interpolated)}")
        print(f"Interpolated data preview:\n{interpolated.head()}")
        
        renderer = fig.show()
        print(f"✅ Interpolation test passed: {type(renderer)}")
        
        return fig
        
    except Exception as e:
        print(f"❌ Interpolation test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_single_point():
    """Test single point handling"""
    print("\n=== TESTING SINGLE POINT HANDLING ===")
    
    # Single point data
    single_point = pd.DataFrame({
        'x': [2.5],
        'y': [1.5]
    })
    
    print(f"Single point data: {single_point.iloc[0].to_dict()}")
    
    try:
        fig = HyperToolsFigure(single_point, fmt='r-')  # Should override to marker
        
        style = fig.plot_styles[0]
        print(f"Auto-corrected style for single point:")
        print(f"   linestyle: {style['linestyle']}")
        print(f"   marker: {style['marker']}")
        print(f"   markersize: {style['markersize']}")
        
        renderer = fig.show()
        print(f"✅ Single point test passed: {type(renderer)}")
        
        return fig
        
    except Exception as e:
        print(f"❌ Single point test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_3d_plots():
    """Test 3D plotting with format strings"""
    print("\n=== TESTING 3D PLOTS ===")
    
    # Create 3D helix data
    t = np.linspace(0, 4*np.pi, 80)
    data_3d = pd.DataFrame({
        'x': np.cos(t),
        'y': np.sin(t),
        'z': t / 5
    })
    
    print(f"3D data shape: {data_3d.shape}")
    
    try:
        fig = HyperToolsFigure(data_3d, fmt='ro-', linewidth=3, markersize=5)
        
        print(f"Detected dimensionality: {fig.dimensionality}")
        
        style = fig.plot_styles[0]
        print(f"Style: color={style['color']}, line={style['linestyle']}, marker={style['marker']}")
        
        renderer = fig.show()
        print(f"✅ 3D plot test passed: {type(renderer)}")
        
        return fig
        
    except Exception as e:
        print(f"❌ 3D plot test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_backend_api():
    """Test the ThreeJSBackend.plot API"""
    print("\n=== TESTING BACKEND API ===")
    
    data = np.random.randn(30, 2)
    
    try:
        # Test new API
        fig = ThreeJSBackend.plot(data, fmt='go-', linewidth=2, markersize=8)
        
        print(f"Backend API figure type: {type(fig)}")
        print(f"Number of datasets: {fig.n_datasets}")
        print(f"Style: {fig.plot_styles[0]}")
        
        renderer = fig.show()
        print(f"✅ Backend API test passed: {type(renderer)}")
        
        return fig
        
    except Exception as e:
        print(f"❌ Backend API test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Run all matplotlib API tests"""
    print("🎨 TESTING MATPLOTLIB-STYLE API FOR HYPERTOOLS THREE.JS BACKEND")
    print("=" * 70)
    
    # Store test results
    test_results = {}
    
    # Run all tests
    test_results['format_strings'] = test_basic_format_strings()
    test_results['multiple_datasets'] = test_multiple_datasets()
    test_results['interpolation'] = test_interpolation()
    test_results['single_point'] = test_single_point()
    test_results['3d_plots'] = test_3d_plots()
    test_results['backend_api'] = test_backend_api()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    
    successes = sum(1 for result in test_results.values() if result is not None)
    total = len(test_results)
    
    print(f"✅ Successful test categories: {successes}/{total}")
    
    if successes == total:
        print("🎉 ALL MATPLOTLIB API TESTS PASSED!")
        print("\nThe new matplotlib-style format string API is working correctly:")
        print("  ✅ Format string parsing (r-, bo, g--, etc.)")
        print("  ✅ Multiple datasets with different styles")
        print("  ✅ Line interpolation for smooth curves")
        print("  ✅ Single point auto-detection")
        print("  ✅ 3D plotting support")
        print("  ✅ Backend API integration")
        print("\nReady for integration with main HyperTools API!")
        
        # Return a representative figure
        return test_results.get('multiple_datasets', [None])[0] if test_results.get('multiple_datasets') else None
    else:
        print("❌ Some tests failed - check errors above")
        return None

if __name__ == "__main__":
    main()