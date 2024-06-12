import folium
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

# Définir les coordonnées intermédiaires pour les deux tubes du tunnel
tube_montant_lat = [49.439966, 49.442181, 49.444812, 49.449039, 49.449677, 49.450406]
tube_montant_lon = [1.132131, 1.134705, 1.138290, 1.144256, 1.144901, 1.145384]

tube_descendant_lat = [49.450426, 49.449262, 49.443497, 49.442241, 49.440935, 49.440111] 
tube_descendant_lon = [1.144979, 1.143984, 1.135721, 1.134128, 1.132908, 1.131983]

# Interpoler les points pour avoir 1000 points pour chaque tube
num_points = 1000

def interpolate_points(lats, lons, num_points):
    distance = np.linspace(0, 1, len(lats))
    interp_lat = interp1d(distance, lats, kind='cubic')
    interp_lon = interp1d(distance, lons, kind='cubic')
    interpolated_distance = np.linspace(0, 1, num_points)
    return interp_lat(interpolated_distance), interp_lon(interpolated_distance)

latitudes_1, longitudes_1 = interpolate_points(tube_montant_lat, tube_montant_lon, num_points)
latitudes_2, longitudes_2 = interpolate_points(tube_descendant_lat, tube_descendant_lon, num_points)
mesures_1 = np.random.uniform(4.0, 6.0, num_points)
mesures_2 = np.random.uniform(4.0, 6.0, num_points)

# Combiner les données des deux tubes
latitudes = np.concatenate((latitudes_1, latitudes_2))
longitudes = np.concatenate((longitudes_1, longitudes_2))
mesures = np.concatenate((mesures_1, mesures_2))

# Créer un DataFrame
df = pd.DataFrame({
    'latitude': latitudes,
    'longitude': longitudes,
    'mesure': mesures
})

# Sauvegarder le DataFrame en fichier CSV
df.to_csv('lcms_data.csv', index=False)

print("Fichier 'lcms_data.csv' généré avec succès.")

# Charger les données LCMS
data = pd.read_csv('lcms_data.csv')

# Créer une carte centrée sur Rouen
m = folium.Map(location=[49.445, 1.138], zoom_start=14)

# Ajouter les points de mesure à la carte
for i, row in data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=3,
        tooltip=f'Mesure: {row["mesure"]}',
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

# Sauvegarder la carte dans un fichier HTML
m.save('lcms_map.html')

# Ouvrir la carte dans le navigateur par défaut
import webbrowser
webbrowser.open('lcms_map.html')
