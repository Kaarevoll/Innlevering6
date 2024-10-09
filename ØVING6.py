import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Overordnet oppgavebeskrivelse: Lesing av to separate .csv-filer med værdata for temperaturanalyse.
# En fil fra UiS og en fil fra Sola værstasjon.

# Les inn data fra Sola værstasjon
df_sola = pd.read_csv("temperatur_trykk_met_samme_rune_time_datasett.csv.txt", sep=";", skipinitialspace=True)

# Konverterer tidspunktene i Sola data til datetime-format (DD.MM.YYYY HH:MM)
df_sola['Tid(norsk normaltid)'] = pd.to_datetime(df_sola['Tid(norsk normaltid)'], format='%d.%m.%Y %H:%M', errors='coerce')

# Konverterer temperatur til numerisk format
df_sola['Lufttemperatur'] = pd.to_numeric(df_sola['Lufttemperatur'].str.replace(',', '.'), errors='coerce')

# Les inn data fra lokal værstasjon (professor Rune Wiggo Time)
df_local = pd.read_csv("trykk_og_temperaturlogg_rune_time.csv.txt", sep=";", skipinitialspace=True)

# Konverterer tidspunktene i lokal data til datetime-format (MM.DD.YYYY HH:MM)
df_local['Dato og tid'] = pd.to_datetime(df_local['Dato og tid'], format='%m.%d.%Y %H:%M', errors='coerce')

# Fjerner ugyldige datoer
df_local = df_local.dropna(subset=['Dato og tid'])

# Legger til sekunder siden start for nøyaktig tidsberegning
df_local['Tid siden start (sek)'] = pd.to_numeric(df_local['Tid siden start (sek)'], errors='coerce')
df_local['Dato og tid'] = df_local['Dato og tid'] + pd.to_timedelta(df_local['Tid siden start (sek)'], unit='s')

# Konverterer temperatur til numerisk format
df_local['Temperatur (gr Celsius)'] = pd.to_numeric(df_local['Temperatur (gr Celsius)'].str.replace(',', '.'), errors='coerce')

# Plotter temperaturdata
plt.figure(figsize=(10, 6))

# Temperatur fra Sola
plt.plot(df_sola['Tid(norsk normaltid)'], df_sola['Lufttemperatur'], label='Sola Lufttemperatur', color='blue')

# Temperatur fra lokal værstasjon
plt.plot(df_local['Dato og tid'], df_local['Temperatur (gr Celsius)'], label='Lokal Lufttemperatur', color='orange')

# Legger til tittel, akseetiketter og legend
plt.title('Temperatur over tid')
plt.xlabel('Tidspunkt')
plt.ylabel('Temperatur (°C)')
plt.legend()

# Viser temperaturplottet
plt.tight_layout()
plt.show()


######### Vise trykk over tid

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Overordnet oppgavebeskrivelse: Lesing av to separate .csv-filer med værdata for trykkanalyse.
# En fil fra UiS og en fil fra Sola værstasjon.

# Les inn data fra Sola værstasjon
df_sola = pd.read_csv("temperatur_trykk_met_samme_rune_time_datasett.csv.txt", sep=";", skipinitialspace=True)

# Konverterer tidspunktene i Sola data til datetime-format (DD.MM.YYYY HH:MM)
df_sola['Tid(norsk normaltid)'] = pd.to_datetime(df_sola['Tid(norsk normaltid)'], format='%d.%m.%Y %H:%M', errors='coerce')

# Konverterer trykk til numerisk format
df_sola['Lufttrykk i havnivå'] = pd.to_numeric(df_sola['Lufttrykk i havnivå'].str.replace(',', '.'), errors='coerce')

# Les inn data fra lokal værstasjon (professor Rune Wiggo Time)
df_local = pd.read_csv("trykk_og_temperaturlogg_rune_time.csv.txt", sep=";", skipinitialspace=True)

# Konverterer tidspunktene i lokal data til datetime-format (MM.DD.YYYY HH:MM)
df_local['Dato og tid'] = pd.to_datetime(df_local['Dato og tid'], format='%m.%d.%Y %H:%M', errors='coerce')

# Fjerner ugyldige datoer
df_local = df_local.dropna(subset=['Dato og tid'])

# Legger til sekunder siden start for nøyaktig tidsberegning
df_local['Tid siden start (sek)'] = pd.to_numeric(df_local['Tid siden start (sek)'], errors='coerce')
df_local['Dato og tid'] = df_local['Dato og tid'] + pd.to_timedelta(df_local['Tid siden start (sek)'], unit='s')

# Konverterer trykk til numerisk format
df_local['Trykk - barometer (bar)'] = pd.to_numeric(df_local['Trykk - barometer (bar)'].str.replace(',', '.'), errors='coerce')

# Plotter trykkdata
plt.figure(figsize=(10, 6))

# Trykk fra Sola
plt.plot(df_sola['Tid(norsk normaltid)'], df_sola['Lufttrykk i havnivå'], label='Sola Lufttrykk', color='green')

# Trykk fra lokal værstasjon
plt.plot(df_local['Dato og tid'], df_local['Trykk - barometer (bar)'], label='Lokal Barometertrykk', color='purple')

# Legger til tittel, akseetiketter og legend
plt.title('Trykk over tid')
plt.xlabel('Tidspunkt')
plt.ylabel('Trykk (hPa)')
plt.legend()

# Viser trykkplottet
plt.tight_layout()
plt.show()
