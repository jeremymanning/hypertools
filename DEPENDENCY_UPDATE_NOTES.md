# HyperTools Dependency Update Progress

**Date**: 2025-01-13  
**Status**: Planning completed, ready to start with datawrangler updates

## Analysis Completed

### Current Dependency Issues Identified
1. **datawrangler**: Core dependency used in 28 files across all modules - needs NumPy 2+ and Pandas 2+ compatibility
2. **BrainIAK**: SRM algorithms copied to `external/brainiak.py` (self-contained), but may still be listed in dependencies - should be removed
3. **Test figures**: 77 reference `.fig` files in `tests/reference_figures/` that will need regeneration after updates
4. **Version constraints**: Many packages lack proper version pinning

### datawrangler Usage Analysis
- **Files using datawrangler**: 28 files found via grep
- **Import pattern**: `import datawrangler as dw`
- **Key usage**: Data format conversion, DataFrame operations, decorators like `@dw.decorate.apply_stacked`
- **Core to architecture**: Central to HyperTools' data flow pipeline

### BrainIAK Status
- **External copy**: Complete SRM implementation in `hypertools/external/brainiak.py`
- **Import locations**: Referenced in `model.py` and `srm.py`
- **Self-contained**: No external BrainIAK installation needed
- **Action needed**: Remove from any dependency lists

### Test Suite Challenge  
- **Reference figures**: 77 `.fig` files used for plot regression testing
- **Issue**: Dependency updates will likely change plot outputs
- **Strategy needed**: Regenerate and manually validate new reference figures

## Planned Update Strategy

### Phase 1: Update datawrangler (NEXT STEP)
- **Priority**: Update datawrangler first in separate session
- **Goal**: Ensure NumPy 2+ and Pandas 2+ compatibility
- **Impact**: Core to HyperTools functionality

### Phase 2: Resume HyperTools Updates
- **Dependency audit**: Remove BrainIAK from dependency lists
- **Incremental updates**: One major dependency at a time
- **Test strategy**: Skip figure tests initially (`pytest -k "not fig"`)

### Phase 3: Figure Regeneration
- **Create regeneration script**: Automate example running and figure saving
- **Manual validation**: Review new figures for correctness
- **Staged approach**: Handle figures in small batches

## Key Files and Locations

### Dependencies
- `requirements.txt` - main dependencies
- `requirements_dev.txt` - development dependencies  
- `setup.py` - package installation requirements
- `dev.yaml` - conda environment file

### Core Architecture
- `hypertools/core/model.py` - model loading system (references brainiak)
- `hypertools/external/brainiak.py` - self-contained SRM implementation
- `hypertools/external/__init__.py` - external module imports

### Testing
- `tests/reference_figures/` - 77 reference plot files
- Figure comparison tests throughout test suite

## Current Status
- Analysis: ✅ Complete
- Planning: ✅ Complete  
- datawrangler update: ⏳ Ready to start (separate session)
- HyperTools updates: ⏳ Waiting for datawrangler completion

## Notes for Next Session
- Start with datawrangler repository
- Focus on NumPy 2+ and Pandas 2+ compatibility
- Test with HyperTools integration after datawrangler fixes
- Return to this repository once datawrangler is stable