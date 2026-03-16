#!/usr/bin/env python3
"""
Muqatta'at Phonetic Basis Hypothesis Test
==========================================
Tests whether the 14 Arabic Muqatta'at letters form a mathematical basis
for the entire human phonetic space, using the PHOIBLE database.

Optimized version with vectorized operations and corrected phoneme mappings.
"""

import csv
import sys
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════
# STEP 1: Load and Prepare Data
# ═══════════════════════════════════════════════════════════════

print("=" * 60)
print("STEP 1: LOADING AND PREPARING DATA")
print("=" * 60)

def parse_feat(val):
    """Parse PHOIBLE +/-/0 to numeric. Returns None if ambiguous."""
    v = str(val).strip().strip('"')
    if v == '+': return 1.0
    if v == '-': return 0.0
    if v == '0': return None
    if ',' in v: return None
    return None

def compute_place(row):
    """
    Derive place of articulation (0-10) from PHOIBLE features.
    Handles all place categories: bilabial through glottal.
    """
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
    spread_gl = parse_feat(row.get('spreadGlottis', '0'))
    constr_gl = parse_feat(row.get('constrictedGlottis', '0'))
    
    # Bilabial: labial but not labiodental
    if lab == 1 and labdent != 1:
        return 0.5
    # Labiodental
    if lab == 1 and labdent == 1:
        return 1.5
    # Coronal sounds
    if cor == 1:
        if ant == 1 and dist == 1:
            return 3.0  # dental
        if ant == 1 and dist != 1:
            return 5.0  # alveolar
        if ant == 0 and dist == 1:
            return 5.5  # post-alveolar/palato-alveolar
        if ant == 0 and dist == 0:
            return 4.5  # retroflex
        if ant == 0:
            return 5.5  # default post-alveolar
        return 5.0  # default alveolar for coronal
    # Dorsal sounds
    if dors == 1:
        if high == 1 and (back == 0 or back is None):
            return 6.5  # palatal
        if high == 1 and back == 1:
            return 7.5  # velar
        if (high == 0 or high is None) and back == 1:
            return 8.25  # uvular
        if low == 1 and rtr == 1:
            return 8.75  # pharyngeal (dorsal + low + RTR)
        if low == 1:
            return 8.25  # uvular (dorsal + low)
        return 7.5  # default velar
    # No major oral place features => glottal or pharyngeal
    # pharyngeal: RTR=+ or low=+ without dorsal
    if rtr == 1:
        return 8.75  # pharyngeal
    # glottal: spreadGlottis or constrictedGlottis, or no place at all
    return 9.5  # glottal

def compute_manner(row):
    """
    Derive manner of articulation (0-6) from PHOIBLE features.
    0=stop, 1=affricate, 2=fricative, 3=nasal, 4=trill/tap, 5=approximant/lateral, 6=vowel
    """
    syl = parse_feat(row.get('syllabic', '-'))
    son = parse_feat(row.get('sonorant', '-'))
    cont = parse_feat(row.get('continuant', '-'))
    dr = parse_feat(row.get('delayedRelease', '-'))
    nas = parse_feat(row.get('nasal', '-'))
    lat = parse_feat(row.get('lateral', '-'))
    approx = parse_feat(row.get('approximant', '-'))
    trill = parse_feat(row.get('trill', '-'))
    tap = parse_feat(row.get('tap', '-'))
    cons = parse_feat(row.get('consonantal', '-'))
    
    if syl == 1 and cons != 1:
        return 6.0  # vowel
    if nas == 1 and son == 1:
        return 3.0  # nasal
    if trill == 1 or tap == 1:
        return 4.0  # trill/tap
    if lat == 1:
        return 5.0  # lateral
    if approx == 1 and son == 1:
        return 5.0  # approximant
    if cont == 0 and dr != 1:
        return 0.0  # stop
    if dr == 1:
        return 1.0  # affricate
    if cont == 1 and son == 0:
        return 2.0  # fricative
    if cont == 1 and cons == 1:
        return 2.0  # fricative
    if son == 1:
        return 5.0  # approximant
    return None

