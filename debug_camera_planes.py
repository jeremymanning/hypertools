#!/usr/bin/env python3
"""
Camera plane debugging test - render squares on XY, XZ, and YZ planes
to determine camera orientation and visible planes
"""

import numpy as np
import pythreejs as p3js
from IPython.display import display

def create_plane_debug_scene():
    """Create a scene with three colored squares on different planes"""
    print("🎯 CAMERA PLANE DEBUG TEST")
    print("=" * 40)
    
    # Create scene
    scene = p3js.Scene()
    
    # Create three squares on different planes, all centered at origin
    
    # 1. XY plane (Z=0) - RED square
    xy_geometry = p3js.PlaneGeometry(width=4, height=4)
    xy_material = p3js.MeshBasicMaterial(color='red', side='DoubleSide', transparent=True, opacity=0.7)
    xy_plane = p3js.Mesh(geometry=xy_geometry, material=xy_material)
    xy_plane.position = [0, 0, 0]  # Z=0 (XY plane)
    scene.add(xy_plane)
    
    # 2. XZ plane (Y=0) - GREEN square  
    xz_geometry = p3js.PlaneGeometry(width=4, height=4)
    xz_material = p3js.MeshBasicMaterial(color='green', side='DoubleSide', transparent=True, opacity=0.7)
    xz_plane = p3js.Mesh(geometry=xz_geometry, material=xz_material)
    xz_plane.position = [0, 0, 0]  # Y=0 (XZ plane)
    xz_plane.rotation = [np.pi/2, 0, 0]  # Rotate to XZ plane
    scene.add(xz_plane)
    
    # 3. YZ plane (X=0) - BLUE square
    yz_geometry = p3js.PlaneGeometry(width=4, height=4)
    yz_material = p3js.MeshBasicMaterial(color='blue', side='DoubleSide', transparent=True, opacity=0.7)
    yz_plane = p3js.Mesh(geometry=yz_geometry, material=yz_material)
    yz_plane.position = [0, 0, 0]  # X=0 (YZ plane)
    yz_plane.rotation = [0, np.pi/2, 0]  # Rotate to YZ plane
    scene.add(yz_plane)
    
    # Add coordinate axes for reference
    # X axis - red line
    x_axis_geometry = p3js.BufferGeometry(
        attributes={
            'position': p3js.BufferAttribute(
                array=np.array([-3, 0, 0, 3, 0, 0], dtype=np.float32),
                itemSize=3
            )
        }
    )
    x_axis_material = p3js.LineBasicMaterial(color='darkred', linewidth=3)
    x_axis = p3js.Line(geometry=x_axis_geometry, material=x_axis_material)
    scene.add(x_axis)
    
    # Y axis - green line
    y_axis_geometry = p3js.BufferGeometry(
        attributes={
            'position': p3js.BufferAttribute(
                array=np.array([0, -3, 0, 0, 3, 0], dtype=np.float32),
                itemSize=3
            )
        }
    )
    y_axis_material = p3js.LineBasicMaterial(color='darkgreen', linewidth=3)
    y_axis = p3js.Line(geometry=y_axis_geometry, material=y_axis_material)
    scene.add(y_axis)
    
    # Z axis - blue line
    z_axis_geometry = p3js.BufferGeometry(
        attributes={
            'position': p3js.BufferAttribute(
                array=np.array([0, 0, -3, 0, 0, 3], dtype=np.float32),
                itemSize=3
            )
        }
    )
    z_axis_material = p3js.LineBasicMaterial(color='darkblue', linewidth=3)
    z_axis = p3js.Line(geometry=z_axis_geometry, material=z_axis_material)
    scene.add(z_axis)
    
    # Add lighting
    ambient = p3js.AmbientLight(color='#ffffff', intensity=0.6)
    scene.add(ambient)
    
    directional = p3js.DirectionalLight(color='#ffffff', intensity=0.4)
    directional.position = [1, 1, 1]
    scene.add(directional)
    
    return scene

def test_camera_positions(scene):
    """Test different camera positions to see which planes are visible"""
    
    test_configs = [
        {
            'name': '2D Mode (looking down at XY plane)',
            'position': [0, 0, 8],
            'target': [0, 0, 0],
            'up': [0, 1, 0],
            'expected': 'RED square (XY plane) should be visible'
        },
        {
            'name': 'Side view (looking at YZ plane)',
            'position': [8, 0, 0],
            'target': [0, 0, 0],
            'up': [0, 1, 0],
            'expected': 'BLUE square (YZ plane) should be visible'
        },
        {
            'name': 'Front view (looking at XZ plane)',
            'position': [0, 8, 0],
            'target': [0, 0, 0],
            'up': [0, 0, 1],
            'expected': 'GREEN square (XZ plane) should be visible'
        },
        {
            'name': '3D diagonal view',
            'position': [5, 5, 5],
            'target': [0, 0, 0],
            'up': [0, 1, 0],
            'expected': 'All three squares should be visible'
        }
    ]
    
    renderers = []
    
    for config in test_configs:
        print(f"\n📷 {config['name']}")
        print(f"Camera position: {config['position']}")
        print(f"Expected: {config['expected']}")
        
        # Create camera
        camera = p3js.PerspectiveCamera(
            fov=60,
            aspect=1.0,
            near=0.1,
            far=100
        )
        camera.position = config['position']
        camera.up = config['up']
        
        # Create controls
        controls = p3js.OrbitControls(
            controlling=camera,
            target=config['target'],
            enableDamping=True
        )
        
        # Create renderer
        renderer = p3js.Renderer(
            camera=camera,
            scene=scene,
            controls=[controls],
            width=400,
            height=400
        )
        
        renderers.append({
            'name': config['name'],
            'renderer': renderer,
            'expected': config['expected']
        })
    
    return renderers

def run_plane_debug():
    """Run the complete plane debugging test"""
    
    # Create the debug scene
    scene = create_plane_debug_scene()
    
    # Test different camera positions
    renderers = test_camera_positions(scene)
    
    print(f"\n" + "=" * 40)
    print("🎯 PLANE DEBUG RESULTS")
    print("=" * 40)
    print("Look at each renderer below:")
    print("- RED square = XY plane (Z=0) - where our 2D data lives")
    print("- GREEN square = XZ plane (Y=0)")
    print("- BLUE square = YZ plane (X=0)")
    print("- Colored axes show coordinate system")
    print("")
    print("This will tell us:")
    print("1. Which plane the camera is actually looking at")
    print("2. If there's a coordinate system issue")
    print("3. The correct camera position for 2D data")
    print("=" * 40)
    
    return renderers

if __name__ == "__main__":
    # Run in command line mode
    renderers = run_plane_debug()
    print(f"\nGenerated {len(renderers)} test renderers")
    print("Run this in Jupyter to see the visual results!")