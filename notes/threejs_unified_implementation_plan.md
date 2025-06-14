# Three.js Unified Backend Implementation Plan

## 🎯 **Strategic Decision: Single Three.js Rendering Engine**

**Core Philosophy**: One rendering engine for everything
- ✅ **No backend selection** - users just call `hyp.plot()`
- ✅ **Unified API** - same code works for 2D, 3D, static, animated
- ✅ **Consistent quality** - vector output for everything
- ✅ **Universal compatibility** - works in all Jupyter environments

---

## 🎨 **Three.js 2D Capabilities Verification**

### **Three.js is Excellent for 2D Plots**

#### **Approach 1: Orthographic Camera (True 2D)**
```javascript
// Three.js 2D rendering approach
const camera = new THREE.OrthographicCamera(
    -width/2, width/2, height/2, -height/2, 0.1, 1000
);
camera.position.z = 1;

// Results in perfect 2D plots with 3D engine benefits:
// - Hardware acceleration
// - Vector export via SVGRenderer  
// - Smooth animations
// - Consistent with 3D pipeline
```

#### **Approach 2: Fixed Perspective (2D in 3D space)**
```javascript
// 2D plot as plane in 3D space
const camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);
camera.position.set(0, 0, distance);
camera.lookAt(0, 0, 0);
// Disable orbit controls for pure 2D behavior
```

### **2D Plot Types in Three.js:**
- ✅ **Scatter plots**: Points as THREE.Points or THREE.Sprites
- ✅ **Line plots**: THREE.Line with BufferGeometry
- ✅ **Filled areas**: THREE.Shape + THREE.ShapeGeometry
- ✅ **Heatmaps**: THREE.PlaneGeometry with custom shaders
- ✅ **Annotations**: THREE.CSS2DRenderer for HTML text
- ✅ **Legends/Axes**: Custom geometry + text rendering

---

## 🏗️ **Architecture Overview**

### **Unified Data Flow:**
```python
# Single API for everything
hyp.plot(data)                    # → Auto-detect 2D/3D → Three.js
hyp.plot(data, animate='window')  # → Animated → Three.js
hyp.plot(data, save='plot.svg')   # → Vector export → Three.js SVGRenderer

# No backend parameter needed - Three.js handles everything
```

### **Core Components:**

```python
class HyperToolsFigure:
    """Universal figure object - always Three.js backend"""
    
    def __init__(self, data, plot_type, **kwargs):
        self.data = data
        self.plot_type = plot_type
        self.kwargs = kwargs
        self.threejs_scene = None
        self._create_threejs_plot()
    
    def show(self):
        """Display interactive Three.js plot"""
        return self.threejs_widget
    
    def to_matplotlib(self):
        """Convert to matplotlib figure for fine-tuning"""
        return self._convert_to_matplotlib()
    
    def save(self, filename):
        """Save figure object for later reloading"""
        # Serialize data + parameters
    
    def export(self, filename, **kwargs):
        """Export in various formats (SVG, PNG, HTML)"""
        # Use Three.js renderers

class HyperToolsThreeJS:
    """Unified Three.js rendering system"""
    
    def plot(self, data, **kwargs):
        # Always returns HyperToolsFigure object
        return HyperToolsFigure(data, self._detect_plot_type(data), **kwargs)
```

---

## 📋 **Detailed Implementation Plan**

### **Phase 1: Foundation (Week 1-2)**

#### **Week 1: Basic Three.js Integration**

**Goals:**
- ✅ Working Three.js plots in Jupyter (all platforms)
- ✅ Basic 2D scatter/line plots  
- ✅ Basic 3D scatter/line plots
- ✅ Interactive controls (zoom, pan, rotate)

**Tasks:**
1. **Set up pythreejs integration**
   ```python
   # hypertools/core/threejs_backend.py
   import pythreejs as p3js
   import numpy as np
   
   class ThreeJSBackend:
       def __init__(self):
           self.p3js = p3js
           
       def create_basic_plot(self, data):
           # Convert data to Three.js geometry
           # Set up scene, camera, renderer
           # Return interactive widget
   ```

