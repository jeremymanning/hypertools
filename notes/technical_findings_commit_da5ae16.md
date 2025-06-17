# Technical Findings & Code Analysis - Commit da5ae16

**Session Date:** 2025-06-17  
**Branch:** `matplotlib-backend-revert`  
**Commit Hash:** `da5ae16` (Document matplotlib backend testing results and next steps)  
**Previous Implementation:** `ccb1d63` (Implement matplotlib backend for hypertools plotting)

## 🧪 **Tested Code Snippets & Results**

### **✅ WORKING: 2D/3D Scatter Plots**

**Location:** `hypertools/plot/matplotlib_plotting.py:45-78`

```python
class HyperToolsPlot:
    def __init__(self, data, ndims=3, **kwargs):
        self.fig = plt.figure(figsize=(10, 8))
        if ndims == 3:
            self.ax = self.fig.add_subplot(111, projection='3d')
        else:
            self.ax = self.fig.add_subplot(111)
        
    def scatter(self, x, y, z=None, **kwargs):
        if z is not None:
            return self.ax.scatter(x, y, z, **kwargs)
        else:
            return self.ax.scatter(x, y, **kwargs)
```

**Test Result:** ✅ Both 2D and 3D scatter plots render correctly with proper axis detection.

### **✅ WORKING: Automatic Color Assignment**

**Location:** `hypertools/plot/matplotlib_plotting.py:156-170`

```python
def plot_matplotlib(data, mode='scatter', colors=None, **kwargs):
    if colors is None:
        n_datasets = len(data) if isinstance(data, list) else 1
        colors = plt.cm.tab10(np.linspace(0, 1, n_datasets))
    
    for i, dataset in enumerate(data):
        color = colors[i] if isinstance(colors, (list, np.ndarray)) else colors
        # Plot with assigned color
```

**Test Result:** ✅ Automatic color cycling works correctly for multiple datasets.

### **❌ BROKEN: Format String Parsing**

**Location:** `hypertools/plot/matplotlib_plotting.py:108-145`

```python
def parse_format_string(fmt):
    """Parse matplotlib-style format strings like 'ro-', 'b--', 'g^:'"""
    color_map = {'r': 'red', 'g': 'green', 'b': 'blue', 'c': 'cyan', 
                 'm': 'magenta', 'y': 'yellow', 'k': 'black', 'w': 'white'}
    marker_map = {'.': '.', 'o': 'o', '^': '^', 'v': 'v', 's': 's', '*': '*'}
    # LINE STYLE PARSING IS INCOMPLETE HERE
    linestyle_map = {'-': '-', '--': '--', ':': ':', '-.': '-.'}
```

**Issue:** Line style components (`--`, `:`, `-.`) are not being correctly extracted from format strings.

**Error Example:** Format string `'ro--'` should produce red circles with dashed lines, but only parses color and marker.

### **❌ CRASHED: Line Plot (Trajectory Visualization)**

**Location:** `hypertools/plot/matplotlib_plotting.py:80-95`

```python
def plot_line(self, x, y, z=None, **kwargs):
    if z is not None:
        return self.ax.plot(x, y, z, **kwargs)
    else:
        return self.ax.plot(x, y, **kwargs)
```

**Error:** Crashes during trajectory visualization, likely due to data format assumptions or missing error handling.

**Stack Trace Context:** Jupyter notebook cell execution failed when processing time-series line data.

### **✅ WORKING: Lines + Markers Mode**

**Location:** `hypertools/plot/matplotlib_plotting.py:201-215`

```python
if mode == 'lines+markers':
    line_artists = plotter.plot_line(x, y, z, color=color, linewidth=linewidth)
    scatter_artists = plotter.scatter(x, y, z, color=color, s=markersize**2)
```

**Test Result:** ✅ Combined line and marker rendering works correctly.

## 🎨 **Visual Fidelity Analysis**

### **Current vs. Original Hypertools Aesthetic**

**Critical Gap Identified:** Current matplotlib backend produces standard matplotlib plots, NOT the distinctive hypertools visual style.

**Original Repository Reference:** https://github.com/ContextLab/hypertools

