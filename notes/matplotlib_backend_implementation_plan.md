# Matplotlib Backend Implementation Plan

## Overview
Revert hypertools to use matplotlib as the primary plotting backend while maintaining the improved code organization from recent development. This plan addresses performance issues with Plotly animations and rendering accuracy issues with D3.js/Three.js approaches.

## Phase 1: Code Analysis and Preparation

### 1.1 Analyze Current Plotting Architecture
- Review `hypertools/plot/` module structure
- Identify all Plotly-specific code paths
- Document matplotlib equivalents for each plot type
- Compare with original ContextLab/hypertools implementation

### 1.2 Dependencies Audit
- Remove plotly, pythreejs, and any D3.js/Three.js wrappers
- Ensure matplotlib, seaborn are properly configured
- Check for any backend-specific utility functions

## Phase 2: Core Plotting Implementation

### 2.1 Static Plots
- **2D Scatter/Line plots**: Use `matplotlib.pyplot.scatter()` and `plot()`
- **3D Scatter/Line plots**: Use `mpl_toolkits.mplot3d.Axes3D`
- **Trajectory plots**: Implement with line collections
- **Group-based coloring**: Leverage seaborn color palettes

### 2.2 Animation Framework
- Use `matplotlib.animation.FuncAnimation` for all animations
- Implement three animation types:
  - **Rotating camera**: Animate view angles in 3D plots
  - **Sliding window**: Show data progression over time
  - **Trajectory animation**: Reveal paths progressively
- Consider blitting for performance optimization

### 2.3 Backend Management
- Properly detect and set matplotlib backend based on environment
- Handle Jupyter notebook inline display vs interactive windows
- Implement proper figure cleanup to prevent memory leaks

## Phase 3: Visual Inspection Infrastructure

### 3.1 Test Gallery System
- Create `tests/visual_inspection/` directory
- Generate one example of each plot type:
  - 2D/3D scatter plots (single and grouped)
  - 2D/3D line plots
  - All animation types
  - Edge cases (single points, overlapping data)

### 3.2 Comparison Framework
- Side-by-side comparison with reference implementation
- Save plots as high-resolution PNGs for inspection
- Generate HTML gallery for easy browsing
- Include plot generation parameters with each figure

### 3.3 Interactive Testing
- Jupyter notebook with all plot types
- Parameter sliders for testing different configurations
- Memory and timing profilers for each plot type

## Phase 4: Performance Optimization

### 4.1 Rendering Optimizations
- Use collections (LineCollection, PathCollection) for large datasets
- Implement data decimation for very large datasets
- Optimize marker/line rendering with rasterization where appropriate
- Cache color mappings and transformations

### 4.2 Animation Performance
- Implement blitting for animations
- Pre-compute animation frames where possible
- Optimize update functions to minimize redraws
- Use appropriate frame rates and intervals

### 4.3 Memory Management
- Proper figure and axis cleanup
- Implement context managers for plot generation
- Monitor memory usage during batch plotting
- Clear matplotlib's internal caches appropriately

## Phase 5: Feature Parity and Testing

### 5.1 Feature Checklist
- [ ] All plot types from original implementation
- [ ] All styling options (colors, markers, sizes, etc.)
- [ ] Animation export (GIF, MP4)
- [ ] Publication-quality figure export
- [ ] Interactive features (zoom, pan, rotate)

### 5.2 Regression Testing
- Update existing tests for matplotlib backend
- Ensure all reference figures match expected output
- Test edge cases and error handling
- Verify memory usage is reasonable

### 5.3 Documentation Updates
- Update plotting examples for matplotlib
- Document any API changes
- Add performance tuning guide
- Include troubleshooting section

## Implementation Order

1. **Week 1**: Static 2D plots and infrastructure
2. **Week 2**: Static 3D plots and visual inspection system
3. **Week 3**: Animation framework implementation
4. **Week 4**: Performance optimization and testing
5. **Week 5**: Documentation and final polish

## Success Criteria

- All plot types render accurately with matplotlib
- Animation performance is smooth for typical datasets (1000-10000 points)
- Memory usage is predictable and bounded
- Figures are publication-quality when exported
- Visual inspection confirms accuracy for all plot types
- Performance benchmarks show improvement over Plotly for animations

## Notes

- Reference original implementation at https://github.com/ContextLab/hypertools
- Maintain backward compatibility where possible
- Consider matplotlib 3.5+ features for better performance
- Keep architecture flexible for potential future backend additions