# pythreejs Y-Axis Debugging Session - June 14, 2025

## 🚨 **CRITICAL UNRESOLVED ISSUE**

**Status**: ❌ **Y-axis rendering still broken** despite multiple fixes
**Time Spent**: Several hours of systematic debugging
**Core Problem**: All 2D points render on y=0 line in Jupyter, despite correct data processing

---

## 📊 **PROBLEM SUMMARY**

### **Current Symptoms**
1. **Y-axis collapse**: All points appear on horizontal line (y=0) regardless of actual Y values
2. **Visual issues**: Points rendered as squares (not circles), lines too thin
3. **Camera confusion**: Camera positioning seems correct but view is wrong
4. **Jupyter-specific**: Issue only appears in Jupyter notebooks with pythreejs widgets

### **User Testing Results**
After all fixes applied:
- ✅ Dot sizes better (after removing 2x multiplier)
- ✅ Data processing correct (Y values preserved: 3, 0, -3)
- ❌ All coordinates still on y=0 line
- ❌ Lines still too thin
- ❌ Points rendering as squares instead of circles

---

## 🔧 **FIXES ATTEMPTED**

### **1. Camera Positioning Evolution**

**Original Setup**:
```python
self.camera.position = [0, 0, 1]  # Too close
```

**First Fix** (didn't work):
```python
self.camera.position = [x_center, y_center, 10]
self.camera.lookAt = [x_center, y_center, z_center]
```

**Second Fix** (still didn't work):
```python
# Changed from OrthographicCamera to PerspectiveCamera
self.camera = p3js.PerspectiveCamera(fov=45, aspect=1.0)
self.camera.position = [x_center, y_center, camera_distance]
```

**Final Fix** (current state - STILL NOT WORKING):
```python
# Camera directly above data center looking down
self.camera.position = [x_center, y_center, camera_distance]
self.camera.up = [0, 1, 0]
self.controls = [p3js.OrbitControls(
    target=[x_center, y_center, 0],  # Look at XY plane
    enableRotate=False
)]
```

### **2. BufferAttribute Normalization**

**Critical Discovery**: BufferAttribute had `normalized=True` causing position flattening

**Fix Applied**:
```python
'position': p3js.BufferAttribute(
    array=positions.astype(np.float32),
    itemSize=3,
    normalized=False  # Added this to all geometries
)
```

### **3. Material Improvements**
- Adjusted point sizes (removed 2x multiplier)
- Increased line thickness to 1.5x
- Enhanced lighting system (ambient + directional + point)
- Removed vertexColors settings

---

## 🔍 **DIAGNOSTIC FINDINGS**

### **Data Processing Verification**
```python
# Test data: [[0, 3], [0, 0], [0, -3]]
3D positions:
[[ 0.  3.  0.]
 [ 0.  0.  0.]
 [ 0. -3.  0.]]
Y values in 3D: [ 3.  0. -3.]  # ✅ CORRECT
```

### **Camera Debug Output**
```
Camera position: (0.0, 0.0, 9.0)  # Directly above
Camera target: (0.0, 0.0, 0.0)    # Looking at origin
Camera up: (0.0, 1.0, 0.0)        # Y-up
```

### **Geometry Inspection**
```
BufferGeometry(attributes={'position': BufferAttribute(
    array=array([0., 3., 0., 0., 0., 0., 0., -3., 0.], dtype=float32)
)})
```
The Y values (3, 0, -3) are present in the geometry! ✅

---

## 🎯 **NEXT DEBUGGING PLAN**

### **Theory 1: Camera Matrix Issue**
The camera might need explicit matrix updates:
```python
# Test 1: Force camera to look at XY plane
self.camera.lookAt([x_center, y_center, 0])
self.camera.updateProjectionMatrix()
self.camera.updateMatrixWorld()
```

### **Theory 2: Widget Rendering Pipeline**
pythreejs might have issues with how it translates Three.js objects to the widget:
```python
# Test 2: Create minimal pythreejs example
# Compare raw Three.js vs pythreejs widget rendering
# Check if issue is in pythreejs library itself
```

### **Theory 3: Coordinate System Mismatch**
Three.js and pythreejs might have different coordinate conventions:
```python
# Test 3: Try different coordinate orientations
# Swap Y/Z coordinates
# Test with camera looking along different axes
```

### **Theory 4: Scene Transform Issue**
The scene or renderer might have a transform applied:
```python
# Test 4: Check scene and renderer transforms
# Look for any scaling or rotation on the scene
# Check renderer viewport settings
```

### **Theory 5: WebGL/Browser Rendering**
The issue might be in how the browser renders the WebGL context:
```python
# Test 5: Export scene to HTML and check raw WebGL
# Compare notebook rendering vs standalone HTML
# Test in different browsers
```

---

## 🛠️ **DETAILED DEBUGGING PLAN FOR NEXT SESSION**

### **Step 1: Minimal pythreejs Test**
Create the absolute simplest pythreejs example that should show Y variation:
```python
import pythreejs as p3js
import numpy as np

# Just 3 points: top, middle, bottom
positions = np.array([
    [0, 1, 0],   # Top
    [0, 0, 0],   # Center  
    [0, -1, 0]   # Bottom
], dtype=np.float32).flatten()

# Basic scene
scene = p3js.Scene()
geometry = p3js.BufferGeometry(
    attributes={'position': p3js.BufferAttribute(array=positions, itemSize=3)}
)
material = p3js.PointsMaterial(color='red', size=10)
points = p3js.Points(geometry=geometry, material=material)
scene.add(points)

# Simple camera looking down Z axis at XY plane
camera = p3js.PerspectiveCamera(position=[0, 0, 5])
renderer = p3js.Renderer(camera=camera, scene=scene, width=400, height=400)
```

### **Step 2: Camera Orientation Tests**
Test different camera orientations systematically:
```python
# Test A: Look down Z axis (current approach)
camera.position = [0, 0, 5]
camera.lookAt([0, 0, 0])

# Test B: Look down Y axis  
camera.position = [0, 5, 0]
camera.lookAt([0, 0, 0])
camera.up = [0, 0, 1]

# Test C: Look down X axis
camera.position = [5, 0, 0]
camera.lookAt([0, 0, 0])
camera.up = [0, 1, 0]
```

### **Step 3: Raw Three.js Comparison**
Create identical scene in raw Three.js (via HTML) to isolate pythreejs issues:
```html
<script src="three.js"></script>
<script>
// Exact same scene setup in raw Three.js
// Compare rendering results
</script>
```

### **Step 4: Matrix Debugging**
Log all transformation matrices:
```python
print(f"Camera matrix: {camera.matrix}")
print(f"Camera projection: {camera.projectionMatrix}")
print(f"Scene matrix: {scene.matrix}")
```

### **Step 5: Alternative Approaches**
If pythreejs continues to fail:
1. Try older pythreejs version
2. Use different Three.js Python binding
3. Generate static HTML with Three.js
4. Consider Plotly 3D scatter as fallback

---

## 📁 **KEY FILES TO REFERENCE**

### **Implementation Files**
- `hypertools/core/threejs_backend.py` - Main implementation (lines 383-421 for camera)
- `hypertools/plot/plot.py` - Plot interface with auto-show

### **Test Files**
- `test_normalized_fix_jupyter.ipynb` - Latest test notebook
- `debug_jupyter_issue.py` - Diagnostic script showing correct data
- `test_complete_fix_jupyter.ipynb` - Comprehensive test cases

---

## 💡 **CRITICAL INSIGHTS**

1. **Data is correct**: Y values are properly stored in geometry (verified multiple times)
2. **Camera math seems right**: Position and target calculations are theoretically correct
3. **Issue is rendering-specific**: Only affects Jupyter widget display
4. **pythreejs might be the culprit**: Library-level issue possible

---

## 🎯 **PRIORITY FOR NEXT SESSION**

**MUST SOLVE**: The Y-axis rendering issue before any other work

**Approach**: Start with the minimal pythreejs test to isolate whether:
1. It's our camera setup code
2. It's a pythreejs library bug
3. It's a coordinate system mismatch
4. It's a Jupyter widget rendering issue

**Success Metric**: Points displaying at correct Y positions in Jupyter notebooks

---

## 📝 **SESSION SUMMARY**

Despite extensive debugging and multiple fixes, the core issue remains: **2D points render on y=0 line in Jupyter notebooks**. The data processing is correct, camera positioning seems right, but the visual output is wrong. This suggests a deeper issue with either pythreejs widget rendering or a fundamental misunderstanding of the coordinate system.

**Next session should start with the minimal pythreejs test to isolate the exact cause.**