# Work Zone Map Viewer

An interactive Streamlit application for visualizing work zone data for Texas and California.

## Features

- Interactive map visualization using Folium
- Toggle between Texas and California work zones
- Responsive design with full-width layout
- File size information for each map

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd Capstone
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run workzone_map_viewer.py
```

The app will open in your default browser at `http://localhost:8501`

## Project Structure

```
Capstone/
├── workzone_map_viewer.py   # Main Streamlit application
├── outputs/
│   └── maps/
│       ├── texas_workzones_map.html
│       └── california_work_zones_map.html
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Requirements

- Python 3.8+
- Streamlit 1.28.0+
- See `requirements.txt` for full list of dependencies

## Maps

The application displays pre-generated HTML maps created from work zone and crash data for:
- **Texas**: Work zones across the state
- **California**: Work zones across the state

## Local Deployment

To deploy locally:

1. Ensure all map files are in the `outputs/maps/` directory
2. Install dependencies
3. Run the Streamlit app as shown above

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
