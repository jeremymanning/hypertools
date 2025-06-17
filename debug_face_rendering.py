#!/usr/bin/env python3
"""
Debug face rendering issue - test different ways to create filled squares
"""

import numpy as np
import pythreejs as p3js
from IPython.display import display

def test_simple_triangle():
    """Test the simplest possible triangle rendering"""
    
    # Create a simple triangle
    vertices = np.array([
        [0, 0, 0],   # Bottom point
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
    
    # Try different materials
    materials = [
        ('Basic (solid)', p3js.MeshBasicMaterial(color='red', side='DoubleSide')),
        ('Basic (wireframe)', p3js.MeshBasicMaterial(color='blue', wireframe=True, side='DoubleSide')),
        ('Lambert', p3js.MeshLambertMaterial(color='green', side='DoubleSide')),
    ]
    
    results = []
    
    for name, material in materials:
        scene = p3js.Scene()
        
        # Add triangle
        triangle = p3js.Mesh(geometry=geometry, material=material)
        scene.add(triangle)
        
        # Add lighting for Lambert material
        ambient = p3js.AmbientLight(color='#ffffff', intensity=0.8)
        scene.add(ambient)
        
        # Create camera
        camera = p3js.PerspectiveCamera(fov=60, aspect=1.0, near=0.1, far=100)
        camera.position = [0, 0, 3]
        
        controls = p3js.OrbitControls(controlling=camera, target=[0, 0, 0])
        
        renderer = p3js.Renderer(
            camera=camera,
            scene=scene,
            controls=[controls],
            width=300,
            height=250
        )
        
        results.append((name, renderer))
        print(f"Created {name} triangle test")
    
    return results

def test_points_vs_mesh():
    """Compare how points vs mesh render the same positions"""
    
    # Same positions for both tests
    positions = np.array([
        [0, 1, 0],   # Top
        [1, 0, 0],   # Right  
        [0, -1, 0],  # Bottom
        [-1, 0, 0],  # Left
        [0, 0, 0]    # Center
    ], dtype=np.float32)
    
    # Test 1: Points
    scene1 = p3js.Scene()
    
    point_geometry = p3js.BufferGeometry(
        attributes={
            'position': p3js.BufferAttribute(array=positions.flatten(), itemSize=3)
        }
    )
    
    point_material = p3js.PointsMaterial(
        color='red',
        size=15,
        sizeAttenuation=False
    )
    
    points = p3js.Points(geometry=point_geometry, material=point_material)
    scene1.add(points)
    
    # Add lighting
    ambient1 = p3js.AmbientLight(color='#ffffff', intensity=1.0)
    scene1.add(ambient1)
    
    # Camera for points
    camera1 = p3js.PerspectiveCamera(fov=60, aspect=1.0, near=0.1, far=100)
    camera1.position = [0, 0, 3]
    
    controls1 = p3js.OrbitControls(controlling=camera1, target=[0, 0, 0])
    
    renderer1 = p3js.Renderer(
        camera=camera1,
        scene=scene1,
        controls=[controls1],
        width=300,
        height=250
    )
    
    # Test 2: Mesh (connecting the points)
    scene2 = p3js.Scene()
    
    # Create a simple quad using the outer 4 points
    mesh_faces = np.array([0, 1, 4, 1, 2, 4, 2, 3, 4, 3, 0, 4], dtype=np.uint32)
    
    mesh_geometry = p3js.BufferGeometry(
        attributes={
            'position': p3js.BufferAttribute(array=positions.flatten(), itemSize=3),
            'index': p3js.BufferAttribute(array=mesh_faces)
        }
    )
    
    mesh_material = p3js.MeshBasicMaterial(color='blue', side='DoubleSide', wireframe=False)
    
    mesh = p3js.Mesh(geometry=mesh_geometry, material=mesh_material)
    scene2.add(mesh)
    
    # Add lighting
    ambient2 = p3js.AmbientLight(color='#ffffff', intensity=1.0)
    scene2.add(ambient2)
    
    # Camera for mesh
    camera2 = p3js.PerspectiveCamera(fov=60, aspect=1.0, near=0.1, far=100)
    camera2.position = [0, 0, 3]
    
    controls2 = p3js.OrbitControls(controlling=camera2, target=[0, 0, 0])
    
    renderer2 = p3js.Renderer(
        camera=camera2,
        scene=scene2,
        controls=[controls2],
        width=300,
        height=250
    )
    
    return [
        ('Points (should show 5 red dots)', renderer1),
        ('Mesh (should show blue diamond shape)', renderer2)
    ]

if __name__ == "__main__":
    print("🔍 FACE RENDERING DEBUG TEST")
    print("This tests if triangle/mesh rendering works correctly")
    
    triangle_tests = test_simple_triangle()
    comparison_tests = test_points_vs_mesh()
    
    print(f"\nCreated {len(triangle_tests)} triangle tests")
    print(f"Created {len(comparison_tests)} comparison tests")
    print("\nRun in Jupyter to see visual results!")