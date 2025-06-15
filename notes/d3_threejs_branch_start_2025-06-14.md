# D3.js + Three.js Backend Implementation - Branch Start

## Branch Information
- **Branch**: `d3-threejs-backend`
- **Started**: June 14, 2025
- **Parent Branch**: `threejs-backend` (commit 63af56a)
- **Implementation Plan**: See `d3_threejs_implementation_plan_2025-06-14.md`

## Current Status
Starting fresh implementation of unified D3.js + Three.js backend:

### Completed Research Phase
- ✅ Identified pythreejs rendering issues (mesh faces appear as wireframes)
- ✅ Evaluated alternative backends (VisPy, PyVista, K3D, Plotly)
- ✅ Decided on D3.js (2D) + Three.js (3D) approach
- ✅ Created comprehensive implementation plan
- ✅ Documented all research findings

### Implementation Strategy
- **2D Plots**: D3.js (SVG/Canvas) - consistent renderer for all 2D
- **3D Plots**: Three.js (WebGL) - consistent renderer for all 3D  
- **No Backend Switching**: Simple, predictable behavior
- **Universal Export**: All plots exportable to PDF, GIF/MP4, matplotlib

### Next Steps (Phase 1)
1. Create `hypertools/core/d3_backend.py`
2. Implement HTML template generation system
3. Basic D3.js integration via HTML injection
4. Simple scatter plot rendering

### Key Design Decisions
- **Simplicity First**: Start simple, optimize later
- **Direct Integration**: Bypass widget libraries, call D3/Three.js directly
- **Consistent API**: Maintain existing hypertools.plot() interface
- **HyperToolsFigure**: Unified class for all export capabilities

## Development Environment
- Working directory: `/Users/jmanning/hypertools`
- Python environment: Default system environment
- Dependencies: Will need to add D3.js, Three.js assets

## Files to Create
```
hypertools/core/
├── d3_backend.py        # D3.js integration & HTML generation
├── threejs_backend.py   # Three.js integration & HTML generation (replace current)
├── figure.py            # HyperToolsFigure class
├── export.py            # PDF/GIF/MP4 export utilities
└── matplotlib_converter.py  # Convert to matplotlib figures

hypertools/assets/
├── d3.min.js           # D3.js library
├── three.min.js        # Three.js library
└── templates/
    ├── d3_plot.html    # D3.js plot template
    └── threejs_plot.html # Three.js plot template
```

## Success Criteria for Phase 1 (Weeks 1-4)
- [ ] Basic D3.js scatter plots rendering in Jupyter
- [ ] Line plots with matplotlib-style format strings
- [ ] SVG export functionality
- [ ] Animation system with D3.js transitions
- [ ] Clean, maintainable code architecture

Ready to begin implementation! 🚀