# Read CSV and build phoneme vectors
print("Loading phoible.csv...")
phoneme_data = {}
language_set = set()
raw_count = 0

with open('phoible.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        raw_count += 1
        phoneme = row['Phoneme']
        seg_class = row.get('SegmentClass', '')
        if seg_class == 'tone':
            continue
        
        language_set.add(row.get('Glottocode', '') or row['InventoryID'])
        
        place = compute_place(row)
        manner = compute_manner(row)
        if place is None or manner is None:
            continue
        
        voice = parse_feat(row.get('periodicGlottalSource', '-'))
        syl_v = parse_feat(row.get('syllabic', '-'))
        nas_v = parse_feat(row.get('nasal', '-'))
        lat_v = parse_feat(row.get('lateral', '-'))
        cont_v = parse_feat(row.get('continuant', '-'))
        
        vec = np.array([
            place, manner,
            voice if voice is not None else 0.0,
            syl_v if syl_v is not None else 0.0,
            nas_v if nas_v is not None else 0.0,
            lat_v if lat_v is not None else 0.0,
            cont_v if cont_v is not None else 0.0
        ])
        
        if phoneme not in phoneme_data:
            phoneme_data[phoneme] = []
        phoneme_data[phoneme].append(vec)

# Average vectors per phoneme (same phoneme may appear across inventories)
unique_phonemes = {}
for ph, vecs in phoneme_data.items():
    unique_phonemes[ph] = np.mean(vecs, axis=0)

n_phonemes = len(unique_phonemes)
n_languages = len(language_set)

print(f"Raw rows processed: {raw_count}")
print(f"Unique phonemes: {n_phonemes}")
print(f"Languages: {n_languages}")
print(f"Features: 7 (place, manner, voice, syllabic, nasal, lateral, continuant)")

# Build world phoneme matrix
all_ph_list = sorted(unique_phonemes.keys())
W = np.array([unique_phonemes[ph] for ph in all_ph_list])
print(f"W matrix shape: {W.shape}")
print()

# ═══════════════════════════════════════════════════════════════
# STEP 2: Map the 14 Muqatta'at
# ═══════════════════════════════════════════════════════════════

print("=" * 60)
print("STEP 2: MAPPING THE 14 MUQATTAAT")
print("=" * 60)

# Mapping each Muqatta letter to IPA candidates (in priority order)
muqattaat_map = [
    ("Alef", "ا", ['ʔ']),           # glottal stop
    ("Lam",  "ل", ['l', 'lˠ']),      # lateral
    ("Mim",  "م", ['m']),            # bilabial nasal
    ("Ra",   "ر", ['r', 'ɾ']),       # alveolar trill/tap
    ("Kaf",  "ك", ['k']),            # velar stop
    ("Ha",   "ه", ['h', 'ɦ']),       # glottal fricative
    ("Ya",   "ي", ['j']),            # palatal approximant
    ("Ayn",  "ع", ['ʕ']),            # pharyngeal fricative
    ("Sad",  "ص", ['sˤ', 'sˠ', 's']),# emphatic s (fallback to s)
    ("Ta",   "ط", ['tˤ', 'tˠ', 't']),# emphatic t (fallback to t)
    ("Sin",  "س", ['s']),            # alveolar fricative
    ("Hha",  "ح", ['ħ']),            # voiceless pharyngeal
    ("Qaf",  "ق", ['q']),            # uvular stop
    ("Nun",  "ن", ['n']),            # alveolar nasal
]

muq_vectors = {}
muq_ipa = {}

for name, arabic, candidates in muqattaat_map:
    label = f"{name} ({arabic})"
    found = False
    for c in candidates:
        if c in unique_phonemes:
            muq_vectors[label] = unique_phonemes[c].copy()
            muq_ipa[label] = c
            found = True
            break
    if not found:
        # Try base character
        for c in candidates:
            base = c[0]
            if base in unique_phonemes:
                muq_vectors[label] = unique_phonemes[base].copy()
                muq_ipa[label] = base
                found = True
                break
    if not found:
        print(f"  WARNING: {label} NOT FOUND!")

# Handle Sad/Sin distinction: if Sad fell back to 's', make emphatic adjustment
sad_label = "Sad (ص)"
sin_label = "Sin (س)"
if sad_label in muq_ipa and sin_label in muq_ipa:
    if muq_ipa[sad_label] == muq_ipa[sin_label]:
        # Sad is pharyngealized s: retracted place
        muq_vectors[sad_label] = muq_vectors[sad_label].copy()
        muq_vectors[sad_label][0] = min(muq_vectors[sad_label][0] + 2.0, 10.0)
        print(f"  Adjusted {sad_label}: pharyngealized (place +2)")

# Handle Ta/generic t distinction
ta_label = "Ta (ط)"
if ta_label in muq_ipa and muq_ipa[ta_label] == 't':
    muq_vectors[ta_label] = muq_vectors[ta_label].copy()
    muq_vectors[ta_label][0] = min(muq_vectors[ta_label][0] + 2.0, 10.0)
    print(f"  Adjusted {ta_label}: pharyngealized (place +2)")

print(f"\nMapped {len(muq_vectors)}/14 letters:")
for label in sorted(muq_vectors.keys()):
    ipa = muq_ipa.get(label, '?')
    v = muq_vectors[label]
    print(f"  {label:15s} -> /{ipa:3s}/ : place={v[0]:5.2f} manner={v[1]:.0f} "
          f"voice={v[2]:.0f} syl={v[3]:.0f} nas={v[4]:.0f} lat={v[5]:.0f} cont={v[6]:.0f}")

# Build M matrix
M_labels = sorted(muq_vectors.keys())
M = np.array([muq_vectors[lb] for lb in M_labels])
print(f"\nM matrix: {M.shape}")
print()

# ═══════════════════════════════════════════════════════════════
# STEP 3: Mathematical Tests
# ═══════════════════════════════════════════════════════════════

print("=" * 60)
print("STEP 3: MATHEMATICAL TESTS")
print("=" * 60)

# === TEST A: Matrix Rank ===
print("\n--- TEST A: Matrix Rank ---")
rank_M = np.linalg.matrix_rank(M)
rank_W = np.linalg.matrix_rank(W)
print(f"rank(M) = {rank_M}/7")
print(f"rank(W) = {rank_W}/7")
print(f"Equal? {rank_M == rank_W}")
if rank_M == rank_W:
    print("=> Muqattaat span the SAME dimensional subspace as all world phonemes.")
else:
    print(f"=> Muqattaat span {rank_M} dims vs {rank_W} for world phonemes.")

# === TEST B: Coverage (Vectorized) ===
print("\n--- TEST B: Coverage (Representation) ---")

def compute_coverage_vectorized(basis, targets, threshold=0.15):
    """Vectorized least-squares coverage computation."""
    # Solve: basis.T @ X = targets.T  =>  X = lstsq(basis.T, targets.T)
    # basis.T is (7, n_basis), targets.T is (7, n_targets)
    BT = basis.T  # 7 x n_basis
    TT = targets.T  # 7 x n_targets
    X, residuals, rank, sv = np.linalg.lstsq(BT, TT, rcond=None)
    # Reconstruction
    recon = BT @ X  # 7 x n_targets
    errors = np.sum((recon - TT) ** 2, axis=0)  # per-target error
    coverage = np.mean(errors < threshold) * 100
    return coverage, errors

cov_pct, muq_errors = compute_coverage_vectorized(M, W)
print(f"Muqattaat coverage: {cov_pct:.2f}%  (error < 0.15)")

# Random comparison (1000 sets, vectorized)
print("Running 1000 random comparisons (vectorized)...")
np.random.seed(42)
rand_covs = []
for _ in range(1000):
    idx = np.random.choice(W.shape[0], size=14, replace=False)
    rM = W[idx]
    if np.linalg.matrix_rank(rM) > 0:
        rc, _ = compute_coverage_vectorized(rM, W)
        rand_covs.append(rc)
    else:
        rand_covs.append(0.0)

rand_covs = np.array(rand_covs)
cov_percentile = np.mean(rand_covs <= cov_pct) * 100
print(f"Random: mean={np.mean(rand_covs):.2f}% +/- {np.std(rand_covs):.2f}%")
print(f"Muqattaat percentile: {cov_percentile:.1f}%")

# === TEST C: SVD Dimensionality ===
print("\n--- TEST C: SVD Dimensionality ---")

_, S_m, _ = np.linalg.svd(M, full_matrices=False)
_, S_w, _ = np.linalg.svd(W, full_matrices=False)

cumvar_m = np.cumsum(S_m**2) / np.sum(S_m**2)
cumvar_w = np.cumsum(S_w**2) / np.sum(S_w**2)

dims95_m = int(np.searchsorted(cumvar_m, 0.95)) + 1
dims95_w = int(np.searchsorted(cumvar_w, 0.95)) + 1

print(f"M: {dims95_m} dims for 95% variance")
print(f"W: {dims95_w} dims for 95% variance")
print(f"M singular values: {np.round(S_m, 4)}")
print(f"W singular values: {np.round(S_w, 4)}")
print(f"M cumvar: {np.round(cumvar_m*100, 2)}%")
print(f"W cumvar: {np.round(cumvar_w*100, 2)}%")

# === TEST D: Geometric Spread ===
print("\n--- TEST D: Geometric Spread ---")

def spread_measure(points):
    """Compute spread as sqrt of abs det of covariance."""
    centered = points - np.mean(points, axis=0)
    if centered.shape[0] < centered.shape[1]:
        # Fewer points than dims: use pseudo-measure
        cov = centered.T @ centered / max(centered.shape[0] - 1, 1)
    else:
        cov = np.cov(centered.T)
    return np.sqrt(abs(np.linalg.det(cov)))

vol_m = spread_measure(M)
print(f"Muqattaat spread measure: {vol_m:.6f}")

# Try ConvexHull with QJ option for joggled input
hull_vol_m = None
try:
    from scipy.spatial import ConvexHull
    hull = ConvexHull(M, qhull_options='QJ')
    hull_vol_m = hull.volume
    print(f"Convex hull volume (QJ): {hull_vol_m:.6f}")
except Exception as e:
    print(f"ConvexHull failed: {e}")
    print("Using covariance-based spread measure instead.")

# Compare with random
print("Computing spread for 1000 random sets...")
np.random.seed(42)
rand_vols = []
rand_hull_vols = []
for _ in range(1000):
    idx = np.random.choice(W.shape[0], size=14, replace=False)
    rM = W[idx]
    rand_vols.append(spread_measure(rM))
    if hull_vol_m is not None:
        try:
            rh = ConvexHull(rM, qhull_options='QJ')
            rand_hull_vols.append(rh.volume)
        except:
            rand_hull_vols.append(0.0)

rand_vols = np.array(rand_vols)

if hull_vol_m is not None and len(rand_hull_vols) > 0:
    rand_hull_vols = np.array(rand_hull_vols)
    hull_ptile = np.mean(rand_hull_vols <= hull_vol_m) * 100
    print(f"Hull volume percentile: {hull_ptile:.1f}%")
    effective_vol = hull_vol_m
    effective_ptile = hull_ptile
else:
    vol_ptile = np.mean(rand_vols <= vol_m) * 100
    print(f"Spread percentile: {vol_ptile:.1f}%")
    effective_vol = vol_m
    effective_ptile = vol_ptile
    hull_ptile = vol_ptile

print(f"Random spread: mean={np.mean(rand_vols):.6f} +/- {np.std(rand_vols):.6f}")

# === TEST E: Articulation Coverage ===
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
    ('glottal',     9,  10.01),  # include 10
]

