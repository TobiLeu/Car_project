Bei diesem Repository handelt es sich um ein Projekt für ein ferngesteuertes Auto:

Ein Video des Fahrzeugs ist im Repository vorhanden.
Programmierung ist mit Micropython erfolgt.
Es wurde ein Bausatz eines Kettenlaufwerks verwendet. Stattdessen kann mit dem Code im Repository auch ein Fahrzeug verwendet werden, das über Einzelansteuerung des beiden Fahrzeugseiten lenkt.


Beschreibung:

Auto:
Es wurde ein Bausatz eines Kettenlaufwerks verwendet, im Internet unter den Namen T101 oder TP101 zu finden. Ein Datenblatt für den Bausatz ist nicht erhältlich.
Der verwendete Bausatz hat 2 12V DC Motoren. Diese werden über eine H-Brücke versorgt. Als Batterie wurden alte Lithium Akkus verwendet.
Die Karosserie wurde mit einem 3D-Drucker hergestellt, Modell im Repository.
Es wurde ein ESP32 verwendet. Dieser steuert das Auto und erhält die Steuersignale von einem zweiten ESP32 im Controller, das ESPNow Modul wurde für die Datenübertragung verwendet.
Die Beleuchtung des Autos erfolgt mit LED's, die über den Controller an bzw. ausschaltbar sind.

Controller:
Der Controller für die Fernsteuerung wurde selbst gebaut. Hierzu wurde eine Abzweigdose verwendet, in die ein ESP32 eingebaut wurde. Der ESP32 wird mit einer 5V-Powerbank versorgt.
Der Controller hat 2 Joysticks mit Tasterfunktion, die je eine Kette des Fahrzeugs steuern. Die Tasterfunktion eines Joysticks wird für die An-/Ausschaltung des Fahrzeuglichts verwendet.
Zusätzlich ist im Controller ein 5V LCD-Display verbaut worden, Datenblatt nicht vorhanden. Das Display die Geschwindigkeit jeder einzelnen Kette in Prozent an.
Ein Start des Controllers führt zum Reset des Microcontrollers des Autos.

