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
 - Mac Adressen ausgelesen (Annika) 
-   1: MAC-Adresse des ESP32: 88:13:bf:6f:c1:9c   (controller - sender) 
-   2: MAC-Adresse des ESP32: ac:15:18:e9:8c:7c
-   3: MAC-Adresse des ESP32: 88:13:bf:6f:b9:bc   (Auto - Empfänger) 

 - ESP 32 Treiber heruntergeladen und geflasht ( Tobi) 
 - Funktion für die Vorwärtsfahrt erstellt ( Christian) 


### Quellen:
 - https://wolles-elektronikkiste.de/esp-now    ( Auslesen der Mac-Adresse) 




## Woche 3 ( 11. - 17.11.2024)

### Aktivitäten:
- Informationen über ESP Now gesammelt (Tobi)
 -Chat GPT über biderektionale Verbindung zweier ESP's gefragt:
 - Probleme: esp.init() wird nicht gefunden
             OSError wird gemeldet: OSError: (-12389, 'ESP_ERR_ESPNOW_NOT_INIT')
             bisher noch keine Lösung gefunden

- Code für Fahrfunktionen schreiben (Chris)
 -Joysticks auf den ESP Auto montiert (Annika)
 -Fahrbetrieb getestet (Annika, Chris)
 -Verdrahtung Auto (Annika)
 
-Über Schaltplanzeichnen informiert (Chris)


### Quellen:
 - https://chatgpt.com/g/g-cKXjWStaE-python/c/6719f789-da14-800c-9771-9de5a383086b ; Link Chatgpt
 - https://docs.micropython.org/en/latest/library/espnow.html
