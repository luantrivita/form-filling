# Deferred Work After Benchmark

This file is intentionally planning-only. There is no fine-tuning or distillation implementation in the current repository phase.

After the six DEV runs and the locked TEST evaluation, create an ADR deciding:
1. selected teacher/reference backbone;
2. selected B1/B2/P1 architecture;
3. whether errors are model-capability limited or data/schema/retrieval limited;
4. whether sufficient high-quality Vietnamese data exists to justify SFT;
5. whether distillation to a smaller student should proceed.

Only after that ADR may implementation folders/configs for SFT/distillation be added.
