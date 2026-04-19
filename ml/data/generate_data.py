"""
Smart Rail Mumbai — Data Generation Module
Generates realistic synthetic ridership data based on actual Mumbai Metro statistics.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# ── Real Mumbai Metro ridership (2025 actuals) ───────────────────────────────
DAILY_RIDERSHIP = {
    1: 525000,   # Line 1 Blue  (Versova–Ghatkopar) — 12 stations
    2: 165000,   # Line 2A Yellow — 17 stations
    3: 170000,   # Line 3 Aqua  — 27 stations
    7: 165000,   # Line 7 Red   — 14 stations
    5: 15000,    # Monorail     — 17 stations
}

STATION_COUNTS = {1: 12, 2: 17, 3: 27, 7: 14, 5: 17}
LINE_CAPACITY  = {1: 2500, 2: 1800, 3: 2400, 7: 1800, 5: 600}

STATIONS = [
    (1,"Versova",1,"Blue",0),(2,"D.N. Nagar",1,"Blue",0),
    (3,"Azad Nagar",1,"Blue",0),(4,"Andheri",1,"Blue",1),
    (5,"Western Express Highway",1,"Blue",0),(6,"Chakala",1,"Blue",0),
    (7,"Airport Road",1,"Blue",0),(8,"Marol Naka",1,"Blue",1),
    (9,"Saki Naka",1,"Blue",0),(10,"Asalpha",1,"Blue",0),
    (11,"Jagruti Nagar",1,"Blue",0),(12,"Ghatkopar",1,"Blue",1),

    (13,"Dahisar East",2,"Yellow",0),(14,"Anand Nagar",2,"Yellow",0),
    (15,"Kandarpada",2,"Yellow",0),(16,"Mandapeshwar",2,"Yellow",0),
    (17,"Eksar",2,"Yellow",0),(18,"Borivali West",2,"Yellow",1),
    (19,"Shimpoli",2,"Yellow",0),(20,"Kandivali West",2,"Yellow",1),
    (21,"Dahanukarwadi",2,"Yellow",0),(22,"Valnai–Meeth Chowky",2,"Yellow",0),
    (23,"Malad West",2,"Yellow",0),(24,"Lower Malad",2,"Yellow",0),
    (25,"Bangur Nagar",2,"Yellow",1),(26,"Goregaon West",2,"Yellow",0),
    (27,"Oshiwara",2,"Yellow",0),(28,"Lower Oshiwara",2,"Yellow",0),
    (29,"Andheri West",2,"Yellow",0),

    (30,"Aarey JVLR",3,"Aqua",0),(31,"SEEPZ",3,"Aqua",0),
    (32,"MIDC-Andheri",3,"Aqua",1),(33,"Marol Naka",3,"Aqua",1),
    (34,"Airport T2",3,"Aqua",0),(35,"Sahar Road",3,"Aqua",1),
    (36,"Airport T1",3,"Aqua",0),(37,"Santacruz",3,"Aqua",0),
    (38,"Bandra Colony",3,"Aqua",1),(39,"BKC",3,"Aqua",1),
    (40,"Dharavi",3,"Aqua",0),(41,"Shitaladevi Mandir",3,"Aqua",0),
    (42,"Dadar",3,"Aqua",0),(43,"Siddhivinayak",3,"Aqua",0),
    (44,"Worli",3,"Aqua",0),(45,"Acharya Atre Chowk",3,"Aqua",1),
    (46,"Science Centre",3,"Aqua",0),(47,"Mahalaxmi",3,"Aqua",0),
    (48,"Jagannath Shankar Sheth",3,"Aqua",1),(49,"Grant Road",3,"Aqua",0),
    (50,"Girgaon",3,"Aqua",0),(51,"Kalbadevi",3,"Aqua",0),
    (52,"CSMT",3,"Aqua",0),(53,"Hutatma Chowk",3,"Aqua",0),
    (54,"Churchgate",3,"Aqua",0),(55,"Vidhan Bhavan",3,"Aqua",1),
    (56,"Cuffe Parade",3,"Aqua",0),

    (57,"Dahisar East L7",7,"Red",1),(58,"Ovaripada",7,"Red",0),
    (59,"Rashtriya Udyan",7,"Red",0),(60,"Devipada",7,"Red",0),
    (61,"Magathane",7,"Red",0),(62,"Poisar",7,"Red",1),
    (63,"Akurli",7,"Red",0),(64,"Kurar",7,"Red",0),
    (65,"Dindoshi",7,"Red",0),(66,"Aarey",7,"Red",0),
    (67,"Goregaon East",7,"Red",0),(68,"Jogeshwari East",7,"Red",0),
    (69,"Mogra",7,"Red",0),(70,"Gundavali",7,"Red",0),

    (71,"Chembur",5,"Mono",1),(72,"Bhakti Park",5,"Mono",0),
    (73,"Fertilizer Township",5,"Mono",0),(74,"Mysore Colony",5,"Mono",0),
    (75,"Bharat Petroleum",5,"Mono",0),(76,"Wadala",5,"Mono",1),
    (77,"GTB Nagar",5,"Mono",0),(78,"Acharya Atre M",5,"Mono",0),
    (79,"Antop Hill",5,"Mono",0),(80,"Sion Circle",5,"Mono",0),
    (81,"Sant Gadge Chowk",5,"Mono",0),(82,"Curry Road",5,"Mono",0),
    (83,"Naigaon",5,"Mono",0),(84,"Lower Parel Mono",5,"Mono",1),
    (85,"Ambewadi",5,"Mono",0),(86,"Chinchpokli",5,"Mono",0),
    (87,"Jacob Circle",5,"Mono",0),
]

# ── Mumbai Festivals / Holidays 2024–2025 ────────────────────────────────────
MUMBAI_FESTIVALS = {
    "2024-01-26": ("Republic Day", 0.7),
    "2024-03-25": ("Holi", 0.65),
    "2024-04-14": ("Ambedkar Jayanti", 0.75),
    "2024-04-17": ("Ram Navami", 0.6),
    "2024-05-23": ("Buddha Purnima", 0.6),
    "2024-07-17": ("Eid ul-Adha", 0.55),
    "2024-08-15": ("Independence Day", 0.8),
    "2024-08-26": ("Ganesh Chaturthi", 1.6),  # MASSIVE surge
    "2024-09-04": ("Ganesh Visarjan", 1.8),   # Biggest day
    "2024-10-02": ("Gandhi Jayanti", 0.7),
    "2024-10-12": ("Dussehra", 1.2),
    "2024-10-13": ("Navratri peak", 1.3),
    "2024-11-01": ("Diwali", 1.4),
    "2024-11-02": ("Diwali 2", 0.5),          # Low — people stay home
    "2024-11-15": ("Guru Nanak Jayanti", 0.8),
    "2024-12-25": ("Christmas", 0.9),
    "2025-01-26": ("Republic Day", 0.75),
    "2025-03-14": ("Holi", 0.65),
    "2025-04-18": ("Good Friday", 0.7),
    "2025-08-15": ("Independence Day", 0.8),
    "2025-08-27": ("Ganesh Chaturthi", 1.6),
}

# ── Hourly distribution profile (peak hours Mumbai commute) ─────────────────
HOURLY_WEIGHTS = {
    0: 0.02, 1: 0.01, 2: 0.01, 3: 0.01, 4: 0.02, 5: 0.04,
    6: 0.06, 7: 0.09, 8: 0.11, 9: 0.10, 10: 0.06, 11: 0.04,
    12: 0.04, 13: 0.05, 14: 0.04, 15: 0.04, 16: 0.05,
    17: 0.08, 18: 0.10, 19: 0.09, 20: 0.07, 21: 0.05,
    22: 0.04, 23: 0.02
}

# ── Station importance scores ────────────────────────────────────────────────
STATION_IMPORTANCE = {}
per_station_daily = {lid: DAILY_RIDERSHIP[lid] / STATION_COUNTS[lid]
                     for lid in DAILY_RIDERSHIP}

for sid, name, lid, color, interchange in STATIONS:
    base = per_station_daily[lid]
    # Interchange stations get 1.5–2.5x boost
    mult = np.random.uniform(1.5, 2.5) if interchange else np.random.uniform(0.6, 1.2)
    # Special stations
    specials = {
        "Andheri": 2.8, "Ghatkopar": 2.5, "BKC": 2.2,
        "Dadar": 2.6, "Churchgate": 2.0, "CSMT": 2.3,
        "Airport T2": 1.9, "Airport T1": 1.8, "Chembur": 1.6,
        "Dharavi": 1.5, "Borivali West": 1.7,
    }
    for key, factor in specials.items():
        if key.lower() in name.lower():
            mult = factor
            break
    STATION_IMPORTANCE[sid] = min(base * mult, DAILY_RIDERSHIP[lid] * 0.4)


def get_weather_conditions(date: datetime):
    """Simulate Mumbai weather based on month."""
    month = date.month
    if month in [6, 7, 8, 9]:   # Monsoon
        cond = np.random.choice(["Heavy Rain", "Moderate Rain", "Light Rain"],
                                p=[0.35, 0.45, 0.2])
        temp = np.random.uniform(24, 30)
        rain_effect = {"Heavy Rain": 1.25, "Moderate Rain": 1.12, "Light Rain": 1.05}[cond]
    elif month in [12, 1, 2]:   # Winter/pleasant
        cond = np.random.choice(["Clear", "Partly Cloudy"], p=[0.7, 0.3])
        temp = np.random.uniform(18, 28)
        rain_effect = 1.0
    elif month in [3, 4, 5]:    # Summer / hot
        cond = np.random.choice(["Clear", "Hazy", "Partly Cloudy"], p=[0.5, 0.3, 0.2])
        temp = np.random.uniform(30, 40)
        rain_effect = 1.0
    else:                        # Oct–Nov transition
        cond = np.random.choice(["Clear", "Partly Cloudy", "Light Rain"], p=[0.5, 0.35, 0.15])
        temp = np.random.uniform(25, 33)
        rain_effect = 1.03 if "Rain" in cond else 1.0
    return cond, round(temp, 1), rain_effect


def assign_crowd_level(ridership: float, capacity: float) -> str:
    """Classify crowd level based on load factor."""
    load = ridership / capacity
    if load < 0.45:
        return "LOW"
    elif load < 0.80:
        return "MEDIUM"
    else:
        return "HIGH"


def generate_dataset(
    start_date: str = "2024-01-01",
    end_date: str   = "2025-03-25",
    output_path: str = "data/mumbai_metro_ridership.csv"
) -> pd.DataFrame:
    """Generate the full synthetic dataset."""

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end   = datetime.strptime(end_date,   "%Y-%m-%d")
    days  = (end - start).days

    print(f"🚇 Generating dataset: {days} days × {len(STATIONS)} stations × 24 hours")
    print(f"   Expected rows: {days * len(STATIONS) * 24:,}")

    records = []
    prev_ridership = {}   # (station_id, day_offset, hour) → ridership

    for day_offset in range(days):
        date = start + timedelta(days=day_offset)
        date_str = date.strftime("%Y-%m-%d")
        dow = date.weekday()       # 0=Mon ... 6=Sun
        is_weekend = 1 if dow >= 5 else 0

        # Festival / holiday lookup
        fest_info = MUMBAI_FESTIVALS.get(date_str, None)
        is_holiday = 1 if fest_info else 0
        festival_name = fest_info[0] if fest_info else "None"
        festival_factor = fest_info[1] if fest_info else 1.0

        # Weekend ridership dampening
        weekend_factor = 0.68 if is_weekend else 1.0

        weather, temp, rain_factor = get_weather_conditions(date)

        for sid, name, lid, color, interchange in STATIONS:
            capacity = LINE_CAPACITY[lid]
            base_daily = STATION_IMPORTANCE[sid]

            for hour in range(24):
                ts = date + timedelta(hours=hour)
                hourly_frac = HOURLY_WEIGHTS[hour]

                # Base ridership for this hour
                base = base_daily * hourly_frac * weekend_factor * festival_factor * rain_factor

                # Add Gaussian noise
                noise = np.random.normal(1.0, 0.08)
                ridership = max(0, base * noise)

                # Entries/exits split (30–70 morning, 70–30 evening, balanced midday)
                if 6 <= hour <= 11:
                    entry_frac = np.random.uniform(0.55, 0.75)
                elif 16 <= hour <= 21:
                    entry_frac = np.random.uniform(0.25, 0.45)
                else:
                    entry_frac = np.random.uniform(0.45, 0.55)

                entries = int(ridership * entry_frac)
                exits   = int(ridership * (1 - entry_frac))

                # Previous hour ridership
                prev_hour_key = (sid, day_offset, hour - 1)
                prev_hour_rid = prev_ridership.get(prev_hour_key, ridership * 0.9)

                # Previous day same hour
                prev_day_key = (sid, day_offset - 1, hour)
                prev_day_rid = prev_ridership.get(prev_day_key, ridership * 0.95)

                prev_ridership[(sid, day_offset, hour)] = ridership

                # Derived features
                peak_hour = 1 if (7 <= hour <= 10 or 17 <= hour <= 21) else 0
                station_importance_score = round(
                    STATION_IMPORTANCE[sid] / max(STATION_IMPORTANCE.values()), 4)
                holiday_effect = festival_factor
                ridership_growth = round(
                    (ridership - prev_hour_rid) / max(prev_hour_rid, 1) * 100, 2)

                crowd_level = assign_crowd_level(ridership, capacity * hourly_frac * 60 / 5)

                records.append({
                    "timestamp":                    ts.strftime("%Y-%m-%d %H:%M:%S"),
                    "station_id":                   sid,
                    "station_name":                 name,
                    "line_id":                      lid,
                    "line_color":                   color,
                    "month_of_year":               ts.month,
                    "day_of_month":                ts.day,
                    "hour_of_day":                  hour,
                    "day_of_week":                  dow,
                    "is_weekend":                   is_weekend,
                    "is_holiday":                   is_holiday,
                    "festival_flag":                is_holiday,
                    "festival_name":                festival_name,
                    "weather_condition":            weather,
                    "temperature":                  temp,
                    "rain_factor":                  round(rain_factor, 3),
                    "passenger_entries":            entries,
                    "passenger_exits":              exits,
                    "total_ridership":              int(ridership),
                    "previous_hour_ridership":      int(prev_hour_rid),
                    "previous_day_same_hour_ridership": int(prev_day_rid),
                    "station_type":                 "interchange" if interchange else "regular",
                    "interchange_flag":             interchange,
                    "peak_hour_flag":               peak_hour,
                    "station_importance_score":     station_importance_score,
                    "holiday_effect_factor":        round(holiday_effect, 3),
                    "ridership_growth_rate":        ridership_growth,
                    "crowd_level":                  crowd_level,
                })

    df = pd.DataFrame(records)

    # Rolling averages (3-hour and 6-hour)
    df = df.sort_values(["station_id", "timestamp"]).reset_index(drop=True)
    df["rolling_avg_3h"] = (
        df.groupby("station_id")["total_ridership"]
          .transform(lambda x: x.rolling(3, min_periods=1).mean())
          .round(1)
    )
    df["rolling_avg_6h"] = (
        df.groupby("station_id")["total_ridership"]
          .transform(lambda x: x.rolling(6, min_periods=1).mean())
          .round(1)
    )

    df.to_csv(output_path, index=False)
    print(f"\n✅ Dataset saved: {output_path}")
    print(f"   Rows: {len(df):,} | Columns: {len(df.columns)}")
    print(f"\n📊 Crowd level distribution:")
    dist = df["crowd_level"].value_counts()
    for lvl, cnt in dist.items():
        print(f"   {lvl}: {cnt:,} ({cnt/len(df)*100:.1f}%)")
    return df


if __name__ == "__main__":
    df = generate_dataset()
    print(df.head())
