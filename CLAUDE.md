# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Testing
- Run tests: `pytest` (requires `pip install pytest`)
- Tests are located in `tests/hyp/` with comprehensive coverage
- Reference figures stored as binary `.fig` files for plot regression testing

### Installation
- Development install: `pip install -e .`
- Install requirements: `pip install -r requirements.txt`
- Conda environment available via `dev.yaml`

### Documentation
- Docs built with Sphinx, located in `docs/`
- Examples auto-generated from `examples/` directory
- API docs auto-generated from docstrings

## Architecture Overview

HyperTools is a high-dimensional data visualization library with 7 main modules:

### Core Modules
- **`align/`**: Data alignment algorithms (HyperAlign, Procrustes, SRM)
- **`cluster/`**: Clustering wrapper around scikit-learn
- **`core/`**: Configuration system (config.ini), model abstraction, utilities
- **`io/`**: Data loading/saving (Google Drive, URLs, built-in datasets)
- **`manip/`**: Data preprocessing (normalize, zscore, resample, smooth)
- **`plot/`**: Visualization system (static/animated, Plotly/matplotlib backends)
- **`reduce/`**: Dimensionality reduction wrapper for scikit-learn methods

### Configuration System
- Central configuration in `hypertools/core/config.ini`
- Module-specific parameter sections (e.g., `[plot]`, `[UMAP]`, `[cluster]`)
- Runtime override via function kwargs
- `RobustDict` provides graceful fallback for missing config

### Plotting Architecture
- **Primary backend**: Plotly for interactive 3D plots and animations
- **Secondary backend**: matplotlib with sophisticated backend management
- Auto-detects environment (Jupyter vs command line) for renderer selection
- Static plots: 2D/3D scatter, line plots with customizable styling
- Animated plots: rotating cameras, sliding time windows, trajectory animations

### Data Flow Pattern
```
Raw Data → Format (via datawrangler) → [Align] → [Reduce] → [Cluster] → Plot
```

### Key Abstractions
- Built on pandas DataFrames with MultiIndex for grouped data
- `@dw.decorate.apply_stacked` decorator for automatic data format handling
- Unified `apply_model` function for all ML algorithms
- Color management via seaborn palettes with automatic group-based coloring

### Dependencies
- **Core**: numpy, pandas, scipy, scikit-learn
- **Visualization**: plotly, matplotlib, seaborn  
- **Specialized**: umap-learn, datawrangler (custom data handling library)
- **External**: BrainIAK integration for neuroimaging algorithms

## Code Patterns

### Adding New Algorithms
- Extend the appropriate module (`reduce/`, `align/`, etc.)
- Add default parameters to `core/config.ini`
- Use `apply_model` for scikit-learn compatibility
- Add comprehensive tests with reference figures

### Plotting Customization
- Leverage existing color management system
- Use `get_cmap()` for consistent color palette handling
- Support both matplotlib and Plotly backends
- Consider animation support for time-series data

### Data Handling
- Expect pandas DataFrames as primary data structure
- Use datawrangler decorators for format conversion
- Support grouped data via MultiIndex structure
- Handle missing data gracefully in preprocessing