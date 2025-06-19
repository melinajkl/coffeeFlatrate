# Kaffeabonnementsystem "CoffeeClub"
## Businesskontext

Das Projekt zielt darauf ab, ein Backend-System für ein abonnementbasiertes Kaffeemodell zu entwickeln. 
Hiermit richtet es sich an Cafés, die ihren Kund:innen die Möglichkeit bieten möchten, Vorteile zu erlangen bei regelmäßigem Besuch des Cafés. 
Dabei können die Abomodelle jeweils vom Verwalter eines Kaffees angepasst werden.
So kann eine langfristige Kundenbindung anvisiert werden und bieten sowohl Konsumenten als auch Cafés weitere Vorteile. 
Wichtig ist, dass die jeweiligen Systeme einfach zu verwalten und auf kleine Cafés zugeschnitten werden können.
Hierbei hat jedes Café sein eigenes System, sodass Probleme, die an einem Container, falschen Konfigurationen oder andere, die nur einzelne Kunden betreffen nicht alle Nutzer betreffen. So wird die Zuverlässigkeit erhöht.

## Beschreibung
Das Projekt wird mit einem FastAPI-Backend umgesetzt, die REST-Schnittstellen für mobile und webbasierte UIs bereitstellen. 
Die Datenpersistenz wird mit einer Datenbank (hier mit sqlite) gewährleistet.
Es gibt ein rollenbasiertes Zugriffssystem, welches im weiteren Verlauf weiter erklärt wird.

### Funktionen für Hauptadmins (Caféverwalter\:innen):

* Pro Kaffee gibt es wenige einen Hauptadmins, die das Angebot des Kaffees verwalten und 
* Abos verwalten
  * Abotemplates, die genutzt oder abgeändert werden können:
    * small: 3 normale Kaffees pro Woche (7€/Woche)
    * small+: 3 besondere Kaffees pro Woche (10€/Woche)
    * medium: 5 normale Kaffees pro Woche (11€/pro Woche)
    * medium+: 5 besondere Kaffees pro Woche (19€/pro Woche)
    * large: 7 normale Kaffees pro Woche (15€/Woche)
    * large+: 7 besondere Kaffees pro Woche (22€/Woche)
    * unlimited: 200 Filterkaffee pro Woche (30€/Woche)
    * unlimited+: 200 Kaffees pro Woche (40€/ Woche)
* Reports/Backgroundtasks:
  * wöchentlich Auswertung mit neu abgeschlossenen Abos, genutzten Kaffee und Bestandskunden
  * monatliche Reports mit Einnahmen und Ausgaben
* Verwaltung von Mitarbeitern

### Funktionen für Admins (Cafémitarbeiter\:innen):

* Log-In
* neue Abos erstellen (Kundenanmeldung geht nur über Cafémitarbeiter)
* Kundenkarte scannen und freien Kaffee eintragen, dass dieser abgeholt wurde

### Funktionen für Aboinhaber\:innen:

* Übersicht über Abo, man kann nur ein Abo haben -> E-Mail adresse muss unique sein
* Statistik wann wieviel Kaffee getrunken wurde
* Erinnerungen, dass noch Kaffee abgeholt werden kann
* Zahlungsstatus
* Online-Karte mit wechselndem QR-Code

## 5 Aspekte aus der Vorlesung 

### 1. **Authentifizierung, Autorisierung und Authentisierung**

Diese drei Begriffe werden oft verwechselt, sind aber grundlegend verschieden und spielen alle eine wichtige Rolle in der Sicherheit eines Systems.

* **Authentifizierung** (engl. *Authentication*):
  Dies ist der Prozess, bei dem geprüft wird, ob ein Nutzer tatsächlich derjenige ist, der er vorgibt zu sein. Beispielsweise durch Eingabe von Benutzername und Passwort oder Bestätigung einer E-Mail-Adresse. Im Kontext unseres Systems bedeutet das, dass nur legitime Nutzer Zugriff erhalten.
  Beispiel: Ein Kunde registriert sich mit seiner E-Mail-Adresse und erhält eine Bestätigungsmail. Erst nach Bestätigung ist der Account aktiv.

* **Autorisierung** (engl. *Authorization*):
  Nachdem ein Nutzer authentifiziert wurde, entscheidet die Autorisierung, was der Nutzer tun darf. Sie legt Rollen und Berechtigungen fest und sorgt dafür, dass Nutzer nur auf die Ressourcen zugreifen können, die ihnen erlaubt sind.
  Beispiel: Ein Hauptadmin darf Abo-Vorlagen anpassen, Mitarbeiter jedoch nicht. Ein Kunde kann nur sein eigenes Abo einsehen, aber keine anderen.

* **Authentisierung** (oft synonym mit *Login* oder *Anmeldung* verwendet):
  Dies bezeichnet den Vorgang, wie ein Nutzer seine Identität gegenüber dem System bestätigt, z.B. durch Einloggen mit Benutzerdaten. Beim Login wird oft ein Token (z.B. ein JSON Web Token, JWT) ausgestellt, der für die Dauer der Session den Zugang ermöglicht.

**Im Projekt:**

* Für die Hauptadmins, Kunden und Mitarbeiter wird ein sicheres Login-System implementiert, das Token-basierte Sessions verwaltet. Dies dient lediglich zur Authentifizierung.
* Die Sessions werden mit JWT realisiert, um Manipulationen zu verhindern.
* Rollenbasiertes Zugriffssystem sorgt dafür, dass z.B. Mitarbeiter keine Abos löschen oder Reports sehen können. Dafür wird für jeden 
* Es wird sichergestellt, dass mindestens ein Hauptadmin pro Café existiert, um eine permanente Verwaltung zu garantieren.

