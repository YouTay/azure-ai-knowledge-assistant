# Tradeoffs + Cost Heuristics (Spartan)

Ziel:
Der Advisor muss Entscheidungen als Tradeoffs formulieren.
Keine "beste Lösung" ohne Kontext.

---

Core Tradeoffs (immer erwähnbar)

Managed vs Control
- Managed Services: weniger Ops, schneller, aber weniger low-level Kontrolle.
- Self-managed (z.B. AKS/VM): mehr Kontrolle, aber hoher Ops- und Security-Aufwand.

Speed vs Governance
- Schnell starten: minimaler Prozess, höheres Risiko.
- Enterprise Governance: langsamer, dafür stabil + auditierbar.

Cost vs Reliability
- Multi-region + redundancy erhöhen Verfügbarkeit, aber Kosten + Komplexität steigen.
- Single region ist ok, wenn RTO/RPO und Business-Risk es erlauben.

Simplicity vs Microservices
- Monolith/Modular Monolith oft sinnvoll als Start.
- Microservices nur bei Team-/Domänen-Komplexität.

---

Cost Drivers (keine exakten Zahlen)

Compute
- Always-on Kapazität (AKS Nodes, Premium Plans) ist teuer.
- Autoscaling reduziert Kosten, aber braucht saubere Signals.

Data
- Cosmos: RU/s + falsches Partitioning = teuer.
- SQL: höhere Tiers + IO/DTU/vCore treiben Kosten.
- Storage: günstig, aber egress + hot tier kann überraschen.

Networking
- Egress (aus Region/Zone) kann dominant werden.
- WAF/Front Door/App Gateway sind zusätzliche Fixkosten.

Observability
- Log Volume + Retention in Log Analytics sind häufige Kostentreiber.

---

Cost Levers (pragmatisch)
- Right-sizing + autoscaling
- Logs reduzieren (Sampling, Retention, getrennte Workspaces)
- Caching (z.B. Redis) zur Entlastung von DB/Compute
- Private networking nur dort, wo es Security wirklich braucht