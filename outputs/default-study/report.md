# Furnace Report: default-study

## Summary

- Model: `toy_mlp`
- Dataset: `synthetic_classification`
- Recommended candidate: `baseline`
- Recommendation status: `recommended`

## Candidate Comparison

| candidate | method | accuracy | f1 | latency | memory | model_size | quality_loss | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | baseline | 0.67578125 | 0.6681939131719301 | 0.04693749906437006 | 0.00067901611328125 | 0.0028963088989257812 | 0.0 | recommended |
| dynamic_int8 | dynamic_quantization | 0.671875 | 0.6637842465753424 | 0.1771437482602778 | 0.0 | 0.0037965774536132812 | 0.00390625 | valid |

## Constraints

- Max quality loss: `0.05`
- Max latency ms: `1000.0`
- Max memory mb: `4096.0`
- Max model size mb: `512.0`