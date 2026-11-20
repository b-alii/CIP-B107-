# CIP-B107-LAB01: AI-Assisted IP Evidence Identification and Model Evaluation

**Case ID:** ICDFA-DFIR-AI-026
**Course:** CIP-B107, AI for Forensics and Capstone Intelligence (Mewar International University / ICDFA)
**Student:** `TODO: full name` | **Student ID:** `TODO` | **Date:** `TODO`

> Controlled educational exercise using **synthetic teaching data only**. Nothing in this package establishes that any address is malicious. "Positive" means the source annotation of an intended IP-evidence candidate, not proof of a routable, safe, public or malicious address.

---

## 1. Package contents

| Item | File | Description |
|---|---|---|
| 1 | `CIP-B107_Forensic_Report.pdf` | Signed forensic report (Phases A to F, memorandum, checklist, declaration) |
| 2 | `scripts/` or `notebooks/` | Reproducible Python scripts (listed in section 4) |
| 3 | `evidence_manifest.csv` | Chain of custody: filename, SHA-256, byte size, WAT timestamp, source, examiner |
| 4 | `results/candidate_review.csv` | Regex/IPv4 candidate review (source_row, context, candidate, regex_match, ipv4_valid, source_label, analyst_note) |
| 5 | `results/predictions.csv` | Actual vs predicted labels for all 46 test records (offline classifier) |
| 6 | `results/confusion_matrix.png` and charts | Confusion matrix and performance charts |
| 7 | `README.md` | This file |
| 8 | `CIP-B107_Executive_Briefing.pdf` | Two-page executive briefing |
| 9 | `screenshots/` | Timestamped screenshots of the examiner's own terminal outputs |

The submission ZIP must be named `CIP-B107-LAB01_<StudentID>_<Surname>.zip`.

**Excluded on purpose:** the virtual environment, any credentials or tokens, and datasets copied from unrelated sources. The historical upload, create-job and prediction scripts were **not executed** (obsolete API patterns, embedded credentials) and are not included.

## 2. Folder layout

```
CIP-B107-LAB01/
├── originals/     untouched supplied files (read-only evidence copies)
├── working/       intermediate files
├── scripts/       analysis scripts
├── results/       generated outputs (hashes, CSVs, predictions, charts)
├── screenshots/   terminal evidence
├── reports/       report and briefing
└── notebooks/     optional notebooks
```

Supplied files in `originals/`: `dataset_small.csv`, `dataset_train.jsonl`, `dataset_test.jsonl`, `result.csv`, `fine_tuning_steps.txt`.

## 3. Environment

- OS: Kali Linux
- Python: `TODO: output of python --version` (3.10+ recommended)
- Libraries: pandas, scikit-learn, matplotlib (jupyter optional)
- Hardware: no GPU and no paid API account required
- Random seed: `TODO: seed used, or "none: default deterministic solver"`

Set up and record versions:

```bash
cd ~/CIP-B107-LAB01
python3 -m venv venv
source venv/bin/activate
pip install pandas scikit-learn matplotlib
pip freeze > results/requirements_frozen.txt   # keep this file in the ZIP
```

## 4. How to reproduce (run from the project root)

Run the steps in this order. Script names are as used in the lab; adjust if yours differ.

```bash
# Phase A: evidence preservation and profiling
sha256sum originals/* | tee results/sha256_hashes.txt
python scripts/profile_dataset.py        # 229 records, 77 duplicates
python scripts/inspect_jsonl.py          # train 183 / test 46

# Phase B: candidate extraction and validation
python scripts/ip_extractor.py           # controlled demonstration samples
python scripts/test_ip_regex.py          # writes results/candidate_review.csv (71 / 61 / 10)

# Phase C: offline classifier and rule baseline
python scripts/train_classifier.py       # writes results/predictions.csv
python scripts/rule_baseline.py          # rule baseline predictions
python scripts/03_evaluate_rule_baseline.py

# Phase D: historical evidence (read-only analysis, no new training)
python scripts/analyze_history.py

# Phase E: evaluation
python scripts/evaluate_model.py         # writes results/confusion_matrix.png
```

After each step, compare your output with the figures in the report.

## 5. Expected results

These are the values the report documents for the 46-record test set. A correct rerun should reproduce them.

| Approach | Confusion matrix [[TN, FP], [FN, TP]] | Accuracy |
|---|---|---|
| Offline TF-IDF + Logistic Regression | [[4, 8], [0, 34]] | 82.61% |
| Rule baseline (strictly valid IPv4 present) | [[10, 2], [0, 34]] | 95.65% |
| Majority class (always positive), computed | n/a | 73.91% |

Regex candidates on the test set: 71 matches, 61 strictly valid, 10 invalid.

## 6. Evidence integrity

SHA-256 values recorded at collection (from `results/sha256_hashes.txt`):

```
74dbffb10b5d9e277f1da6a20d02ccd039b1f6ac754d04c8f621633206ab3e56  dataset_small.csv
93938b9d3b627b9dd4126f1d1948e374c10fee5b0733f415572a0fd8b9f35c27  dataset_train.jsonl
77cc78ecec96f5f24175bc894713b54bc5b631b3aaa684665fe2e59663e21e22  dataset_test.jsonl
a2985fb577678515c7ca8dad529beec77e91dd1555b4ed515d43000129e0fe58  result.csv
TODO                                                              fine_tuning_steps.txt
```

Verify at any time:

```bash
cd originals && sha256sum dataset_small.csv dataset_train.jsonl dataset_test.jsonl result.csv fine_tuning_steps.txt
```

## 7. Historical vs new results

`originals/result.csv` and `fine_tuning_steps.txt` describe a **previous** fine-tuning experiment. They are reference material only. **No fine-tuned model was run for this capstone.** All new results come from the locally trained scikit-learn classifier and the rule baseline.

## 8. Known limitations

- Small, imbalanced test set (46 records, 73.9% positive); 77 of 229 CSV rows are duplicates.
- Train/test overlap check: `TODO: record result`.
- The eight-record review (`results/eight_record_review.csv`) requires the examiner's observations and initials.
- AUROC/AUPRC were not computed (predictions are hard labels).

## 9. Pre-submission checklist

- [ ] Name, student ID and date filled in (report, briefing, this README)
- [ ] `evidence_manifest.csv` complete (sizes, WAT times, source, examiner, `fine_tuning_steps.txt` hash)
- [ ] Python version, seed and `pip freeze` recorded
- [ ] Five CSV-to-JSONL comparisons verified
- [ ] Eight-record review confirmed and initialled
- [ ] Historical charts attached; remaining `result.csv` metrics transcribed
- [ ] Report PDF signed
- [ ] No secrets, virtual environment or unrelated datasets in the ZIP
