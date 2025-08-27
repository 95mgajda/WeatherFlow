# src/weatherflow/validation.py
import pandera as pa
from pandera import Column, Check
from pandera.typing import DataFrame

class WeatherSchema(pa.SchemaModel):
    timestamp: Column(pa.DateTime, nullable=False)
    station_id: Column(pa.String, nullable=False)

    temp_c: Column(float, nullable=True, checks=Check.in_range(min_value=-50, max_value=60))
    humidity_pct: Column(int, nullable=True, checks=Check.in_range(min_value=0, max_value=100))
    pressure_hpa: Column(int, nullable=True, checks=Check.in_range(min_value=850, max_value=1100))
    wind_speed_ms: Column(float, nullable=True, checks=Check.ge(0))
    wind_dir_deg: Column(int, nullable=True, checks=Check.in_range(min_value=0, max_value=360))
    rain_mm: Column(float, nullable=True, checks=Check.ge(0))

    class Config:
        name = "WeatherSchema"
        coerce = True  # automatyczne rzutowanie typów, jeśli możliwe

# Dodatkowy check: unikalność klucza złożonego
def validate_unique_key(df):
    dup = df.duplicated(subset=["station_id", "timestamp"]).any()
    if dup:
        raise pa.errors.SchemaError("Duplicate (station_id, timestamp) found.")
    return df

def validate_dataframe(df) -> DataFrame[WeatherSchema]:
    validated = WeatherSchema.validate(df, lazy=True)  # zbierze wszystkie błędy naraz
    validate_unique_key(validated)
    return validated
