# Remaining Todo Items for Matplotlib Backend

## High Priority Tasks (Next Session)

### 1. **Update animate.py to use matplotlib.animation** 
- **Status:** Pending
- **Priority:** High
- **Details:** Current animate.py still uses Plotly (plotly.graph_objects)
- **Implementation needed:**
  - Replace Plotly Frame objects with matplotlib FuncAnimation
  - Convert animation styles: window, chemtrails, precog, bullettime, grow, shrink, spin
  - Implement proper frame generation for matplotlib
  - Add animation export capabilities (GIF, MP4)

### 2. **Optimize matplotlib performance**
- **Status:** Pending  
- **Priority:** Medium
- **Details:** Current implementation works but could be optimized
- **Optimizations needed:**
  - Implement blitting for smooth animations
  - Use matplotlib collections for large datasets
  - Memory management and figure cleanup
  - Faster rendering for real-time updates

## Completed Items (This Session)

✅ Create new branch for matplotlib backend implementation  
✅ Take notes for detailed matplotlib implementation plan  
✅ Commit all helper/debugging scripts for backup  
✅ Clean up project notes and debugging scripts  
✅ Revise code to use matplotlib/seaborn exclusively  
✅ Implement visual inspection infrastructure  
✅ Create matplotlib_plotting.py module  
✅ Update static.py helper functions for matplotlib  
✅ Update plot.py to use matplotlib backend  
✅ Create visual test suite  

## Implementation Status

**Core Backend:** ✅ Complete and functional (5/5 tests passing)  
**Animation Support:** ❌ Not yet implemented  
**Performance:** ⚠️ Basic optimization complete, advanced optimization pending  

## Files Ready for Animation Implementation

- `hypertools/plot/animate.py` - Needs complete matplotlib.animation conversion
- `hypertools/plot/matplotlib_plotting.py` - Animation functions can be added here
- Test notebook ready for animation testing once implemented