muq_places = np.array([muq_vectors[lb][0] for lb in M_labels])
world_places = W[:, 0]

# We also need to count per-language coverage for world languages
# For simplicity, count unique phonemes in each region

region_results = {}
for rname, rlo, rhi in regions:
    muq_n = int(np.sum((muq_places >= rlo) & (muq_places < rhi)))
    world_n = int(np.sum((world_places >= rlo) & (world_places < rhi)))
    region_results[rname] = (muq_n, world_n)

header = "Muqattaat"
print(f"{'Region':<15} {header:>10} {'World':>10}")
print("-" * 40)
regions_covered = 0
for rname, rlo, rhi in regions:
    mn, wn = region_results[rname]
    mark = "Y" if mn > 0 else "-"
    if mn > 0:
        regions_covered += 1
    print(f"{rname:<15} {mn:>10} {wn:>10}  {mark}")

world_populated = sum(1 for v in region_results.values() if v[1] > 0)
matched = sum(1 for v in region_results.values() if v[0] > 0 and v[1] > 0)
print(f"\nMuqattaat cover {regions_covered}/9 regions")
print(f"World has phonemes in {world_populated}/9 regions")
print(f"Matched: {matched}/{world_populated}")

# === TEST F: Monte Carlo 10,000 (Vectorized) ===
print("\n--- TEST F: Statistical Significance (Monte Carlo 10,000) ---")

