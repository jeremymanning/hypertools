#!/usr/bin/env python3
"""
Simple face rendering test - run this directly in Jupyter
"""

import numpy as np
import pythreejs as p3js

def create_simple_test():
    """Create a simple test to see if we can render a filled triangle"""
    
    print("🔍 SIMPLE FACE RENDERING TEST")
    print("=" * 40)
    
    # Test 1: Simple triangle
    vertices = np.array([
        [0, 0, 0],   # Bottom
        [1, 1, 0],   # Top right
        [-1, 1, 0]   # Top left
    ], dtype=np.float32)
    
    faces = np.array([0, 1, 2], dtype=np.uint32)
    
    geometry = p3js.BufferGeometry(
        attributes={
            'position': p3js.BufferAttribute(array=vertices.flatten(), itemSize=3),
            'index': p3js.BufferAttribute(array=faces)
        }
    )
    
    material = p3js.MeshBasicMaterial(color='red', side='DoubleSide')
    triangle = p3js.Mesh(geometry=geometry, material=material)
    
    scene = p3js.Scene()
    scene.add(triangle)
    
    # Add lighting
    ambient = p3js.AmbientLight(color='#ffffff', intensity=1.0)
    scene.add(ambient)
    
    # Create camera
    camera = p3js.PerspectiveCamera(fov=60, aspect=1.0, near=0.1, far=100)
    camera.position = [0, 0, 3]
    
    controls = p3js.OrbitControls(controlling=camera, target=[0, 0.5, 0])
    
    renderer = p3js.Renderer(
        camera=camera,
        scene=scene,
        controls=[controls],
        width=400,
        height=300
    )
    
    print("Triangle test created")
    print("EXPECTED: Solid red triangle")
    print("If you see lines instead → Face rendering is broken")
    
    return renderer

def create_points_test():
    """Test points rendering for comparison"""
    
    positions = np.array([
        [0, 1, 0],   # Top
        [1, 0, 0],   # Right  
        [0, -1, 0],  # Bottom
        [-1, 0, 0],  # Left
        [0, 0, 0]    # Center
    ], dtype=np.float32)
    
    scene = p3js.Scene()
    
    point_geometry = p3js.BufferGeometry(
        attributes={
            'position': p3js.BufferAttribute(array=positions.flatten(), itemSize=3)
        }
    )
    
    point_material = p3js.PointsMaterial(
        color='blue',
        size=20,
        sizeAttenuation=False
    )
    
    points = p3js.Points(geometry=point_geometry, material=point_material)
    scene.add(points)
    
    # Add lighting
    ambient = p3js.AmbientLight(color='#ffffff', intensity=1.0)
    scene.add(ambient)
    
    # Camera
    camera = p3js.PerspectiveCamera(fov=60, aspect=1.0, near=0.1, far=100)
    camera.position = [0, 0, 3]
    
    controls = p3js.OrbitControls(controlling=camera, target=[0, 0, 0])
    
    renderer = p3js.Renderer(
        camera=camera,
        scene=scene,
        controls=[controls],
        width=400,
        height=300
    )
    
    print("Points test created")
    print("EXPECTED: 5 blue dots in cross pattern")
    
    return renderer

if __name__ == "__main__":
    # Run in command line
    triangle_renderer = create_simple_test()
    points_renderer = create_points_test()
    print("\nRun these functions in Jupyter to see the renderers!")