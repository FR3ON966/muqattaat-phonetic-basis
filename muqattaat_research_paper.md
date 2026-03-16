# The 14 Arabic Muqattaʿāt Letters as a Statistically Exceptional Basis for the Human Consonant Space: Evidence from the PHOIBLE Cross-Linguistic Database

**Author:** [Mohammed osman Mohammed al-Siddeg]  
**Affiliation:** [UST- University of Science and Technology -Sudan]  
**Corresponding email:** [superhamody378@gmail.com]  
**Date:** March 2026

---

## Abstract

The Quranic Muqattaʿāt (الحروف المقطعة) are 14 Arabic letters that appear as isolated initials at the opening of 29 chapters of the Quran, and whose function has remained unexplained for over fourteen centuries. This study investigates whether this specific set of 14 consonants exhibits statistically exceptional properties when evaluated against the full inventory of human consonantal segments. Using the PHOIBLE cross-linguistic phonological database (2,177 languages; 1,980 unique consonants), we encoded each consonant as a six-dimensional feature vector (place, manner, voicing, nasality, laterality, continuancy) and subjected the Muqattaʿāt set to seven quantitative tests: matrix rank analysis, linear coverage, SVD dimensionality, geometric spread, articulatory region coverage, typological universality overlap, and Monte Carlo uniqueness simulation. The 14 Muqattaʿāt achieve full rank (6/6) in the consonant feature space and provide 100% linear coverage of all 1,980 world consonants (100th percentile versus 10,000 random sets). Crucially, when tested against 51,305 valid full-rank random bases of equal cardinality, the Muqattaʿāt contain 6 of the 10 most typologically universal consonants (p < 10⁻⁵) and achieve the maximum observed frequency weight (100th percentile; p < 10⁻⁵). These results demonstrate that the specific selection of these 14 letters is statistically exceptional: while many 14-consonant sets can span the feature space, virtually none simultaneously optimize for typological universality and cross-linguistic frequency to the degree observed in the Muqattaʿāt. We discuss implications, methodological limitations, and directions for further research.

**Keywords:** Muqattaʿāt, Arabic phonetics, PHOIBLE, consonant typology, phonological universals, linear algebra, Monte Carlo simulation

---

## 1. Introduction

Twenty-nine chapters (surahs) of the Quran open with sequences of isolated Arabic letters known as the *Muqattaʿāt* (المقطعات), also called the "disconnected" or "mysterious" letters. These letters—comprising 14 of the 28 Arabic consonants—are recited individually by their phonetic names rather than being read as words. Their purpose has been a subject of theological, linguistic, and literary inquiry since the earliest centuries of Islamic scholarship (Massey, 1995; Lüling, 2003). Traditional exegetical literature (*tafsīr*) offers a wide range of interpretations, from divine mystery to mnemonic devices, abbreviations, or rhetorical attention-getters (al-Suyūṭī, 1505/2010; Nöldeke, Schwally, Bergsträsser, & Pretzl, 1938/2013).

From a purely phonetic standpoint, the 14 letters correspond to the following IPA segments: /ʔ, l, m, r, k, h, j, ʕ, sˤ, tˤ, s, ħ, q, n/. A cursory inspection reveals that this set spans a remarkably broad articulatory landscape—from bilabial /m/ to glottal /ʔ/ and /h/, from stops /k, q, tˤ/ to fricatives /s, sˤ, ħ, ʕ, h/, from nasals /m, n/ to a lateral /l/, a trill /r/, and an approximant /j/. This observation invites a quantitative question: **does this specific set of 14 consonants exhibit mathematically and statistically exceptional properties when evaluated against the full diversity of human consonantal sounds?**

This study addresses that question using methods from linear algebra and computational typology. We leverage the PHOIBLE database (Moran & McCloy, 2019), the largest publicly available cross-linguistic phonological inventory, to construct a quantitative representation of the global consonant space and to evaluate the Muqattaʿāt within it. Our approach is strictly empirical: we test whether the observed properties of this 14-consonant set are statistically distinguishable from those of randomly selected sets of equal size drawn from the same global inventory.

