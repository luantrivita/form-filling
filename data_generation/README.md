# ESF_DATA_GEN_HANDOFF_V1

Mục tiêu: contract để Data Team xây synthetic clinical conversation pipeline theo **fact-first generation**.

## Flow
`canonical registry → gold fact graph → generation controls → conversation → evidence alignment → validation`.

## Không được làm
- Generate conversation trước rồi dùng LLM tạo gold.
- Tự tạo diagnosis/treatment/exam findings ngoài gold.
- Đồng nhất `NOT_MENTIONED` với negative.
- Scale trước khi 3–5 handshake samples và pilot 100–200 pass quality gate.

## Handoff sequence
1. Parse schemas.
2. Validate `examples/example_case_001.json`.
3. Trả 3–5 samples theo cùng contract.
4. Fix errors.
5. Generate pilot.

Schemas dùng JSON Schema Draft 2020-12.
