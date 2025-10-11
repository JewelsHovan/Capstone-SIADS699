# Repository Refactoring Plan

## Current State Analysis

**Total files in root: 27**
- Python scripts: 8
- JSON data: 2
- CSV data: 2
- HTML maps: 2
- Documentation: 6
- Images: 4
- Plus wzdx/ subdirectory (spec repo)

**Issues:**
- ❌ Everything in root directory (messy)
- ❌ Duplicate documentation files
- ❌ Mixed concerns (code, data, docs, outputs)
- ❌ Hard to navigate for team members
- ❌ No clear separation of modules vs scripts

---

## Proposed New Structure

```
Capstone/
├── README.md                          # Main project readme
├── .gitignore                         # Git ignore file
│
├── src/                               # Source code modules
│   ├── __init__.py
│   ├── wzdx_analyzer.py              # Core analysis module
│   ├── wzdx_mapping.py               # Mapping module
│   └── utils/                         # Utility functions
│       └── __init__.py
│
├── notebooks/                         # Jupyter notebooks for analysis
│   ├── 01_data_ingestion.ipynb       # Fetch and parse data
│   ├── 02_california_analysis.ipynb  # CA specific analysis
│   ├── 03_mapping.ipynb              # Create maps
│   └── 04_multi_state.ipynb          # Multi-state comparison
│
├── scripts/                           # Standalone analysis scripts
│   ├── analyze_california_feed.py
│   ├── analyze_ny_feed.py
│   ├── create_california_map.py
│   ├── create_multi_state_map.py
│   ├── visualize_data.py
│   └── feed_behavior_analysis.py
│
├── data/                              # Data files
│   ├── raw/                           # Raw API responses
│   │   ├── ca_wzdx_feed.json
│   │   └── ny_wzdx_feed.json
│   └── processed/                     # Processed/cleaned data
│       ├── ca_work_zones_analysis.csv
│       └── ny_work_zones_analysis.csv
│
├── outputs/                           # Generated outputs
│   ├── maps/                          # HTML maps
│   │   ├── california_work_zones_map.html
│   │   └── multi_state_comparison_map.html
│   └── visualizations/                # Charts/graphs
│       ├── work_zone_analysis_1.png
│       ├── work_zone_analysis_2.png
│       ├── work_zone_timeline.png
│       └── top_roads.png
│
├── docs/                              # Documentation
│   ├── PROJECT_SCOPE.md
│   ├── CALIFORNIA_ANALYSIS.md
│   ├── FEED_EXPLAINED.md
│   ├── MODULE_SUMMARY.md
│   ├── QUICK_START.md
│   └── notebooks/                     # Notebook guides
│       ├── JUPYTER_NOTEBOOK_GUIDE.md
│       └── JUPYTER_NOTEBOOK_GUIDE_UPDATED.md
│
├── tmp/                               # Temporary/test files
│   └── .gitkeep                       # Keep directory in git
│
└── external/                          # External resources
    └── wzdx/                          # WZDx specification repo
```

---

## File Categorization

### Keep in Root (3 files)
- `README.md` - Main project readme (will update)
- `.gitignore` - Git configuration (will create)

### Move to `src/` (2 files)
Core library modules:
- `wzdx_analyzer.py` → `src/wzdx_analyzer.py`
- `wzdx_mapping.py` → `src/wzdx_mapping.py`

### Move to `scripts/` (6 files)
Standalone analysis scripts:
- `analyze_california_feed.py` → `scripts/analyze_california_feed.py`
- `analyze_ny_feed.py` → `scripts/analyze_ny_feed.py`
- `create_california_map.py` → `scripts/create_california_map.py`
- `create_multi_state_map.py` → `scripts/create_multi_state_map.py`
- `visualize_data.py` → `scripts/visualize_data.py`
- `feed_behavior_analysis.py` → `scripts/feed_behavior_analysis.py`

### Move to `data/raw/` (2 files)
Raw API responses:
- `ca_wzdx_feed.json` → `data/raw/ca_wzdx_feed.json`
- `ny_wzdx_feed.json` → `data/raw/ny_wzdx_feed.json`

### Move to `data/processed/` (2 files)
Processed datasets:
- `ca_work_zones_analysis.csv` → `data/processed/ca_work_zones_analysis.csv`
- `ny_work_zones_analysis.csv` → `data/processed/ny_work_zones_analysis.csv`

### Move to `outputs/maps/` (2 files)
Generated maps:
- `california_work_zones_map.html` → `outputs/maps/california_work_zones_map.html`
- `multi_state_comparison_map.html` → `outputs/maps/multi_state_comparison_map.html`

### Move to `outputs/visualizations/` (4 files)
Charts and graphs:
- `work_zone_analysis_1.png` → `outputs/visualizations/work_zone_analysis_1.png`
- `work_zone_analysis_2.png` → `outputs/visualizations/work_zone_analysis_2.png`
- `work_zone_timeline.png` → `outputs/visualizations/work_zone_timeline.png`
- `top_roads.png` → `outputs/visualizations/top_roads.png`

