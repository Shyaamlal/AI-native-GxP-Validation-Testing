---
artifact_type: Risk_Assessment
feature: Logout
version: 1.0
status: Approved
ai_assistance:
  agent_skill: validation-risk-assessment
  model: claude-opus-4-7
  invocation_timestamp: 2026-05-18T13:50:00Z
  prompt_version: v1.0
human_review:
  reviewer: shyaamlal
  approval_timestamp: 2026-05-18T20:39:28Z
  comment: null
traceability:
  upstream:
    - Feature_Scoping_Logout.md
risk_classification:
  framework: GAMP 5 RBA
  category: GAMP Category 5 — High GxP impact (security control supporting 21 CFR Part 11 access requirements)
---

# Risk Assessment — Logout

## 1. Framework Applied

- **Framework:** GAMP 5 Risk-Based Approach.
- **Selection rationale:** Default selection per the framework skill — organisation-specific framework can be substituted in the prompt. Sambhava is a bespoke web application (Voice Intelligence platform), which the GAMP 5 decision tree classifies as a Category 5 custom application. Feature-level risk is assessed within that overall Category 5 system context.
- **CR-level inheritance:** Not applied. This feature is assessed standalone; no change-request-level classification has been carried in.

## 2. GxP Impact Assessment

- **Does the feature touch GxP records or processes?** Indirectly, yes. Logout itself neither creates, modifies, nor reads GxP records (it terminates a session). However, the feature is a primary access-control surface for the application: a logout failure or weakness directly enables unauthorised access to any GxP record the application stores or displays (per the Feature Scoping artifact §1 and §2.3, the application hosts voice-analysis records — patient/subject data, behavioural scores, reports — behind the same session boundary that logout closes).
- **What GxP requirements apply?**
  - **21 CFR Part 11 §11.10(d)** — *"Limiting system access to authorized individuals."* Logout is the mechanism by which a previously authorised individual relinquishes access; failure to fully terminate the session leaves an authenticated surface available to a subsequent unauthorised user of the same workstation/browser.
  - **21 CFR Part 11 §11.10(g)** — *"Use of authority checks to ensure that only authorized individuals can use the system."* Authority checks depend on the session-state contract that logout terminates.
  - **EU Annex 11 §12 (Security)** — physical and/or logical controls should restrict access to authorised personnel. Logout is a logical control.
  - **ALCOA+ Attributable** — actions performed in the application must be attributable to the correct authenticated user. A failed logout that leaves a session active under a previous user's identity creates a direct attribution failure (see §4).
- **Impact severity:** **High.** The feature is not GxP-record-producing, but its correct functioning is a precondition for the access-control posture that every GxP-record-producing feature in the application depends on.

## 3. Patient Safety Risk

- **Could a failure of this feature directly or indirectly affect patient safety?**
  - **Direct:** No. Logout has no direct effect on patient care, dosing, diagnostic output, or device function.
  - **Indirect:** Possibly, depending on how the platform's voice-analysis outputs are used in care. The Feature Scoping artifact (§2 and §3) describes a "Voice Intelligence" platform producing reports against subjects/users including behavioural-competency scoring. If those reports inform clinical, occupational-health, or fitness-for-role decisions about identifiable individuals, then an attribution failure caused by a faulty logout (one user's actions or reports recorded against another user's identity) could propagate into a clinical or quasi-clinical decision. The Feature Scoping artifact does not confirm clinical intent of use; raised in §7 as Open Question.
- **Severity if it failed:** **Low to Medium (conditional).** Low if the platform is used for non-clinical workforce assessment; Medium if reports inform clinical/health decisions about subjects. To be confirmed by the validation lead in light of the intended-use statement for the platform (not available from Phase 1 observation alone).

## 4. Data Integrity Risk

- **What data does the feature create, modify, or expose?** Logout does not itself create or modify domain records. It mutates session state. The data exposed *by virtue of an active session* (and therefore protected by correct logout) includes (from Feature Scoping §2.4 and §3): the analyses listing on `/voice/history` (subject names, gender, DOB, owner, date, status), report content (per the report routes referenced in the snapshot), and user/workspace administration surfaces visible in the sidebar (`/users`, `/usage`).

- **ALCOA+ exposure:**
  - **Attributable — HIGH risk.** This is the principal ALCOA+ concern for logout. If a session is not fully terminated and a different person uses the same browser, actions and records they create will be attributed to the originally authenticated user. This is the canonical attribution failure mode.
  - **Original / Accurate — Medium risk (downstream of Attributable).** Records created or edited under a misattributed session are still "original" and may be technically "accurate" as data, but the metadata identifying the responsible party is wrong, which under ALCOA+ is itself an integrity defect.
  - **Contemporaneous, Legible, Complete, Consistent, Enduring, Available — Not materially affected by logout in isolation.** Logout's effect on these attributes is indirect via Attributable.

- **Audit-trail considerations:**
  - Logout itself should generate an audit-trail event (who logged out, when, from where) per 21 CFR Part 11 §11.10(e) audit-trail requirements for security-relevant events. The Feature Scoping artifact records (Open Question Q7) that no end-user-visible audit signal was observed on logout; whether the server emits an audit-log entry is not determinable from end-user UI observation and remains an open verification item.
  - The cross-tab behaviour observed (Feature Scoping §2.4 — stale tab retains rendered protected content until next navigation) does not, in itself, allow new authenticated actions in the stale tab (the next protected request triggers a redirect to `/login`), but it does mean **viewing** of previously-fetched protected content continues post-logout for an undefined window. From an ALCOA+ standpoint this is a *disclosure* concern (access control), not a record-integrity concern, but it warrants test coverage.

## 5. Risk Classification

