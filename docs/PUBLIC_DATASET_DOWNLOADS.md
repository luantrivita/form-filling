# Public dataset files required for Step 2B

## SYNUR — required
Source repository: https://huggingface.co/datasets/microsoft/SYNUR

Download these files and upload them to ChatGPT (individual files or one ZIP):

1. `synur_schema.json`
2. `data/mediqa_synur_train-00000-of-00001.jsonl`
3. `data/mediqa_synur_dev-00000-of-00001.jsonl`
4. `data/mediqa_synur_test-00000-of-00001.jsonl`

Expected public sizes from the repository page: train ~344 kB, dev ~276 kB, test ~529 kB. The dataset card states 193 observation concepts and four value types: SINGLE_SELECT, MULTI_SELECT, STRING, NUMERIC.

## MTS-Dialog — required
Source repository: https://github.com/abachaa/MTS-Dialog

Simplest: download the repository as ZIP and upload the ZIP.
Alternatively upload the CSV files in `Main-Dataset/`:
- `MTS-Dialog-TrainingSet.csv`
- `MTS-Dialog-ValidationSet.csv`
- `MTS-Dialog-TestSet-1-MEDIQA-Chat-2023.csv`
- `MTS-Dialog-TestSet-2-MEDIQA-Sum-2023.csv`

## Why local files are needed
The source sites are publicly readable and their structure has been verified, but full binary/raw dataset transfer into the current execution sandbox is restricted. Local files are required to run the complete audit, split statistics, baseline inference and evaluation reproducibly.