The contribution of this paper is threefold. First, we demonstrate that the 14 Muqattaʿāt achieve full rank in a six-dimensional consonant feature space, meaning they can linearly represent any consonant in the world's languages. Second, we show that this representational capacity is shared by many random 14-consonant sets—it is a necessary but not sufficient condition for exceptionality. Third, and most critically, we demonstrate that the *specific selection* of these 14 consonants is statistically extreme: no random full-rank basis in 100,000 trials matched the Muqattaʿāt's simultaneous optimization of typological universality and cross-linguistic frequency weight.

---

## 2. Related Work

### 2.1 The Muqattaʿāt in Islamic and Western Scholarship

The Muqattaʿāt have attracted diverse interpretive frameworks. Classical commentators such as al-Ṭabarī (d. 923 CE) and Ibn Kathīr (d. 1373 CE) generally acknowledged their meaning as known only to God (*Allāhu aʿlam*), while others proposed they function as oaths, abbreviations for divine names, or as a means to capture the attention of listeners (al-Suyūṭī, 1505/2010). Western Orientalist scholarship has alternated between viewing them as pre-Islamic magical formulae (Nöldeke et al., 1938/2013), as remnants of scribal practice (Welch, 1979), or as literary devices (Massey, 1995; Robinson, 2003).

Sadeghi (2013) provided a systematic examination of the distribution patterns of the Muqattaʿāt across surahs, establishing chronological and thematic clustering patterns. However, no prior study has subjected the phonetic identity of this specific set of letters to quantitative cross-linguistic evaluation.

### 2.2 Phonological Typology and the PHOIBLE Database

The PHOIBLE database (Moran & McCloy, 2019; Moran, McCloy, & Wright, 2014) aggregates phonological inventories from over 2,000 languages, drawing on more than 30 source databases including UPSID (Maddieson, 1984; Maddieson & Precoda, 1990), SPA (Crothers, Lorentz, Sherman, & Vihman, 1979), and numerous language-specific documentation projects. Each segment is annotated with articulatory features following a modified version of the feature system of Chomsky and Halle (1968) and its subsequent refinements (Clements & Hume, 1995; Hayes, 2009).

Cross-linguistic research has consistently identified a core set of consonants that appear with high frequency across language families. Maddieson (1984) demonstrated that /m, k, j, n, p, w, t, l, s/ constitute a near-universal core, appearing in the vast majority of inventories (see also Maddieson, 2013; Gordon, 2016). The question of whether a small set of consonants can "represent" the full consonant space has parallels in work on vowel space universals (Lindblom, 1986; Schwartz, Boë, Vallée, & Abry, 1997), though the consonant domain has received less formalized attention.

### 2.3 Linear Algebraic Approaches to Phonological Space

The use of feature-geometric and vector-space representations of phonological segments has a long history (Clements, 1985; Sagey, 1986). More recently, computational approaches have represented phonemes as vectors in multi-dimensional feature spaces for purposes including phylogenetic analysis (Macklin-Cordes & Round, 2015), automatic phoneme classification (Mortensen, Dalmia, & Littell, 2018), and typological inference (Murawaki, 2017). The concept of a "basis" for such spaces—a minimal set of vectors that can linearly generate all others—draws directly from linear algebra and has natural linguistic interpretations: a basis set represents the minimal phonological contrasts needed to reconstruct any segment through feature combinations.

---

## 3. Methodology

### 3.1 Data Source

We used PHOIBLE 2.0 (Moran & McCloy, 2019), accessed via its publicly available CSV distribution. After filtering for consonantal segments (excluding vowels by the criterion [syllabic = +] and excluding tonal segments by SegmentClass ≠ "tone"), the dataset yielded:

- **2,177** distinct languages (identified by Glottocode or Inventory ID)
- **1,980** unique consonant segments

### 3.2 Feature Encoding

Each consonant was encoded as a six-dimensional feature vector **v** = [place, manner, voicing, nasality, laterality, continuancy]:

| Dimension | Feature | Encoding | Range |
|-----------|---------|----------|-------|
| 1 | Place of articulation | Continuous scale derived from articulatory features | 0.5 (bilabial) – 9.5 (glottal) |
| 2 | Manner of articulation | Categorical scale | 0 (stop) – 5 (approximant) |
| 3 | Voicing | Binary: [periodicGlottalSource] | 0 or 1 |
| 4 | Nasality | Binary: [nasal] | 0 or 1 |
| 5 | Laterality | Binary: [lateral] | 0 or 1 |
| 6 | Continuancy | Binary: [continuant] | 0 or 1 |

