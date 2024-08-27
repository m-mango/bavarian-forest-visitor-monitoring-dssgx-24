# feature_selection.py

FEATURES_CONFIG = {
    "overall_park_model": {
        "target": {
            "relative_traffic": "occupancy_norm",
            "absolute_traffic": "occupancy_abs"
        },
        "input": {
            "num_features": ['Temperature (°C)','Relative Humidity (%)','Precipitation (mm)',
                             'Wind Speed (km/h)','Sunshine Duration (min)','Tag','Monat','Jahr',
                             'Niederschlagsmenge','Schneehoehe','GS mit','GS max',],
            "cat_features": ['Wochentag', 'Jahreszeit'],
            "binary_features": ['Wochenende','Laubfärbung','Schulferien_Bayern','Schulferien_CZ','Feiertag_Bayern',
                                'Feiertag_CZ','HEH_geoeffnet','HZW_geoeffnet','WGM_geoeffnet','Lusenschutzhaus_geoeffnet',
                                'Racheldiensthuette_geoeffnet','Falkensteinschutzhaus_geoeffnet','Schwellhaeusl_geoeffnet']
        }
    },
    "individual_sensor_model": {
        "sensors": {
            "Bayerisch Eisenstein": ['Bayerisch Eisenstein IN', 'Bayerisch Eisenstein OUT'],
            "Brechhäuslau": ['Brechhäuslau IN', 'Brechhäuslau OUT'],
            "Bučina": ['Bucina MERGED IN', 'Bucina MERGED OUT'],
            "Deffernik": ['Deffernik IN', 'Deffernik OUT'],
            "Diensthüttenstraße": ['Diensthüttenstraße IN', 'Diensthüttenstraße OUT'],
            "Felswandergebiet": ['Felswandergebiet IN', 'Felswandergebiet OUT'],
            "Ferdinandsthal": ['Ferdinandsthal IN', 'Ferdinandsthal OUT'],
            "Fredenbrücke": ['Fredenbrücke IN', 'Fredenbrücke OUT'],
            "Gfäll": ['Gfäll IN', 'Gfäll OUT'],
            "Gsenget": ['Gsenget IN', 'Gsenget OUT'],
            "Klingenbrunner Wald": ['Klingenbrunner Wald IN', 'Klingenbrunner Wald OUT'],
            "Klosterfilz": ['Klosterfilz IN', 'Klosterfilz OUT'],
            "Racheldiensthütte": ['Racheldiensthütte IN', 'Racheldiensthütte OUT'],
            "Sagwassersäge": ['Sagwassersäge IN','Sagwassersäge OUT'],
            "Scheuereck": ['Scheuereck IN', 'Scheuereck OUT'],
            "Schillerstraße": ['Schillerstraße IN', 'Schillerstraße OUT'],
            "Schwarzbachbrücke": ['Schwarzbachbrücke IN', 'Schwarzbachbrücke OUT'],
            "TFG Falkenstein 1": ['Falkenstein 1 MERGED IN', 'Falkenstein 1 MERGED OUT'],
            "TFG Falkenstein 2": ['Falkenstein 2 IN', 'Falkenstein 2 OUT'],
            "TFG Lusen 1": ['Lusen 1 MERGED IN', 'Lusen 1 MERGED OUT'],
            "TFG Lusen 2": ['Lusen 2 IN', 'Lusen 2 OUT'],
            "TFG Lusen 3": ['Lusen 3 IN', 'Lusen 3 OUT'],
            "Trinkwassertalsperre": ['Trinkwassertalsperre MERGED IN', 'Trinkwassertalsperre MERGED OUT'],
            "Waldhausreibe": ['Waldhausreibe IN', 'Waldhausreibe OUT'],
            "Waldspielgelände": ['Waldspielgelände IN', 'Waldspielgelände OUT'],
            "Wistlberg": ['Wistlberg IN', 'Wistlberg OUT'],
            
        },
        # Common features across all sensors
        "input": {
            "num_features": ['Temperature (°C)','Relative Humidity (%)','Precipitation (mm)',
                             'Wind Speed (km/h)','Sunshine Duration (min)','Tag','Monat','Jahr',
                             'Niederschlagsmenge','Schneehoehe','GS mit','GS max',],
            "cat_features": ['Wochentag', 'Jahreszeit'],
            "binary_features": ['Wochenende','Laubfärbung','Schulferien_Bayern','Schulferien_CZ','Feiertag_Bayern',
                                'Feiertag_CZ','HEH_geoeffnet','HZW_geoeffnet','WGM_geoeffnet','Lusenschutzhaus_geoeffnet',
                                'Racheldiensthuette_geoeffnet','Falkensteinschutzhaus_geoeffnet','Schwellhaeusl_geoeffnet']
        }
    }
}

