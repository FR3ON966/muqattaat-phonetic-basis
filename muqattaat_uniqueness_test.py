#!/usr/bin/env python3
"""
Muqatta'at Phonetic Consonant Basis - Final Uniqueness Test
==========================================================
Tests whether the specific 14 Arabic Muqatta'at letters are
statistically exceptional among all mathematically equivalent
(full-rank) 14-consonant bases, specifically in terms of 
typological universality (top 10 consonants & frequency weight).
"""

import csv
import numpy as np
import warnings
from collections import defaultdict
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════
# STEP 1: SETUP AND DATA LOADING
# ═══════════════════════════════════════════════════════════════

def parse_feat(val):
    v = str(val).strip().strip('"')
    if v == '+': return 1.0
    if v == '-': return 0.0
    if v == '0': return None
    if ',' in v: return None
    return None

def compute_place(row):
    lab = parse_feat(row.get('labial', '0'))
    labdent = parse_feat(row.get('labiodental', '0'))
    cor = parse_feat(row.get('coronal', '0'))
    ant = parse_feat(row.get('anterior', '0'))
    dist = parse_feat(row.get('distributed', '0'))
    dors = parse_feat(row.get('dorsal', '0'))
    high = parse_feat(row.get('high', '0'))
    low = parse_feat(row.get('low', '0'))
    back = parse_feat(row.get('back', '0'))
    rtr = parse_feat(row.get('retractedTongueRoot', '0'))
    if lab == 1 and labdent != 1: return 0.5
    if lab == 1 and labdent == 1: return 1.5
    if cor == 1:
        if ant == 1 and dist == 1: return 3.0
        if ant == 1 and dist != 1: return 5.0
        if ant == 0 and dist == 1: return 5.5
        if ant == 0 and dist == 0: return 4.5
        if ant == 0: return 5.5
        return 5.0
    if dors == 1:
        if high == 1 and (back == 0 or back is None): return 6.5
        if high == 1 and back == 1: return 7.5
        if (high == 0 or high is None) and back == 1: return 8.25
        if low == 1 and rtr == 1: return 8.75
        if low == 1: return 8.25
        return 7.5
    if rtr == 1: return 8.75
    return 9.5

def compute_manner(row):
    son = parse_feat(row.get('sonorant', '-'))
    cont = parse_feat(row.get('continuant', '-'))
    dr = parse_feat(row.get('delayedRelease', '-'))
    nas = parse_feat(row.get('nasal', '-'))
    lat = parse_feat(row.get('lateral', '-'))
    approx = parse_feat(row.get('approximant', '-'))
    trill = parse_feat(row.get('trill', '-'))
    tap = parse_feat(row.get('tap', '-'))
    cons = parse_feat(row.get('consonantal', '-'))
    if nas == 1 and son == 1: return 3.0
    if trill == 1 or tap == 1: return 4.0
    if lat == 1: return 5.0
    if approx == 1 and son == 1: return 5.0
    if cont == 0 and dr != 1: return 0.0
    if dr == 1: return 1.0
    if cont == 1 and son == 0: return 2.0
    if cont == 1 and cons == 1: return 2.0
    if son == 1: return 5.0
    return None

print("Loading phoible.csv...")
phoneme_vectors = {}
phoneme_freq = defaultdict(set)
languages = set()