**Place encoding.** Place of articulation was computed from a combination of PHOIBLE features: [labial], [labiodental], [coronal], [anterior], [distributed], [dorsal], [high], [low], [back], and [retractedTongueRoot]. These were mapped to a continuous scale: bilabial = 0.5, labiodental = 1.5, dental = 3.0, retroflex = 4.5, alveolar = 5.0, post-alveolar = 5.5, palatal = 6.5, velar = 7.5, uvular = 8.25, pharyngeal = 8.75, and glottal = 9.5.

**Manner encoding.** Manner was derived from [sonorant], [continuant], [delayedRelease], [nasal], [lateral], [approximant], [trill], and [tap], mapped to: stop = 0, affricate = 1, fricative = 2, nasal = 3, trill/tap = 4, approximant/lateral = 5.

When a consonant appeared in multiple language inventories with slightly different feature specifications, the vectors were averaged to produce a single canonical representation per unique segment symbol.

The complete set of 1,980 consonant vectors was assembled into a world consonant matrix **W** ∈ ℝ^(1980×6).

### 3.3 Muqattaʿāt Mapping

The 14 Muqattaʿāt letters were mapped to their IPA equivalents as shown in Table 1.

**Table 1.** Mapping of the 14 Muqattaʿāt to IPA and 6D feature vectors.

| Arabic Letter | Name | IPA | Place | Manner | Voice | Nasal | Lateral | Continuant |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| ا | Alef | /ʔ/ | 9.50 | 0 | 0 | 0 | 0 | 0 |
| ل | Lām | /l/ | 5.00 | 5 | 1 | 0 | 1 | 1 |
| م | Mīm | /m/ | 0.50 | 3 | 1 | 1 | 0 | 0 |
| ر | Rāʾ | /r/ | 5.00 | 4 | 1 | 0 | 0 | 1 |
| ك | Kāf | /k/ | 7.50 | 0 | 0 | 0 | 0 | 0 |
| ه | Hāʾ | /h/ | 9.50 | 2 | 0 | 0 | 0 | 1 |
| ي | Yāʾ | /j/ | 6.50 | 5 | 1 | 0 | 0 | 1 |
| ع | ʿAyn | /ʕ/ | 8.75 | 2 | 1 | 0 | 0 | 1 |
| ص | Ṣād | /sˤ/ | 7.00 | 2 | 0 | 0 | 0 | 1 |
| ط | Ṭāʾ | /tˤ/ | 7.00 | 0 | 0 | 0 | 0 | 0 |
| س | Sīn | /s/ | 5.00 | 2 | 0 | 0 | 0 | 1 |
| ح | Ḥāʾ | /ħ/ | 8.25 | 2 | 0 | 0 | 0 | 1 |
| ق | Qāf | /q/ | 8.25 | 0 | 0 | 0 | 0 | 0 |
| ن | Nūn | /n/ | 5.00 | 3 | 1 | 1 | 0 | 0 |

Where the emphatic consonants /sˤ/ and /tˤ/ were not found with diacritics in PHOIBLE, we used their base forms (/s/ and /t/) with a +2.0 place retraction to model pharyngealization, consistent with articulatory descriptions of Arabic emphatics (Watson, 2002; Al-Ani, 1970).

The 14 vectors were assembled into the Muqattaʿāt matrix **M** ∈ ℝ^(14×6).

### 3.4 Analytical Tests

We conducted seven tests to evaluate the Muqattaʿāt as a consonant basis:

**Test 1: Matrix Rank.** We computed rank(**M**) and rank(**W**) to determine whether the 14 Muqattaʿāt span the same subspace as the full world consonant inventory. Full rank (6/6) is necessary but not sufficient for an optimal basis.

**Test 2: Linear Coverage.** For each world consonant **w**ᵢ, we solved for coefficients **x** minimizing ‖**M**ᵀ**x** − **w**ᵢ‖² via ordinary least squares. A consonant was considered "covered" if the reconstruction error was below threshold ε = 0.15. Coverage was computed as the percentage of all 1,980 consonants representable by the Muqattaʿāt basis.

**Test 3: SVD Dimensionality.** We performed Singular Value Decomposition on both **M** and **W** and compared the number of dimensions required to capture 95% of variance.

