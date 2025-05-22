### 📘 **1. Businesskontext**

Immer mehr Cafés bieten **Kaffee-Flatrates** an – Kunden zahlen monatlich einen Betrag und erhalten täglich eine Tasse Kaffee. „CoffeeClub“ ist ein webbasiertes Verwaltungssystem, das es **Cafés** ermöglicht, Abos und Kunden digital zu verwalten, und Kunden erlaubt, ihren Verbrauch zu sehen, Abos zu pausieren oder zu kündigen.

## Beschreibung

Ein webbasiertes Verwaltungssystem, das die Verwaltung von Kaffeeabos ermöglicht.
Abos werden über Admins eingepflegt und umfasst eine Flatrate für Kaffees, z.B. ein Kaffee täglich.
Kunden bekommen Zugangsdaten und können so ihren Konsum und Zahlungsinformationen und -status einsehen.
Ein Service bei dem sich Kaffees registrieren können und customized Abos anbieten. Kaffees fallen verschiede

* 3 - 4 API Punkte

Aufgaben des BackEnds:

* Anlagen neuer Kunden und Aboverwaltung
* Kunden können Statistiken abrufen, Abolaufzeit etc. nach Anmeldung
* 5 ct sparen bei Voranmeldung
* Auswertung für Café -> Reports wie viele Abos gibt es und wie viele werden wirklich genutzt
* QR-Code (Sicherheit)
* Tracken ob Kaffee eingelöst würde

Authentifizierung muss nicht implementiert aber beschrieben sein.

### Funktionen für Hauptadmins (Caféverwalter\:innen):

* Kaffee registrieren mit Code der per Post versendet wurde
* Abos verwalten

  * Abotemplates

    * small: 3 normale Kaffees pro Woche (7€/Woche)
    * small+: 3 besondere Kaffees pro Woche (12€/Woche)
    * medium: 5 normale Kaffees pro Woche (11€/pro Woche)
    * medium +: 5 besondere Kaffees pro Woche (19€/pro Woche)
    * large: 7 normale Kaffees pro Woche (15€/Woche)
    * large+: 7 besondere Kaffees pro Woche (22€/Woche)
* Reports/Backgroundtasks:

  * wöchentlich Auswertung mit neu abgeschlossenen Abos, genutzten Kaffee und Bestandskunden
  * monatliche Reports mit Einnahmen und Ausgaben

### Funktionen für Admins (Cafémitarbeiter\:innen):

* Log-In
* neue Abos erstellen (Kundenanmeldung geht nur über Cafémitarbeiter)
* Kundenkarte scannen und freien Kaffee eintragen, dass dieser abgeholt wurde

### Funktionen für Aboinhaber\:innen:

* Übersicht über Abo
* Statistik wann wieviel Kaffee getrunken wurde
* Erinnerungen, dass noch Kaffee abgeholt werden kann
* Zahlungsstatus
* Online-Karte mit wechselndem QR-Code