**Missing Visual Elements (Hypothesis):**
1. **Color Palettes:** Likely custom seaborn-based color schemes
2. **3D Styling:** Specific camera angles, lighting, axis styling
3. **Plot Aesthetics:** Font choices, grid styling, background colors
4. **Animation Effects:** Smooth transitions and trajectory rendering

## 🏗️ **Architecture Comparison**

### **Current Implementation (Commit ccb1d63)**

```python
# hypertools/plot/plot.py - Main entry point
def plot(data, **kwargs):
    return plot_matplotlib(data, **kwargs)

# hypertools/plot/matplotlib_plotting.py - Backend implementation
def plot_matplotlib(data, mode='scatter', **kwargs):
    plotter = HyperToolsPlot(data, **kwargs)
    # Plotting logic here
```

**Advantages:**
- Clean separation of concerns
- Backend-agnostic API design
- Maintainable modular structure

**Current Limitations:**
- Basic matplotlib defaults
- Missing hypertools-specific styling
- Incomplete feature parity

### **Original Hypertools (Need to Analyze)**

**Research Required:**
- How does original plotting system work?
- Where is visual styling configured?
- What makes the plots distinctive?

## 🐛 **Specific Bug Fixes Needed**

### **1. Format String Parser Fix**

**Location:** `hypertools/plot/matplotlib_plotting.py:108-145`

**Problem:** Regex pattern doesn't correctly handle compound format strings.

**Current Code:**
```python
# Incomplete implementation
def parse_format_string(fmt):
    # Missing proper regex for line styles
    pass
```

**Required Solution Pattern:**
```python
def parse_format_string(fmt):
    # Need regex like: r'([rgbcmykw]?)([.o^vs*]?)([-:]{1,2}|-.)?'
    # To parse color + marker + linestyle in any order
```

### **2. Line Plot Crash Fix**

**Location:** `hypertools/plot/matplotlib_plotting.py:80-95`

**Problem:** Data format assumptions causing crashes.

**Required Analysis:**
- What data format does hypertools expect for trajectories?
- How should time-series data be handled?
- What error handling is needed?

## 📊 **Implementation Strategy Forward**

### **Phase 1: Original Codebase Analysis** ⚠️ DECISION POINTS

1. **Clone original hypertools repository**
2. **Study plotting system architecture** 
   - ⚠️ **Decision Point:** How much of original architecture to preserve?
3. **Document visual styling system**
   - ⚠️ **Decision Point:** Which styling elements are priority?
4. **Extract default configurations**
   - ⚠️ **Decision Point:** How to integrate with new config system?

### **Phase 2: Bug Fixes** ⚠️ DECISION POINTS

1. **Fix format string parsing**
   - ⚠️ **Decision Point:** Should parsing follow matplotlib exactly or hypertools conventions?
2. **Resolve line plot crashes**
   - ⚠️ **Decision Point:** How should trajectory data be handled differently from scatter?
3. **Implement missing features**
   - ⚠️ **Decision Point:** Feature priority order and compatibility requirements?

### **Phase 3: Visual Fidelity** ⚠️ DECISION POINTS

1. **Extract original styling system**
   - ⚠️ **Decision Point:** How to preserve new architecture while matching old aesthetics?
2. **Implement hypertools-specific defaults**
   - ⚠️ **Decision Point:** Which visual elements are negotiable vs. fixed?
3. **Validate visual output parity**
   - ⚠️ **Decision Point:** Acceptable tolerance for visual differences?

## 🔍 **Commit References**

- **`ccb1d63`** - Core matplotlib backend implementation (working foundation)
- **`da5ae16`** - Testing analysis and findings documentation (this session)
- **`c875f71`** - Previous session documentation
- **`d4822e9`** - Backup of all debugging scripts (reference point)

## 🚨 **Critical Next Steps**

1. **STOP before implementing** - All ambiguous decisions require user consultation
2. **Research original hypertools** - Visual and architectural analysis required
3. **Fix immediate bugs** - Format parsing and line plot crashes
4. **Establish visual baselines** - Compare output side-by-side with original

---

**Technical Status:** 🔧 PARTIAL FUNCTIONALITY  
**Visual Status:** ❌ AESTHETIC MISMATCH  
**Next Priority:** 🔍 ORIGINAL CODEBASE ANALYSIS  
**Implementation Protocol:** ⚠️ CONSULT ON ALL AMBIGUITIES