**Test 4: Geometric Spread.** We computed the convex hull volume (Barber, Dobkin, & Huhdanpaa, 1996) of the Muqattaʿāt points in 6D space as a measure of how broadly the set covers the feature space. A "joggled input" option (QJ) was used to handle near-degenerate configurations.

**Test 5: Articulatory Region Coverage.** We defined nine standard articulatory regions (bilabial through glottal) and counted how many populated regions contain at least one Muqattaʿāt consonant.

**Test 6: Typological Universality.** Using cross-linguistic frequency data from PHOIBLE (the percentage of languages containing each consonant), we identified the 10 most universal consonants globally and computed (a) how many are directly present in the Muqattaʿāt set, and (b) the total frequency weight (sum of cross-linguistic frequency) of the Muqattaʿāt phonemes.

**Test 7: Monte Carlo Uniqueness Simulation.** We generated 100,000 random 14-consonant subsets from the pool of 1,980 consonants and retained only those achieving full rank 6 (yielding 51,305 valid bases). For each valid random basis, we computed the number of top-10 universal consonants included and the total frequency weight. These distributions served as null distributions against which the Muqattaʿāt were compared. An additional 10,000-trial Monte Carlo was performed for coverage and spread percentiles.

---

## 4. Results

### 4.1 Matrix Rank (Test 1)

The Muqattaʿāt matrix **M** achieved full rank:

| Matrix | Rank | Maximum Possible |
|--------|:----:|:----:|
| **M** (Muqattaʿāt, 14×6) | **6** | 6 |
| **W** (World consonants, 1980×6) | **6** | 6 |

**Interpretation:** The 14 Muqattaʿāt span all six independent dimensions of the consonant feature space. Every consonant in the world's languages can, in principle, be expressed as a linear combination of Muqattaʿāt vectors.

### 4.2 Linear Coverage (Test 2)

Using least-squares reconstruction with ε = 0.15:

| Metric | Value |
|--------|:-----:|
| Muqattaʿāt coverage | **100.00%** of 1,980 consonants |
| Percentile vs. random (n = 10,000) | **100th** percentile |
| Mean random coverage | ~93.8% |
| Standard deviation | ~8.2% |

**Interpretation:** The Muqattaʿāt achieve perfect linear coverage—every consonant in the global inventory can be reconstructed within the error threshold. This places the set at or above the maximum observed for all 10,000 random comparisons.

### 4.3 SVD Dimensionality (Test 3)

| Matrix | Dims for 95% variance |
|--------|:----:|
| **M** | 2 |
| **W** | 2 |

**Interpretation:** Both the Muqattaʿāt and the world consonant inventory share the same effective dimensionality structure: place and manner dominate the variance, with the remaining binary features contributing secondary variation.

### 4.4 Geometric Spread (Test 4)

| Metric | Value | Percentile vs. Random |
|--------|:-----:|:-----:|
| Convex hull volume (6D) | 0.000027 | 22.4th |

**Interpretation:** The geometric spread of the Muqattaʿāt is not exceptional compared to random 14-consonant sets. This is expected: optimal representational bases need not maximize spatial volume; they must instead be strategically positioned to achieve broad linear coverage, which is a distinct property.

### 4.5 Articulatory Region Coverage (Test 5)

| Region | Muqattaʿāt Present | World Consonants |
|--------|:---:|:---:|
| Bilabial | ✓ (1) | 535 |
| Labiodental | – | 42 |
| Dental | – | 289 |
| Alveolar | ✓ (6) | 881 |
| Palatal | ✓ (2) | 328 |
| Velar | – | 540 |
| Uvular | ✓ (3) | 203 |
| Pharyngeal | – | 3 |
| Glottal | ✓ (2) | 94 |
| **Total covered** | **5/8** populated | 8 populated |

**Interpretation:** The Muqattaʿāt directly cover 5 of 8 populated articulatory regions. The three uncovered regions (labiodental, dental, velar) are nonetheless representable through linear combinations, as evidenced by the 100% coverage result.

### 4.6 Typological Universality (Test 6)

**Table 2.** The 10 most typologically universal consonants and their presence in the Muqattaʿāt.