2. **Implement data → geometry conversion**
   ```python
   def data_to_threejs_geometry(data):
       # Convert pandas DataFrame to Three.js BufferGeometry
       positions = np.array(data[['x', 'y', 'z']]).flatten()
       geometry = p3js.BufferGeometry(
           attributes={'position': p3js.BufferAttribute(positions, 3)}
       )
       return geometry
   ```

3. **Basic plot types**
   - Scatter plots (THREE.Points)
   - Line plots (THREE.Line)
   - Both 2D and 3D variants

4. **Interactive controls**
   - OrbitControls for 3D
   - Pan/zoom for 2D (disabled rotation)

**Deliverable**: `hyp.plot(data)` works for basic 2D/3D static plots

#### **Week 2: 2D Plot Excellence + Matplotlib Conversion**

**Goals:**
- ✅ Publication-quality 2D plots
- ✅ All major 2D plot types  
- ✅ Proper 2D camera setup
- ✅ Text rendering (axes, labels, legends)
- ✅ **Matplotlib conversion system**

**Tasks:**
1. **Orthographic 2D camera system**
   ```python
   class TwoD_Camera_Manager:
       def setup_2d_camera(self, data_bounds):
           # Calculate optimal orthographic bounds
           # Set up camera for perfect 2D viewing
           # Disable inappropriate 3D controls
   ```

2. **2D-specific plot types**
   - Filled polygons (areas under curves)
   - Error bars
   - Histograms/bar plots
   - Heatmaps (via custom shaders)

3. **Text rendering system**
   ```python
   # Use CSS2DRenderer for crisp text
   label_renderer = p3js.CSS2DRenderer()
   # Overlay HTML text on Three.js scene
   ```

4. **Axis and legend system**
   - Automatic axis generation
   - Tick marks and labels
   - Color legends
   - Grid lines

5. **🆕 Matplotlib conversion engine**
   ```python
   class ThreeJSToMatplotlib:
       def convert_figure(self, hypertools_fig):
           # Extract data and parameters from Three.js scene
           # Recreate equivalent matplotlib figure
           # Preserve styling, colors, labels
           return matplotlib_figure
   ```

**Deliverable**: Beautiful 2D plots + matplotlib conversion capability

### **Phase 2: Animation System (Week 3-4)**

#### **Week 3: Animation Framework**

**Goals:**
- ✅ Smooth interpolated animations
- ✅ Multiple animation styles (window, precog, etc.)
- ✅ Animation controls (play/pause/scrub)
- ✅ 60fps performance

**Tasks:**
1. **Interpolation engine**
   ```python
   class ThreeJSAnimator:
       def create_interpolated_trajectory(self, data, n_frames=300):
           # Use scipy.interpolate for smooth trajectories
           # Generate Three.js keyframes
           # Return AnimationMixer setup
   ```

2. **Animation styles**
   - Window (sliding window)
   - Precog (window + future trail)
   - Growth (accumulating plot)
   - Camera rotation

3. **Three.js animation integration**
   ```python
   # Use Three.js AnimationMixer
   mixer = p3js.AnimationMixer()
   action = mixer.clipAction(animation_clip)
   action.play()
   ```

4. **Interactive controls**
   - Play/pause buttons (ipywidgets)
   - Frame scrubbing slider
   - Speed control
   - Loop options

**Deliverable**: Smooth animations with interactive controls

#### **Week 4: Animation Polish**

**Goals:**
- ✅ Fix any performance issues
- ✅ Advanced animation features
- ✅ Seamless 2D/3D animation switching
- ✅ Export animated plots

**Tasks:**
1. **Performance optimization**
   - Buffer geometry reuse
   - LOD (Level of Detail) for large datasets
   - GPU-based interpolation where possible

2. **Advanced features**
   - Multiple simultaneous animations
   - Custom easing functions
   - Synchronized multi-plot animations

3. **Export capabilities**
   - Frame-by-frame PNG export
   - MP4/GIF generation
   - Interactive HTML export

**Deliverable**: Production-ready animation system

### **Phase 3: Vector Export & Quality (Week 5-6)**

#### **Week 5: SVG Export System**

