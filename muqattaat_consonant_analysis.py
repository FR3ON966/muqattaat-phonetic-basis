#!/usr/bin/env python3
"""
Muqatta'at Phonetic Consonant Basis Hypothesis
=============================================
Tests whether the 14 Arabic Muqatta'at letters form a mathematical basis
specifically for the CONSONANT space of human language (6D).
"""

import csv
import sys
import numpy as np
import warnings
from collections import defaultdict
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════
# STEP 1: Load and Prepare Data (Consonants Only)
# ═══════════════════════════════════════════════════════════════

print("=" * 60)
print("STEP 1: PREPARING CONSONANT-ONLY DATASET")
print("=" * 60)

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
    
    # Bilabial: labial but not labiodental
    if lab == 1 and labdent != 1: return 0.5
    # Labiodental
    if lab == 1 and labdent == 1: return 1.5
    # Coronal sounds
    if cor == 1:
        if ant == 1 and dist == 1: return 3.0  # dental
        if ant == 1 and dist != 1: return 5.0  # alveolar
        if ant == 0 and dist == 1: return 5.5  # post-alveolar
        if ant == 0 and dist == 0: return 4.5  # retroflex
        if ant == 0: return 5.5
        return 5.0  # default alveolar
    # Dorsal sounds
    if dors == 1:
        if high == 1 and (back == 0 or back is None): return 6.5  # palatal
        if high == 1 and back == 1: return 7.5  # velar
        if (high == 0 or high is None) and back == 1: return 8.25  # uvular
        if low == 1 and rtr == 1: return 8.75  # pharyngeal
        if low == 1: return 8.25  # uvular
        return 7.5  # default velar
    # Pharyngeal/Glottal
    if rtr == 1: return 8.75  # pharyngeal
    return 9.5  # glottal

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
phoneme_freq = defaultdict(set)  # phoneme -> set of language IDs
languages = set()