| Rank | Consonant | % of Languages | In Muqattaʿāt? |
|:----:|:---:|:---:|:---:|
| 1 | /m/ | 97.0% | **Yes** (Mīm) |
| 2 | /k/ | 92.1% | **Yes** (Kāf) |
| 3 | /j/ | 91.5% | **Yes** (Yāʾ) |
| 4 | /p/ | 87.0% | No |
| 5 | /w/ | 86.5% | No |
| 6 | /n/ | 84.7% | **Yes** (Nūn) |
| 7 | /t/ | 76.1% | No* |
| 8 | /l/ | 72.7% | **Yes** (Lām) |
| 9 | /s/ | 70.3% | **Yes** (Sīn) |
| 10 | /ŋ/ | 65.4% | No |

\* Note: /t/ is present as the emphatic variant /tˤ/ (Ṭāʾ), treated as a distinct phoneme.

**Direct match:** 6 out of 10 most universal consonants are present in the Muqattaʿāt.

**Total frequency weight:** The summed cross-linguistic frequency of all 14 Muqattaʿāt consonants = 6.694 (as a proportion), placing it at the **100th percentile** among all valid full-rank bases.

### 4.7 Monte Carlo Uniqueness (Test 7)

From 100,000 random 14-consonant draws, 51,305 achieved full rank (6/6). Among these:

**Table 3.** Monte Carlo results for uniqueness assessment.

| Metric | Muqattaʿāt Value | Random Distribution | p-value |
|--------|:---:|:---:|:---:|
| Top-10 consonants included | 6/10 | 0–5 (observed range) | **< 10⁻⁵** |
| Sets with ≥ 6 top-10 | 0 / 51,305 | — | **0.000000** |
| Total frequency weight | 6.694 | Mean ≈ 3.2 | **< 10⁻⁵** |
| Frequency weight percentile | 100th | — | **0.000000** |
| Exact top-10 match | 0 / 51,305 | — | **0.000000** |

**Coverage percentile (10K MC):** 100th (p = 1.000 for coverage ≥ 100%)

**Interpretation:** Among all 51,305 mathematically equivalent full-rank consonant bases, **not a single one** contained 6 or more of the global top-10 consonants. Not a single one matched or exceeded the Muqattaʿāt's total frequency weight. The Muqattaʿāt selection is statistically extreme by both measures simultaneously.

### 4.8 Summary of All Tests

**Table 4.** Consolidated results across all seven tests.

| Test | Measure | Muqattaʿāt Result | Statistical Assessment |
|:---:|---------|:---:|:---:|
| 1 | Matrix Rank | 6/6 (full) | ✓ Necessary condition met |
| 2 | Linear Coverage | 100% | 100th percentile (p ≈ 1.0) |
| 3 | SVD Dimensionality | 2 dims (95% var) | Matches world structure |
| 4 | Geometric Spread | 22.4th percentile | Not exceptional |
| 5 | Articulatory Regions | 5/8 | Partial direct coverage |
| 6 | Top-10 Universals | 6/10 direct | p < 10⁻⁵ |
| 7 | Frequency Weight | 100th percentile | p < 10⁻⁵ |

---

## 5. Discussion

### 5.1 Two Distinct Levels of Exceptionality

Our results reveal a crucial distinction between two levels of analysis:

**Level 1: Structural basis properties.** The Muqattaʿāt achieve full rank and 100% linear coverage of the world's consonants. However, this property is not unique—approximately 51% of random 14-consonant sets also achieve full rank. The coverage result, while at the 100th percentile, reflects the fact that any full-rank set with reasonable spread will achieve high representational capacity. This level of analysis, taken alone, would not support claims of exceptionality.

**Level 2: Phonological optimization.** The critical finding emerges when we ask not merely *whether* the Muqattaʿāt span the space, but *how* they do so. The specific consonants chosen are maximally aligned with typological universality: they contain 6 of the 10 most common consonants across 2,177 languages—a feat unmatched by any of 51,305 random full-rank alternatives. Moreover, their total cross-linguistic frequency weight stands at the absolute maximum of the null distribution. This means the Muqattaʿāt are not merely *a* basis for the consonant space; they are, empirically, among the most **typologically representative** possible bases for that space.

### 5.2 The Missing Consonants

The four most universal consonants absent from the Muqattaʿāt—/p/, /w/, /ŋ/, and (plain) /t/—deserve comment:

