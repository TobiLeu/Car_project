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



## Woche 4 ( 18. - 24.11.2024)

### Aktivitäten:
- Code für Controller geschrieben und angepasst (Tobi, Annika)
    -Umwandlung von Byte-Signal
    -Codevorlage von mycropython.org angepasst


- Code Fahrfunktion überarbeitet (Chris, Tobi):
    -lineare Transformation Probleme behoben
    -Umwandlung vom Sendersignal von 16 bit auf 10 bit von Chat GPT Funktion schreiben lassen

-Abzweigdose für Controller vorbereitet
- Code für Fahrfunktionen schreiben (Chris)
 -Fahrbetrieb getestet (Annika, Chris, Tobi)

 
### Quellen:
 - https://chatgpt.com/g/g-cKXjWStaE-python/c/6719f789-da14-800c-9771-9de5a383086b
 - https://docs.micropython.org/en/latest/library/espnow.html



## Woche 5 ( 25.11 - 01.12.2024)

### Aktivitäten:
- Controller
    - Öffnungen mit Dremel ausfräsen (Annika)
    - Displayhalterung gedruckt (Chris)
    - Controller bis auf Ein-/Ausschalter mechanisch fertiggestellt (Annika)


- Code Auto (Tobi)
    -Sendefunktion überarbeitet: 
        Problem, dass Steuerung nicht funktioniert, wenn der Controller nach dem Auto eingeschaltet wird
        Lösung: reboot Befehl an Auto ESP senden, wenn der Controller ESP eingeschaltet wird
    
- Code Controller (Annika)
    - Tasterbefehl einlesen und an Auto senden

- Spannungsversorgung Auto, mit Festspannungsregler; 2x 9V Blöcke in Reihe auf 12V regeln (Chris)
    - Die 9 V Blöcke, aufladbar per USB-C, haben eine Laderegelung, die abschaltet. -> 9V NiMh Akkus verwenden

- Schaltung für LED's Autobeleuchtung (Tobi)
    - LED's direkt über den ESP ansteuern: hat nicht funktioniert, vermutlich zu viel Strom -> extra Schaltung nötig


### Quellen:
 LED Flussspannungen: https://www.mikrocontroller.net/articles/LED#Flu%C3%9Fspannung



## Woche 6 ( 02.12 - 08.12.2024)

### Aktivitäten:

- Code Auto (Chris)
    - Pinout für Beleuchtung programmiert
    
- Controller (Annika)
    - Taster verdrahtet

- Spannungsversorgung (Chris, Annika):
    - Controller: Senden funktioniert nicht mit 3,3V -> 5V Powerbank verwenden
    - 24V Batterieblock demontiert und einzelne Zellen verwenden (14V)
    

- Schaltung für LED's Autobeleuchtung (Tobi)
    - Schaltung berechnet, verdrahtet und getestet

- Auto (Chris)
    - Bauteile auf Lochrasterplatine gelötet


### Quellen:
 LED Flussspannungen: https://www.mikrocontroller.net/articles/LED#Flu%C3%9Fspannung

 To Do:
 - Controller Spannungsversorgung verdrahten und testen
 - Konstruktion Wanne und Karosserie
 - LCD Display
 - Löten