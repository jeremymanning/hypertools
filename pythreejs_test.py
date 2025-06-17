#!/usr/bin/env python3
"""
Basic pythreejs functionality test to verify the widget system works
"""

import pythreejs as p3js
import numpy as np

def test_basic_pythreejs():
    """Test if pythreejs can create basic objects"""
    print("Testing basic pythreejs functionality...")
    
    try:
        # Create a basic scene
        scene = p3js.Scene()
        print("✅ Scene created successfully")
        
        # Create a camera
        camera = p3js.PerspectiveCamera(fov=75, aspect=1.0, near=0.1, far=1000)
        camera.position = [0, 0, 5]
        print("✅ Camera created successfully")
        
        # Create a simple cube geometry
        geometry = p3js.BoxGeometry(width=1, height=1, depth=1)
        material = p3js.MeshBasicMaterial(color='red')
        cube = p3js.Mesh(geometry=geometry, material=material)
        scene.add(cube)
        print("✅ Cube mesh created and added to scene")
        
        # Create renderer
        renderer = p3js.Renderer(
            camera=camera,
            scene=scene,
            controls=[p3js.OrbitControls(controlling=camera)],
            width=400,
            height=300
        )
        print("✅ Renderer created successfully")
        
        # Test position arrays (like our data points)
        positions = np.array([
            1.0, 2.0, 0.0,  # Point 1
            -1.0, -2.0, 0.0,  # Point 2
            0.0, 0.0, 1.0   # Point 3
        ], dtype=np.float32)
        
        point_geometry = p3js.BufferGeometry(
            attributes={
                'position': p3js.BufferAttribute(
                    array=positions,
                    itemSize=3
                )
            }
        )
        point_material = p3js.PointsMaterial(color='blue', size=0.1)
        points = p3js.Points(geometry=point_geometry, material=point_material)
        scene.add(points)
        print("✅ Points geometry created successfully")
        
        print("\n🎯 pythreejs basic functionality test: PASSED")
        print("📋 Renderer object ready for display")
        
        return renderer
        
    except Exception as e:
        print(f"❌ pythreejs test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_2d_positions():
    """Test the specific case causing issues: 2D positions with Z=0"""
    print("\nTesting 2D position handling...")
    
    try:
        # Simulate our 2D data conversion
        data_2d = np.array([
            [1.5, -2.3],
            [0.5, 1.2], 
            [-1.0, 0.8],
            [2.0, -0.5]
        ])
        
        # Convert to 3D positions like our code does
        positions_3d = np.column_stack([
            data_2d[:, 0],  # x
            data_2d[:, 1],  # y  
            np.zeros(len(data_2d))  # z = 0
        ])
        
        positions_flat = positions_3d.flatten().astype(np.float32)
        
        print(f"Original 2D data shape: {data_2d.shape}")
        print(f"Original 2D data:\n{data_2d}")
        print(f"3D positions shape: {positions_3d.shape}")
        print(f"3D positions:\n{positions_3d}")
        print(f"Flattened positions shape: {positions_flat.shape}")
        print(f"Flattened positions: {positions_flat}")
        
        # Create geometry
        geometry = p3js.BufferGeometry(
            attributes={
                'position': p3js.BufferAttribute(
                    array=positions_flat,
                    itemSize=3
                )
            }
        )
        
        # Check the created attribute
        pos_attr = geometry.attributes['position']
        print(f"BufferAttribute array length: {len(pos_attr.array)}")
        print(f"BufferAttribute itemSize: {pos_attr.itemSize}")
        print(f"Expected point count: {len(pos_attr.array) / pos_attr.itemSize}")
        
        print("✅ 2D position conversion test: PASSED")
        
        return geometry
        
    except Exception as e:
        print(f"❌ 2D position test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("=" * 50)
    print("PYTHREEJS DIAGNOSTIC TEST")
    print("=" * 50)
    
    # Test 1: Basic functionality
    renderer = test_basic_pythreejs()
    
    # Test 2: 2D position handling
    geometry = test_2d_positions()
    
    print("\n" + "=" * 50)
    if renderer and geometry:
        print("🎉 ALL TESTS PASSED - pythreejs is working correctly")
        print("📝 The issue may be elsewhere (widget display, camera setup, etc.)")
    else:
        print("❌ TESTS FAILED - pythreejs has fundamental issues")
    print("=" * 50)