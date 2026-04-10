import pandas as pd
import json
import math

COUNTRY_COORDS = {
    "AFG": [33.94, 67.71], "AGO": [-11.20, 17.87], "ALB": [41.15, 20.17],
    "ARE": [23.42, 53.85], "ARG": [-38.42, -63.62], "ARM": [40.07, 45.04],
    "AUS": [-25.27, 133.78], "AUT": [47.52, 14.55], "AZE": [40.14, 47.58],
    "BDI": [-3.37, 29.92], "BEL": [50.50, 4.47], "BEN": [9.31, 2.32],
    "BFA": [12.24, -1.56], "BGD": [23.68, 90.36], "BGR": [42.73, 25.49],
    "BHR": [26.07, 50.56], "BHS": [25.03, -77.40], "BIH": [43.92, 17.68],
    "BLR": [53.71, 27.95], "BLZ": [17.19, -88.50], "BOL": [-16.29, -63.59],
    "BRA": [-14.24, -51.93], "BRN": [4.54, 114.73], "BTN": [27.51, 90.43],
    "BWA": [-22.33, 24.68], "CAF": [6.61, 20.94], "CAN": [56.13, -106.35],
    "CHE": [46.82, 8.23], "CHL": [-35.68, -71.54], "CHN": [35.86, 104.20],
    "CIV": [7.54, -5.55], "CMR": [7.37, 12.35], "COD": [-4.04, 21.76],
    "COG": [-0.23, 15.83], "COL": [4.57, -74.30], "CRI": [9.75, -83.75],
    "CYP": [35.13, 33.43], "CZE": [49.82, 15.47], "DEU": [51.17, 10.45],
    "DJI": [11.83, 42.59], "DNK": [56.26, 9.50], "DOM": [18.74, -70.16],
    "DZA": [28.03, 1.66], "ECU": [-1.83, -78.18], "EGY": [26.82, 30.80],
    "ERI": [15.18, 39.78], "ESP": [40.46, -3.75], "EST": [58.60, 25.01],
    "ETH": [9.15, 40.49], "FIN": [61.92, 25.75], "FJI": [-17.71, 178.07],
    "FRA": [46.23, 2.21], "GAB": [-0.80, 11.61], "GBR": [55.38, -3.44],
    "GEO": [42.32, 43.36], "GHA": [7.95, -1.02], "GIN": [9.95, -9.70],
    "GMB": [13.44, -15.31], "GNB": [11.80, -15.18], "GNQ": [1.65, 10.27],
    "GRC": [39.07, 21.82], "GTM": [15.78, -90.23], "GUY": [4.86, -58.93],
    "HKG": [22.40, 114.11], "HND": [15.20, -86.24], "HRV": [45.10, 15.20],
    "HTI": [18.97, -72.29], "HUN": [47.16, 19.50], "IDN": [-0.79, 113.92],
    "IND": [20.59, 78.96], "IRL": [53.14, -7.69], "IRN": [32.43, 53.69],
    "IRQ": [33.22, 43.68], "ISL": [64.96, -19.02], "ISR": [31.05, 34.85],
    "ITA": [41.87, 12.57], "JAM": [18.11, -77.30], "JOR": [30.59, 36.24],
    "JPN": [36.20, 138.25], "KAZ": [48.02, 66.92], "KEN": [-0.02, 37.91],
    "KGZ": [41.20, 74.77], "KHM": [12.57, 104.99], "KOR": [35.91, 127.77],
    "KWT": [29.31, 47.48], "LAO": [19.86, 102.50], "LBN": [33.85, 35.86],
    "LBR": [6.43, -9.43], "LBY": [26.34, 17.23], "LKA": [7.87, 80.77],
    "LSO": [-29.61, 28.23], "LTU": [55.17, 23.88], "LUX": [49.82, 6.13],
    "LVA": [56.88, 24.60], "MAR": [31.79, -7.09], "MDA": [47.41, 28.37],
    "MDG": [-18.77, 46.87], "MEX": [23.63, -102.55], "MKD": [41.51, 21.75],
    "MLI": [17.57, -4.00], "MMR": [21.91, 95.96], "MNE": [42.71, 19.37],
    "MNG": [46.86, 103.85], "MOZ": [-18.67, 35.53], "MRT": [21.01, -10.94],
    "MUS": [-20.35, 57.55], "MWI": [-13.25, 34.30], "MYS": [4.21, 101.98],
    "NAM": [-22.96, 18.49], "NER": [17.61, 8.08], "NGA": [9.08, 8.68],
    "NIC": [12.87, -85.21], "NLD": [52.13, 5.29], "NOR": [60.47, 8.47],
    "NPL": [28.39, 84.12], "NZL": [-40.90, 174.89], "OMN": [21.51, 55.92],
    "PAK": [30.38, 69.35], "PAN": [8.54, -80.78], "PER": [-9.19, -75.02],
    "PHL": [12.88, 121.77], "PNG": [-6.31, 143.96], "POL": [51.92, 19.15],
    "PRT": [39.40, -8.22], "PRY": [-23.44, -58.44], "QAT": [25.35, 51.18],
    "ROU": [45.94, 24.97], "RUS": [61.52, 105.32], "RWA": [-1.94, 29.87],
    "SAU": [23.89, 45.08], "SDN": [12.86, 30.22], "SEN": [14.50, -14.45],
    "SGP": [1.35, 103.82], "SLE": [8.46, -11.78], "SLV": [13.79, -88.90],
    "SRB": [44.02, 21.01], "SSD": [6.88, 31.31], "SVK": [48.67, 19.70],
    "SVN": [46.15, 14.99], "SWE": [60.13, 18.64], "SWZ": [-26.52, 31.47],
    "SYR": [34.80, 38.99], "TCD": [15.45, 18.73], "TGO": [8.62, 1.21],
    "THA": [15.87, 100.99], "TJK": [38.86, 71.28], "TKM": [38.97, 59.56],
    "TTO": [10.69, -61.22], "TUN": [33.89, 9.54], "TUR": [38.96, 35.24],
    "TZA": [-6.37, 34.89], "UGA": [1.37, 32.29], "UKR": [48.38, 31.17],
    "URY": [-32.52, -55.77], "USA": [37.09, -95.71], "UZB": [41.38, 64.59],
    "VEN": [6.42, -66.59], "VNM": [14.06, 108.28], "YEM": [15.55, 48.52],
    "ZAF": [-30.56, 22.94], "ZMB": [-13.13, 27.85], "ZWE": [-19.02, 29.15],
    "TWN": [23.70, 120.96], "PSE": [31.95, 35.23], "XKX": [42.60, 20.90],
}

