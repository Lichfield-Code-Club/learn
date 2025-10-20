from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import os
import json
from stations import (
    refresh_station_data, station_data, raw_data, read_json,
    station_file, save_json
)
from plot import sample_plot, template_plot

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dummy weather data
weather_data = {
    "2021-01-01": {"temperature":  5, "description": "Sunny"},
    "2021-01-02": {"temperature":  3, "description": "Cloudy"},
    "2021-01-03": {"temperature": -1, "description": "Snowy"},
    "2024-04-19": {"temperature": -1, "description": "Snowy"},
    "2024-04-20": {"temperature": -1, "description": "Snowy"},
    "2024-04-21": {"temperature": -1, "description": "Snowy"},
}

@app.get("/refresh/stations",response_class=HTMLResponse)
async def refresh_data(request: Request):
    # Real weather data
    stations = refresh_station_data()
    return templates.TemplateResponse("stations.html", {
        "request": request,
        "station_list": stations
        }
    )

@app.get("/stations",response_class=HTMLResponse)
async def stations(request: Request):
    fname="data/station_stations.json"
    with open(fname,'r') as fr:
        stations = json.load(fp=fr)
    return templates.TemplateResponse("stations.html", {
        "request": request,
        "station_list": stations
        }
    )


def ensure_data_files(station_name: str) -> tuple[str, str]:
    """Ensure data files exist for a station, refresh if needed."""
    datadir = 'data'
    os.makedirs(datadir, exist_ok=True)
    
    station_json = f'{datadir}/station_stations.json'
    if not os.path.exists(station_json):
        refresh_station_data()
        
    with open(station_json, 'r') as f:
        stations = json.load(f)
        
    station_info = next((s for s in stations if s['station'] == station_name), None)
    if not station_info:
        raise ValueError(f"Station {station_name} not found")
        
    text_file = station_info['text']
    json_file = station_info['json']
    
    if not os.path.exists(text_file) or not os.path.exists(json_file):
        print(f"Refreshing data for {station_name}")
        station_file(href=station_info['href'], fname=text_file)
        data = station_data(infile=text_file)
        save_json(fname=json_file, data=data)
        
    return text_file, json_file

@app.get("/station/data/{station_name}",response_class=HTMLResponse)
async def text_data(station_name: str, request: Request):
    try:
        text_file, _ = ensure_data_files(station_name)
        data = station_data(infile=text_file)
        return templates.TemplateResponse("data.html", {
            "data": data,
            "title": f'{station_name} Text Data',
            "request": request
            }
        )
    except ValueError as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": str(e)
        }, status_code=404)

@app.get("/station/json/{station_name}",response_class=HTMLResponse)
async def json_data(station_name: str, request: Request):
    datadir = 'data'
    datafile = f'{datadir}/{station_name}data.json'
    data = raw_data(datafile)
    data = [x.strip('\n') for x in data]
    return templates.TemplateResponse("json.html", {
        "data": data,
        "title": f'{station_name} json',
        "request": request
        }
    )

@app.get("/dates", response_class=HTMLResponse)
async def dates(request: Request):
    return templates.TemplateResponse("dates.html", {"request": request})
    
@app.post("/weather", response_class=HTMLResponse)
async def get_weather(request: Request, start_date: str = Form(...), end_date: str = Form(...)):
    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Filter weather data within the date range
    filtered_weather_data = {
        date: data for date, data in weather_data.items()
        if start_date <= datetime.strptime(date, "%Y-%m-%d") <= end_date
    }
    
    return templates.TemplateResponse(
        "weather.html",
        {
            "request": request,
            "weather_data": filtered_weather_data,
            "start_date": start_date,
            "end_date": end_date
        }
    )

@app.get("/plot", response_class=HTMLResponse)
async def plot_weather(request: Request, station: str = "Cardiff"):
    try:
        _, json_file = ensure_data_files(station)
        data = read_json(json_file)
        
        if not data:
            raise ValueError(f"No data available for station {station}")
            
        return template_plot(data)
    except ValueError as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": str(e)
        }, status_code=404)

@app.get("/help", response_class=HTMLResponse)
async def help(request: Request):
    fname="data/station_stations.json"
    with open(fname,'r') as fr:
        stations = json.load(fp=fr)
    
    return templates.TemplateResponse("help.html", {"request": request, "station_list": stations})

@app.get("/plotform", response_class=HTMLResponse)
async def plot_form(request: Request):
    # Load station list
    fname = "data/station_stations.json"
    if not os.path.exists(fname):
        stations = refresh_station_data()
    else:
        with open(fname, "r") as fr:
            stations = json.load(fr)
    # Use latest year from first station as default
    first_station = stations[0] if stations else None
    default_year = "2023"
    if first_station:
        text_file = first_station["text"]
        if os.path.exists(text_file):
            data = station_data(infile=text_file)
            years = sorted(set(row["year"] for row in data))
            if years:
                default_year = years[-1]
    return templates.TemplateResponse("plot_form.html", {
        "request": request,
        "station_list": stations,
        "default_year": default_year,
        "plot_html": None
    })

@app.post("/plotform", response_class=HTMLResponse)
async def plot_form_post(request: Request, station: str = Form(...), year: str = Form(...), variable: str = Form(...)):
    # Load station list
    fname = "data/station_stations.json"
    with open(fname, "r") as fr:
        stations = json.load(fr)
    plot_html = None
    try:
        text_file, json_file = ensure_data_files(station)
        data = read_json(json_file)
        # Filter for year and variable
        filtered = [row for row in data if row["year"] == year and row[variable] not in (None, '', '---')]
        if not filtered:
            plot_html = f"<p>No data for {variable} in {year} at {station}</p>"
        else:
            import plotly.express as px
            import pandas as pd
            months = [row["month"] for row in filtered]
            values = [float(row[variable]) for row in filtered]
            df = pd.DataFrame({"month": months, variable: values})
            fig = px.line(df, x="month", y=variable, title=f"{station} {variable} {year}")
            plot_html = fig.to_html(full_html=False)
    except Exception as e:
        plot_html = f"<p>Error: {e}</p>"
    return templates.TemplateResponse("plot_form.html", {
        "request": request,
        "station_list": stations,
        "default_year": year,
        "plot_html": plot_html
    })