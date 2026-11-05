# Spreadsheet Cross-Check Verification Report

**Purpose:** Document the validation methodology ensuring mathematical parity between Python (Pandas/NumPy/SciPy) statistical routines and standard spreadsheet formulas (Microsoft Excel, Google Sheets, LibreOffice Calc).

---

## 1. Cross-Check Methodology & Artifact Overview

In enterprise data engineering and quantitative research, programmatic analytics must undergo cross-tool reconciliation against spreadsheet formulas to catch subtle bugs, indexing errors, degrees-of-freedom mismatches, and interpolation discrepancies.

### Generated Cross-Check Artifacts:
1. **Excel Workbook (`data/spreadsheet_cross_check.xlsx`):**
   - **Sheet 1 (`Sample_Data`):** 1,000 student records sampled from the population ($N=1,000,000$, seed `42`).
   - **Sheet 2 (`Cross_Check_Summary`):** 52 statistical metrics evaluated using **live Excel formulas** directly referencing `Sample_Data!`, placed side-by-side with Pandas calculations.
   - **Sheet 3 (`Population_vs_Sample`):** Quantitative audit comparing sample parameters to the 1,000,000-record ground truth to verify sampling fidelity.
2. **Tabular CSV (`data/spreadsheet_cross_check.csv`):**
   - Version-controlled plain-text export of the verification matrix for direct diff inspection.
3. **Sample Dataset (`data/sample_students.csv`):**
   - Clean, isolated CSV containing the exact 1,000 rows for external formula replication.

---

## 2. Statistical Function Mapping & Degrees of Freedom

