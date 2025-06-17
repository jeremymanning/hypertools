#!/usr/bin/env python3
"""
Debug why points still appear on y=0 in Jupyter
"""

import numpy as np
import pythreejs as p3js
import sys
sys.path.insert(0, '/Users/jmanning/hypertools')

def test_pythreejs_directly():
    """Test pythreejs rendering directly without HyperTools"""
    print("🔍 TESTING PYTHREEJS DIRECTLY")
    print("=" * 50)
    
    # Create simple test data
    positions = np.array([
        [0.0, 3.0, 0.0],   # Top
        [0.0, 0.0, 0.0],   # Center
        [0.0, -3.0, 0.0],  # Bottom
    ], dtype=np.float32)
    
    print(f"Test positions:\n{positions}")
    print(f"Y values: {positions[:, 1]}")
    
    # Create scene
    scene = p3js.Scene()
    
    # Create geometry with positions
    geometry = p3js.BufferGeometry(
        attributes={
            'position': p3js.BufferAttribute(
                array=positions.flatten(),
                itemSize=3
            )
        }
    )
    
    # Create points material (circles, not squares)
    material = p3js.PointsMaterial(
        color='red',
        size=10,  # Reasonable size
        sizeAttenuation=False
    )
    
    points = p3js.Points(geometry=geometry, material=material)
    scene.add(points)
    
    # Create camera looking down at XY plane
    camera = p3js.PerspectiveCamera(
        fov=50,
        aspect=1.0,
        near=0.1,
        far=100
    )
    camera.position = [0, 0, 10]  # Look down from above
    camera.up = [0, 1, 0]  # Y is up
    
    # Create renderer
    renderer = p3js.Renderer(
        camera=camera,
        scene=scene,
        controls=[p3js.OrbitControls(
            controlling=camera,
            target=[0, 0, 0],
            enableRotate=False
        )],
        width=400,
        height=400
    )
    
    print("\n✅ Created pythreejs renderer directly")
    print("📋 Expected: 3 red dots at Y = 3, 0, -3")
    
    return renderer

def check_hypertools_data():
    """Check what HyperTools is doing with the data"""
    import hypertools as hyp
    
    print("\n🔍 CHECKING HYPERTOOLS DATA PROCESSING")
    print("=" * 50)
    
    # Simple test data
    data = np.array([
        [0, 3],    # Top
        [0, 0],    # Center
        [0, -3]    # Bottom
    ])
    
    # Create figure without showing
    fig = hyp.plot(data, 'ro', markersize=10)
    
    # Check the internal data
    print(f"Number of datasets: {fig.n_datasets}")
    print(f"Dataset shape: {fig.datasets[0].shape}")
    print(f"Dataset:\n{fig.datasets[0]}")
    
    # Check 3D positions
    positions = fig._data_to_positions(fig.datasets[0])
    positions_3d = positions.reshape(-1, 3)
    print(f"\n3D positions:\n{positions_3d}")
    print(f"Y values in 3D: {positions_3d[:, 1]}")
    
    # Check camera
    print(f"\nCamera type: {type(fig.camera).__name__}")
    print(f"Camera position: {fig.camera.position}")
    print(f"Camera up: {fig.camera.up if hasattr(fig.camera, 'up') else 'N/A'}")
    
    # Check if there's a transform issue
    print(f"\nScene children: {len(fig.scene.children)}")
    for i, child in enumerate(fig.scene.children):
        print(f"  Child {i}: {type(child).__name__}")
        if isinstance(child, p3js.Points):
            print(f"    Geometry: {child.geometry}")
            print(f"    Material: {child.material}")
            
    return fig

if __name__ == "__main__":
    print("🚨 JUPYTER Y=0 DEBUG")
    print("=" * 60)
    
    # Test 1: Raw pythreejs
    renderer = test_pythreejs_directly()
    
    # Test 2: HyperTools processing
    fig = check_hypertools_data()
    
    print("\n" + "=" * 60)
    print("📋 ANALYSIS:")
    print("- Check if raw pythreejs shows correct Y positions")
    print("- Check if HyperTools data processing is correct")
    print("- Identify where Y coordinates get lost")
    print("=" * 60)