**Goals:**
- ✅ True vector 3D export via SVGRenderer
- ✅ High-quality 2D vector export
- ✅ Publication-ready output
- ✅ Multiple export formats

**Tasks:**
1. **SVGRenderer integration**
   ```python
   def export_as_vector(scene, camera, width=800, height=600):
       svg_renderer = p3js.SVGRenderer()
       svg_renderer.setSize(width, height)
       svg_renderer.render(scene, camera)
       return svg_renderer.domElement.outerHTML
   ```

2. **Vector optimization**
   - Optimize SVG output size
   - Clean up redundant elements
   - Ensure crisp lines and text

3. **Multi-format export**
   - SVG (vector)
   - PDF (via SVG conversion)
   - PNG (high-resolution raster)
   - EPS (PostScript)

4. **Quality assurance**
   - Typography quality
   - Line rendering precision
   - Color accuracy

**Deliverable**: Publication-quality vector export

#### **Week 6: Advanced Features**

**Goals:**
- ✅ Advanced rendering features
- ✅ Custom shaders for special effects
- ✅ Performance optimization
- ✅ Platform compatibility testing

**Tasks:**
1. **Advanced rendering**
   - Custom materials and shaders
   - Lighting models for 3D
   - Anti-aliasing optimization
   - Shadow rendering (optional)

2. **Large dataset handling**
   - Instanced rendering for performance
   - LOD systems
   - Streaming data support

3. **Platform testing**
   - Comprehensive testing on all Jupyter platforms
   - Performance benchmarking
   - Memory usage optimization

**Deliverable**: Robust, high-performance system

### **Phase 4: API Integration & Polish (Week 7-8)**

#### **Week 7: HyperTools API Integration + Figure Persistence**

**Goals:**
- ✅ Seamless integration with existing HyperTools API
- ✅ Backward compatibility
- ✅ Figure saving/loading system
- ✅ Documentation

**Tasks:**
1. **API integration**
   ```python
   # Replace existing plot() function - always returns HyperToolsFigure
   def plot(data, **kwargs):
       # All existing parameters work
       # Always Three.js backend
       return HyperToolsFigure(data, **kwargs)
   ```

2. **Feature parity**
   - All existing plot types
   - All existing parameters
   - Dimensionality reduction integration
   - Clustering visualization

3. **🆕 Figure persistence system**
   ```python
   # Save/load HyperTools figures
   fig = hyp.plot(data)
   fig.save('myplot.hyp')           # Serialize figure object
   loaded_fig = hyp.load('myplot.hyp')  # Reload later
   mpl_fig = loaded_fig.to_matplotlib()  # Convert to matplotlib
   ```

4. **Documentation**
   - API documentation
   - Example notebooks
   - Migration guide

**Deliverable**: Fully integrated system with persistence

#### **Week 8: Testing & Optimization**

**Goals:**
- ✅ Comprehensive testing
- ✅ Performance optimization
- ✅ Bug fixes
- ✅ Release preparation

**Tasks:**
1. **Testing suite**
   - Unit tests for all components
   - Integration tests
   - Platform-specific tests
   - Performance benchmarks

2. **Optimization**
   - Memory usage optimization
   - Rendering performance
   - Loading time optimization
   - Bundle size reduction

3. **Edge case handling**
   - Large datasets
   - Unusual data formats
   - Error handling and recovery

4. **Release preparation**
   - Version management
   - Packaging
   - Distribution setup

**Deliverable**: Production-ready release

---

## 🎯 **Success Metrics**

### **Technical Goals:**
- ✅ **Performance**: 60fps animations for datasets up to 10k points
- ✅ **Quality**: Vector export indistinguishable from matplotlib
- ✅ **Compatibility**: Works on all major Jupyter platforms
- ✅ **Usability**: No backend selection required

### **User Experience Goals:**
- ✅ **Simplicity**: Same API as current HyperTools
- ✅ **Power**: New capabilities (interactive, vector 3D)
- ✅ **Reliability**: No crashes, consistent behavior
- ✅ **Speed**: Faster than current implementation

---

## 📦 **Dependencies & Requirements**

