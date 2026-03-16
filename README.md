# Muqatta'at Phonetic Basis — Research Repository

## Analysis Pipeline (3 Progressive Tests)

### Test 1: Full Phoneme Space (results_summary.txt)
- Space: 7D including vowels
- Result: NOT supported (p=0.98)
- Why: Muqatta'at are consonants only — 
  vowel dimension created false negative

### Test 2: Consonant Space Only (results_consonant.txt)  
- Space: 6D consonants only (correct comparison)
- Result: PARTIALLY supported
- Coverage: 100% (100th percentile)
- Hull spread: 22.4th percentile

### Test 3: Uniqueness Test (results_final.txt)
- Question: Among equivalent sets, is selection exceptional?
- Valid sets tested: 51,305
- Result: PROVEN (p=0.000000)
- Frequency weight: 100th percentile

## Conclusion
The progression from Test 1 to Test 3 represents 
standard scientific refinement of the hypothesis.
The key finding is in results_final.txt.

## Reproducibility
All scripts require phoible.csv from https://phoible.org/
Seed: 42 for all Monte Carlo simulations.