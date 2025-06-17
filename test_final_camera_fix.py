#!/usr/bin/env python3
"""
Test the final camera and material improvements
"""

import numpy as np
import sys
sys.path.insert(0, '/Users/jmanning/hypertools')
import hypertools as hyp

def test_final_improvements():
    """Test camera fix and material improvements"""
    print("🎯 TESTING FINAL IMPROVEMENTS")
    print("=" * 45)
    
    # Test 1: Clear vertical separation
    print("Test 1: Clear vertical separation")
    test_data = np.array([
        [0, 3],    # Top
        [0, 0],    # Center
        [0, -3]    # Bottom
    ])
    
    print(f"Data Y range: {test_data[:, 1].min()} to {test_data[:, 1].max()}")
    
    fig1 = hyp.plot(test_data, 'ro', markersize=15, alpha=0.9)
    print(f"Camera: {type(fig1.camera).__name__}")
    print(f"Camera position: {fig1.camera.position}")
    print(f"Camera FOV: {fig1.camera.fov if hasattr(fig1.camera, 'fov') else 'N/A'}")
    
    # Test 2: Line plot
    print("\nTest 2: Enhanced line plot")
    t = np.linspace(0, 2*np.pi, 20)
    circle = np.column_stack([np.cos(t), np.sin(t)])
    
    fig2 = hyp.plot(circle, 'b-', linewidth=3, alpha=0.8)
    print(f"Camera position: {fig2.camera.position}")
    
    print("\n✅ Tests completed")
    print("📋 Improvements:")
    print("  - Perspective camera instead of orthographic")
    print("  - 2x larger points for better visibility") 
    print("  - 2x thicker lines")
    print("  - Enhanced lighting (ambient + directional + point)")
    print("  - Better material properties")
    
    return fig1, fig2

if __name__ == "__main__":
    print("🚀 FINAL CAMERA & MATERIAL FIX TEST")
    print("=" * 50)
    
    fig1, fig2 = test_final_improvements()
    
    print("\n" + "=" * 50)
    print("🎯 Ready for Jupyter testing!")
    print("Expected: Points clearly separated vertically")
    print("Expected: Larger, more visible points and lines")
    print("=" * 50)