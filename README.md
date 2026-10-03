# Firmware Malware Detector

Classical ML-based firmware scanner using Random Forest.

## Results

| Metric | Value |
|---|---|
| Model accuracy | 100% |
| Baseline accuracy | 50% |
| Improvement | +50% |

## Features

| Feature | Importance | Meaning |
|---|---|---|
| entropy | 0.380 | Packed/encrypted detection |
| opcode_freq | 0.324 | Byte diversity |
| file_size | 0.296 | Basic pattern |

## Why this approach

Three questions framework:
1. **Do we have labeled data?** Yes → supervised learning
2. **How much?** <1000 samples → classical ML (Random Forest)
3. **Explainable in 30 seconds?** Yes → feature importances

## Project structure

\`\`\`
firmware_detector/
├── data/
│   └── samples.csv
├── firmware/
│   ├── benign/
│   └── malicious/
├── extract_features.py
├── model.py
├── .gitignore
└── README.md
\`\`\`

## Usage

### 1. Install dependencies
\`\`\`bash
pip install pandas scikit-learn --break-system-packages
\`\`\`

### 2. Build dataset
\`\`\`bash
python3 extract_features.py
\`\`\`

### 3. Train + evaluate
\`\`\`bash
python3 model.py
\`\`\`

### 4. Predict on new file
\`\`\`bash
python3 model.py path/to/firmware.bin
\`\`\`

## Safety

Run only in isolated VM. Never execute unknown firmware.

## License

MIT
