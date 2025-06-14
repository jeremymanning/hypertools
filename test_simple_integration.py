#!/usr/bin/env python3
"""
Simple test of Three.js integration with HyperTools
"""

import numpy as np
import sys

# Add hypertools to path
sys.path.insert(0, '/Users/jmanning/hypertools')

import hypertools as hyp
from hypertools.core.threejs_backend import HyperToolsFigure

def test_basic_integration():
    """Test basic hyp.plot() integration"""
    print("=== TESTING BASIC INTEGRATION ===")
    
    # Create simple test data
    data = np.array([[0, 0], [1, 1], [2, 0], [3, 1]])
    
    print(f"Data shape: {data.shape}")
    print(f"Data:\n{data}")
    
    try:
        # Test basic plot
        fig = hyp.plot(data, 'ro-', linewidth=3, markersize=8)
        
        print(f"✅ hyp.plot() returned: {type(fig)}")
        print(f"   Is HyperToolsFigure: {isinstance(fig, HyperToolsFigure)}")
        
        if isinstance(fig, HyperToolsFigure):
            print(f"   Number of datasets: {fig.n_datasets}")
            print(f"   Dimensionality: {fig.dimensionality}")
            
            style = fig.plot_styles[0]
            print(f"   Style: color={style['color']}, line={style['linestyle']}, marker={style['marker']}")
            print(f"   Custom: linewidth={style['linewidth']}, markersize={style['markersize']}")
            
            # Test show method
            renderer = fig.show()
            print(f"   ✅ fig.show() works: {type(renderer)}")
            
            return fig
        else:
            print(f"   ❌ Expected HyperToolsFigure, got {type(fig)}")
            return None
        
    except Exception as e:
        print(f"❌ Basic integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_3d_integration():
    """Test 3D data integration"""
    print("\n=== TESTING 3D INTEGRATION ===")
    
    # Create 3D test data
    t = np.linspace(0, 2*np.pi, 20)
    data_3d = np.column_stack([np.cos(t), np.sin(t), t/3])
    
    print(f"3D data shape: {data_3d.shape}")
    
    try:
        fig = hyp.plot(data_3d, 'b-', linewidth=2)
        
        print(f"✅ 3D plot created: {type(fig)}")
        
        if isinstance(fig, HyperToolsFigure):
            print(f"   Dimensionality: {fig.dimensionality}")
            print(f"   Dataset shape: {fig.datasets[0].shape}")
            print(f"   Dataset columns: {list(fig.datasets[0].columns)}")
            
            renderer = fig.show()
            print(f"   ✅ 3D visualization works: {type(renderer)}")
            
            return fig
        else:
            print(f"   ❌ Expected HyperToolsFigure, got {type(fig)}")
            return None
            
    except Exception as e:
        print(f"❌ 3D integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Run simple integration tests"""
    print("🔗 SIMPLE THREE.JS INTEGRATION TEST")
    print("=" * 50)
    
    # Run tests
    result1 = test_basic_integration()
    result2 = test_3d_integration()
    
    # Summary
    print("\n" + "=" * 50)
    successes = sum(1 for r in [result1, result2] if r is not None)
    total = 2
    
    print(f"✅ Successful tests: {successes}/{total}")
    
    if successes == total:
        print("🎉 INTEGRATION SUCCESS!")
        print("Three.js backend is working with hyp.plot()")
        return result1
    else:
        print("❌ Some tests failed")
        return None

if __name__ == "__main__":
    main()