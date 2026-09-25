# ESF Pre-Visit Scope Matrix — v0.1

## Patient/caregiver reportable — IN SCOPE
- reason for visit / chief complaint
- current symptoms
- onset, duration, course, severity
- symptom location/character/frequency when reported
- associated symptoms
- prior care/treatment reported by patient
- past conditions and hospitalizations
- past surgery/procedures
- current medication as reported
- allergy history
- family history
- smoking/alcohol/occupational exposure
- specialty-specific history when explicitly collected

## HIS-provided — IN SCOPE AS OPTIONAL CONTEXT
- documented prior conditions/history
- medication/allergy history
- prior encounters when contractually available
- structured facts mapped through a vendor adapter

## NOT AUTO-FILLED FROM PATIENT CONVERSATION
- physical examination findings
- measured vital signs unless explicitly supplied as a trusted structured source
- laboratory/imaging results unless supplied as a trusted structured source
- clinician diagnosis
- treatment recommendation
- ICD coding

## State policy
- `NOT_MENTIONED` is not `NEGATIVE`.
- Historical is not current.
- Resolved is not the same as explicit negative.
- Conflict between HIS and conversation is preserved and flagged; it is not silently overwritten.