---

### 2. **Inputvalidierung**

Inputvalidierung bedeutet, alle Eingaben der Nutzer oder Clients systematisch auf Korrektheit und Vollständigkeit zu überprüfen.

* **Warum ist Inputvalidierung wichtig?**
  Um Datenbankkonsistenz zu bewahren, Fehler zu vermeiden und Sicherheitslücken (z.B. SQL-Injection, Cross-Site Scripting) zu verhindern.

* **Frontend und Backend Validierung:**
  Die erste Kontrollinstanz befindet sich im Frontend, welches nicht implementiert ist, um Nutzern direkt Feedback zu geben. Doch nur die Backendvalidierung ist sicher, da Nutzer das Frontend umgehen können (z.B. durch direkte API-Requests).

* **Beispiele im Projekt:**

  * E-Mail-Adressen müssen gültig formatiert.
  * Abo-Daten, Nutzer und Daten von Cafes müssen den vorgegebenen Mustern entsprechen. Es werden Pydantic-Schemata genutzt.
  * Bankdaten der Cafés wie IBAN und BIC werden mithilfe von Field Validators überprüft.
  * Bei Änderung von Abos wird geprüft, ob der Kunde bereits ein Abo besitzt.

---

### 3. **Containerisierung:**
Für eine verbesserte Portabilität, lässt sich das gesamte Projekt als 

---

### 4. **Wiederkehrende Aufgaben und Hintergrundprozesse**

Viele Systeme benötigen zeitgesteuerte Prozesse, die automatisch und regelmäßig laufen.

* **Beispiele für wiederkehrende Aufgaben:**

  * Erstellen von wöchentlichen und monatlichen Reports zu Abonnementzahlen, Nutzungsverhalten und Finanzen.
  * Versenden von Erinnerungs-E-Mails an Kunden, die noch Kaffee abholen können.
  * Überprüfung und Aktualisierung des Status von Abos (z.B. automatische Kündigung bei Ablauf).

* **Technische Umsetzung:**
  Diese Aufgaben werden häufig als Hintergrundjobs (Cron Jobs, Scheduled Tasks) implementiert, damit sie außerhalb der Benutzerinteraktion und ohne Zeitdruck ausgeführt werden.

* **Vorteile:**

  * Entlastung des Frontends und der Benutzer durch Automatisierung.
  * Konsistente, zeitnahe Auswertungen und Benachrichtigungen.
  * Bessere Skalierbarkeit und Wartbarkeit.

* **Im Projekt:**
  * Es wird nicht automatisch durchgeführt aber man kann sich Statistiken geben lassen und als Dummy implementiert. So lassen sich die Dokumente an einem zentralen Ort einsehen und werden nicht erst bei der Anfrage generiert.
  -> Würde man diese als wiederkehrende Aufgaben implementieren könnte man es genauso handhaben.
---

### 5. **Sessionhandling**

Sessionmanagement sorgt für eine sichere und nutzerfreundliche Verwaltung von Benutzerzuständen.

* **Tokenbasierte Sessions:**

  * Nach erfolgreichem Login erhält der Nutzer einen Token, der seine Identität bestätigt.
  * Der Token enthält Informationen über die Rolle und Berechtigungen.
  * Der Server prüft bei jeder Anfrage den Token auf Gültigkeit und Berechtigung. Dies ist nicht implementiert.

* **Sicherheitsaspekte:**

  * Um Missbrauch zu verhindern, ein Token verliert nach 20 min seine Gültigkeit. So kann verhindert werden, dass unauthorisierte Nutzer Tokens abfangen und zeitlich uneingeschränkt Zugriff auf das System haben können.
  * Tokens sind digital signiert, um Manipulation zu erkennen.
  * Bei Logout oder Inaktivität wird die Session invalidiert. (nicht implementiert, es wurde lediglich ein Login für Angestellte und Nutzer implementiert)
---

### 6. **Weitere relevante technische Aspekte**

* **ETL (Extract, Transform, Load):**
  ETL bezeichnet den Prozess, Daten aus unterschiedlichen Quellen zu extrahieren, zu transformieren (z.B. Format- oder Strukturänderung) und in ein Zielsystem zu laden.
  Im Projekt kann ETL z.B. relevant sein beim Import von Kundendaten aus anderen Systemen oder Backups.

* **Datenkonvertierung:**
  Da verschiedene Systeme unterschiedliche Datenformate verwenden (JSON, XML, CSV, SQL), ist die Konvertierung notwendig, um eine reibungslose Kommunikation zu gewährleisten.

* **Containerisierung:**
  Einsatz von Containern (z.B. Docker) ermöglicht es, die Backend-Anwendung konsistent und isoliert in verschiedenen Umgebungen (Entwicklung, Test, Produktion) zu betreiben.
  Dies erhöht die Portabilität, Skalierbarkeit und Wartbarkeit.

* **Verbindungstechnologien:**

  * REST API für die Kommunikation zwischen Frontend und Backend.
  * WebSocket-Verbindungen könnten für Echtzeitfeatures wie dynamische QR-Codes verwendet werden. (nicht implementiert)

* **Design Patterns und Architekturen:**

  * Eine Trennung der Verantwortlichkeiten durch eine Model-Controller-Service-Architecture.
  * Patterns wie Dependency Injection fördern lose Kopplung und Testbarkeit.