# Migration Guide - New Repository Structure

## What Changed

The repository has been reorganized for better modularity, team collaboration, and maintainability.

---

## Before → After

### Old Structure (Everything in root)
```
Capstone/
├── wzdx_analyzer.py
├── wzdx_mapping.py
├── analyze_california_feed.py
├── ca_wzdx_feed.json
├── california_work_zones_map.html
├── ... (25+ files in root)
```

### New Structure (Organized)
```
Capstone/
├── src/                 # Modules
├── scripts/             # Analysis scripts
├── data/                # Data files
├── outputs/             # Generated files
├── docs/                # Documentation
├── notebooks/           # Jupyter notebooks
├── tmp/                 # Temporary files
└── external/            # External dependencies
```

---

## Import Path Changes

### For Python Scripts
**Old**:
```python
from wzdx_mapping import WorkZoneMapper
```

**New**:
```python
from src.wzdx_mapping import WorkZoneMapper
```

### For Jupyter Notebooks
**Old**:
```python
from wzdx_mapping import WorkZoneMapper
```

**New** (from notebooks/ directory):
```python
import sys
sys.path.append('../')
from src.wzdx_mapping import WorkZoneMapper
```

---

## File Path Changes

### Data Files
**Old**:
```python
df = pd.read_csv('ca_work_zones_analysis.csv')
with open('ca_wzdx_feed.json') as f:
```

**New**:
```python
df = pd.read_csv('data/processed/ca_work_zones_analysis.csv')
with open('data/raw/ca_wzdx_feed.json') as f:
```

### Output Files
**Old**:
```python
mapper.save_map('california_map.html')
plt.savefig('chart.png')
```

**New**:
```python
mapper.save_map('outputs/maps/california_map.html')
plt.savefig('outputs/visualizations/chart.png')
```

---

## Quick Reference

### From Root Directory
```python
from src.wzdx_mapping import WorkZoneMapper
from src.wzdx_analyzer import WZDxAnalyzer

df = pd.read_csv('data/processed/ca_work_zones_analysis.csv')
mapper.save_map('outputs/maps/my_map.html')
```

### From notebooks/ Directory
```python
import sys
sys.path.append('../')

from src.wzdx_mapping import WorkZoneMapper
from src.wzdx_analyzer import WZDxAnalyzer

df = pd.read_csv('../data/processed/ca_work_zones_analysis.csv')
mapper.save_map('../outputs/maps/my_map.html')
```

### From scripts/ Directory
```python
import sys
sys.path.append('../')

from src.wzdx_mapping import WorkZoneMapper
from src.wzdx_analyzer import WZDxAnalyzer

df = pd.read_csv('../data/processed/ca_work_zones_analysis.csv')
mapper.save_map('../outputs/maps/my_map.html')
```

---

## Updated Scripts

All scripts in `scripts/` have been updated with correct import paths. No action needed.

---

## File Locations

### Modules (import from here)
- `src/wzdx_analyzer.py`
- `src/wzdx_mapping.py`

### Analysis Scripts (run these)
- `scripts/analyze_california_feed.py`
- `scripts/analyze_ny_feed.py`
- `scripts/create_california_map.py`
- `scripts/create_multi_state_map.py`
- `scripts/visualize_data.py`
- `scripts/feed_behavior_analysis.py`

### Data Files
**Raw**:
- `data/raw/ca_wzdx_feed.json`
- `data/raw/ny_wzdx_feed.json`

**Processed**:
- `data/processed/ca_work_zones_analysis.csv`
- `data/processed/ny_work_zones_analysis.csv`

### Generated Outputs
**Maps**:
- `outputs/maps/california_work_zones_map.html`
- `outputs/maps/multi_state_comparison_map.html`

**Visualizations**:
- `outputs/visualizations/work_zone_analysis_1.png`
- `outputs/visualizations/work_zone_analysis_2.png`
- `outputs/visualizations/work_zone_timeline.png`
- `outputs/visualizations/top_roads.png`

### Documentation
- `docs/PROJECT_SCOPE.md`
- `docs/CALIFORNIA_ANALYSIS.md`
- `docs/FEED_EXPLAINED.md`
- `docs/MODULE_SUMMARY.md`
- `docs/QUICK_START.md`
- `docs/notebooks/JUPYTER_NOTEBOOK_GUIDE.md`
- `docs/notebooks/JUPYTER_NOTEBOOK_GUIDE_UPDATED.md`

---

## Running Scripts

### Old
```bash
python analyze_california_feed.py
python create_california_map.py
```

### New
```bash
python scripts/analyze_california_feed.py
python scripts/create_california_map.py
```

Or from scripts directory:
```bash
cd scripts
python analyze_california_feed.py
```

---

## Adding New Files

### New Jupyter Notebook
1. Save to: `notebooks/my_analysis.ipynb`
2. Import modules:
   ```python
   import sys
   sys.path.append('../')
   from src.wzdx_mapping import WorkZoneMapper
   ```

### New Python Script
1. Save to: `scripts/my_script.py`
2. Import modules:
   ```python
   import sys
   sys.path.append('../')
   from src.wzdx_mapping import WorkZoneMapper
   ```

### New Module
1. Save to: `src/my_module.py`
2. Import from notebooks/scripts:
   ```python
   from src.my_module import MyClass
   ```

### New Data File
- Raw: `data/raw/my_data.json`
- Processed: `data/processed/my_data.csv`

### New Output
- Map: `outputs/maps/my_map.html`
- Chart: `outputs/visualizations/my_chart.png`

---

## Git Ignore

Data and output files are gitignored:
- `data/raw/*.json`
- `data/processed/*.csv`
- `outputs/maps/*.html`
- `outputs/visualizations/*.png`

To share data with team:
1. Use cloud storage
2. Document data source in README
3. Provide fetch scripts

---

## Benefits

✅ **Cleaner root** - Only README and .gitignore
✅ **Organized** - Everything in logical folders
✅ **Professional** - Industry-standard structure
✅ **Team-friendly** - Easy to navigate
✅ **Scalable** - Room to grow

---

## Checklist for Team Members

- [ ] Pull latest changes
- [ ] Update notebook import paths
- [ ] Update data file paths
- [ ] Update output save paths
- [ ] Test that everything works
- [ ] Read new README.md

---

## Help

If something doesn't work:
1. Check import paths
2. Check file paths
3. Make sure you're in the right directory
4. Read the new README.md

---

**Migration completed**: October 2025
**Old structure removed**: All files moved
**Backward compatibility**: Update your imports
