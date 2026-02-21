# Compute Service Decision Guide (Azure)

Ziel:
Compute-Auswahl begründen.
Nicht nur Service nennen — Entscheidung erklären.

---

Azure Container Apps (ACA)

Use when:
- Containerisierte APIs / Backends
- Event-driven Workloads
- Moderate Komplexität
- Schnelle Delivery wichtiger als maximale Kontrolle

Strength:
- Serverless Containers
- Autoscaling inkl. KEDA
- Geringer Ops-Aufwand

Risks:
- Weniger Low-Level Control als AKS
- Networking-Szenarien begrenzt möglich

---

Azure Kubernetes Service (AKS)

Use when:
- Plattform-Team vorhanden
- Komplexe Microservices
- Custom Networking / Security nötig
- Multi-Tenant Plattform

Strength:
- Maximale Kontrolle
- Cloud-native Standard

Risks:
- Hoher Ops-Aufwand
- Monitoring/Governance Pflicht
- Overkill für kleine Workloads

---

Azure App Service

Use when:
- Klassische Web Apps / APIs
- Schneller Time-to-Market
- Standard Deployment Pattern

Strength:
- Stabil, mature Plattform
- Geringer Betriebsaufwand

Risks:
- Weniger flexibel für komplexe Container-Setups
- Networking Isolation abhängig vom Plan

---

Azure Functions

Use when:
- Event-driven Compute
- Spiky Workloads
- Glue-Code / Integration

Strength:
- Consumption-basierte Kosten
- Minimal Ops

Risks:
- Cold Starts
- Execution Limits
- Monitoring wichtig

---

VM-based Compute

Use when:
- Legacy Software
- Spezialsoftware
- Custom OS Anforderungen

Strength:
- Maximale Kontrolle

Risks:
- Höchster Betriebsaufwand
- Patch/Hardening Verantwortung