- **Resulting classification:** **GAMP Category 5 — High GxP impact (security control supporting 21 CFR Part 11 access requirements).** Within the GAMP 5 RBA model, the feature is a custom-developed access-control component of a Category 5 application. Its risk profile is dominated by indirect GxP impact (access control to GxP records) and a direct Attributable-axis data-integrity exposure if the feature malfunctions.
- **Rationale:** Logout does not produce GxP records, but it is a load-bearing security control: it is the user-initiated mechanism by which authenticated access to every GxP record the application holds is relinquished. A defect — for example, incomplete server-side session revocation, persistence of authenticated state in stale tabs, restoration of authenticated views via browser back/bfcache, or absence of an audit event on logout — has plausible regulatory exposure under 21 CFR Part 11 §11.10(d)(e)(g) and EU Annex 11 §12, and a credible ALCOA+ Attributable failure path. The patient-safety exposure is bounded by the platform's intended use, which is not yet confirmed (§3 and §7).
- **Mitigations:** Mitigations are addressed downstream — specific risks the OQ Protocol should target are listed in §6 and acceptance criteria will be authored in Phase 5 (FRS).

## 6. Downstream Implications

*Informs Validation Scope (Phase 3) and OQ Protocol (Phase 6).*

- **Testing depth implied:** Custom-application (Category 5) treatment — full lifecycle testing of the feature: functional behaviour, negative paths, security-adjacent behaviour (session termination semantics, cross-tab effects, history/back semantics), and audit-trail emission. This is heavier than the Category 4 *configuration-verification* level appropriate for non-custom features.
- **Required artifacts beyond standard chain:**
  - **Security review evidence** for the session-termination implementation. Recommended as an input to the OQ Protocol; the framework treats this as evidence to reference rather than to produce. Discuss with the validation lead whether existing org security review covers this surface.
  - **Penetration-test or session-management test evidence.** Same status as above — reference if available; do not produce within this chain.
  - **Audit-log inspection evidence** confirming that a logout event is recorded server-side with the expected ALCOA+-conformant fields. This is not directly observable from the end-user UI and will require coordination with whoever has audit-log access. Flagged for the Validation Scope phase.
- **Specific risks the OQ Protocol should target** (must not be overlooked by Phase 6):
  1. **Server-side session revocation.** Verify that a session token issued before logout is rejected by the server after logout, not merely cleared from the browser. Tied to Feature Scoping Open Question Q2.
  2. **Stale-tab disclosure window.** Verify the behaviour observed in Feature Scoping §2.4 — that a second tab continues to display previously fetched protected content after logout in another tab — and either confirm it is intended (lazy-redirect-on-next-navigation) or surface it as a defect. Tied to Feature Scoping Q4.
  3. **Back-button / bfcache behaviour.** Verify that no protected authenticated view is restored via browser back, forward, or bfcache after logout. Feature Scoping §2.5 records the observed behaviour as redirect-to-login; the OQ should make this an explicit pass criterion across representative protected routes.
  4. **Audit-trail emission on logout.** Verify that logout produces an attributable, contemporaneous audit event. Tied to Feature Scoping Q7.
  5. **In-flight request handling.** Verify behaviour when a long-running authenticated request is in flight at the moment of logout (does it complete under the old session, get rejected, or behave inconsistently?). Tied to Feature Scoping Q3.
  6. **Logout availability across all authenticated routes.** Spot-verify that the logout control is reachable and functional from every authenticated route, not only those exercised in scoping. Tied to Feature Scoping Q5.

## 7. Open Questions for the Human

*Risks that could not be classified confidently from the Feature Scoping artifact alone.*

1. **Intended use of the platform's outputs.** Are voice-analysis reports used to inform clinical, occupational-health, or fitness-for-role decisions about identifiable individuals (Medium patient-safety severity), or are they limited to non-clinical workforce/educational assessment (Low severity)? This determines whether the §3 indirect patient-safety pathway is in scope. The validation lead must confirm with the product owner / regulatory affairs.
2. **Regulatory framework declaration for the platform.** Has Sambhava been formally classified as a 21 CFR Part 11 system, an EU Annex 11 system, both, or neither, for the regulated activity this client is performing? The §2 obligations cited above presume Part 11 + Annex 11 apply. If the platform is operated outside these jurisdictions / regulated processes, the GxP impact framing changes.
3. **Existence and scope of prior security review.** Has the session-management implementation (including logout) already been subject to an org-level security review or penetration test? If so, that evidence is referenceable in Validation Scope; if not, the validation lead should consider whether to commission one before relying solely on OQ.
4. **Multi-role / multi-workspace logout variants.** The Feature Scoping artifact (Q6) records that only the Client role of one workspace was observed. If higher-privilege roles (admin, workspace owner) exist with different sidebars or logout placement, their risk profile may differ and should be assessed before Validation Scope closes.
5. **SSO / federated-identity integration.** Is the logout observed a local application logout only, or does it propagate to an upstream identity provider (SSO single-sign-out)? If SSO is in use, "logout" has a broader contract than the Feature Scoping artifact could observe end-to-end, and the risk surface extends to IdP behaviour.

## 8. Notes

- This assessment treats Sambhava as a GAMP 5 custom application based on the bespoke nature of the platform observable from the Feature Scoping artifact. If the platform is in fact a configured deployment of a third-party product (Category 4) or is GAMP-out-of-scope for this client, the validation lead must override this classification.
- The assessment is bounded by what Phase 1 observed. Implementation-level questions (server-side session revocation, audit emission, in-flight handling, SSO) are explicitly raised as Open Questions or as OQ-Protocol-targeted risks rather than assumed away.
- No mitigations are prescribed here. Mitigations live in the FRS acceptance criteria (Phase 5) and the OQ Protocol (Phase 6), per the framework's separation of concerns.