print("Running 10,000 Monte Carlo trials (vectorized)...")
np.random.seed(42)
mc_covs = np.zeros(10000)
mc_vols = np.zeros(10000)

for i in range(10000):
    idx = np.random.choice(W.shape[0], size=14, replace=False)
    rM = W[idx]
    
    # Coverage (vectorized)
    if np.linalg.matrix_rank(rM) > 0:
        mc_covs[i], _ = compute_coverage_vectorized(rM, W)
    
    # Spread
    mc_vols[i] = spread_measure(rM)

p_value_cov = float(np.mean(mc_covs >= cov_pct))
p_value_vol = float(np.mean(mc_vols >= effective_vol))

print(f"Coverage p-value: {p_value_cov:.6f}")
print(f"  (prob random >= {cov_pct:.2f}% coverage)")
print(f"Spread p-value: {p_value_vol:.6f}")
print(f"  (prob random >= {effective_vol:.6f} spread)")

# ═══════════════════════════════════════════════════════════════
# RESULTS SUMMARY
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("RESULTS SUMMARY")
print("=" * 60)

results = []
results.append(f"RESULT_RANK: {rank_M}/7 vs {rank_W}/7")
results.append(f"RESULT_COVERAGE: {cov_pct:.2f}% (percentile: {cov_percentile:.1f}%)")
results.append(f"RESULT_SVD_M: {dims95_m} dimensions")
results.append(f"RESULT_SVD_W: {dims95_w} dimensions")
results.append(f"RESULT_HULL_PERCENTILE: {hull_ptile:.1f}%")
results.append(f"RESULT_ARTICULATION: {regions_covered}/9 regions covered")
results.append(f"RESULT_PVALUE: {p_value_cov:.6f}")
results.append(f"RESULT_N_PHONEMES: {n_phonemes}")
results.append(f"RESULT_N_LANGUAGES: {n_languages}")

