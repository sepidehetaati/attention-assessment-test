# Attention Assessment Test
A lightweight Python package that implements three widely‑used cognitive‑attention measures – the Attention Control Scale (ACS‑20), the Mindful Attention Awareness Scale (MAAS), and a Trail‑Making Test (TMT) – for research and clinical screening.

## Features

- ACS‑20: 20‑item self‑report, 4‑point Likert (1 = almost never → 4 = always) assessing focusing (9 items) and shifting (11 items) 
Scoring yields raw totals 20–80; higher scores indicate better attentional control 

- MAAS: 15‑item trait mindfulness scale, 6‑point frequency (1 = almost always → 6 = almost never) capturing present‑focused awareness 
  Scoring is the mean of all items 

- TMT: computerized Trail‑Making Test (parts A & B) measuring processing speed and set‑shifting.

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