### **Core Dependencies:**
```python
# Required packages
pythreejs>=2.4.0      # Three.js integration
ipywidgets>=8.0       # Interactive controls  
numpy>=1.20           # Data processing
scipy>=1.7            # Interpolation
pandas>=1.3           # Data handling

# Optional for advanced features
PIL>=8.0              # Image processing
matplotlib>=3.5       # Fallback text rendering
```

### **Platform Requirements:**
- **Jupyter**: Any version with widget support
- **Python**: 3.8+
- **Browser**: Modern browser with WebGL support
- **Memory**: 2GB+ for large datasets

---

## 🚀 **Expected Outcomes**

### **After 8 Weeks:**
- ✅ **Unified backend**: Single Three.js engine for everything
- ✅ **Publication quality**: Vector 2D and 3D export
- ✅ **Smooth animations**: 60fps interpolated motion
- ✅ **Universal compatibility**: Works everywhere
- ✅ **Enhanced capabilities**: Features impossible with matplotlib/plotly

### **Long-term Vision:**
- **Industry leadership**: Best vector 3D visualization in Python
- **Community adoption**: New standard for scientific visualization
- **Research impact**: Enable new types of data exploration
- **Commercial potential**: Professional-grade tool for data science

---

## 🎨 **Example Usage (Target API)**

```python
import hypertools as hyp

# Everything just works with Three.js backend
hyp.plot(data_2d)                    # Beautiful 2D plot
hyp.plot(data_3d)                    # Interactive 3D plot  
hyp.plot(data, animate='window')     # Smooth animation
hyp.plot(data, save='figure.svg')    # Vector export

# New capabilities enabled by Three.js
hyp.plot(data, interactive=True)     # Real-time updates
hyp.plot([data1, data2], sync=True)  # Synchronized plots
hyp.plot(data, lighting='auto')      # 3D lighting effects

# Advanced features
fig = hyp.plot(data_3d, return_widget=True)
fig.add_animation_controls()          # Interactive controls
fig.link_to_data(live_data_stream)    # Real-time updates
fig.export_video('animation.mp4')    # Video export

# 🆕 MATPLOTLIB CONVERSION & PERSISTENCE (Critical Feature)
fig = hyp.plot(data_2d)               # Always returns HyperToolsFigure object
fig.show()                            # Display interactive Three.js plot
mpl_fig = fig.to_matplotlib()         # Convert to matplotlib for fine-tuning

# Persistence & reloading
fig.save('myplot.hyp')                # Save HyperTools figure object
fig = hyp.load('myplot.hyp')          # Reload for later use
mpl_fig = fig.to_matplotlib()         # Convert loaded figure to matplotlib

# Export options
fig.export('plot.svg')                # Vector export via Three.js
fig.export('plot.png', dpi=300)       # High-res raster
fig.export('plot.html')               # Interactive HTML
```

---

## 💡 **Risk Mitigation**

### **Technical Risks:**
1. **Performance issues**: Mitigation via LOD, instancing, optimization
2. **Platform incompatibility**: Extensive testing, fallback options
3. **Three.js complexity**: Incremental implementation, proven patterns

### **Project Risks:**
1. **Scope creep**: Fixed 8-week timeline, clear milestones
2. **Integration challenges**: Early API design, continuous testing
3. **Quality concerns**: Vector export testing, visual regression tests

### **Contingency Plans:**
- **Week 4 checkpoint**: Reassess if major issues arise
- **Fallback options**: Keep matplotlib backend during transition
- **Community feedback**: Early beta testing with power users

---

## 🏁 **Ready to Begin**

This plan provides:
- ✅ **Clear roadmap**: 8-week implementation timeline  
- ✅ **Technical feasibility**: Proven Three.js capabilities
- ✅ **Strategic vision**: Unified backend, enhanced capabilities
- ✅ **Risk management**: Mitigation strategies and contingencies

**Next step**: Begin Phase 1 - Foundation implementation with basic Three.js integration and 2D/3D plot capabilities.

**Expected outcome**: HyperTools becomes the premier Python library for interactive, publication-quality 2D and 3D visualization with smooth animations and true vector export capabilities.