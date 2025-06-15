# Visualization Backend Research and Decision - June 14, 2025

## Current Problem
HyperTools Three.js backend has fundamental rendering issues in Jupyter environments:
- **Root Issue**: pythreejs widget face rendering is broken - all mesh faces render as wireframes/lines only
- **Symptom**: 2D scatter points appear collapsed to y=0 line, squares show as lines in camera plane tests
- **Data Processing**: Verified to be correct - issue is purely in rendering layer

## Requirements Analysis
Core requirements for HyperTools visualization:
1. **Performance**: Fast rendering for 2D/3D, static/animated plots
2. **Aesthetics**: Beautiful, publication-quality appearance
3. **Interactivity**: Zoom, rotate, animation controls  
4. **Jupyter Support**: Flawless operation across all Jupyter environments
5. **Export**: Vector graphics (PDF) + animations (GIF/MP4)
6. **Matplotlib Compatibility**: Convert to matplotlib with matched appearance
7. **Styling**: Line styles, markers, labels, legends
8. **Simplicity**: Consistent renderers, avoid complex backend switching

## Research Findings

### pythreejs (Current - REJECTED)
- **Issue**: Fundamental mesh rendering problems in Jupyter widgets
- **Evidence**: Camera plane test showed all squares as lines, not filled faces
- **Verdict**: Technical blocker, uncertain if fixable

### Plotly (REJECTED)
- **Issue**: Poor animation performance, slow rendering
- **Previous Experience**: User reported animations were very slow and difficult to render correctly
- **Verdict**: Performance requirements not met

### VisPy
- **Pros**: Extremely high performance (GPU OpenGL), millions of points, real-time animation
- **Cons**: Limited vector export, jupyter_rfb dependency, smaller ecosystem
- **Assessment**: Excellent performance but complex integration

### PyVista + Trame
- **Pros**: Excellent 3D via VTK, multiple Jupyter backends, matplotlib embedding
- **Cons**: VTK learning curve, SVG export may be rasterized for 3D
- **Assessment**: Strong 3D option but complex for 2D use cases

### K3D-jupyter
- **Pros**: High-performance WebGL 3D, great Jupyter integration
- **Cons**: 3D-focused, limited 2D capabilities, no clear vector export
- **Assessment**: Specialized for 3D only

### D3.js + Three.js (SELECTED)
- **D3.js Performance**: 1K points (SVG), 10K points (Canvas), 1M+ points (WebGL)
- **Three.js 3D**: Industry standard, WebGL acceleration, proven Jupyter integration patterns
- **Vector Export**: Perfect SVG export for D3.js 2D plots
- **Ecosystem**: Mature, stable, huge community
- **Jupyter Integration**: Multiple proven approaches (iPyWidgets, HTML injection)

## Decision Rationale

### Why D3.js for 2D:
1. **User Preference**: "I like the look of d3 plots a lot, and their performance is excellent"
2. **Perfect Vector Export**: D3.js SVG output provides true vector graphics
3. **Proven Performance**: Handles typical scientific datasets well
4. **Aesthetic Quality**: Beautiful, customizable styling
5. **Mature Ecosystem**: Stable, well-documented, large community

### Why Three.js for 3D:
1. **Direct Integration**: Bypass pythreejs widget issues by calling Three.js directly
2. **Performance**: WebGL acceleration for smooth 3D interactions
3. **Industry Standard**: Proven solution for web-based 3D graphics
4. **Jupyter Compatible**: Can be integrated via custom widgets or HTML

### Why Unified Renderers:
1. **Simplicity**: "It's ok if we need to sacrifice some quality to make implementation simpler"
2. **Consistency**: Same renderer for all 2D plots, potentially separate for 3D
3. **Maintainability**: Easier to debug and optimize single rendering paths
4. **User Experience**: Predictable behavior across all plot types

## Alternative Approaches Considered
- **Multi-backend switching**: Rejected for complexity
- **PyVista hybrid**: Rejected - too complex for 2D use cases
- **VisPy**: Rejected - vector export limitations
- **Custom moderngl**: Rejected - massive development effort

## Technical Risk Assessment
- **Development Effort**: High (custom JavaScript integration)
- **Technical Risk**: Medium (proven patterns exist)
- **Performance Risk**: Low (D3.js and Three.js are proven)
- **Maintenance Risk**: Low (stable, standard web technologies)

## Success Criteria
1. **Visual Quality**: D3.js plots should be beautiful and publication-ready
2. **Export Quality**: Perfect SVG vector graphics for 2D plots
3. **Performance**: Smooth animations and interactions
4. **Jupyter Compatibility**: Works across Classic Jupyter, JupyterLab, Colab
5. **API Compatibility**: Drop-in replacement for current HyperTools interface