with open('phoible.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        syl = parse_feat(row.get('syllabic', '-'))
        seg_class = row.get('SegmentClass', '')
        if syl == 1 or seg_class == 'tone':
            continue
            
        ph = row['Phoneme']
        lang_id = row.get('Glottocode', '') or row['InventoryID']
        languages.add(lang_id)
        
        place = compute_place(row)
        manner = compute_manner(row)
        if place is None or manner is None:
            continue
            
        voice = parse_feat(row.get('periodicGlottalSource', '-'))
        nas = parse_feat(row.get('nasal', '-'))
        lat = parse_feat(row.get('lateral', '-'))
        cont = parse_feat(row.get('continuant', '-'))
        
        vec = np.array([
            place, manner,
            voice if voice is not None else 0.0,
            nas if nas is not None else 0.0,
            lat if lat is not None else 0.0,
            cont if cont is not None else 0.0
        ])
        
        if ph not in phoneme_vectors:
            phoneme_vectors[ph] = []
        phoneme_vectors[ph].append(vec)
        phoneme_freq[ph].add(lang_id)

unique_consonants = {}
for ph, vecs in phoneme_vectors.items():
    unique_consonants[ph] = np.mean(vecs, axis=0)

n_consonants = len(unique_consonants)
n_languages = len(languages)

all_c_list = sorted(list(unique_consonants.keys()))
W = np.array([unique_consonants[ph] for ph in all_c_list])

# Global frequencies
univ_percentages = {ph: len(langs) / n_languages for ph, langs in phoneme_freq.items()}
top_sorted = sorted(univ_percentages.items(), key=lambda x: x[1], reverse=True)
top_10 = top_sorted[:10]
top_10_set = set([ph for ph, pct in top_10])

# Muqatta'at Mapping
muqattaat_map = [
    ("Alef", "ا", ['ʔ']),
    ("Lam",  "ل", ['l', 'lˠ']),
    ("Mim",  "م", ['m']),
    ("Ra",   "ر", ['r', 'ɾ']),
    ("Kaf",  "ك", ['k']),
    ("Ha",   "ه", ['h', 'ɦ']),
    ("Ya",   "ي", ['j']),
    ("Ayn",  "ع", ['ʕ']),
    ("Sad",  "ص", ['sˤ', 'sˠ', 's']),
    ("Ta",   "ط", ['tˤ', 'tˠ', 't']),
    ("Sin",  "س", ['s']),
    ("Hha",  "ح", ['ħ']),
    ("Qaf",  "ق", ['q']),
    ("Nun",  "ن", ['n']),
]

muq_ipa = {}
for name, arabic, candidates in muqattaat_map:
    label = f"{name} ({arabic})"
    found = False
    for c in candidates:
        if c in unique_consonants:
            muq_ipa[label] = c
            found = True
            break
    if not found:
        for c in candidates:
            base = c[0]
            if base in unique_consonants:
                muq_ipa[label] = base
                found = True
                break

m_ipa_set = set(muq_ipa.values())
m_top10_count = len(m_ipa_set.intersection(top_10_set))
m_top10_exact = m_ipa_set.intersection(top_10_set)
m_freq_weight = sum(univ_percentages[ph] for ph in m_ipa_set)

# ═══════════════════════════════════════════════════════════════
# STEP 2 & 3: FIND VALID SETS AND COUNT TOP 10
# ═══════════════════════════════════════════════════════════════

print("\nSampling 100,000 random sets...")
N_SAMPLES = 100000
np.random.seed(42)

valid_top10_counts = []
valid_freq_weights = []
exact_match_count = 0

# Convert keys to list for fast indexing
all_ph_array = np.array(all_c_list)
univ_pct_array = np.array([univ_percentages[ph] for ph in all_c_list])
top_10_mask = np.array([ph in top_10_set for ph in all_c_list])

for i in range(N_SAMPLES):
    # Fast random choice
    idx = np.random.choice(n_consonants, size=14, replace=False)
    rM = W[idx]
    
    # Check full rank (6)
    if np.linalg.matrix_rank(rM) == 6:
        # It is a valid set
        # Count top 10
        top10_n = np.sum(top_10_mask[idx])
        valid_top10_counts.append(top10_n)
        
        # Frequency weight
        weight = np.sum(univ_pct_array[idx])
        valid_freq_weights.append(weight)
        
        # Check exact same 9 if applicable
        if top10_n == m_top10_count:
            set_top10 = set(all_ph_array[idx]).intersection(top_10_set)
            if set_top10 == m_top10_exact:
                exact_match_count += 1

valid_top10_counts = np.array(valid_top10_counts)
valid_freq_weights = np.array(valid_freq_weights)

n_valid = len(valid_top10_counts)
fraction_geq9 = np.mean(valid_top10_counts >= m_top10_count)
pvalue_top10 = float(fraction_geq9)
exact_match_fraction = exact_match_count / n_valid

weight_ptile = np.mean(valid_freq_weights <= m_freq_weight) * 100
weight_pvalue = np.mean(valid_freq_weights >= m_freq_weight)

# ═══════════════════════════════════════════════════════════════
# OUTPUT RESULTS
# ═══════════════════════════════════════════════════════════════

res = []
res.append("RESULT_TOP10: " + ", ".join([f"/{ph}/({pct*100:.1f}%)" for ph, pct in top_10]))
res.append(f"RESULT_VALID_POOL_SIZE: {n_valid}")
res.append(f"RESULT_MUQATTAAT_TOP10_COUNT: {m_top10_count}")
res.append(f"RESULT_FRACTION_GEQ9: {fraction_geq9:.6f} ({fraction_geq9*100:.4f}%)")
res.append(f"RESULT_PVALUE_TOP10: {pvalue_top10:.6f}")
res.append(f"RESULT_EXACT_MATCH_FRACTION: {exact_match_fraction:.6f} ({exact_match_fraction*100:.4f}%)")
res.append(f"RESULT_FREQ_WEIGHT_M: {m_freq_weight:.4f}")
res.append(f"RESULT_FREQ_WEIGHT_PERCENTILE: {weight_ptile:.1f}%")
res.append(f"RESULT_FREQ_WEIGHT_PVALUE: {weight_pvalue:.6f}")

print("\n" + "="*60 + "\nRESULTS SUMMARY\n" + "="*60)
for r in res: print(r)

# Strict Conclusion
parts = []
if fraction_geq9 < 0.05:
    severity = "highly exceptional" if fraction_geq9 < 0.01 else "exceptional"
    parts.append(f"The Muqatta'at selection is statistically {severity}.")
else:
    parts.append(f"The Muqatta'at selection is NOT statistically exceptional.")

parts.append(f"Out of {n_valid} mathematically equivalent (full-rank) consonant bases, "
             f"only {fraction_geq9*100:.4f}% contained {m_top10_count} or more of the global top 10 consonants (p={pvalue_top10:.6f}).")

parts.append(f"Furthermore, its total frequency weight ({m_freq_weight:.2f}) sits at the {weight_ptile:.1f}th percentile among all valid bases (p={weight_pvalue:.6f}).")

parts.append(f"Exactly {exact_match_fraction*100:.4f}% of equivalent sets matched the specific {m_top10_count} universal consonants found in the Muqatta'at.")

if fraction_geq9 < 0.05 and weight_ptile > 95:
    parts.append("CONCLUSION: The hypothesis is rigorously PROVEN. While millions of 14-consonant combinations can form a mathematical basis for human consonants, the specific selection of the Muqatta'at is extreme. It maximizes typological universality and global frequency to a degree achieved by almost no other mathematically equivalent sets. The selection is heavily optimized for human phonological reality, not just abstract space spanning.")
else:
    parts.append("CONCLUSION: The hypothesis is DISPROVEN. Even accounting for their full-rank basis properties, the Muqatta'at's inclusion of top universal consonants and total frequency weight falls within normal statistical expectations for a 14-consonant set. There is no evidence of exceptional optimization beyond what random chance generates.")

conclusion = " ".join(parts)
print("\n" + conclusion)

with open('results_final.txt', 'w', encoding='utf-8') as f:
    for r in res: f.write(r + "\n")
    f.write("\n" + conclusion + "\n")
print("\nSaved: results_final.txt")

# ═══════════════════════════════════════════════════════════════
# PLOTTING
# ═══════════════════════════════════════════════════════════════

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    # 1. Distribution of Top 10 Overlap
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#16213e')
    
    counts, bins = np.histogram(valid_top10_counts, bins=np.arange(-0.5, 11.5, 1))
    ax.bar(bins[:-1]+0.5, counts, width=0.8, color='#4a90d9', edgecolor='#16213e')
    
    ax.axvline(x=m_top10_count, color='#FFD700', linestyle='-', linewidth=3, label=f"Muqatta'at ({m_top10_count})")
    
    ax.set_xticks(range(11))
    ax.set_xlabel('Number of Top-10 Consonants Included', fontsize=12, color='white')
    ax.set_ylabel('Count (Valid Sets)', fontsize=12, color='white')
    ax.set_title("How exceptional is the Muqatta'at selection?\n(Distribution among mathematically equivalent bases)", 
                 fontsize=14, color='white', pad=15)
                 
    ax.tick_params(colors='white')
    for sp in ax.spines.values(): sp.set_color('#333')
    ax.grid(axis='y', alpha=0.1, color='white')
    ax.legend(facecolor='#16213e', edgecolor='#FFD700', labelcolor='white')
    
    # Add p-value box
    bbox = dict(boxstyle='round,pad=0.5', facecolor='#0a0a23', edgecolor='#FFD700', alpha=0.9)
    ax.text(0.02, 0.95, f"p-value: {pvalue_top10:.6f}\nPercentile: {100-fraction_geq9*100:.1f}th", 
            transform=ax.transAxes, fontsize=11, verticalalignment='top', bbox=bbox, color='white')
            
    plt.tight_layout()
    plt.savefig('distribution_chart.png', dpi=150, facecolor=fig.get_facecolor())
    plt.close()
    print("Saved: distribution_chart.png")
    
    # 2. Total Frequency Weight
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#16213e')
    
    ax.hist(valid_freq_weights, bins=50, color='#2ecc71', alpha=0.7, edgecolor='none')
    ax.axvline(x=m_freq_weight, color='#FFD700', linestyle='-', linewidth=3, 
               label=f"Muqatta'at (Wt: {m_freq_weight:.1f}, {weight_ptile:.1f}th ptile)")
               
    ax.set_xlabel('Total Frequency Weight (Sum of language %)', fontsize=12, color='white')
    ax.set_ylabel('Count (Valid Sets)', fontsize=12, color='white')
    ax.set_title("Total Frequency Weight of Mathematically Equivalent Bases", 
                 fontsize=14, color='white', pad=15)
                 
    ax.tick_params(colors='white')
    for sp in ax.spines.values(): sp.set_color('#333')
    ax.grid(axis='y', alpha=0.1, color='white')
    ax.legend(facecolor='#16213e', edgecolor='#FFD700', labelcolor='white')
    
    plt.tight_layout()
    plt.savefig('frequency_weight_chart.png', dpi=150, facecolor=fig.get_facecolor())
    plt.close()
    print("Saved: frequency_weight_chart.png")

except Exception as e:
    print(f"Plotting error: {e}")
