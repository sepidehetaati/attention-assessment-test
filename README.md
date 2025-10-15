# Attention Assessment Test
A lightweight Python package that implements three widely‑used cognitive‑attention measures – the Attention Control Scale (ACS‑20), the Mindful Attention Awareness Scale (MAAS), and a Trail‑Making Test (TMT) – for research and clinical screening.

## Features

- ACS 20: 20-item self-report, 4-point Likert (1 = almost never → 4 = always) assessing focusing (9 items) and shifting (11 items)  . Scoring yields raw totals ranging from 20 to 80; higher scores indicate better attentional control. The questions in this code are written in Persian; you can change them to your own language. 
- MAAS: 15-item trait mindfulness scale, 6-point frequency (1 = almost always → 6 = almost never) capturing present-focused awareness . Scoring is the mean of all items.  The questions in this code are written in Persian; you can change them to your own language. 
- TMT: computerized Trail Making Test (parts A & B), measuring processing speed and set shifting. This code consists of a series of TMT-A and TMT-B tests that can be edited in the default part. This code will capture mouse and webcam data, as well as the time, number of correct and incorrect answers.

## Installation
```
git clone https://github.com/sepidehetaati/attention-assessment-test.git
cd attention-assessment-test
```
## Usage
```python
from assessment import ACS, MAAS, TMT

acs = ACS(data)      # data: list of 20 responses
print(acs.score())   # raw score 20‑80

maas = MAAS(data)    # data: list of 15 responses
print(maas.mean())   # mean score 1‑6

tmt = TMT()
tmt.run()            # launches interactive TMT
```
## Validation & Reliability
- ACS‑20 shows strong internal consistency (α ≈ 0.71–0.92) across diverse samples 

- MAAS has been validated in clinical (e.g., cancer) populations and demonstrates good psychometric properties

## References
1.  [http://doi.org/10.5281/zenodo.3406466](URL)

2. Townshend, K. and Bornschlegl, M., 2025. Attention control scale (ACS). In Handbook of Assessment in Mindfulness Research (pp. 1659-1675). Cham: Springer Nature Switzerland.

3. Brown, K.W. and Ryan, R.M., 2003. The benefits of being present: mindfulness and its role in psychological well-being. Journal of personality and social psychology, 84(4), p.822.