with open('phoible.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        syl = parse_feat(row.get('syllabic', '-'))
        seg_class = row.get('SegmentClass', '')
        
        # Filter: keep ONLY consonants (syllabic == 0 or None -> treated as 0)
        # and exclude tones
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
        
        # 6 Features: place, manner, voice, nasal, lateral, continuant
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

print(f"Total unique consonants found:   {n_consonants}")
print(f"Total languages in db:           {n_languages}")
print(f"Feature dimensions: 6 (place, manner, voice, nasal, lateral, continuant)")

all_c_list = sorted(list(unique_consonants.keys()))
W = np.array([unique_consonants[ph] for ph in all_c_list])

# Calculate typological universality (Percentage of languages with this phoneme)
univ_percentages = {ph: len(langs) / n_languages * 100 for ph, langs in phoneme_freq.items()}
top_sorted = sorted(univ_percentages.items(), key=lambda x: x[1], reverse=True)
top_50 = top_sorted[:50]
top_50_set = set([ph for ph, pct in top_50])

print(f"Top consonant: /{top_50[0][0]}/ present in {top_50[0][1]:.1f}% of languages")
print()

# ═══════════════════════════════════════════════════════════════
# STEP 2: Map the 14 Muqatta'at to Consonant Space
# ═══════════════════════════════════════════════════════════════

print("=" * 60)
print("STEP 2: MAPPING MUQATTA'AT (6D SPACE)")
print("=" * 60)

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

muq_vectors = {}
muq_ipa = {}

for name, arabic, candidates in muqattaat_map:
    label = f"{name} ({arabic})"
    found = False
    for c in candidates:
        if c in unique_consonants:
            muq_vectors[label] = unique_consonants[c].copy()
            muq_ipa[label] = c
            found = True
            break
    if not found:
        # Try base char
        for c in candidates:
            base = c[0]
            if base in unique_consonants:
                muq_vectors[label] = unique_consonants[base].copy()
                muq_ipa[label] = base
                found = True
                break
    if not found:
        print(f"  WARNING: {label} NOT FOUND!")

# Distinct handling for Sad vs Sin, Ta vs t
if "Sad (ص)" in muq_ipa and "Sin (س)" in muq_ipa and muq_ipa["Sad (ص)"] == muq_ipa["Sin (س)"]:
    muq_vectors["Sad (ص)"][0] = min(muq_vectors["Sad (ص)"][0] + 2.0, 10.0)

if "Ta (ط)" in muq_ipa and muq_ipa["Ta (ط)"] == 't':
    muq_vectors["Ta (ط)"][0] = min(muq_vectors["Ta (ط)"][0] + 2.0, 10.0)

for label in sorted(muq_vectors.keys()):
    v = muq_vectors[label]
    print(f"  {label:15s} -> /{muq_ipa[label]:3s}/: {np.round(v, 2).tolist()}")

M_labels = sorted(muq_vectors.keys())
M = np.array([muq_vectors[lb] for lb in M_labels])
print(f"\nM matrix shape: {M.shape}")

# ═══════════════════════════════════════════════════════════════
# STEP 3: RUN ALL 6 TESTS
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("STEP 3: EXECUTING ANALYSIS TESTS")
print("=" * 60)

# --- TEST A: Matrix Rank ---
print("\n--- TEST A: Matrix Rank (6D) ---")
rank_m = np.linalg.matrix_rank(M)
rank_w = np.linalg.matrix_rank(W)
print(f"rank(M) = {rank_m}/6")
print(f"rank(W) = {rank_w}/6")

# --- TEST B: Coverage Vectorized ---
print("\n--- TEST B & F: Coverage & Universals ---")
def compute_coverage(basis, targets, threshold=0.15):
    BT = basis.T
    TT = targets.T
    X, _, _, _ = np.linalg.lstsq(BT, TT, rcond=None)
    recon = BT @ X
    errors = np.sum((recon - TT) ** 2, axis=0)
    return np.mean(errors < threshold) * 100, (errors < threshold)

cov_pct, in_cov_mask = compute_coverage(M, W)
print(f"Muqattaat coverage: {cov_pct:.2f}% of all consonants representable")

# Test F implementation: Universal Coverage
top_50_W = np.array([unique_consonants[ph] for ph, _ in top_50])
m_ipa_set = set(muq_ipa.values())

exact_univ_match = sum(1 for ph, _ in top_50 if ph in m_ipa_set)
univ_cov_pct, _ = compute_coverage(M, top_50_W)

print(f"Universals EXACT match: {exact_univ_match}/50 top consonants are in Muqatta'at")
print(f"Universals COVERED match: {univ_cov_pct:.1f}% of top 50 representable by Muqatta'at")

# --- TEST C: SVD Dimensionality ---
print("\n--- TEST C: SVD ---")
_, Sm, _ = np.linalg.svd(M, full_matrices=False)
_, Sw, _ = np.linalg.svd(W, full_matrices=False)
cumvar_m = np.cumsum(Sm**2) / np.sum(Sm**2)
cumvar_w = np.cumsum(Sw**2) / np.sum(Sw**2)
dims95_m = int(np.searchsorted(cumvar_m, 0.95)) + 1
dims95_w = int(np.searchsorted(cumvar_w, 0.95)) + 1
print(f"M: {dims95_m} dims for 95% var. W: {dims95_w} dims for 95% var")

# --- TEST D: Geometric Spread ---
print("\n--- TEST D: Geometric Spread ---")
def spread_measure(pts):
    c = pts - np.mean(pts, axis=0)
    cov = np.cov(c.T) if c.shape[0] >= c.shape[1] else c.T @ c / max(1, c.shape[0]-1)
    return np.sqrt(abs(np.linalg.det(cov)))

vol_m = spread_measure(M)
print(f"Muqattaat spread: {vol_m:.6f}")

try:
    from scipy.spatial import ConvexHull
    hull_m = ConvexHull(M, qhull_options='QJ').volume
    print(f"ConvexHull (QJ) volume: {hull_m:.6f}")
except Exception as e:
    hull_m = vol_m
    print("Fallback to covariance spread.")

# --- TEST E: Articulation Coverage ---
print("\n--- TEST E: Articulation Coverage ---")
regions = [
    ('bilabial',    0,   1),
    ('labiodental', 1,   2),
    ('dental',      2,   4),
    ('alveolar',    4,   6),
    ('palatal',     6,   7),
    ('velar',       7,   8),
    ('uvular',      8,   8.5),
    ('pharyngeal',  8.5, 9),
    ('glottal',     9,  10.01),
]

muq_pl = M[:, 0]
world_pl = W[:, 0]
reg_cov = 0
world_pop = 0
for rname, rlo, rhi in regions:
    mn = np.sum((muq_pl >= rlo) & (muq_pl < rhi))
    wn = np.sum((world_pl >= rlo) & (world_pl < rhi))
    if mn > 0: reg_cov += 1
    if wn > 0: world_pop += 1

print(f"Muqatta'at cover {reg_cov}/{world_pop} populated consonant regions")

# --- TEST G & F combined in Monte Carlo ---
print("\n--- TEST G: UNIQUENESS TEST (Monte Carlo 10,000) ---")
np.random.seed(42)

N = 10000
mc_cov = np.zeros(N)
mc_vol = np.zeros(N)
mc_univ_cov = np.zeros(N)
valid_full_rank = 0

for i in range(N):
    idx = np.random.choice(W.shape[0], size=14, replace=False)
    rM = W[idx]
    
    # Uniqueness requires full rank
    if np.linalg.matrix_rank(rM) == rank_w:
        valid_full_rank += 1
        mc_cov[i], _ = compute_coverage(rM, W)
        mc_univ_cov[i], _ = compute_coverage(rM, top_50_W)
        try:
            mc_vol[i] = ConvexHull(rM, qhull_options='QJ').volume
        except:
            mc_vol[i] = spread_measure(rM)
    else:
        # Invalid / deficient rank
        mc_cov[i] = 0
        mc_vol[i] = 0
        mc_univ_cov[i] = 0

# Calculate percentiles among FULL RANK random sets only
valid_covs = mc_cov[mc_cov > 0]
valid_vols = mc_vol[mc_vol > 0]
valid_univ_covs = mc_univ_cov[mc_univ_cov > 0]

ptile_cov = np.mean(valid_covs <= cov_pct) * 100
ptile_vol = np.mean(valid_vols <= hull_m) * 100
ptile_univ = np.mean(valid_univ_covs <= univ_cov_pct) * 100

# p-values (percent exceeding)
p_val_cov = np.mean(valid_covs >= cov_pct)

print(f"Generated {N} random 14-consonant sets")
print(f"Sets achieving full consonant rank (6): {valid_full_rank}/{N}")
print(f"Coverage percentile: {ptile_cov:.1f}%")
print(f"Spread percentile:   {ptile_vol:.1f}%")
print(f"Univ. cov ptile:     {ptile_univ:.1f}%")

# ═══════════════════════════════════════════════════════════════
# OUTPUT REPORTS
# ═══════════════════════════════════════════════════════════════

res = []
res.append(f"RESULT_RANK: {rank_m}/6 vs {rank_w}/6")
res.append(f"RESULT_COVERAGE: {cov_pct:.2f}% (percentile: {ptile_cov:.1f}%)")
res.append(f"RESULT_PVALUE: {p_val_cov:.6f}")
res.append(f"RESULT_SVD_M: {dims95_m} dimensions")
res.append(f"RESULT_SVD_W: {dims95_w} dimensions")
res.append(f"RESULT_HULL_PERCENTILE: {ptile_vol:.1f}%")
res.append(f"RESULT_ARTICULATION: {reg_cov}/{world_pop}")
res.append(f"RESULT_UNIVERSAL_MATCH: {exact_univ_match}/50 top consonants in Muqatta'at directly")
res.append(f"RESULT_UNIVERSAL_COVERAGE: {univ_cov_pct:.1f}% of top 50 representable by Muqatta'at")

# Combine top percentiles to find uniqueness
aggr_score = (ptile_cov + ptile_vol + ptile_univ) / 3.0
res.append(f"RESULT_UNIQUENESS_RANK: top {100-aggr_score:.1f}% of all full-rank 14-consonant sets")
res.append(f"RESULT_N_CONSONANTS: {n_consonants}")
res.append(f"RESULT_N_LANGUAGES: {n_languages}")

print("\n" + "="*60 + "\nRESULTS SUMMARY\n" + "="*60)
for r in res: print(r)

print("\nTOP_50_UNIVERSAL_CONSONANTS:")
top_50_output = []
for ph, pct in top_50:
    in_muq = "YES" if ph in m_ipa_set else "NO"
    line = f"  /{ph:<3}/ : {pct:4.1f}% languages | In Muqatta'at: {in_muq}"
    top_50_output.append(line)
    print(line)

# Build strict scientific conclusion based on data
parts = []
if rank_m == rank_w:
    parts.append(f"The Muqatta'at matrix reaches full rank ({rank_m}/{rank_w}) in the target consonant space, confirming mathematical basis properties without the zero-variance interference of vowels.")
else:
    parts.append(f"The Muqatta'at matrix reaches rank {rank_m} vs {rank_w} for the world consonant space, failing to form a complete basis even when restricted to consonants.")

parts.append(f"It provides a linear combination representing {cov_pct:.1f}% of all {n_consonants} human consonants, which sits at the {ptile_cov:.1f}th percentile compared to random valid 14-letter sets (p={p_val_cov:.4f}).")

if univ_cov_pct > 80:
    parts.append(f"Typologically, it captures the core of human language, exactly containing {exact_univ_match}/50 of the most universal consonants and mathematically representing {univ_cov_pct:.1f}% of them (at the {ptile_univ:.1f}th percentile).")
else:
    parts.append(f"Typologically, it exactly contains {exact_univ_match}/50 of the most universal consonants and mathematically represents {univ_cov_pct:.1f}% of them, ranking at the {ptile_univ:.1f}th percentile among random bases.")

parts.append(f"Geometrically, it exhibits a spread spanning {reg_cov}/{world_pop} articulatory regions (volume percentile: {ptile_vol:.1f}%).")

if aggr_score > 90 and rank_m == rank_w:
    parts.append("CONCLUSION: The hypothesis is strongly supported. By restricting the scope to the consonantal phonetic space, the 14 Arabic Muqatta'at demonstrate highly atypical, optimized mathematical properties, forming a full-rank typological basis that broadly covers universal human consonants significantly better than random selections.")
elif rank_m == rank_w and aggr_score > 50:
    parts.append("CONCLUSION: The hypothesis is partially supported. As a consonant-only basis, the Muqatta'at reach full structural rank and provide above-average coverage of universal consonants. However, they are mathematically non-unique, as numerous random 14-consonant sets drawn from global phonology can achieve equivalent or superior spanning properties.")
else:
    parts.append("CONCLUSION: The hypothesis remains unsupported even in a restricted consonant space. While eliminating vowels improves relative rank, the 14 Muqatta'at perform comparably to—or worse than—random phoneme assemblages in generating the phonetic space and capturing typological universals.")

conclusion = " ".join(parts)
print("\n" + conclusion)

with open('results_consonant.txt', 'w', encoding='utf-8') as f:
    for r in res: f.write(r + "\n")
    f.write("\nTOP_50_UNIVERSAL_CONSONANTS:\n")
    for l in top_50_output: f.write(l + "\n")
    f.write("\n" + conclusion + "\n")
print("\nSaved: results_consonant.txt")


# ═══════════════════════════════════════════════════════════════
# PLOTTING
# ═══════════════════════════════════════════════════════════════

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    # 1. Consonant Space Plot
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#16213e')
    
    freqs = np.array([len(phoneme_freq[ph]) for ph in all_c_list])
    sizes = np.clip(freqs / np.max(freqs) * 400, 10, 400)
    
    # World consonants
    ax.scatter(W[:, 0], W[:, 1], c='#4a90d9', alpha=0.2, s=sizes,
              label=f'World Consonants (size=freq)', zorder=1, edgecolors='none')
              
    # Top 50 universals
    top_W = np.array([unique_consonants[ph] for ph, _ in top_50])
    ax.scatter(top_W[:, 0], top_W[:, 1], c='#2ecc71', alpha=0.5, s=sizes[:50]*1.5,
              marker='o', label='Top 50 Universals', zorder=2, edgecolors='none')
              
    # Muqattaat
    Mplot = np.array([muq_vectors[lb] for lb in M_labels])
    ax.scatter(Mplot[:, 0], Mplot[:, 1], c='#FFD700', marker='*', s=450,
              label="14 Muqatta'at", zorder=3, edgecolors='#FF8C00', linewidth=1.5)
              
    for i, lb in enumerate(M_labels):
        ipa = muq_ipa.get(lb, '')
        short = lb.split('(')[0].strip()
        ax.annotate(f"{short}\n/{ipa}/", (Mplot[i, 0], Mplot[i, 1]),
                   textcoords="offset points", xytext=(12, 8),
                   fontsize=8, color='#FFD700', fontweight='bold', alpha=0.9)
                   
    from scipy.spatial import ConvexHull
    try:
        hull2d = ConvexHull(Mplot[:, :2])
        verts = Mplot[hull2d.vertices, :2]
        verts = np.vstack([verts, verts[0]])
        ax.plot(verts[:, 0], verts[:, 1], color='#FFD700', linewidth=2,
               linestyle='--', alpha=0.7, zorder=2)
        ax.fill(verts[:, 0], verts[:, 1], color='#FFD700', alpha=0.08, zorder=1)
    except Exception: pass
    
    ax.set_xlabel('Place of Articulation', fontsize=14, color='white', fontweight='bold')
    ax.set_ylabel('Manner of Articulation', fontsize=14, color='white', fontweight='bold')
    ax.set_title("Consonant Space: Muqatta'at vs Typological Universals",
                fontsize=16, color='white', fontweight='bold', pad=20)
                
    manner_labels = ['Stop', 'Affricate', 'Fricative', 'Nasal', 'Trill/Tap', 'Approximant', '']
    ax.set_yticks(range(7))
    ax.set_yticklabels(manner_labels, fontsize=11, color='#cccccc')
    
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    rpos = [0.5, 1.5, 3.0, 5.0, 6.5, 7.5, 8.25, 8.75, 9.5]
    rlbl = ['Bilab.', 'Labdent.', 'Dental', 'Alveolar', 'Palatal', 'Velar', 'Uvular', 'Pharyn.', 'Glottal']
    ax2.set_xticks(rpos)
    ax2.set_xticklabels(rlbl, fontsize=9, color='#888', rotation=45)
    
    ax.tick_params(colors='#ccc')
    ax2.tick_params(colors='#ccc', length=0)
    
    leg = ax.legend(loc='lower left', fontsize=11, framealpha=0.8,
                   facecolor='#16213e', edgecolor='#4a90d9')
    for t in leg.get_texts(): t.set_color('white')
    
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 5.5)
    for sp in ax.spines.values(): sp.set_color('#333')
    
    plt.tight_layout()
    plt.savefig('consonant_space.png', dpi=150, facecolor=fig.get_facecolor())
    plt.close()
    print("Saved: consonant_space.png")
    
    # 2. Bar Chart of Universals
    fig, ax = plt.subplots(figsize=(16, 6))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#16213e')
    
    ph_labels = [ph for ph, _ in top_50]
    ph_pcts = [pct for _, pct in top_50]
    
    # Determine colors
    colors = []
    # Re-run coverage for top 50 to get individual mask
    _, mask = compute_coverage(M, top_50_W)
    
    for i, ph in enumerate(ph_labels):
        if ph in m_ipa_set:
            colors.append('#FFD700')  # Gold = inside Muqattaat
        elif mask[i]:
            colors.append('#2ecc71')  # Green = representable
        else:
            colors.append('#4a90d9')  # Blue = neither
            
    bars = ax.bar(range(50), ph_pcts, color=colors, edgecolor='#16213e', linewidth=0.5)
    
    ax.set_xticks(range(50))
    ax.set_xticklabels(ph_labels, fontsize=12, color='white', rotation=45)
    ax.set_ylabel('% of World Languages', fontsize=12, color='white')
    ax.set_title('Top 50 Universal Consonants & Muqatta\'at Representation', fontsize=15, color='white')
    
    ax.tick_params(axis='y', colors='#ccc')
    for sp in ax.spines.values(): sp.set_color('#333')
    ax.grid(axis='y', alpha=0.1, color='white')
    
    import matplotlib.patches as mpatches
    g_patch = mpatches.Patch(color='#FFD700', label='In Muqatta\'at (Direct)')
    gr_patch = mpatches.Patch(color='#2ecc71', label='Representable (Linear Comb.)')
    b_patch = mpatches.Patch(color='#4a90d9', label='Not Representable')
    leg = ax.legend(handles=[g_patch, gr_patch, b_patch], loc='upper right', facecolor='#16213e', edgecolor='#333')
    for t in leg.get_texts(): t.set_color('white')
    
    plt.tight_layout()
    plt.savefig('universals_chart.png', dpi=150, facecolor=fig.get_facecolor())
    plt.close()
    print("Saved: universals_chart.png")

except Exception as e:
    print(f"Plotting error: {e}")
