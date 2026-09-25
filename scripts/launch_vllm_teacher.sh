#!/usr/bin/env bash
set -euo pipefail
MODEL_CONFIG=${1:?usage: launch_vllm_teacher.sh configs/models/<model>.json [port]}
PORT=${2:-8000}
MODEL=$(python - "$MODEL_CONFIG" <<'PY'
import json,sys
print(json.load(open(sys.argv[1]))['hf_model'])
PY
)
TP=$(python - "$MODEL_CONFIG" <<'PY'
import json,sys
print(json.load(open(sys.argv[1])).get('serving',{}).get('tensor_parallel_size',2))
PY
)
echo "Launching $MODEL on port $PORT with tensor parallel=$TP"
exec vllm serve "$MODEL" --host 0.0.0.0 --port "$PORT" --tensor-parallel-size "$TP" --dtype bfloat16
