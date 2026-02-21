# Network + Security Baseline (Enterprise)

Ziel:
Der Advisor muss bei jeder Architektur Network und Security explizit adressieren.
Default: Zero-Trust-orientiert. Private-by-default für sensitive Daten.

---

Identity (immer zuerst)
Default:
- Entra ID als Identity Plane
- Managed Identity für Azure-to-Azure
- RBAC least privilege (Scope so klein wie möglich)

Red Flags:
- Secrets in App Config statt Key Vault
- Contributor auf Subscription für Apps/Teams
- Shared Accounts / fehlende Separation von Duties

---

Ingress / Edge
Optionen (abhängig von global vs regional):
- Regional: Application Gateway (mit WAF) als L7 Ingress
- Global: Front Door für global entry + failover + WAF

Red Flags:
- Public endpoints ohne WAF bei Internet Exposure
- Kein Rate limiting / kein Bot protection bei public APIs

---

Network Isolation
Default für sensible Daten:
- VNet Integration für Compute (wo möglich)
- Private Endpoints für Data Services
- DNS sauber planen (Private DNS Zones)

Tradeoff:
- Private Networking erhöht Komplexität + Kosten
- Dafür deutlich besserer Security Posture

Red Flags:
- Datenservices nur über Public Endpoint erreichbar
- Unklare DNS/Name Resolution bei Private Endpoints

---

Secrets / Keys
Default:
- Key Vault für Secrets/Keys/Certs
- Zugriff via Managed Identity
- Rotation/Expiry Policies definieren

Red Flags:
- Long-lived secrets ohne Rotation
- Zugangsschlüssel in CI/CD oder Code

---

Governance Guardrails (Minimum)
- Azure Policy: block public access (wo nötig), enforce tags, allowed locations/SKUs
- Resource hierarchy: Management Groups -> Subscriptions -> RG
- Naming + tagging standardisieren

---

Security Monitoring
Minimum:
- Defender for Cloud aktivieren (Posture + Recommendations)
- Logs zentral (Log Analytics)
- Alerts für auth failures, WAF events, resource changes