### Move to `docs/` (5 files)
Main documentation:
- `PROJECT_SCOPE.md` → `docs/PROJECT_SCOPE.md`
- `CALIFORNIA_ANALYSIS.md` → `docs/CALIFORNIA_ANALYSIS.md`
- `FEED_EXPLAINED.md` → `docs/FEED_EXPLAINED.md`
- `MODULE_SUMMARY.md` → `docs/MODULE_SUMMARY.md`
- `QUICK_START.md` → `docs/QUICK_START.md`

### Move to `docs/notebooks/` (2 files)
Notebook guides:
- `JUPYTER_NOTEBOOK_GUIDE.md` → `docs/notebooks/JUPYTER_NOTEBOOK_GUIDE.md`
- `JUPYTER_NOTEBOOK_GUIDE_UPDATED.md` → `docs/notebooks/JUPYTER_NOTEBOOK_GUIDE_UPDATED.md`

### Move to `tmp/` (1 file)
Test files:
- `test_mapping_module.py` → `tmp/test_mapping_module.py`

### Move to `external/` (1 directory)
External dependencies:
- `wzdx/` → `external/wzdx/`

### Delete (1 file)
Old duplicate:
- `fetch_real_feeds.py` - Superseded by newer scripts

---

## Benefits of New Structure

### For Development
✅ Clear separation of concerns
✅ Easy to find files
✅ Modular code organization
✅ Professional project structure

### For Team
✅ Intuitive navigation
✅ Clear where to add new files
✅ Easy to onboard new members
✅ Better for version control

### For Notebooks
✅ Clean import paths: `from src.wzdx_mapping import WorkZoneMapper`
✅ Organized notebook sequence
✅ Clear data locations
✅ Easy to share outputs

---

## Import Changes

### Before (current)
```python
from wzdx_mapping import WorkZoneMapper
```

### After (new structure)
```python
import sys
sys.path.append('../')  # If in notebooks/
from src.wzdx_mapping import WorkZoneMapper
```

Or better, install as package:
```python
# In Capstone root
pip install -e .
# Then anywhere:
from src.wzdx_mapping import WorkZoneMapper
```

---

## Execution Steps

### Phase 1: Create Directory Structure
1. Create all new directories
2. Add `__init__.py` files for Python packages
3. Add `.gitkeep` for empty directories

### Phase 2: Move Files
1. Move modules to `src/`
2. Move scripts to `scripts/`
3. Move data to `data/raw/` and `data/processed/`
4. Move outputs to `outputs/maps/` and `outputs/visualizations/`
5. Move documentation to `docs/`
6. Move external to `external/`
7. Move test files to `tmp/`

### Phase 3: Update References
1. Update import statements in scripts
2. Update file paths in scripts
3. Update documentation references

### Phase 4: Clean Up
1. Delete obsolete files
2. Create new README.md
3. Create .gitignore
4. Verify all imports work

### Phase 5: Documentation
1. Update README with new structure
2. Create migration guide
3. Update notebook guides with new paths

---

## Commands to Execute

### 1. Create directories
```bash
mkdir -p src/utils
mkdir -p notebooks
mkdir -p scripts
mkdir -p data/raw data/processed
mkdir -p outputs/maps outputs/visualizations
mkdir -p docs/notebooks
mkdir -p tmp
mkdir -p external
```

### 2. Create __init__.py files
```bash
touch src/__init__.py
touch src/utils/__init__.py
```

### 3. Create .gitkeep files
```bash
touch tmp/.gitkeep
```

### 4. Move files (batch operations)
```bash
# Modules to src/
mv wzdx_analyzer.py src/
mv wzdx_mapping.py src/

# Scripts
mv analyze_*.py scripts/
mv create_*.py scripts/
mv visualize_data.py scripts/
mv feed_behavior_analysis.py scripts/

# Data files
mv *_wzdx_feed.json data/raw/
mv *_work_zones_analysis.csv data/processed/

# Maps
mv *_map.html outputs/maps/

# Visualizations
mv *.png outputs/visualizations/

# Documentation
mv PROJECT_SCOPE.md CALIFORNIA_ANALYSIS.md FEED_EXPLAINED.md MODULE_SUMMARY.md QUICK_START.md docs/
mv JUPYTER_NOTEBOOK_GUIDE*.md docs/notebooks/

# Test files
mv test_mapping_module.py tmp/

# External
mv wzdx external/
```

### 5. Delete obsolete
```bash
rm fetch_real_feeds.py
```

---

## Post-Refactoring Checklist

- [ ] All directories created
- [ ] All files moved to correct locations
- [ ] No files left in root (except README.md, .gitignore)
- [ ] Import statements updated
- [ ] File paths updated in scripts
- [ ] New README.md created
- [ ] .gitignore created
- [ ] Documentation updated
- [ ] Test that imports work from notebooks/
- [ ] Git commit with "Refactor: Reorganize project structure"

---

## Timeline

**Estimated time**: 15-20 minutes
- Create structure: 2 min
- Move files: 5 min
- Update imports: 5 min
- Documentation: 5 min
- Testing: 3 min

---

## Risk Mitigation

**Before starting:**
- Commit current state to git (if using)
- Or create backup: `cp -r Capstone Capstone_backup`

**During refactoring:**
- Execute in order (structure → move → update → clean)
- Test imports after moving modules
- Verify file paths in scripts

**After refactoring:**
- Run test script to verify everything works
- Update team members on new structure

---

Ready to execute? The plan is clear and organized.
