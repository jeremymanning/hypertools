# D3.js + Three.js Implementation Plan - June 14, 2025

## Architecture Overview

### Unified Renderer Approach
- **2D Plots**: D3.js (SVG/Canvas) for ALL 2D visualizations
- **3D Plots**: Three.js (WebGL) for ALL 3D visualizations  
- **No Backend Switching**: Consistent renderer per dimensionality
- **Export Unity**: All plots wrapped in HyperToolsFigure class

### Core Design Principles
1. **Simplicity Over Optimization**: Start simple, optimize later
2. **Consistent Renderers**: Same technology for same dimensionality
3. **Direct Integration**: Bypass widget libraries, call D3/Three.js directly
4. **Universal Export**: Every figure exportable to PDF, GIF/MP4, matplotlib

## HyperToolsFigure Class Design

### Core Interface
```python
class HyperToolsFigure:
    def __init__(self, data, fmt=None, **kwargs):
        """Initialize with data and styling"""
        
    def show(self) -> DisplayObject:
        """Display in Jupyter (HTML widget)"""
        
    def to_pdf(self, filename: str):
        """Export static plot to PDF"""
        
    def to_gif(self, filename: str):
        """Export animation to GIF"""
        
    def to_mp4(self, filename: str):
        """Export animation to MP4"""
        
    def to_matplotlib(self) -> matplotlib.Figure:
        """Convert to matplotlib figure (2D or 3D)"""
        
    def to_matplotlib_animation(self) -> matplotlib.animation.Animation:
        """Convert to matplotlib animation"""
        
    def save(self, filename: str):
        """Save figure object (.hyp file)"""
```

### Export Implementation Strategy
```python
# PDF Export (Static)
2D: D3.js SVG → PDF (vector graphics)
3D: Three.js → High-res PNG → PDF (embedded raster)

# Animation Export  
2D: D3.js animation frames → ImageIO → GIF/MP4
3D: Three.js animation frames → ImageIO → GIF/MP4

# Matplotlib Conversion
2D: Recreate plot using matplotlib with same data/styling
3D: Use matplotlib's Axes3D with same data/styling
```

## Implementation Architecture

### 1. JavaScript Integration Layer
```
JavaScript Layer (runs in browser):
├── d3_renderer.js       # D3.js 2D plotting engine
├── threejs_renderer.js  # Three.js 3D plotting engine  
├── export_utils.js      # SVG/Canvas export utilities
├── animation_utils.js   # Animation frame capture
└── jupyter_bridge.js    # Python ↔ JavaScript communication
```

### 2. Python Backend Layer
```python
# Core backend architecture
hypertools/core/
├── d3_backend.py        # D3.js integration & HTML generation
├── threejs_backend.py   # Three.js integration & HTML generation
├── figure.py            # HyperToolsFigure class
├── export.py            # PDF/GIF/MP4 export utilities
└── matplotlib_converter.py  # Convert to matplotlib figures
```

### 3. Jupyter Integration Strategy
**Phase 1: HTML Injection (Simple)**
- Generate HTML with embedded JavaScript
- Use IPython.display.HTML for direct injection
- No custom widgets required

**Phase 2: Custom iPyWidget (Advanced)**
- Migrate to custom iPyWidget for better integration
- Bidirectional Python ↔ JavaScript communication
- Better performance and user experience

## Technical Implementation Plan

### Phase 1: D3.js 2D Foundation (3-4 weeks)

#### Week 1: Core Infrastructure
- [ ] Create `hypertools/core/d3_backend.py`
- [ ] Implement HTML template generation system
- [ ] Basic D3.js integration via HTML injection
- [ ] Simple scatter plot rendering

#### Week 2: 2D Plot Types
- [ ] Scatter plots with markers
- [ ] Line plots with interpolation
- [ ] Format string parsing (matplotlib-style)
- [ ] Color system integration

