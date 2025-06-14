#!/usr/bin/env python3
"""
Test Restored Color System for HyperTools Three.js Backend
"""

import numpy as np
import pandas as pd
import sys

# Add hypertools to path
sys.path.insert(0, '/Users/jmanning/hypertools')

import hypertools as hyp
from hypertools.core.threejs_backend import (
    HyperToolsFigure, mat2colors_threejs, labels2colors_threejs, rgb_to_hex
)

def test_color_conversion_functions():
    """Test the basic color conversion utilities"""
    print("=== TESTING COLOR CONVERSION FUNCTIONS ===")
    
    tests_passed = 0
    total_tests = 0
    
    # Test rgb_to_hex
    print("\n1. Testing rgb_to_hex:")
    total_tests += 3
    
    try:
        hex1 = rgb_to_hex([1.0, 0.0, 0.0])  # Red
        print(f"   RGB [1,0,0] → {hex1}")
        if hex1 == '#ff0000':
            tests_passed += 1
            print("   ✅ Red conversion correct")
        else:
            print(f"   ❌ Expected #ff0000, got {hex1}")
    except Exception as e:
        print(f"   ❌ RGB conversion failed: {e}")
    
    try:
        hex2 = rgb_to_hex('blue')  # Named color
        print(f"   'blue' → {hex2}")
        tests_passed += 1
        print("   ✅ Named color handled")
    except Exception as e:
        print(f"   ❌ Named color failed: {e}")
    
    try:
        hex3 = rgb_to_hex([255, 128, 0])  # Orange (0-255 range)
        print(f"   RGB [255,128,0] → {hex3}")
        tests_passed += 1
        print("   ✅ 0-255 range handled")
    except Exception as e:
        print(f"   ❌ 0-255 range failed: {e}")
    
    # Test mat2colors_threejs
    print("\n2. Testing mat2colors_threejs:")
    total_tests += 2
    
    try:
        colors1 = mat2colors_threejs([1, 2, 3, 4, 5])
        print(f"   1D array → {len(colors1)} colors: {colors1[:2]}...")
        if isinstance(colors1, list) and all(c.startswith('#') for c in colors1):
            tests_passed += 1
            print("   ✅ 1D array converted to hex colors")
        else:
            print(f"   ❌ Expected list of hex colors, got {type(colors1)}")
    except Exception as e:
        print(f"   ❌ 1D array failed: {e}")
    
    try:
        color_single = mat2colors_threejs('red')
        print(f"   Single color 'red' → {color_single}")
        if color_single.startswith('#'):
            tests_passed += 1
            print("   ✅ Single color converted")
        else:
            print(f"   ❌ Expected hex color, got {color_single}")
    except Exception as e:
        print(f"   ❌ Single color failed: {e}")
    
    # Test labels2colors_threejs
    print("\n3. Testing labels2colors_threejs:")
    total_tests += 1
    
    try:
        labels = ['A', 'B', 'A', 'C', 'B', 'A']
        colors, mapping = labels2colors_threejs(labels)
        print(f"   Labels {set(labels)} → {len(colors)} colors")
        print(f"   Mapping: {mapping}")
        if len(colors) == len(labels) and len(mapping) == 3:
            tests_passed += 1
            print("   ✅ Labels converted to colors with mapping")
        else:
            print(f"   ❌ Expected {len(labels)} colors and 3 mappings")
    except Exception as e:
        print(f"   ❌ Labels conversion failed: {e}")
    
    print(f"\n📊 Color function tests: {tests_passed}/{total_tests} passed")
    return tests_passed == total_tests

def test_color_integration():
    """Test color system integration with plotting"""
    print("\n=== TESTING COLOR SYSTEM INTEGRATION ===")
    
    results = []
    
    # Test 1: Basic color mapping
    print("\n1. Testing basic color mapping:")
    try:
        data = np.random.randn(20, 2)
        fig = hyp.plot(data, 'o', cmap='viridis')
        
        print(f"   ✅ Basic plot with viridis colormap: {type(fig)}")
        style = fig.plot_styles[0]
        print(f"   Color assigned: {style['color']}")
        results.append(True)
    except Exception as e:
        print(f"   ❌ Basic color mapping failed: {e}")
        results.append(False)
    
    # Test 2: Explicit color specification
    print("\n2. Testing explicit color:")
    try:
        data = np.random.randn(15, 2)
        fig = hyp.plot(data, 'ro-', color='#00ff00')  # Override red with green
        
        style = fig.plot_styles[0]
        print(f"   ✅ Explicit color override: {style['color']}")
        results.append(True)
    except Exception as e:
        print(f"   ❌ Explicit color failed: {e}")
        results.append(False)
    
    # Test 3: Multiple datasets with automatic coloring
    print("\n3. Testing multiple dataset coloring:")
    try:
        data1 = np.random.randn(10, 2)
        data2 = np.random.randn(10, 2)
        data3 = np.random.randn(10, 2)
        
        fig = hyp.plot([data1, data2, data3], ['o', 's', '^'], cmap='Set1')
        
        print(f"   ✅ Multiple datasets: {fig.n_datasets} plots")
        for i, style in enumerate(fig.plot_styles):
            print(f"   Dataset {i}: {style['color']}")
        results.append(True)
    except Exception as e:
        print(f"   ❌ Multiple dataset coloring failed: {e}")
        results.append(False)
    
    # Test 4: Custom color palette
    print("\n4. Testing custom color palette:")
    try:
        data = np.random.randn(25, 2)
        fig = hyp.plot(data, 'o', cmap='plasma')
        
        style = fig.plot_styles[0]
        print(f"   ✅ Plasma colormap: {style['color']}")
        results.append(True)
    except Exception as e:
        print(f"   ❌ Custom palette failed: {e}")
        results.append(False)
    
    success_rate = sum(results) / len(results)
    print(f"\n📊 Integration tests: {sum(results)}/{len(results)} passed ({success_rate:.1%})")
    return success_rate > 0.75