for r in results:
    print(r)

# Build conclusion
parts = []
if rank_M == rank_W:
    parts.append(f"The Muqattaat matrix achieves the same rank ({rank_M}) as the world phoneme matrix, "
                 f"indicating these 14 phonemes span the full {rank_W}-dimensional feature space.")
else:
    parts.append(f"The Muqattaat matrix has rank {rank_M}, falling short of the world matrix rank {rank_W}. "
                 f"This means the 14 letters do NOT span the complete feature space in this encoding.")

if cov_percentile > 90:
    parts.append(f"Coverage is {cov_pct:.1f}%, placing the set at the {cov_percentile:.0f}th "
                 f"percentile vs random—significantly above chance.")
elif cov_percentile > 50:
    parts.append(f"Coverage is {cov_pct:.1f}% ({cov_percentile:.0f}th percentile)—above average but not exceptional.")
else:
    parts.append(f"Coverage is {cov_pct:.1f}% ({cov_percentile:.0f}th percentile)—at or below what random "
                 f"14-phoneme selections achieve (mean {np.mean(mc_covs):.1f}%).")

parts.append(f"SVD shows {dims95_m} dimension(s) capture 95% of Muqattaat variance vs {dims95_w} for world phonemes.")
parts.append(f"Geometric spread is at the {hull_ptile:.0f}th percentile vs random sets.")
parts.append(f"Articulation coverage: {regions_covered}/9 regions (matched {matched}/{world_populated} populated regions).")
parts.append(f"Monte Carlo p-value for coverage: {p_value_cov:.6f}.")