#### Week 3: Interactivity & Animation
- [ ] Zoom/pan controls for 2D plots
- [ ] Animation system using D3.js transitions
- [ ] Timeline controls (play/pause/scrub)

#### Week 4: Export System
- [ ] SVG export for static plots
- [ ] Animation frame capture → GIF/MP4
- [ ] PDF generation from SVG

### Phase 2: Three.js 3D Integration (3-4 weeks)

#### Week 5: Three.js Setup
- [ ] Create `hypertools/core/threejs_backend.py`
- [ ] Basic Three.js scene setup
- [ ] 3D scatter plots with camera controls

#### Week 6: 3D Features
- [ ] 3D line plots and surfaces
- [ ] Lighting and material system
- [ ] Camera animation (rotation, zoom)

#### Week 7: 3D Export
- [ ] High-resolution PNG export
- [ ] 3D animation capture → GIF/MP4
- [ ] PDF export with embedded raster

#### Week 8: Polish
- [ ] Performance optimization
- [ ] Visual style consistency with D3.js
- [ ] Jupyter environment testing

### Phase 3: HyperToolsFigure Integration (2-3 weeks)

#### Week 9: Figure Class
- [ ] Implement `HyperToolsFigure` class
- [ ] Unified API for 2D/3D backends
- [ ] Export method implementation

#### Week 10: Matplotlib Converter
- [ ] `to_matplotlib()` for 2D plots
- [ ] `to_matplotlib()` for 3D plots  
- [ ] Animation converter implementation

#### Week 11: Testing & Polish
- [ ] Cross-environment testing (Classic, Lab, Colab)
- [ ] Performance benchmarking
- [ ] API compatibility with existing hypertools

### Phase 4: Advanced Features (2-3 weeks)

#### Week 12: Styling System
- [ ] Complete matplotlib format string support
- [ ] Advanced color mapping
- [ ] Legend and label system

#### Week 13: Performance Optimization
- [ ] Large dataset handling
- [ ] Animation performance tuning
- [ ] Memory management

#### Week 14: Production Ready
- [ ] Comprehensive testing
- [ ] Documentation
- [ ] Migration guide

## Technical Decisions

### D3.js Renderer Selection
```javascript
// Default to Canvas for better performance
if (dataPoints > 1000) {
    renderer = 'd3-canvas';  // Better performance
} else {
    renderer = 'd3-svg';     // Better export quality
}
```

### Three.js Configuration
```javascript
// Standard WebGL setup for all 3D plots
renderer = new THREE.WebGLRenderer({
    antialias: true,
    preserveDrawingBuffer: true,  // Required for export
    alpha: true
});
```

### Export Strategy Details
- **SVG → PDF**: Use reportlab or weasyprint for vector conversion
- **Canvas → PNG**: HTML5 Canvas.toBlob() for raster export
- **Animation**: Capture frames at 60fps, encode with imageio

## Risk Mitigation

### Technical Risks
1. **Jupyter Compatibility**: Test early across all environments
2. **Performance**: Benchmark with large datasets from day 1
3. **Export Quality**: Validate vector graphics fidelity early

### Development Risks  
1. **JavaScript Complexity**: Start with simple HTML injection
2. **Cross-browser Issues**: Focus on modern browsers initially
3. **Animation Performance**: Implement frame rate limiting

## Success Metrics
- **Visual Quality**: Publication-ready plots matching matplotlib aesthetics
- **Performance**: Smooth 60fps animations up to 10K points (2D), 1K points (3D)
- **Export Fidelity**: Perfect vector graphics for 2D, high-quality raster for 3D
- **Jupyter Compatibility**: 100% success across target environments
- **API Compatibility**: Drop-in replacement for existing hypertools.plot()

## Future Enhancements (Post-MVP)
- Custom iPyWidget development for better integration
- WebGL acceleration for D3.js (large 2D datasets)
- Advanced Three.js features (shadows, post-processing)
- Real-time data streaming for animations