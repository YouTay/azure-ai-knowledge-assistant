# Data Service Decision Guide (Azure)

Ziel:
Datenplattform begründet auswählen.
Immer Konsistenz, Skalierung, Kosten und Operations bedenken.

---

Azure SQL Database

Use when:
- Relationale Daten
- OLTP Workloads
- Starke Konsistenz nötig

Strength:
- ACID garantiert
- Enterprise Features
- Bekanntes SQL Modell

Risks:
- Vertical Scaling Limits
- Sharding Strategie nötig bei Wachstum

---

Azure Cosmos DB

Use when:
- Global Distribution
- Niedrige Latenz weltweit
- Flexible Schema Anforderungen

Strength:
- Multi-region native
- Massive Skalierung
- Flexible Datenmodelle

Risks:
- Partitioning kritisch
- RU/s Kostenmodell komplex
- Fehlkonfiguration teuer

---

Azure Storage (Blob/Data Lake)

Use when:
- Unstrukturierte Daten
- Logs, Files, Media
- Analytics Rohdaten

Strength:
- Sehr günstig skalierbar
- Hohe Haltbarkeit

Risks:
- Keine Query Engine ohne Zusatzservices
- Lifecycle Management wichtig

---

Azure Database for PostgreSQL / MySQL

Use when:
- Open-source Stack
- Relationale Workloads
- Cloud-managed Betrieb gewünscht

Strength:
- Kompatibel mit bestehenden Apps
- Managed Service

Risks:
- Skalierungsstrategie planen
- HA-Konfiguration beachten

---

Data Warehouse / Analytics Stack

Use when:
- BI / Reporting / Analytics
- Große Datenmengen
- Historisierung

Typical Services:
- Synapse Analytics
- Fabric / Lakehouse Patterns

Risks:
- Kosten können stark wachsen
- Governance zwingend notwendig