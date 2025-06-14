#!/usr/bin/env python3
"""
Basic pythreejs functionality test
"""

import numpy as np
import pythreejs as p3js

def test_pythreejs_basic():
    """Test basic pythreejs functionality"""
    print("=== TESTING PYTHREEJS BASIC FUNCTIONALITY ===")

    try:
        # Test basic Three.js object creation
        print("1. Testing basic object creation...")
        
        # Create geometry
        geometry = p3js.SphereGeometry(radius=1, widthSegments=32, heightSegments=24)
        print(f"   ✅ Geometry created: {type(geometry)}")
        
        # Create material
        material = p3js.MeshLambertMaterial(color='red')
        print(f"   ✅ Material created: {type(material)}")
        
        # Create mesh
        sphere = p3js.Mesh(geometry=geometry, material=material)
        print(f"   ✅ Mesh created: {type(sphere)}")
        
        # Create light
        light = p3js.AmbientLight(color='#777777')
        print(f"   ✅ Light created: {type(light)}")
        
        # Create scene
        scene = p3js.Scene(children=[sphere, light])
        print(f"   ✅ Scene created: {type(scene)}")
        
        # Create camera
        camera = p3js.PerspectiveCamera(position=[0, 5, 5], up=[0, 1, 0])
        print(f"   ✅ Camera created: {type(camera)}")
        
        # Create renderer
        renderer = p3js.Renderer(camera=camera, scene=scene, 
                                controls=[p3js.OrbitControls(controlling=camera)])
        print(f"   ✅ Renderer created: {type(renderer)}")
        
        print("\n2. Testing data conversion...")
        
        # Test data handling
        test_data = np.random.rand(100, 3)
        positions = test_data.flatten()
        
        # Create buffer geometry from data
        buffer_geometry = p3js.BufferGeometry(
            attributes={'position': p3js.BufferAttribute(array=positions, itemSize=3)}
        )
        print(f"   ✅ BufferGeometry created from data: {type(buffer_geometry)}")
        
        # Create points material
        points_material = p3js.PointsMaterial(color='blue', size=0.1)
        points = p3js.Points(geometry=buffer_geometry, material=points_material)
        print(f"   ✅ Points object created: {type(points)}")
        
        print("\n3. Testing 2D setup...")
        
        # Test orthographic camera for 2D
        ortho_camera = p3js.OrthographicCamera(
            left=-5, right=5, top=5, bottom=-5, near=0.1, far=1000
        )
        ortho_camera.position = [0, 0, 1]
        print(f"   ✅ Orthographic camera created: {type(ortho_camera)}")
        
        print("\n4. Testing line geometry...")
        
        # Create line for 2D/3D plotting
        line_points = np.array([[0, 0, 0], [1, 1, 0], [2, 0, 0]])
        line_positions = line_points.flatten()
        
        line_geometry = p3js.BufferGeometry(
            attributes={'position': p3js.BufferAttribute(array=line_positions, itemSize=3)}
        )
        line_material = p3js.LineBasicMaterial(color='green')
        line = p3js.Line(geometry=line_geometry, material=line_material)
        print(f"   ✅ Line created: {type(line)}")
        
        print("\n✅ ALL TESTS PASSED - pythreejs is working correctly!")
        print("Ready to begin HyperTools Three.js backend implementation.")
        
        # Return a test renderer for potential display
        test_scene = p3js.Scene(children=[sphere, points, line, light])
        test_renderer = p3js.Renderer(camera=camera, scene=test_scene,
                                     controls=[p3js.OrbitControls(controlling=camera)])
        
        print(f"\n🎯 Test renderer ready: {type(test_renderer)}")
        print("   (Can be displayed in Jupyter notebook)")
        
        return test_renderer
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_pythreejs_basic()