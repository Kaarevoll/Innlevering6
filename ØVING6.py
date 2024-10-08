import pandas as pd

path_to_file = "temperatur_trykk_met_samme_rune_time_datasett.csv.txt"
temperatur = pd.read_csv(path_to_file)
path_to_file = "trykk_og_temperaturlogg_rune_time.csv.txt"
trykk = pd.read_csv(path_to_file)




#""""""""""""""""


import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the temperature and pressure datasets (adjust the file paths as necessary)
df_temp_met = pd.read_csv("temperatur_trykk_met_samme_rune_time_datasett.csv.txt", sep=";", skipinitialspace=True)
df_trykk_temp = pd.read_csv("trykk_og_temperaturlogg_rune_time.csv.txt", sep=";", skipinitialspace=True)

# Convert the time columns to datetime format
df_temp_met['Tid(norsk normaltid)'] = pd.to_datetime(df_temp_met['Tid(norsk normaltid)'], format='%d.%m.%Y %H:%M', errors='coerce')
df_trykk_temp['Dato og tid'] = pd.to_datetime(df_trykk_temp['Dato og tid'], format='%d.%m.%Y %H:%M', errors='coerce')

# Convert temperatures and pressures to numeric
df_temp_met['Lufttemperatur'] = pd.to_numeric(df_temp_met['Lufttemperatur'].str.replace(',', '.'), errors='coerce')
df_temp_met['Lufttrykk i havnivå'] = pd.to_numeric(df_temp_met['Lufttrykk i havnivå'].str.replace(',', '.'), errors='coerce')

df_trykk_temp['Temperatur (gr Celsius)'] = pd.to_numeric(df_trykk_temp['Temperatur (gr Celsius)'].str.replace(',', '.'), errors='coerce')
df_trykk_temp['Trykk - barometer (bar)'] = pd.to_numeric(df_trykk_temp['Trykk - barometer (bar)'].str.replace(',', '.'), errors='coerce')

# Plotting the temperature and pressure data
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

# First subplot: Temperature over time
ax1.plot(df_trykk_temp['Dato og tid'], df_trykk_temp['Temperatur (gr Celsius)'], label='Temperatur (gr Celsius)', color='blue')
ax1.plot(df_temp_met['Tid(norsk normaltid)'], df_temp_met['Lufttemperatur'], label='Lufttemperatur (Met)', color='green')

ax1.set_title('Temperatur over tid')
ax1.set_ylabel('Temperatur (°C)')
ax1.legend()

# Updated moving average function with proper datetime handling
def moving_average(times, temps, n=30):
    avg_times = []
    avg_temps = []
    for i in range(n, len(temps) - n):
        if not pd.isna(times[i]):  # Ensure times are valid
            avg_times.append(times[i])  # Keep the datetime format
            avg_temps.append(sum(temps[i - n:i + n + 1]) / (2 * n + 1))
    return avg_times, avg_temps

# Apply moving average for the temperature file
times = df_trykk_temp['Dato og tid'].tolist()
temps = df_trykk_temp['Temperatur (gr Celsius)'].tolist()
avg_times, avg_temps = moving_average(times, temps)

# Plot the moving average
ax1.plot(avg_times, avg_temps, label='Glidende gjennomsnitt (n=30)', color='orange')

# Plot temperature drop from June 11, 2021 to June 12, 2021
start_time = datetime(2021, 6, 11, 17, 31)
end_time = datetime(2021, 6, 12, 3, 5)

temp_night_data = df_trykk_temp[(df_trykk_temp['Dato og tid'] >= start_time) & (df_trykk_temp['Dato og tid'] <= end_time)]
ax1.plot(temp_night_data['Dato og tid'], temp_night_data['Temperatur (gr Celsius)'], label='Temperaturfall 11-12 Juni', color='purple')

# Second subplot: Pressure over time
ax2.plot(df_trykk_temp['Dato og tid'], df_trykk_temp['Trykk - barometer (bar)'], label='Barometertrykk (bar)', color='green')
ax2.plot(df_temp_met['Tid(norsk normaltid)'], df_temp_met['Lufttrykk i havnivå'], label='Lufttrykk i havnivå', color='blue')

ax2.set_title('Trykk over tid')
ax2.set_xlabel('Tidspunkt')
ax2.set_ylabel('Trykk (hPa)')
ax2.legend()

# Adjust layout for better visibility
plt.tight_layout()

# Show the plot
plt.show()
