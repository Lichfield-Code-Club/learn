# tomasz-plots

Graph plots from UK Met Office weather data. Access historical weather station data through either a command-line interface or web application.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the interactive CLI:
```bash
python3 main.py
```

Or start the web server:
```bash
uvicorn weather:app --reload
```

## Command Line Interface

The CLI supports three modes of operation:

### 1. Interactive Mode (Default)
```bash
python3 main.py
```
- Shows a menu of available weather stations
- Lets you choose the year from available data
- Select what to plot (rainfall, temperature, etc.)
- Opens plot in browser and saves HTML file

### 2. Semi-Interactive Mode
Specify some options and get prompted for others:
```bash
python3 main.py --station "Cardiff Bute Park" --year 2023
```
```bash
python3 main.py --variable tmax  # choose station/year interactively
```

### 3. Non-Interactive Mode
Specify all options for automation:
```bash
python3 main.py --non-interactive --station Aberporth --year 2023 --variable rain
```

### CLI Options
```
--station, -s    Station name or index number
--year, -y       Year to plot (defaults to latest)
--variable, -v   Variable to plot (default: rain)
--output, -o     Custom HTML output path
--non-interactive  Don't show prompts, use defaults
```

### Available Variables
- `tmax` - Maximum temperature
- `tmin` - Minimum temperature
- `af` - Air frost days
- `rain` - Rainfall
- `sun` - Sunshine hours

### Output
- Plots are saved to `plots/` directory by default
- Files named as `station_variable_year.html`
- Interactive plots open in your browser
- Use `--output` for custom file location

## Web Interface

Start the web server:
```bash
uvicorn weather:app --reload
```
Or to run on a different port (e.g. 8001):
```bash
uvicorn weather:app --reload --port 8001
```
Or with python -m:
```bash
python3 -m uvicorn weather:app --reload --port 8001
```

