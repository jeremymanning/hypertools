#!/usr/bin/env python3
"""
Quick test to simulate what the notebook should now show
"""

import numpy as np
import sys
sys.path.insert(0, '/Users/jmanning/hypertools')
import hypertools as hyp

def main():
    print("🎯 SIMULATING FIXED NOTEBOOK BEHAVIOR")
    print("=" * 50)
    
    # Test the exact first case from the failing notebook
    print("Figure 1: 2D Scatter Plot (red circles)")
    np.random.seed(123)
    data_2d_scatter = np.random.randn(50, 2) * 2
    print(f"Data shape: {data_2d_scatter.shape}")
    print(f"Y range: {data_2d_scatter[:, 1].min():.2f} to {data_2d_scatter[:, 1].max():.2f}")
    
    fig1 = hyp.plot(data_2d_scatter, 'ro', markersize=8, alpha=0.7)
    
    print(f"Camera position: {fig1.camera.position}")
    print(f"Camera target: {fig1.controls[0].target if hasattr(fig1.controls[0], 'target') else 'N/A'}")
    
    # Verify the camera is looking down at the data
    cam_z = fig1.camera.position[2]
    if cam_z > 5:
        print("✅ Camera properly positioned above data plane")
        print(f"   Distance from data: {cam_z} units")
    else:
        print("❌ Camera positioning issue")
    
    # Check if the camera center matches the data center
    data_center_x = data_2d_scatter[:, 0].mean()
    data_center_y = data_2d_scatter[:, 1].mean()
    cam_center_x = fig1.camera.position[0]
    cam_center_y = fig1.camera.position[1]
    
    print(f"Data center: ({data_center_x:.2f}, {data_center_y:.2f})")
    print(f"Camera center: ({cam_center_x:.2f}, {cam_center_y:.2f})")
    
    if abs(cam_center_x - data_center_x) < 0.1 and abs(cam_center_y - data_center_y) < 0.1:
        print("✅ Camera properly centered on data")
    else:
        print("❌ Camera centering issue")
    
    print("\n" + "=" * 50)
    print("🎉 CAMERA FIX VERIFICATION:")
    print("- Points should now be distributed across full Y range")
    print("- No more clustering on y=0 line")
    print("- Interactive controls should work smoothly")
    print("=" * 50)
    
    return fig1

if __name__ == "__main__":
    fig = main()
    
    # Optional: Test matplotlib conversion still works
    print("\n📊 Testing matplotlib compatibility...")
    try:
        mpl_fig = fig.to_matplotlib()
        print("✅ Matplotlib conversion works")
    except Exception as e:
        print(f"❌ Matplotlib issue: {e}")
