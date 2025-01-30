# tennis-predictor
Predict tennis match result and give a betting strategy accordingly.

**DISCLAIMER: The returns are not worth the risks (Sharpe ratio < 1). Use at your own risk, this is not financial advice.**

## Installation
```bash
python3 -m venv .venv  # Create a dedicated environnement
source .venv/bin/activate
pip3 install -r requirements.txt  # Install dependencies
make make_all  # Run preprocessing, prediction and evaluation
```

## Usage
As command line interface:
```bash
python src/tennis_predictor/advisor.py --player1="De Jong J." --player2="Cobolli F." --odds1=2.3 --odds2=1.51
```
Or from python:
```python
from tennis_predictor import advise
advise("De Jong J.", "Cobolli F.", odds1=2.3, odds2=1.51)
```
### Result
```text
Player 207411 has ELO 2124 with 380 matches
Player 207925 has ELO 2329 with 324 matches
De Jong J. has a 23.5% estimated winrate.
We should bet 30.4% of our bankroll on Cobolli F..
```