if cov_percentile > 90 and hull_ptile > 80 and rank_M == rank_W:
    verdict = ("The evidence supports the hypothesis that the Muqattaat form a well-chosen, "
               "near-optimal basis for the human phonetic space as encoded by these 7 features.")
elif rank_M == rank_W:
    verdict = ("While the Muqattaat achieve full rank, their coverage and spread are not exceptional "
               "compared to random selections, suggesting the basis property is a natural consequence "
               "of phonetic diversity rather than a unique mathematical property.")
else:
    verdict = ("The hypothesis is NOT supported by this analysis. The Muqattaat do not achieve full rank "
               "in the 7-feature space, and their coverage does not exceed random expectations. "
               "This is likely because consonant-only sets inherently lack syllabic vowel coverage, "
               "and the 14 letters cluster in certain articulatory regions. "
               "A stronger test would require a higher-dimensional feature representation and/or "
               "comparison with other typologically diverse 14-consonant sets.")

parts.append(verdict)
conclusion = "CONCLUSION: " + " ".join(parts)
print(f"\n{conclusion}")

# Save results_summary.txt
with open('results_summary.txt', 'w', encoding='utf-8') as f:
    f.write("MUQATTAAT PHONETIC BASIS HYPOTHESIS TEST\n")
    f.write("=" * 60 + "\n\n")
    for r in results:
        f.write(r + "\n")
    f.write(f"\n{conclusion}\n")
    f.write("\n\nDETAILED DATA:\n" + "-" * 60 + "\n")
    f.write("\nMuqattaat mappings:\n")
    for lb in M_labels:
        ipa = muq_ipa.get(lb, '?')
        v = muq_vectors[lb]
        f.write(f"  {lb} -> /{ipa}/: {np.round(v, 3).tolist()}\n")
    f.write(f"\nSVD M: {np.round(S_m, 4).tolist()}\n")
    f.write(f"SVD W: {np.round(S_w, 4).tolist()}\n")
    f.write(f"\nMonte Carlo (10,000):\n")
    f.write(f"  Coverage: mean={np.mean(mc_covs):.2f}%, std={np.std(mc_covs):.2f}%, muq={cov_pct:.2f}%\n")
    f.write(f"  Spread: mean={np.mean(mc_vols):.6f}, std={np.std(mc_vols):.6f}, muq={effective_vol:.6f}\n")
    f.write(f"\nRegion coverage:\n")
    for rname, _, _ in regions:
        mn, wn = region_results[rname]
        f.write(f"  {rname}: muq={mn}, world={wn}\n")

print("\nSaved: results_summary.txt")

# ═══════════════════════════════════════════════════════════════
# Generate Plot
# ═══════════════════════════════════════════════════════════════

