# Dokumentation <TEAMNAME>

**Mitglieder:**
- Annika Hoffmanns
- Christian Löhner
- Tobias Leuthel

## Woche 1 (28.10- 03.11.2024)

### Aktivitäten:
- Zusammenbauen des Kettenradsatzes, Austesten an 9V Batterieblock

### Probleme und Lösungen:
- ChatGPT ist nicht hilfreich. Konkretere prompts sind nötig.

### Code:
- Siehe git history.

### Quellen:



## Woche 2 ( 04. - 10.11.2024)

### Aktivitäten:
- Informationen über ESP Now gesammelt
- Mac Adressen ausgelesen
-   1: MAC-Adresse des ESP32: 88:13:bf:6f:c1:9c
-   2: MAC-Adresse des ESP32: ac:15:18:e9:8c:7c
-   3:

### Code zum Auslesen der MAC Adresse 
import network

# WLAN-Station (Client) Schnittstelle initialisieren
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# MAC-Adresse abrufen
mac_address = wlan.config('mac')
mac_address_str = ':'.join(['{:02x}'.format(b) for b in mac_address])

# MAC-Adresse ausgeben
print("MAC-Adresse des ESP32:", mac_address_str)


### Quellen:
 - https://wolles-elektronikkiste.de/esp-now    ( Auslesen der Mac-Adresse) 
