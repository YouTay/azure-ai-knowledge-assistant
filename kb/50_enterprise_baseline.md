# Enterprise Architecture Baseline (Azure)

Ziel:
Der Advisor muss Enterprise-Readiness bewerten.
Nicht nur Architektur vorschlagen — auch Betriebsfähigkeit.

---

Identity & Access
- Entra ID als zentrale Identity.
- Managed Identity bevorzugen.
- RBAC least privilege.
- Regelmäßige Access Reviews.

Red Flags:
- Shared Accounts.
- Subscription-level Contributor ohne Grund.
- Secrets außerhalb Key Vault.

---

Reliability & DR
Minimum:
- Backup Strategie definiert.
- Restore regelmäßig getestet.
- SLA Anforderungen klar (RTO/RPO).

Optional je nach Kritikalität:
- Zone Redundancy.
- Multi-region active/passive.

Red Flags:
- Kein Restore-Test.
- Monitoring fehlt.
- Single Region ohne Business-Risiko-Bewertung.

---

Observability
Minimum Stack:
- Azure Monitor.
- Log Analytics Workspace zentral.
- Application Insights für Apps.

Operational Essentials:
- Alerts definiert.
- Dashboards vorhanden.
- Incident Response klar.

Red Flags:
- Logs vorhanden, aber niemand schaut sie an.
- Keine Alert Ownership.

---

Governance
Baseline:
- Naming + Tagging Standard.
- Azure Policy Guardrails.
- Kostenbudgets definiert.
- Subscription Struktur sinnvoll.

Red Flags:
- Wildwuchs an Ressourcen.
- Keine Kostenkontrolle.

---

Cost Awareness
Enterprise Fokus:
- Hauptkostentreiber identifizieren.
- Budgets + Alerts definieren.
- Regelmäßige Cost Reviews.

Nicht Ziel:
- Exakte Preisberechnung durch Advisor.
- Fokus auf strukturelle Kostenentscheidungen.