print("\nGenerating phonetic_space.png...")

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#16213e')
    
    # All world phonemes
    ax.scatter(W[:, 0], W[:, 1], c='#4a90d9', alpha=0.12, s=6,
              label=f'World phonemes (n={n_phonemes})', zorder=1, edgecolors='none')
    
    # Muqattaat as gold stars
    Mplot = np.array([muq_vectors[lb] for lb in M_labels])
    ax.scatter(Mplot[:, 0], Mplot[:, 1], c='#FFD700', marker='*', s=350,
              label="14 Muqattaat", zorder=3, edgecolors='#FF8C00', linewidth=1.5)
    
    # Labels
    for i, lb in enumerate(M_labels):
        ipa = muq_ipa.get(lb, '')
        short = lb.split('(')[0].strip()
        ax.annotate(f"{short}\n/{ipa}/", (Mplot[i, 0], Mplot[i, 1]),
                   textcoords="offset points", xytext=(12, 8),
                   fontsize=7, color='#FFD700', fontweight='bold', alpha=0.9,
                   arrowprops=dict(arrowstyle='->', color='#FFD700', alpha=0.4))
    
    # Convex hull outline (2D)
    try:
        from scipy.spatial import ConvexHull
        hull2d = ConvexHull(Mplot[:, :2])
        verts = Mplot[hull2d.vertices, :2]
        verts = np.vstack([verts, verts[0]])
        ax.plot(verts[:, 0], verts[:, 1], color='#FFD700', linewidth=2,
               linestyle='--', alpha=0.7, label='Muqattaat hull', zorder=2)
        ax.fill(verts[:, 0], verts[:, 1], color='#FFD700', alpha=0.04, zorder=1)
    except Exception as e:
        print(f"  2D hull warning: {e}")
    
    ax.set_xlabel('Place of Articulation', fontsize=14, color='white', fontweight='bold')
    ax.set_ylabel('Manner of Articulation', fontsize=14, color='white', fontweight='bold')
    ax.set_title("Arabic Muqattaat in the Human Phonetic Space\n(PHOIBLE Database)",
                fontsize=16, color='white', fontweight='bold', pad=20)
    
    # Manner labels
    manner_labels = ['Stop', 'Affricate', 'Fricative', 'Nasal', 'Trill/Tap', 'Approx.', 'Vowel']
    ax.set_yticks(range(7))
    ax.set_yticklabels(manner_labels, fontsize=10, color='#cccccc')
    
    # Place region labels on top
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    rpos = [0.5, 1.5, 3.0, 5.0, 6.5, 7.5, 8.25, 8.75, 9.5]
    rlbl = ['Bilab.', 'Labdent.', 'Dental', 'Alveolar', 'Palatal',
            'Velar', 'Uvular', 'Pharyn.', 'Glottal']
    ax2.set_xticks(rpos)
    ax2.set_xticklabels(rlbl, fontsize=7, color='#888888', rotation=45)
    ax2.tick_params(axis='x', length=0)
    
    ax.tick_params(axis='x', colors='#cccccc')
    ax.tick_params(axis='y', colors='#cccccc')
    
    # Results box
    info = (f"Rank: {rank_M}/7 vs {rank_W}/7\n"
            f"Coverage: {cov_pct:.1f}% (p{cov_percentile:.0f})\n"
            f"Hull: p{hull_ptile:.0f}\n"
            f"Regions: {regions_covered}/9\n"
            f"p-value: {p_value_cov:.4f}")
    bbox = dict(boxstyle='round,pad=0.5', facecolor='#0a0a23', edgecolor='#FFD700', alpha=0.9)
    ax.text(0.02, 0.98, info, transform=ax.transAxes, fontsize=10,
           verticalalignment='top', bbox=bbox, color='#FFD700', fontfamily='monospace')
    
    leg = ax.legend(loc='lower right', fontsize=10, framealpha=0.8,
                    facecolor='#16213e', edgecolor='#4a90d9')
    for t in leg.get_texts():
        t.set_color('white')
    
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 6.8)
    ax.grid(True, alpha=0.1, color='white')
    for sp in ax.spines.values():
        sp.set_color('#333')
    
    plt.tight_layout()
    plt.savefig('phonetic_space.png', dpi=150, facecolor=fig.get_facecolor(),
                bbox_inches='tight', pad_inches=0.3)
    print("Saved: phonetic_space.png")
    plt.close()

except ImportError as e:
    print(f"matplotlib not available: {e}")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
print("Files saved:")
print("  1. results_summary.txt")
print("  2. muqattaat_analysis.py")
print("  3. phonetic_space.png")
