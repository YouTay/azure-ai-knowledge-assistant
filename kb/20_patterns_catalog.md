# Architecture Pattern Catalog

Der Advisor muss zuerst ein Pattern wählen.
Kein Service-Mix ohne Pattern-Entscheidung.

---

Web Application (3-Tier)
Use when:
- Klassische Web-App oder API
- Klare Trennung: Frontend / Backend / Data
- Moderate Skalierung

Strength:
- Einfach verständlich
- Gut skalierbar
Risk:
- Zu früh zu komplexe Microservices bauen

---

Event-Driven Architecture
Use when:
- Entkoppelte Services
- Asynchrone Verarbeitung
- Burst Traffic

Strength:
- Hohe Resilienz
- Gute Skalierung
Risk:
- Debugging komplexer
- Observability zwingend notwendig

---

Microservices
Use when:
- Mehrere unabhängige Teams
- Komplexe Domäne
- Unterschiedliche Skalierungsprofile

Strength:
- Unabhängige Deployments
Risk:
- Hohe operative Komplexität
- Netzwerk + Security anspruchsvoller

---

Serverless
Use when:
- Unregelmäßiger Traffic
- Event-getrieben
- Minimale Ops gewünscht

Strength:
- Geringe Betriebskosten bei Low Load
Risk:
- Cold Starts
- Limits beachten

---

Data Platform
Use when:
- Hohe Datenmengen
- Analytics / BI / ML
- Datenintegration aus mehreren Quellen

Strength:
- Skalierbar
Risk:
- Governance + Kosten können explodieren

---

Hybrid
Use when:
- On-Prem Integration
- Legacy Systeme
- Regulatorische Anforderungen

Strength:
- Flexibilität
Risk:
- Netzwerk + Identity Komplexität