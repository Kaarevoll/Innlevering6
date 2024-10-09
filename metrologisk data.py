
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Jeg laster inn temperatur- og trykkdata fra to filer. Jeg sørger for at jeg spesifiserer riktig
# filbaner der datafilene mine er lagret.
try:
    df_temp_met = pd.read_csv("temperatur_trykk_met_samme_rune_time_datasett.csv.txt", sep=";", skipinitialspace=True)
    df_trykk_temp = pd.read_csv("trykk_og_temperaturlogg_rune_time.csv.txt", sep=";", skipinitialspace=True)
except FileNotFoundError as e:
    # Hvis filene ikke finnes, gir jeg en feilmelding.
    print(f"Error: {e}")
    exit()

# Jeg konverterer tidskolonnene til datetime-format for å kunne jobbe med tid i plotting.
df_temp_met['Tid(norsk normaltid)'] = pd.to_datetime(df_temp_met['Tid(norsk normaltid)'], format='%d.%m.%Y %H:%M', errors='coerce')
df_trykk_temp['Dato og tid'] = pd.to_datetime(df_trykk_temp['Dato og tid'], format='%d.%m.%Y %H:%M', errors='coerce')

# Deretter konverterer jeg temperatur- og trykkverdiene til numerisk format, slik at jeg kan bruke
# dem i beregninger og plotting. Jeg erstatter komma med punktum for å sikre korrekt tallformat.
df_temp_met['Lufttemperatur'] = pd.to_numeric(df_temp_met['Lufttemperatur'].str.replace(',', '.'), errors='coerce')
df_temp_met['Lufttrykk i havnivå'] = pd.to_numeric(df_temp_met['Lufttrykk i havnivå'].str.replace(',', '.'), errors='coerce')

df_trykk_temp['Temperatur (gr Celsius)'] = pd.to_numeric(df_trykk_temp['Temperatur (gr Celsius)'].str.replace(',', '.'), errors='coerce')
df_trykk_temp['Trykk - barometer (bar)'] = pd.to_numeric(df_trykk_temp['Trykk - barometer (bar)'].str.replace(',', '.'), errors='coerce')

# Nå vil jeg filtrere data for perioden mellom 11. juni 2021 kl. 17:31 og 12. juni 2021 kl. 03:05
# for å finne temperaturfallet om natten.
start_time = datetime(2021, 6, 11, 17, 31)
end_time = datetime(2021, 6, 12, 3, 5)

# Jeg sjekker om det finnes data for det valgte tidsrommet og printer det ut for inspeksjon.
temp_night_data = df_trykk_temp[(df_trykk_temp['Dato og tid'] >= start_time) & (df_trykk_temp['Dato og tid'] <= end_time)]
if temp_night_data.empty:
    # Hvis det ikke er noe data for denne perioden, gir jeg beskjed.
    print(f"Ingen temperaturdata funnet for tidsrommet {start_time} til {end_time}")
else:
    print("Filtrert temperaturdata (11. - 12. juni):")
    print(temp_night_data)

# Jeg begynner med å plotte temperatur- og trykkdata. Jeg lager en figur med to underplott
# slik at jeg kan vise temperatur over tid i det første og trykk i det andre.
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

# Første subplot: Temperatur over tid
ax1.plot(df_trykk_temp['Dato og tid'], df_trykk_temp['Temperatur (gr Celsius)'], label='Temperatur (gr Celsius)', color='blue')
ax1.plot(df_temp_met['Tid(norsk normaltid)'], df_temp_met['Lufttemperatur'], label='Lufttemperatur (Met)', color='green')

# Jeg legger til en tittel og akselabel for temperaturplottet.
ax1.set_title('Temperatur over tid')
ax1.set_ylabel('Temperatur (°C)')
ax1.legend()

# Jeg lager en funksjon som beregner glidende gjennomsnitt over en gitt periode (n=30).
# Denne funksjonen sørger for at vi får en jevnere kurve ved å ta snittet av n verdier før og etter hver tidsverdi.
def moving_average(times, temps, n=30):
    if len(temps) < n:
        # Hvis datasettet er for lite til å beregne glidende gjennomsnitt, gir jeg beskjed.
        print(f"Datasettet er for lite til å beregne glidende gjennomsnitt med vindusstørrelse {n}.")
        return [], []
    avg_times = []
    avg_temps = []
    for i in range(n, len(temps) - n):
        if not pd.isna(times[i]):  # Jeg sjekker om tidspunktene er gyldige
            avg_times.append(times[i])  # Jeg beholder datetime-formatet
            avg_temps.append(sum(temps[i - n:i + n + 1]) / (2 * n + 1))
    return avg_times, avg_temps

# Jeg bruker funksjonen til å beregne glidende gjennomsnitt for temperaturdataene.
times = df_trykk_temp['Dato og tid'].tolist()
temps = df_trykk_temp['Temperatur (gr Celsius)'].tolist()
avg_times, avg_temps = moving_average(times, temps)

# Hvis det er nok data til å beregne glidende gjennomsnitt, plotter jeg det.
if avg_times and avg_temps:
    ax1.plot(avg_times, avg_temps, label='Glidende gjennomsnitt (n=30)', color='orange')

# Jeg plotter også temperaturfallet fra 11. til 12. juni, hvis det finnes data.
if not temp_night_data.empty:
    ax1.plot(temp_night_data['Dato og tid'], temp_night_data['Temperatur (gr Celsius)'], label='Temperaturfall 11-12 Juni', color='purple')

# Andre subplot: Trykk over tid
ax2.plot(df_trykk_temp['Dato og tid'], df_trykk_temp['Trykk - barometer (bar)'], label='Barometertrykk (bar)', color='green')
ax2.plot(df_temp_met['Tid(norsk normaltid)'], df_temp_met['Lufttrykk i havnivå'], label='Lufttrykk i havnivå', color='blue')

# Jeg legger til tittel, akselabel og en legende for trykkplottet.
ax2.set_title('Trykk over tid')
ax2.set_xlabel('Tidspunkt')
ax2.set_ylabel('Trykk (hPa)')
ax2.legend()

# Til slutt justerer jeg layoutet for bedre synlighet og viser plottet.
plt.tight_layout()
plt.show()

