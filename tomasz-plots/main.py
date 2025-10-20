import argparse
import os
import sys
from stations import stations, station_file, station_data
import plotly.express as px
import pandas as pd


def locations(all_stations):
    return [d['station'] for d in all_stations]


def location_data(all_data, station, fname):
    href = [d['href'] for d in all_data if d['station'] == station][0]
    html = station_file(href=href, fname=fname)
    return station_data(fname=fname)


def build_df_for_variable(info, year: str, variable: str) -> pd.DataFrame:
    # First find available years
    years = sorted(set(x['year'] for x in info))
    if not year in years:
        print(f"\nNo data found for year {year}.")
        print(f"Available years: {years[0]}-{years[-1]}")
        if len(years) > 0:
            print(f"Try using --year {years[-1]} for latest data")
        return pd.DataFrame(columns=['month', variable])

    pairs = [
        (x['month'], x.get(variable))
        for x in info
        if str(x.get('year')) == str(year) and x.get(variable) not in (None, '', '---')
    ]

    clean = []
    for month, val in pairs:
        try:
            clean.append((month, float(val)))
        except (ValueError, TypeError):
            continue

    if not clean:
        print(f"\nNo valid {variable} measurements found in {year}")
        print("Available variables: tmax, tmin, af, rain, sun")
        return pd.DataFrame(columns=['month', variable])

    months = [m for m, _ in clean]
    values = [v for _, v in clean]
    return pd.DataFrame({'month': months, variable: values})


def get_variable_description(var):
    descriptions = {
        'tmax': 'Maximum temperature',
        'tmin': 'Minimum temperature',
        'af': 'Air frost days',
        'rain': 'Rainfall',
        'sun': 'Sunshine hours'
    }
    return descriptions.get(var, var)


def interactive_menu(all_stations):
    print('\nAvailable stations:')
    for i, s in enumerate(all_stations):
        print(f"{i:3d}: {s}")
    print('')


def choose_variable():
    variables = ['tmax', 'tmin', 'af', 'rain', 'sun']
    print('\nAvailable variables:')
    for i, var in enumerate(variables):
        print(f"{i:3d}: {var:4s} - {get_variable_description(var)}")
    
    while True:
        choice = input('\nEnter variable number (or name) [rain]: ').strip()
        if not choice:
            return 'rain'
        if choice.isdigit() and 0 <= int(choice) < len(variables):
            return variables[int(choice)]
        if choice in variables:
            return choice
        print("Invalid choice. Try again.")


def choose_year(info):
    years = sorted(set(x['year'] for x in info))
    if not years:
        return None
    
    print(f'\nData available from {years[0]} to {years[-1]}')
    latest = years[-1]
    
    while True:
        choice = input(f'\nEnter year [{latest}]: ').strip()
        if not choice:
            return latest
        if choice in years:
            return choice
        try:
            year = int(choice)
            if str(year) in years:
                return str(year)
            print(f"No data for {year}. Choose between {years[0]}-{years[-1]}")
        except ValueError:
            print("Invalid year. Try again.")


def parse_args():
    p = argparse.ArgumentParser(description='Plot met office station data (CLI)')
    p.add_argument('--station', '-s', help='Station name or index (default: first)')
    p.add_argument('--year', '-y', help='Year to plot (default: latest)')
    p.add_argument('--variable', '-v', default='rain', help='Variable to plot, e.g. rain,tmax,tmin (default: rain)')
    p.add_argument('--output', '-o', help='Write HTML to this file instead of plots/chart.html')
    p.add_argument('--non-interactive', action='store_true', help='Do not prompt; use defaults or provided args')
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()

    fname = 'data/station_stations.json'
    all_data = stations(fname=fname)
    all_locations = locations(all_data)

    # Station selection
    chosen_station = None
    if args.station:
        # allow numeric index or exact name
        if args.station.isdigit():
            idx = int(args.station)
            if 0 <= idx < len(all_locations):
                chosen_station = all_locations[idx]
        else:
            if args.station in all_locations:
                chosen_station = args.station

    if not chosen_station and not args.non_interactive:
        interactive_menu(all_locations)
        while not chosen_station:
            sel = input('\nEnter station index or name (leave blank for first): ').strip()
            if sel == '':
                chosen_station = all_locations[0]
            elif sel.isdigit() and 0 <= int(sel) < len(all_locations):
                chosen_station = all_locations[int(sel)]
            elif sel in all_locations:
                chosen_station = sel
            else:
                print("Invalid station. Try again.")

    if not chosen_station:
        # fallback to first station for non-interactive runs or invalid selection
        chosen_station = all_locations[0]

    station_fname = f'data/{chosen_station}_data.txt'
    print(f"Extracting Data for {chosen_station} to {station_fname}")
    info = location_data(all_data=all_data, station=chosen_station, fname=station_fname)

    # Interactive variable selection
    if not args.non_interactive and not args.variable:
        args.variable = choose_variable()
    
    # Interactive year selection
    if not args.non_interactive and not args.year:
        args.year = choose_year(info)

    df = build_df_for_variable(info=info, year=args.year, variable=args.variable)

    if df.empty:
        print(f'No valid data for {args.variable} in {args.year} for station {chosen_station}')
        sys.exit(0)

    # Create plots directory if it doesn't exist
    os.makedirs('plots', exist_ok=True)

    # Prepare the plot
    var_desc = get_variable_description(args.variable)
    fig = px.line(
        df, 
        x='month', 
        y=args.variable, 
        title=f"{chosen_station} {var_desc} in {args.year}",
        labels={
            'month': 'Month',
            args.variable: var_desc
        }
    )

    # Add station metadata if available
    station_info = next((s for s in all_data if s['station'] == chosen_station), None)
    if station_info and 'location' in station_info:
        fig.add_annotation(
            text=f"Location: {station_info['location']}", 
            xref="paper", yref="paper",
            x=0, y=-0.15,
            showarrow=False,
            font=dict(size=10)
        )

    # Save and display
    if args.output:
        output_file = args.output
    else:
        # Default to plots/station_variable_year.html
        safe_name = chosen_station.lower().replace(' ', '_')
        output_file = f'plots/{safe_name}_{args.variable}_{args.year}.html'

    fig.write_html(output_file, include_plotlyjs='cdn')
    print(f'Wrote plot to {output_file}')
    
    # Also show in browser unless explicitly saving elsewhere
    if not args.output:
        fig.show()
