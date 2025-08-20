# src/weatherflow/generate.py
import csv, time, random, datetime, os
from pathlib import Path

def generate_row(station_id="WF001"):
    now = datetime.datetime.utcnow().replace(microsecond=0)
    return {
        "timestamp": now.isoformat(sep=" "),
        "station_id": station_id,
        "temp_c": round(random.uniform(15, 25), 1),
        "humidity_pct": random.randint(40, 70),
        "pressure_hpa": random.randint(1000, 1020),
        "wind_speed_ms": round(random.uniform(0, 5), 1),
        "wind_dir_deg": random.randint(0, 360),
        "rain_mm": round(random.choice([0, 0, 0.1, 0.2]), 1)
    }

def run_generator(filename=None, interval=5):
    # policz root projektu: .../WeatherFlow/
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    default_file = PROJECT_ROOT / "data" / "incoming" / "weather.csv"
    file_path = Path(filename) if filename else default_file

    # utwórz katalogi
    file_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[Generator] zapisuję do: {file_path}")  # diagnostyka

    with file_path.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp","station_id","temp_c","humidity_pct",
            "pressure_hpa","wind_speed_ms","wind_dir_deg","rain_mm"
        ])
        if f.tell() == 0:
            writer.writeheader()
        while True:
            row = generate_row()
            writer.writerow(row)
            print("Generated:", row)
            time.sleep(interval)

if __name__ == "__main__":
    run_generator()