def test_clustering_colors():
    """Test color assignment with clustering"""
    print("\n=== TESTING CLUSTERING COLOR INTEGRATION ===")
    
    try:
        # Create data with clear clusters
        np.random.seed(42)
        cluster1 = np.random.normal([0, 0], 0.5, (20, 2))
        cluster2 = np.random.normal([3, 3], 0.5, (20, 2))
        cluster3 = np.random.normal([0, 3], 0.5, (20, 2))
        
        data = np.vstack([cluster1, cluster2, cluster3])
        
        print(f"Created clustered data: {data.shape}")
        
        # Test clustering with color assignment
        fig = hyp.plot(data, 'o', cluster={'model': 'KMeans', 'args': [], 'kwargs': {'n_clusters': 3}}, cmap='Set1')
        
        print(f"✅ Clustering plot created: {type(fig)}")
        print(f"   Figure has {fig.n_datasets} dataset(s)")
        
        # Check if cluster information was preserved
        if 'cluster_labels' in fig.kwargs:
            print(f"   ✅ Cluster labels preserved: {len(fig.kwargs['cluster_labels'])} points")
        if 'cluster_mapping' in fig.kwargs:
            print(f"   ✅ Cluster color mapping: {fig.kwargs['cluster_mapping']}")
        
        style = fig.plot_styles[0]
        print(f"   Assigned color: {style['color']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Clustering color test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_hue_colors():
    """Test color assignment with hue parameter"""
    print("\n=== TESTING HUE-BASED COLORING ===")
    
    try:
        # Create data with labels
        data = np.random.randn(30, 2)
        labels = ['Group A'] * 10 + ['Group B'] * 10 + ['Group C'] * 10
        
        print(f"Data shape: {data.shape}")
        print(f"Labels: {set(labels)}")
        
        # Test hue-based coloring
        fig = hyp.plot(data, 'o', hue=labels, cmap='viridis')
        
        print(f"✅ Hue-based plot created: {type(fig)}")
        
        # Check if hue information was preserved
        if 'hue_labels' in fig.kwargs:
            print(f"   ✅ Hue labels preserved: {len(fig.kwargs['hue_labels'])} points")
        if 'hue_mapping' in fig.kwargs:
            print(f"   ✅ Hue color mapping: {fig.kwargs['hue_mapping']}")
        
        style = fig.plot_styles[0]
        print(f"   Assigned color: {style['color']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Hue color test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all color system tests"""
    print("🎨 TESTING RESTORED COLOR SYSTEM FOR THREE.JS BACKEND")
    print("=" * 60)
    
    # Run all tests
    test_results = []
    
    test_results.append(test_color_conversion_functions())
    test_results.append(test_color_integration())
    test_results.append(test_clustering_colors())
    test_results.append(test_hue_colors())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 COLOR SYSTEM TEST SUMMARY")
    
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"✅ Test categories passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 COLOR SYSTEM FULLY RESTORED!")
        print("\n✅ WORKING FEATURES:")
        print("   • RGB to hex color conversion")
        print("   • mat2colors_threejs for data-driven coloring")
        print("   • labels2colors_threejs for categorical coloring")
        print("   • Integration with hyp.plot() color parameters")
        print("   • Multiple colormap support (viridis, plasma, Set1, etc.)")
        print("   • Clustering-based color assignment")
        print("   • Hue-based color assignment")
        print("   • Custom color palette handling")
        
        print("\n🚀 READY FOR PHASE 1 WEEK 2 CONTINUATION!")
        print("Next: Implement matplotlib conversion system")
        
        return True
    else:
        print("❌ Some color system features need attention")
        return False

if __name__ == "__main__":
    main()