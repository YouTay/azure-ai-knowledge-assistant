# Intake Framework

Purpose:
Kein Architekturvorschlag ohne sauberes Workload-Profil.

Wenn Informationen fehlen:
Stelle 3–6 präzise Rückfragen aus dieser Liste.

---

Workload Type:
- API / Web App
- Event-driven
- Batch Processing
- Data Platform
- ML / AI
- Internal Tool
- SaaS (multi-tenant?)

Users & Traffic:
- Internal oder external?
- Erwartete gleichzeitige Nutzer?
- Steady oder burst traffic?
- Global oder regional?

Data:
- Structured / Unstructured / Streaming?
- Aktuelle Größe?
- Wachstum in 12 Monaten?
- Konsistenzanforderungen?
- Backup/Restore Anforderungen?

Security & Compliance:
- Sensible Daten?
- Public exposure erlaubt?
- GDPR / ISO / SOC2 / PCI / HIPAA?
- Network isolation erforderlich?

Reliability:
- RTO?
- RPO?
- Multi-region erforderlich?

Operations:
- Kubernetes Know-how vorhanden?
- IaC Reifegrad?
- DevOps Team Größe?

Cost Priority:
- Cost-first?
- Performance-first?
- Security-first?
- Schnelle Delivery wichtiger als Optimierung?