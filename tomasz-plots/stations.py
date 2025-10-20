from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import re
import os
import ssl
import certifi
from typing import List, Dict


def stations(fname: str) -> List[Dict]:
    url = "https://www.metoffice.gov.uk/research/climate/maps-and-data/historic-station-data"

    # Create SSL context using certifi's bundle so certificate verification
    # works on macOS and other environments where the system CA bundle may
    # not be available to Python's ssl module.
    ctx = ssl.create_default_context(cafile=certifi.where())

    page = urlopen(url, context=ctx)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    data = []
    for row in soup.findAll('tr'):
        aux = row.findAll('td')
        if aux:
            results = {}
            results["station"] = aux[0].string
            results["location"] = aux[1].string
            results["openend"] = aux[2].string
            results["href"] = aux[3].find('a')['href']

            textfile = os.path.basename(results['href'])
            shortname = textfile[:-8]
            textfile = f'data/{textfile}'
            jsonfile = textfile.replace('.txt','.json')
    

            results['text'] = textfile
            results['json'] = jsonfile
            results['shortname'] = shortname
            data.append(results)

    with open(fname, 'w') as f:
        json.dump(data, f,sort_keys=True,indent=4, ensure_ascii=True)
        
    return data

def station_file(href: str,fname: str):
    # reuse certifi-backed SSL context for the file download as well
    ctx = ssl.create_default_context(cafile=certifi.where())
    page = urlopen(href, context=ctx)
    html = page.read().decode("utf-8")
    with open(fname,'w') as fw:
        fw.write(html)
    return html

def raw_data(infile: str) -> list[str]:
    with open(infile,'r') as fr:
        lines  = fr.readlines()
    return lines

def raw_html(lines: list[str]) -> list[str]:
    lines = [x.strip() for x in lines]
    return lines

def filtered_data(infile: str) -> list [str]:
    lines = raw_data(infile=infile)
    # Debug: print first few lines to see format
    print("\nFirst 5 lines of raw data:")
    for line in lines[:5]:
        print(f"Line: '{line}'")
    
    # Look for year at start of line (1xxx-2xxx) after optional whitespace
    matches = [line for line in lines if re.match(r'^\s*([1-2][0-9]{3})',line)]
    if not matches:
        print("\nNo lines matched the year pattern. Trying original pattern...")
        matches = [line for line in lines if re.match(r'^\s{3}([1-3][0-9]{3})',line)]
    
    print(f"\nFound {len(matches)} matching data lines")
    if matches:
        print("First matching line:", matches[0])
    return matches

def save_json(fname: str, data: str) -> None:
    with open(fname, 'w') as f:
        json.dump(data, f,sort_keys=True,indent=4, ensure_ascii=True)

def read_json(fname: str) -> dict | None:
    data = dict()
    with open(fname, 'r') as f:
        data = json.load(fp=f)
    return data

def station_data(infile: str = None, fname: str = None):
    # Accept either `infile` (existing callers) or `fname` (calls from main.py)
    target = infile if infile is not None else fname
    if target is None:
        raise ValueError("station_data requires an 'infile' or 'fname' argument")

    lines = filtered_data(infile=target)
    data = []
    for line in lines:
        # Remove multiple spaces and split, handling possible *'s for estimated values
        clean_line = ' '.join(line.split())
        parts = clean_line.split()
        if len(parts) < 7:
            continue
            
        row = {}
        row['year'] = parts[0].strip()
        row['month'] = parts[1].strip()
        # Handle estimated values marked with *
        row['tmax'] = parts[2].strip().rstrip('*')
        row['tmin'] = parts[3].strip().rstrip('*')
        row['af'] = parts[4].strip().rstrip('*')
        row['rain'] = parts[5].strip().rstrip('*')
        # Some stations might have fewer fields
        row['sun'] = parts[6].strip().rstrip('*') if len(parts) > 6 else '---'
        
        # Skip rows where all values are missing
        if all(v == '---' for v in [row['tmax'], row['tmin'], row['af'], row['rain'], row['sun']]):
            continue
            
        data.append(row)
        
    if not data:
        print(f"\nNo valid data found in {target}")
    else:
        print(f"\nFound {len(data)} valid data points")
        years = sorted(set(row['year'] for row in data))
        print(f"Year range: {years[0]}-{years[-1]}")
    
    return data

def station_json(infile: str) -> dict:
    data = read_json(fname=infile)
    return data

def refresh_station_data() -> dict:
    datadir = 'data'
    fname = f'{datadir}/station_stations.json'
    weather_stations = stations(fname=fname)

    for station in weather_stations:
        text_fname = station['text']
        json_fname = station['json']
        station_file(fname=text_fname, href=station['href'])
        data = station_data(infile=text_fname)
        save_json(fname=json_fname,data=data)
    return weather_stations