### Available URLs
- Main app: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) (or your chosen port)
- API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Interactive plot form: [http://127.0.0.1:8000/plotform](http://127.0.0.1:8000/plotform)

### Web Features
- Browse all weather stations
- View data by date range
- Interactive plots
- Download raw data
- **Interactive Plot Form**: Select station, year, and variable to generate a plot in your browser

### Using the Interactive Plot Form
1. Start the server (see above)
2. Open [http://127.0.0.1:8000/plotform](http://127.0.0.1:8000/plotform) in your browser (replace 8000 with your chosen port)
3. Select:
   - **Station**: Choose from all available UK Met Office stations
   - **Year**: Enter a year within the available range for the station
   - **Variable**: Choose from rainfall, temperature, air frost, sunshine, etc.
4. Click **Generate Plot**
5. The plot will appear below the form, interactive with zoom/pan/hover features

If you change the station, you may need to check the available year range for that station. The form will use the latest year by default.

### Sample Weather Data
```json
"weather-data":  {
    "2021-01-01": {"temperature": 5, "description": "Sunny"},
    "2021-01-02": {"temperature": 3, "description": "Cloudy"},
    "2021-01-03": {"temperature": -1, "description": "Snowy"},
    "2024-04-19": {"temperature": -1, "description": "Snowy"},
    "2024-04-20": {"temperature": -1, "description": "Snowy"},
    "2024-04-21": {"temperature": -1, "description": "Snowy"}
}
```

## Examples

### 1. Interactive Plot Creation
```bash
python3 main.py
# Follow the prompts to:
# 1. Choose a station
# 2. Select a year
# 3. Pick what to plot
```

### 2. Temperature Analysis
```bash
# Plot maximum temperatures for Heathrow in 2023
python3 main.py --station "Heathrow" --year 2023 --variable tmax

# Compare minimum temperatures from winter months
python3 main.py --station "Braemar No 2" --year 2023 --variable tmin

# View air frost days
python3 main.py --station "Durham" --year 2023 --variable af
```

### 3. Rainfall Analysis
```bash
# Latest rainfall data for Cardiff
python3 main.py --station "Cardiff Bute Park" --variable rain

# Save annual rainfall plot
python3 main.py --station "Durham" --year 2020 --variable rain --output "durham_rain_2020.html"

# Check sunshine hours
python3 main.py --station "Eastbourne" --year 2023 --variable sun
```

### 4. Batch Processing
```bash
# Generate plots for multiple stations (example script)
#!/bin/bash
for station in "Heathrow" "Durham" "Cardiff Bute Park"; do
    python3 main.py --non-interactive --station "$station" --year 2023 --variable tmax \
        --output "plots/${station// /_}_2023_tmax.html"
done
```

### Example Plots

The plots are interactive HTML files with hover details, zoom, and pan capabilities.

#### Maximum Temperature Plot
![Example temperature plot for Heathrow](plots/example_temperature.png)
*Maximum temperatures at Heathrow Airport, 2023*

#### Rainfall Plot
![Example rainfall plot for Cardiff](plots/example_rainfall.png)
*Monthly rainfall at Cardiff Bute Park, 2023*

### 5. Web Interface Usage
1. Start the server: `uvicorn weather:app --reload`
2. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
3. Try the available endpoints:
   - `/stations` - List all stations
   - `/refresh/stations` - Update station data
   - `/station/data/{station}` - View station data
   - `/plot` - Generate plots

## Troubleshooting

### SSL Certificate Errors
If you see `CERTIFICATE_VERIFY_FAILED` errors:
```
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```
The script automatically handles this using the `certifi` package. Just ensure you've installed dependencies:
```bash
pip install -r requirements.txt
```

### No Data Found
If you see "No valid data for [variable] in [year]":
1. Check the station's available years:
   ```bash
   python3 main.py  # Choose station, it will show year range
   ```
2. Some variables might not be recorded for all stations/years
3. Use the interactive mode to see valid year ranges

### Missing or Invalid Station
```bash
# List all available stations
python3 main.py --non-interactive  # Shows full station list

# Check if data needs refreshing
python3 main.py --refresh  # Updates station list
```

### Plot Display Issues
1. Plots are saved as HTML files in `plots/` by default
2. Open manually if browser doesn't launch:
   ```bash
   # macOS
   open plots/station_variable_year.html
   # Linux
   xdg-open plots/station_variable_year.html
   ```
3. Use `--output` to save somewhere else:
   ```bash
   python3 main.py --station "Heathrow" --output "/tmp/plot.html"
   ```

### Data Quality Notes
- Missing data marked as "---" in source files
- Estimated values marked with * in source files
- Some stations have limited variables or years
- Sunshine hours might use different measurement methods (see station notes)

## Data Storage

- Station metadata: `data/station_stations.json`
- Raw station data: `data/{station}data.txt`
- Generated plots: `plots/{station}_{variable}_{year}.html`

## Development Guide

### Project Structure
```
tomasz-plots/
├── data/               # Station data and metadata
├── plots/             # Generated plot files
├── static/            # Web UI static assets
├── templates/         # Jinja2 templates for web UI
├── utils/            # Helper scripts
│   └── save_screenshots.py  # Convert plots to PNG
├── main.py           # CLI entry point
├── stations.py       # Station data handling
├── weather.py        # FastAPI web application
├── plot.py           # Plotting utilities
└── requirements.txt  # Python dependencies
```

### Adding New Features

#### 1. New Plot Types
In `plot.py`:
```python
def new_plot_type(data, **kwargs):
    """Add a new plotting function."""
    fig = px.scatter(...)  # or other plot type
    return fig
```

#### 2. New Data Variables
In `stations.py`:
```python
def station_data():
    # Add new field to row{}:
    row['new_field'] = parse_field(weather_data[idx])
```

#### 3. New CLI Options
In `main.py`:
```python
def parse_args():
    p.add_argument('--new-option', 
                  help='Description')
```

#### 4. New Web Routes
In `weather.py`:
```python
@app.get("/new-endpoint")
async def new_feature(request: Request):
    return templates.TemplateResponse(...)
```

### Converting Plots to PNG
For README screenshots or static images:

1. Install requirements:
```bash
pip install -r requirements.txt
playwright install
```

2. Generate example plots:
```bash
python3 main.py --non-interactive --station "Heathrow" \
    --year 2023 --variable tmax \
    --output "plots/example_temperature.html"
```

3. Convert to PNG:
```bash
python3 utils/save_screenshots.py
```

### Adding Tests
1. Create test files in `tests/`
2. Test data parsing:
```python
def test_station_data():
    data = station_data(test_file)
    assert len(data) > 0
    assert 'rain' in data[0]
```

3. Test plotting:
```python
def test_plot_generation():
    fig = create_plot(test_data)
    assert fig.data
```

### Code Style
- Use type hints for function arguments
- Document functions with docstrings
- Follow PEP 8 style guidelines
- Add tests for new features

## Contributing

Found a bug or want to contribute? Please check our [GitHub repository](https://github.com/Lichfield-Code-Club/tomasz-plots).

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request
