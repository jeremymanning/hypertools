#!/usr/bin/env python3
"""
Test if position array flattening is causing the y=0 line issue
"""

import numpy as np
import pythreejs as p3js
import sys
sys.path.insert(0, '/Users/jmanning/hypertools')

def test_flattening_issue():
    """Test different ways of passing position data to BufferAttribute"""
    
    print("🔍 TESTING POSITION FLATTENING ISSUE")
    print("=" * 50)
    
    # Test data with clear Y separation
    test_positions_3d = np.array([
        [0, 2, 0],   # Top
        [1, 1, 0],   # Middle-right
        [2, 0, 0],   # Center
        [3, -1, 0],  # Middle-left
        [4, -2, 0]   # Bottom
    ], dtype=np.float32)
    
    print("Original position data (should have Y values: 2, 1, 0, -1, -2):")
    for i, (x, y, z) in enumerate(test_positions_3d):
        print(f"  Point {i+1}: ({x}, {y}, {z})")
    
    # Test 1: Flattened array (current implementation)
    flattened = test_positions_3d.flatten()
    print(f"\nFlattened array: {flattened}")
    print(f"Length: {len(flattened)} (should be 15 for 5 points * 3 coords)")
    
    # Test 2: Create Points with flattened array
    geometry1 = p3js.BufferGeometry(
        attributes={
            'position': p3js.BufferAttribute(
                array=flattened,
                itemSize=3,
                normalized=False
            )
        }
    )
    
    material1 = p3js.PointsMaterial(
        color='red',
        size=15,
        sizeAttenuation=False
    )
    
    points1 = p3js.Points(geometry=geometry1, material=material1)
    
    scene1 = p3js.Scene()
    scene1.add(points1)
    
    # Add lighting
    ambient1 = p3js.AmbientLight(color='#ffffff', intensity=1.0)
    scene1.add(ambient1)
    
    # Camera
    camera1 = p3js.PerspectiveCamera(fov=45, aspect=1.0, near=0.1, far=100)
    camera1.position = [2, 0, 8]  # Looking at center
    
    controls1 = p3js.OrbitControls(
        controlling=camera1,
        target=[2, 0, 0],
        enableRotate=False,
        enableDamping=True
    )
    
    renderer1 = p3js.Renderer(
        camera=camera1,
        scene=scene1,
        controls=[controls1],
        width=400,
        height=300
    )
    
    # Test 3: Create Points with non-flattened array (test alternative)
    try:
        geometry2 = p3js.BufferGeometry(
            attributes={
                'position': p3js.BufferAttribute(
                    array=test_positions_3d,  # Not flattened
                    itemSize=3,
                    normalized=False
                )
            }
        )
        
        material2 = p3js.PointsMaterial(
            color='blue',
            size=15,
            sizeAttenuation=False
        )
        
        points2 = p3js.Points(geometry=geometry2, material=material2)
        
        scene2 = p3js.Scene()
        scene2.add(points2)
        
        ambient2 = p3js.AmbientLight(color='#ffffff', intensity=1.0)
        scene2.add(ambient2)
        
        camera2 = p3js.PerspectiveCamera(fov=45, aspect=1.0, near=0.1, far=100)
        camera2.position = [2, 0, 8]
        
        controls2 = p3js.OrbitControls(
            controlling=camera2,
            target=[2, 0, 0],
            enableRotate=False,
            enableDamping=True
        )
        
        renderer2 = p3js.Renderer(
            camera=camera2,
            scene=scene2,
            controls=[controls2],
            width=400,
            height=300
        )
        
        non_flattened_works = True
        
    except Exception as e:
        print(f"Non-flattened array failed: {e}")
        renderer2 = None
        non_flattened_works = False
    
    print("\n" + "=" * 50)
    print("ANALYSIS:")
    print("Both tests should show 5 dots spread vertically")
    print("If BOTH show dots on horizontal line → issue is elsewhere")
    print("If flattened fails but non-flattened works → found the bug!")
    print("=" * 50)
    
    return {
        'flattened_renderer': renderer1,
        'non_flattened_renderer': renderer2,
        'non_flattened_works': non_flattened_works,
        'test_data': test_positions_3d,
        'flattened_data': flattened
    }

if __name__ == "__main__":
    results = test_flattening_issue()
    print("\nRun this in Jupyter to see the visual comparison!")