| Statistical Metric | Python / Pandas Syntax | Excel / Google Sheets Formula | Mathematical Definition & Notes |
| :--- | :--- | :--- | :--- |
| **Observation Count** | `len(series)` | `=COUNT(range)` | Total non-null numerical values. |
| **Arithmetic Mean** | `series.mean()` | `=AVERAGE(range)` | $\bar{x} = \frac{1}{n} \sum_{i=1}^n x_i$ |
| **Median (50th %ile)** | `series.median()` | `=MEDIAN(range)` | Middle value of sorted observations. |
| **Sample Std Dev** | `series.std(ddof=1)` | `=STDEV.S(range)` | $s = \sqrt{\frac{1}{n-1} \sum (x_i - \bar{x})^2}$ (Bessel's correction). |
| **Sample Variance** | `series.var(ddof=1)` | `=VAR.S(range)` | $s^2 = \frac{1}{n-1} \sum (x_i - \bar{x})^2$ |
| **Minimum Value** | `series.min()` | `=MIN(range)` | Smallest observed scalar. |
| **25th Percentile ($Q_1$)**| `series.quantile(0.25)`| `=PERCENTILE.INC(range, 0.25)` | First quartile using inclusive linear interpolation. |
| **75th Percentile ($Q_3$)**| `series.quantile(0.75)`| `=PERCENTILE.INC(range, 0.75)` | Third quartile using inclusive linear interpolation. |
| **Interquartile Range** | `q75 - q25` | `=PERCENTILE.INC(...,0.75)-PERCENTILE.INC(...,0.25)` | $\text{IQR} = Q_3 - Q_1$ |
| **Maximum Value** | `series.max()` | `=MAX(range)` | Largest observed scalar. |
| **Skewness** | `series.skew()` | `=SKEW(range)` | Adjusted Fisher-Pearson standardized moment. |
| **Excess Kurtosis** | `series.kurt()` | `=KURT(range)` | Sample excess kurtosis (Normal = 0). |
| **Pearson Correlation**| `s.corr(score_series)` | `=CORREL(range1, range2)` | Linear correlation coefficient $r$. |

### ⚠️ The Degrees-of-Freedom Trap:
A frequent source of corporate reporting discrepancies is the difference between sample standard deviation ($N-1$ divisor) and population standard deviation ($N$ divisor):
- **Pandas Default:** `series.std()` uses `ddof=1` (sample).
- **NumPy Default:** `np.std(array)` uses `ddof=0` (population).
- **Excel Functions:** `STDEV.S` uses $N-1$; `STDEV.P` uses $N$.
In this project, all sample standard deviation calculations explicitly specify $\text{ddof}=1$, ensuring exact mathematical alignment with Excel's `STDEV.S`.

---

## 3. Cross-Check Summary Matrix (52 Verified Points)

Below is an extract of the verification matrix comparing Python calculated values to live Excel formula definitions on the $N=1,000$ sample.

| Feature | Metric | Python (Pandas) | Live Excel Formula Syntax | Parity Status | Absolute Delta |
| :--- | :--- | :---: | :--- | :---: | :---: |
| **Study Hours** | Count | 1000 | `=COUNT(Sample_Data!B2:B1001)` | **PASS** | 0.0000 |
| **Study Hours** | Mean | 15.0882 | `=AVERAGE(Sample_Data!B2:B1001)` | **PASS** | 0.0000 |
| **Study Hours** | Median | 15.1000 | `=MEDIAN(Sample_Data!B2:B1001)` | **PASS** | 0.0000 |
| **Study Hours** | Std Dev (Sample)| 6.8436 | `=STDEV.S(Sample_Data!B2:B1001)` | **PASS** | 0.0000 |
| **Study Hours** | Variance (Sample)| 46.8354 | `=VAR.S(Sample_Data!B2:B1001)` | **PASS** | 0.0000 |
| **Study Hours** | Min | 0.0000 | `=MIN(Sample_Data!B2:B1001)` | **PASS** | 0.0000 |
| **Study Hours** | 25% ($Q_1$) | 10.0000 | `=PERCENTILE.INC(Sample_Data!B2:B1001,0.25)` | **PASS** | 0.0000 |
| **Study Hours** | 75% ($Q_3$) | 19.9000 | `=PERCENTILE.INC(Sample_Data!B2:B1001,0.75)` | **PASS** | 0.0000 |
| **Study Hours** | IQR | 9.9000 | `=PERCENTILE.INC(...,0.75)-PERCENTILE.INC(...,0.25)`| **PASS** | 0.0000 |
| **Study Hours** | Max | 38.6000 | `=MAX(Sample_Data!B2:B1001)` | **PASS** | 0.0000 |
| **Study Hours** | Skewness | +0.1068 | `=SKEW(Sample_Data!B2:B1001)` | **PASS** | 0.0000 |
| **Study Hours** | Kurtosis | -0.1982 | `=KURT(Sample_Data!B2:B1001)` | **PASS** | 0.0000 |
| **Study Hours** | Corr w/ Score | +0.8077 | `=CORREL(Sample_Data!B2:B1001,Sample_Data!E2:E1001)`| **PASS** | 0.0000 |
| **Attendance %** | Mean | 84.8143 | `=AVERAGE(Sample_Data!C2:C1001)` | **PASS** | 0.0000 |
| **Attendance %** | Std Dev (Sample)| 9.5398 | `=STDEV.S(Sample_Data!C2:C1001)` | **PASS** | 0.0000 |
| **Attendance %** | Median | 85.0000 | `=MEDIAN(Sample_Data!C2:C1001)` | **PASS** | 0.0000 |
| **Attendance %** | Corr w/ Score | -0.0125 | `=CORREL(Sample_Data!C2:C1001,Sample_Data!E2:E1001)`| **PASS** | 0.0000 |
| **Participation** | Mean | 5.9650 | `=AVERAGE(Sample_Data!D2:D1001)` | **PASS** | 0.0000 |
| **Participation** | Std Dev (Sample)| 1.9566 | `=STDEV.S(Sample_Data!D2:D1001)` | **PASS** | 0.0000 |
| **Participation** | Corr w/ Score | -0.0076 | `=CORREL(Sample_Data!D2:D1001,Sample_Data!E2:E1001)`| **PASS** | 0.0000 |
| **Total Score** | Mean | 84.8155 | `=AVERAGE(Sample_Data!E2:E1001)` | **PASS** | 0.0000 |
| **Total Score** | Median | 88.2000 | `=MEDIAN(Sample_Data!E2:E1001)` | **PASS** | 0.0000 |
| **Total Score** | Std Dev (Sample)| 15.1973 | `=STDEV.S(Sample_Data!E2:E1001)` | **PASS** | 0.0000 |
| **Total Score** | Min | 22.0000 | `=MIN(Sample_Data!E2:E1001)` | **PASS** | 0.0000 |
| **Total Score** | Max | 100.0000| `=MAX(Sample_Data!E2:E1001)` | **PASS** | 0.0000 |
| **Total Score** | Skewness | -0.8407 | `=SKEW(Sample_Data!E2:E1001)` | **PASS** | 0.0000 |
| **Total Score** | Kurtosis | -0.0385 | `=KURT(Sample_Data!E2:E1001)` | **PASS** | 0.0000 |

*Full 52 metrics are available in `data/spreadsheet_cross_check.csv` and within the live workbook `data/spreadsheet_cross_check.xlsx`.*

---

## 4. Verification Conclusion

All 52 statistical metrics cross-checked between the Python pipeline and spreadsheet formula specifications achieve **100% mathematical parity** (zero delta). This verifies the accuracy of the underlying algorithms and guarantees that stakeholders reviewing the Excel workbook will see identical numerical outputs.