WB_REGIONS = {
    "EAP": ["AUS","BRN","CHN","FJI","HKG","IDN","JPN","KHM","KOR","LAO","MMR","MNG","MYS","NZL","PHL","PNG","SGP","THA","TWN","VNM"],
    "ECA": ["ALB","ARM","AUT","AZE","BEL","BGR","BIH","BLR","CHE","CYP","CZE","DEU","DNK","ESP","EST","FIN","FRA","GBR","GEO","GRC","HRV","HUN","IRL","ISL","ISR","ITA","KAZ","KGZ","LTU","LUX","LVA","MDA","MKD","MNE","NLD","NOR","POL","PRT","ROU","RUS","SRB","SVK","SVN","SWE","TJK","TKM","TUR","UKR","UZB"],
    "LAC": ["ARG","BHS","BLZ","BOL","BRA","CHL","COL","CRI","DOM","ECU","GTM","GUY","HND","HTI","JAM","MEX","NIC","PAN","PER","PRY","SLV","TTO","URY","VEN"],
    "MNA": ["ARE","BHR","DJI","DZA","EGY","IRN","IRQ","JOR","KWT","LBN","LBY","MAR","OMN","PSE","QAT","SAU","SYR","TUN","YEM"],
    "SAS": ["AFG","BGD","BTN","IND","LKA","NPL","PAK"],
    "SSA": ["AGO","BDI","BEN","BFA","BWA","CAF","CIV","CMR","COD","COG","DJI","ERI","ETH","GAB","GHA","GIN","GMB","GNB","GNQ","KEN","LBR","LSO","MDG","MLI","MOZ","MRT","MUS","MWI","NAM","NER","NGA","RWA","SDN","SEN","SLE","SSD","SWZ","TCD","TGO","TZA","UGA","ZAF","ZMB","ZWE"],
    "NAC": ["CAN","USA"],
}

