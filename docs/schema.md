# WeatherFlow – Data Schema (v0)

## Keys & Time
- Primary key: (`station_id`, `timestamp`)
- Timezone: UTC
- Frequency: every 5 minutes (tolerancja: brak >10 min przerwy bez flagi)
- Timestamp format: `YYYY-MM-DD HH:MM:SS`

## Columns
| column         | type     | unit | allowed range        | nullable | notes                                      |
|----------------|----------|------|----------------------|----------|--------------------------------------------|
| timestamp      | datetime | UTC  | —                    | no       | ISO8601; bez sekund też ok? (ustal)        |
| station_id     | string   | —    | —                    | no       | np. WF001                                  |
| temp_c         | float    | °C   | -50..60              | yes      | wartości ekstremalne oznacz jako suspect   |
| humidity_pct   | int      | %    | 0..100               | yes      |                                            |
| pressure_hpa   | int      | hPa  | 850..1100            | yes      | lokalnie zwykle 950..1050                  |
| wind_speed_ms  | float    | m/s  | >= 0                 | yes      |                                            |
| wind_dir_deg   | int      | deg  | 0..360               | yes      | 0/360 = N                                  |
| rain_mm        | float    | mm   | >= 0                 | yes      | **interwał** czy **narastająca**? → WYBÓR  |

## Business rules
- (`station_id`, `timestamp`) must be unique.
- `rain_mm` cannot be negative.
- Jeżeli `humidity_pct` > 100 lub < 0 → rekord nie przechodzi walidacji.
- Jeżeli `wind_dir_deg` poza 0..360 → invalid.
- Jeśli brakuje `timestamp` lub `station_id` → invalid (quarantine).

## Open questions
- [ ] `rain_mm`: interwał
- [ ] częstotliwość: 5 minut
- [ ] dopuszczalne braki (nullable)
