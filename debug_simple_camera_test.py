#!/usr/bin/env python3
"""
Simple camera test - just render points at different positions to see which are visible
"""

import numpy as np
import pythreejs as p3js
from IPython.display import display

def create_simple_test_scene():
    """Create a simple scene with points at known positions"""
    scene = p3js.Scene()
    
    # Create points at specific positions to test coordinate system
    test_points = [
        # Format: [x, y, z, color, label]
        [0, 0, 0, 'white', 'Origin'],
        [2, 0, 0, 'red', '+X axis'],
        [-2, 0, 0, 'darkred', '-X axis'],
        [0, 2, 0, 'green', '+Y axis (UP)'],
        [0, -2, 0, 'darkgreen', '-Y axis (DOWN)'],
        [0, 0, 2, 'blue', '+Z axis'],
        [0, 0, -2, 'darkblue', '-Z axis'],
    ]
    
    for x, y, z, color, label in test_points:
        # Create point geometry
        geometry = p3js.BufferGeometry(
            attributes={
                'position': p3js.BufferAttribute(
                    array=np.array([x, y, z], dtype=np.float32),
                    itemSize=3
                )
            }
        )
        
        # Create point material
        material = p3js.PointsMaterial(
            color=color,
            size=20,  # Large size to be clearly visible
            sizeAttenuation=False
        )
        
        # Create point object
        point = p3js.Points(geometry=geometry, material=material)
        scene.add(point)
        
        print(f"Added {label} point at ({x}, {y}, {z}) in {color}")
    
    # Add lighting
    ambient = p3js.AmbientLight(color='#ffffff', intensity=1.0)
    scene.add(ambient)
    
    return scene

def test_2d_camera_view():
    """Test our 2D camera setup to see which points are visible"""
    
    # Create the test scene
    scene = create_simple_test_scene()
    
    # Set up 2D camera (same as our hypertools setup)
    camera = p3js.PerspectiveCamera(
        fov=45,
        aspect=1.0,
        near=0.1,
        far=1000
    )
    
    # Position camera looking down at XY plane (Z=0)
    camera.position = [0, 0, 8]  # Looking from +Z
    camera.up = [0, 1, 0]  # Y points up
    
    # 2D controls
    controls = p3js.OrbitControls(
        controlling=camera,
        target=[0, 0, 0],  # Look at origin
        enableRotate=False,  # 2D mode
        enableDamping=True
    )
    
    # Create renderer
    renderer = p3js.Renderer(
        camera=camera,
        scene=scene,
        controls=[controls],
        width=600,
        height=500
    )
    
    print("\n" + "="*50)
    print("🎯 2D CAMERA TEST")
    print("="*50)
    print("Camera position: [0, 0, 8] (looking down from +Z)")
    print("Camera target: [0, 0, 0] (origin)")
    print("Camera up: [0, 1, 0] (Y axis points up)")
    print("\nExpected visible points:")
    print("- WHITE dot at origin (0, 0, 0)")
    print("- RED dot on right (+X axis)")
    print("- DARK RED dot on left (-X axis)")
    print("- GREEN dot on top (+Y axis)")
    print("- DARK GREEN dot on bottom (-Y axis)")
    print("\nNOT visible (behind camera):")
    print("- BLUE/DARK BLUE dots (+/-Z axis)")
    print("="*50)
    
    return renderer

if __name__ == "__main__":
    print("🔍 SIMPLE CAMERA DEBUG TEST")
    print("This tests if our coordinate system is working correctly")
    
    renderer = test_2d_camera_view()
    print("\nRun this in Jupyter to see the visual result!")