REGION_NAMES = {
    "EAP": "East Asia & Pacific",
    "ECA": "Europe & Central Asia",
    "LAC": "Latin America & Caribbean",
    "MNA": "Middle East & North Africa",
    "SAS": "South Asia",
    "SSA": "Sub-Saharan Africa",
    "NAC": "North America",
}

CODE_TO_REGION = {}
for reg, codes in WB_REGIONS.items():
    for c in codes:
        CODE_TO_REGION[c] = reg

def load_latest(path, year_pref=None):
    df = pd.read_parquet(path)
    df["val"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")
    df = df.dropna(subset=["val"])
    codes = set(COUNTRY_COORDS.keys())
    df = df[df["REF_AREA"].isin(codes)]
    if year_pref:
        df = df[df["TIME_PERIOD"] == year_pref]
    if df.empty:
        return df
    latest = df.sort_values("TIME_PERIOD").groupby("REF_AREA").last().reset_index()
    return latest[["REF_AREA", "val", "TIME_PERIOD"]]

BASE = "data/raw"

hdi = load_latest(f"{BASE}/development/human_development_index_(hdi)_[highest_=_1].parquet")
hdi = hdi.rename(columns={"val": "hdi", "TIME_PERIOD": "hdi_year"})

exports = load_latest(f"{BASE}/trade/exports_value.parquet")
exports = exports.rename(columns={"val": "exports_usd_k", "TIME_PERIOD": "exports_year"})

merch = load_latest(f"{BASE}/trade/merchandise_trade_(%_gdp).parquet")
merch = merch.rename(columns={"val": "trade_pct_gdp", "TIME_PERIOD": "trade_year"})

fdi_in = load_latest(f"{BASE}/fdi/foreign_direct_investment,_net_inflows_(%_gdp).parquet")
fdi_in = fdi_in.rename(columns={"val": "fdi_inflows_pct_gdp", "TIME_PERIOD": "fdi_year"})

fdi_usd = load_latest(f"{BASE}/fdi/foreign_direct_investment,_net_inflows_(bop,_current_us$).parquet")
fdi_usd = fdi_usd.rename(columns={"val": "fdi_inflows_usd", "TIME_PERIOD": "fdi_usd_year"})

wealth = pd.read_parquet(f"{BASE}/wealth/national_comprehensive_wealth.parquet")
wealth["val"] = pd.to_numeric(wealth["OBS_VALUE"], errors="coerce")
wealth = wealth[(wealth["COMP_BREAKDOWN_1"] == "WB_CWON_PC") & wealth["val"].notna()]
wealth = wealth[wealth["REF_AREA"].isin(set(COUNTRY_COORDS.keys()))]
wealth = wealth.sort_values("TIME_PERIOD").groupby("REF_AREA").last().reset_index()
wealth = wealth[["REF_AREA", "val", "TIME_PERIOD"]].rename(
    columns={"val": "wealth_pc", "TIME_PERIOD": "wealth_year"}
)

merged = hdi[["REF_AREA", "hdi"]].merge(
    exports[["REF_AREA", "exports_usd_k"]], on="REF_AREA", how="outer"
).merge(
    merch[["REF_AREA", "trade_pct_gdp"]], on="REF_AREA", how="outer"
).merge(
    fdi_in[["REF_AREA", "fdi_inflows_pct_gdp"]], on="REF_AREA", how="outer"
).merge(
    fdi_usd[["REF_AREA", "fdi_inflows_usd"]], on="REF_AREA", how="outer"
).merge(
    wealth[["REF_AREA", "wealth_pc"]], on="REF_AREA", how="outer"
)

merged = merged[merged["REF_AREA"].isin(COUNTRY_COORDS)]
merged["lat"] = merged["REF_AREA"].map(lambda c: COUNTRY_COORDS[c][0])
merged["lon"] = merged["REF_AREA"].map(lambda c: COUNTRY_COORDS[c][1])
merged["region"] = merged["REF_AREA"].map(lambda c: CODE_TO_REGION.get(c, "Other"))
merged["region_name"] = merged["region"].map(lambda r: REGION_NAMES.get(r, "Other"))

nodes = []
for _, row in merged.iterrows():
    node = {
        "id": row["REF_AREA"],
        "lat": row["lat"],
        "lon": row["lon"],
        "region": row["region"],
        "region_name": row["region_name"],
    }
    for col in ["hdi", "exports_usd_k", "trade_pct_gdp", "fdi_inflows_pct_gdp", "fdi_inflows_usd", "wealth_pc"]:
        v = row[col]
        node[col] = round(float(v), 4) if pd.notna(v) and not math.isinf(float(v)) else None
    nodes.append(node)

# Build connections for the connection map:
# Connect top 20 exporters to each other (top trade backbone)
valid_exporters = [n for n in nodes if n["exports_usd_k"] is not None]
valid_exporters.sort(key=lambda x: x["exports_usd_k"], reverse=True)
top_hubs = valid_exporters[:15]
hub_ids = {h["id"] for h in top_hubs}

connections = []
seen = set()
for i, h1 in enumerate(top_hubs):
    for h2 in top_hubs[i+1:]:
        if h1["region"] != h2["region"]:
            key = tuple(sorted([h1["id"], h2["id"]]))
            if key not in seen:
                seen.add(key)
                connections.append({
                    "source": h1["id"],
                    "target": h2["id"],
                    "value": min(h1["exports_usd_k"], h2["exports_usd_k"]),
                    "type": "hub-hub"
                })

# Connect top 3 exporters per region to nearest hub in another region
for reg, countries in WB_REGIONS.items():
    reg_nodes = [n for n in valid_exporters if n["id"] in set(countries) and n["id"] not in hub_ids]
    reg_nodes.sort(key=lambda x: x["exports_usd_k"], reverse=True)
    for n in reg_nodes[:5]:
        nearest_hub = min(
            [h for h in top_hubs if h["region"] != n["region"]],
            key=lambda h: (h["lat"] - n["lat"])**2 + (h["lon"] - n["lon"])**2
        )
        key = tuple(sorted([n["id"], nearest_hub["id"]]))
        if key not in seen:
            seen.add(key)
            connections.append({
                "source": n["id"],
                "target": nearest_hub["id"],
                "value": n["exports_usd_k"],
                "type": "spoke"
            })

# Build links for the network graph:
# Connect countries within same region that both have trade data
network_links = []
region_groups = {}
for n in nodes:
    if n["trade_pct_gdp"] is not None and n["hdi"] is not None:
        region_groups.setdefault(n["region"], []).append(n)

for reg, members in region_groups.items():
    members.sort(key=lambda x: x["exports_usd_k"] or 0, reverse=True)
    top_in_region = members[:3]
    for m in members:
        nearest = min(top_in_region, key=lambda t: abs((t["trade_pct_gdp"] or 0) - (m["trade_pct_gdp"] or 0)) if t["id"] != m["id"] else float("inf"))
        if nearest["id"] != m["id"]:
            key = tuple(sorted([m["id"], nearest["id"]]))
            network_links.append({
                "source": m["id"],
                "target": nearest["id"],
                "region": reg,
            })

# Inter-region links: top exporter per region connects to top exporters of other regions
top_per_region = {}
for reg, members in region_groups.items():
    if members:
        top_per_region[reg] = members[0]

regions_list = list(top_per_region.keys())
for i, r1 in enumerate(regions_list):
    for r2 in regions_list[i+1:]:
        network_links.append({
            "source": top_per_region[r1]["id"],
            "target": top_per_region[r2]["id"],
            "region": "inter",
        })

# Deduplicate network links
seen_net = set()
unique_net_links = []
for link in network_links:
    key = tuple(sorted([link["source"], link["target"]]))
    if key not in seen_net:
        seen_net.add(key)
        unique_net_links.append(link)

output = {
    "nodes": nodes,
    "connections": connections,
    "network_links": unique_net_links,
    "regions": {k: v for k, v in REGION_NAMES.items()},
}

with open("viz/data.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Nodes: {len(nodes)}")
print(f"Connection map arcs: {len(connections)}")
print(f"Network graph links: {len(unique_net_links)}")
print("Data written to viz/data.json")