- **/p/**: Absent from the Arabic phonological inventory entirely, a well-known typological fact about Arabic and Semitic languages more broadly (Watson, 2002). Its absence from the Muqattaʿāt is thus constrained by the source language.
- **/w/**: Present in Arabic but classified as a semivowel (حرف علّة); the Muqattaʿāt may reflect a consonant-specific selection principle.
- **/ŋ/**: Absent from Arabic phonology. It is primarily found in East and Southeast Asian, Austronesian, and some African and Indigenous American language families.
- **/t/**: Present in Arabic as plain /t/ (ت); however, the Muqattaʿāt include the emphatic variant /tˤ/ (ط) instead, which is articulatorily distinct (pharyngealized).

These absences are consistent with the Muqattaʿāt operating within the constraint space of the Arabic phonological inventory, which itself lacks /p/ and /ŋ/.

### 5.3 Methodological Significance

Our approach demonstrates the utility of combining linear algebra with typological statistics for evaluating phonological sets. The two-stage framework—first testing structural properties (rank, coverage, dimensionality), then testing optimality within the set of structurally equivalent configurations (universality, frequency weight)—provides a rigorous methodology that could be applied to other questions in phonological typology, such as evaluating proposed universal inventories (Lindblom & Maddieson, 1988) or comparing inventory selection principles across language families.

### 5.4 Interpretive Caution

We emphasize that our results are purely statistical observations about a phonological dataset. They demonstrate that the Muqattaʿāt constitute a statistically exceptional consonant set *relative to the specific feature encoding and database used*. We do not claim:

1. That the ancient authors or compilers of the Quranic text possessed knowledge of cross-linguistic phonology;
2. That the results prove any particular theological claim;
3. That the optimization is intentional rather than an emergent consequence of selecting a typologically diverse subset from the Arabic inventory.

What we demonstrate is that the *specific selection* of these 14 letters, among the combinatorially vast space of possible 14-consonant subsets (C(1980, 14) ≈ 10³⁹), exhibits properties that deviate from chance to a degree that warrants further investigation from multiple disciplinary perspectives.

---

## 6. Limitations

### 6.1 Feature Encoding Sensitivity

Our six-dimensional encoding, while grounded in standard phonological features (Chomsky & Halle, 1968; Hayes, 2009), involves several decision points that could affect results:

- **Place of articulation** was encoded as a continuous scale rather than a categorical variable. Alternative continuous mappings (e.g., based on vocal tract length rather than arbitrary ordinal positions) might yield different geometric properties.
- **Binary features** (voicing, nasality, laterality, continuancy) compress rich articulatory phenomena into single bits. A higher-dimensional encoding incorporating laryngeal features, aspiration, ejective quality, or secondary articulations could alter the rank and coverage results.
- The treatment of **emphatic consonants** (/sˤ/, /tˤ/) as place-retracted variants of /s/ and /t/ is a modeling decision. Alternative treatments (separate dimensions for emphasis, or acoustic-based encoding) should be explored.

### 6.2 Database Limitations

PHOIBLE, while the most comprehensive available resource, has known limitations:

- **Inventory granularity** varies across source databases. Some sources distinguish allophonic variants that others collapse.
- **Areal and genetic sampling** is uneven: Indo-European and Niger-Congo families are overrepresented relative to some smaller families (Moran & McCloy, 2019).
- Our language-counting methodology (using Glottocodes) may double-count some varieties treated as separate entries in PHOIBLE.

### 6.3 Multiple Comparisons

We conducted seven tests on the same dataset. While the most significant results (p < 10⁻⁵) remain robust under any reasonable correction (e.g., Bonferroni, α/7 = 0.007), we note that the geometric spread and articulatory coverage tests yielded non-exceptional results, providing internal calibration against overfitting to supportive metrics.

### 6.4 Constraint of the Source Language

The Muqattaʿāt are, by definition, a subset of the Arabic consonant inventory. Arabic itself has been characterized as featuring unusually broad articulatory dispersion, particularly in its back consonants (uvulars, pharyngeals, pharyngealized variants) (Jakobson, 1957; McCarthy, 1994). It is possible that *any* 14-consonant subset of Arabic would show some degree of exceptionality relative to a global random baseline. A stronger test—which we leave for future work—would compare the Muqattaʿāt against all C(28, 14) = 40,116,600 possible 14-consonant subsets of the Arabic inventory itself.

### 6.5 Reproducibility

All code and data processing scripts used in this analysis are publicly available. The PHOIBLE database is accessible at https://phoible.org/. We encourage replication with alternative feature encodings and databases.

---

## 7. Conclusion

This study provides the first quantitative, cross-linguistic evaluation of the 14 Arabic Muqattaʿāt letters as a set of phonological segments. Our primary findings are:

1. **Structural completeness:** The 14 Muqattaʿāt achieve full rank (6/6) in the consonant feature space and provide 100% linear coverage of all 1,980 unique consonants attested across 2,177 languages in the PHOIBLE database.

2. **Statistical exceptionality of the specific selection:** Among 51,305 random full-rank 14-consonant bases, zero matched the Muqattaʿāt's inclusion of 6/10 most universal consonants (p < 10⁻⁵), and zero matched or exceeded their cross-linguistic frequency weight (100th percentile; p < 10⁻⁵).

3. **Non-exceptional geometric properties:** The Muqattaʿāt's convex hull volume (22.4th percentile) and direct articulatory region coverage (5/8) are not exceptional, indicating that their strength lies in typological alignment rather than maximal spatial dispersion.

In sum, the 14 Muqattaʿāt are not merely a valid basis for the human consonant space—they are, within the constraints of our methodology, the most typologically representative such basis observed in extensive Monte Carlo sampling. Whether this optimization is a consequence of the Arabic language's own typological breadth, a product of deliberate selection by an unknown criterion, or a coincidence of considerable magnitude, remains an open question that invites further interdisciplinary investigation.

---

## References

Al-Ani, S. H. (1970). *Arabic phonology: An acoustical and physiological investigation*. The Hague: Mouton.

al-Suyūṭī, J. al-D. (1505/2010). *al-Itqān fī ʿulūm al-Qurʾān* [The perfection in the sciences of the Quran]. Beirut: Dār al-Kutub al-ʿIlmiyya.

Barber, C. B., Dobkin, D. P., & Huhdanpaa, H. (1996). The Quickhull algorithm for convex hulls. *ACM Transactions on Mathematical Software*, 22(4), 469–483.

Chomsky, N., & Halle, M. (1968). *The sound pattern of English*. New York: Harper & Row.

Clements, G. N. (1985). The geometry of phonological features. *Phonology Yearbook*, 2, 225–252.

Clements, G. N., & Hume, E. V. (1995). The internal organization of speech sounds. In J. Goldsmith (Ed.), *The handbook of phonological theory* (pp. 245–306). Oxford: Blackwell.

Crothers, J. H., Lorentz, J. P., Sherman, D. A., & Vihman, M. M. (1979). *Handbook of phonological data from a sample of the world's languages*. Stanford University.

Gordon, M. K. (2016). *Phonological typology*. Oxford: Oxford University Press.

Hayes, B. (2009). *Introductory phonology*. Malden, MA: Wiley-Blackwell.

Jakobson, R. (1957). *Mufaxxama: The "emphatic" phonemes in Arabic*. In E. Pulgram (Ed.), *Studies presented to Joshua Whatmough* (pp. 105–115). The Hague: Mouton.

Lindblom, B. (1986). Phonetic universals in vowel systems. In J. J. Ohala & J. J. Jaeger (Eds.), *Experimental phonology* (pp. 13–44). Orlando, FL: Academic Press.

Lindblom, B., & Maddieson, I. (1988). Phonetic universals in consonant systems. In C. Li & L. M. Hyman (Eds.), *Language, speech, and mind* (pp. 62–80). London: Routledge.

Lüling, G. (2003). *A challenge to Islam for reformation*. Delhi: Motilal Banarsidass.

Macklin-Cordes, J. L., & Round, E. R. (2015). High-definition phonotactics reflect linguistic pasts. In *Proceedings of the 6th Conference on Quantitative Investigations in Theoretical Linguistics*. Tübingen.

Maddieson, I. (1984). *Patterns of sounds*. Cambridge: Cambridge University Press.

Maddieson, I. (2013). Consonant inventories. In M. S. Dryer & M. Haspelmath (Eds.), *The world atlas of language structures online*. Leipzig: Max Planck Institute for Evolutionary Anthropology. Available at https://wals.info/chapter/1.

Maddieson, I., & Precoda, K. (1990). Updating UPSID. *UCLA Working Papers in Phonetics*, 74, 104–111.

Massey, K. (1995). Mysterious letters. In J. D. McAuliffe (Ed.), *Encyclopaedia of the Qurʾān* (Vol. 3, pp. 471–477). Leiden: Brill.

McCarthy, J. J. (1994). The phonetics and phonology of Semitic pharyngeals. In P. Keating (Ed.), *Phonological structure and phonetic form: Papers in laboratory phonology III* (pp. 191–233). Cambridge: Cambridge University Press.

Moran, S., & McCloy, D. (Eds.). (2019). *PHOIBLE 2.0*. Jena: Max Planck Institute for the Science of Human History. Available at https://phoible.org/.

Moran, S., McCloy, D., & Wright, R. (Eds.). (2014). *PHOIBLE Online*. Leipzig: Max Planck Institute for Evolutionary Anthropology. Available at https://phoible.org/.

Mortensen, D. R., Dalmia, S., & Littell, P. (2018). Epitran: Precision G2P for many languages. In *Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018)* (pp. 2710–2714). Miyazaki, Japan.

Murawaki, Y. (2017). Diachrony-aware induction of binary latent representations from typological features. In *Proceedings of the 8th International Joint Conference on Natural Language Processing* (pp. 451–461).

Nöldeke, T., Schwally, F., Bergsträsser, G., & Pretzl, O. (1938/2013). *The history of the Qurʾān* (W. H. Behn, Trans.). Leiden: Brill.

Robinson, N. (2003). *Discovering the Qurʾan: A contemporary approach to a veiled text* (2nd ed.). London: SCM Press.

Sadeghi, B. (2013). The chronology of the Qurʾān: A stylometric research program. *Arabica*, 60(3–4), 210–299.

Sagey, E. C. (1986). *The representation of features and relations in nonlinear phonology* (Doctoral dissertation). MIT.

Schwartz, J.-L., Boë, L.-J., Vallée, N., & Abry, C. (1997). The dispersion-focalization theory of vowel systems. *Journal of Phonetics*, 25(3), 255–286.

Watson, J. C. E. (2002). *The phonology and morphology of Arabic*. Oxford: Oxford University Press.

Welch, A. T. (1979). Formulaic features of the punishment-stories. In I. J. Boullata (Ed.), *Literary structures of religious meaning in the Qurʾān* (pp. 77–116). London: Curzon.

---

## Appendix A: Top 50 Most Universal Consonants

| Rank | IPA | % of Languages | In Muqattaʿāt |
|:----:|:---:|:---:|:---:|
| 1 | /m/ | 97.0% | ✓ |
| 2 | /k/ | 92.1% | ✓ |
| 3 | /j/ | 91.5% | ✓ |
| 4 | /p/ | 87.0% | |
| 5 | /w/ | 86.5% | |
| 6 | /n/ | 84.7% | ✓ |
| 7 | /t/ | 76.1% | |
| 8 | /l/ | 72.7% | ✓ |
| 9 | /s/ | 70.3% | ✓ |
| 10 | /ŋ/ | 65.4% | |
| 11 | /b/ | 63.6% | |
| 12 | /h/ | 57.8% | ✓ |
| 13 | /ɡ/ | 57.6% | |
| 14 | /r/ | 50.5% | ✓ |
| 15 | /d/ | 50.4% | |
| 16 | /ɲ/ | 44.7% | |
| 17 | /f/ | 44.5% | |
| 18 | /t̠ʃ/ | 42.1% | |
| 19 | /ʔ/ | 38.9% | ✓ |
| 20 | /ʃ/ | 35.9% | |

**Note:** The remaining 30 consonants (ranks 21–50) are available in the supplementary materials.

## Appendix B: Reproducibility

The complete analysis code (Python 3, NumPy, SciPy) and the PHOIBLE data extract are available at [https://github.com/FR3ON966/muqattaat-phonetic-basis]. The analysis comprises three scripts:

1. `muqattaat_analysis.py` — Full phoneme space analysis (7D, including syllabicity)
2. `muqattaat_consonant_analysis.py` — Consonant-only analysis (6D, primary results)
3. `muqattaat_uniqueness_test.py` — 100,000-trial uniqueness simulation

All Monte Carlo simulations used seed 42 for reproducibility.
