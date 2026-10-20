# Knowledge — Performers

Signature craft from technical DJs who mostly don't teach, reverse-engineered per the methodology in `transition-lab/work/edu-survey-G.md`. Moves already implemented live in the engine (cited); this file holds the craft that informs selection and future extraction. Provenance on every entry.

### James Zabiela — the FX technician

The original FX-technician: Pioneer EFX-1000/DJM beat-FX composition (feedback loops, beat rolls, transform effect), live sampling of vocals through the mic input, polyrhythmic pivot loops for tempo modulation. His Pioneer DJ "How To DJ" 8-part series (2009) has controller-cam close-ups of the feedback loop, beat roll, and transform moves; the NXS2 trick videos cover Vinyl Brake acid noise and Helix sampling. Because he teaches on camera, he is an L4 (performer-confirmed) source — the calibration standard for the whole reverse-engineering pipeline.
Provenance: edu-survey-G.md §4 (performer shortlist #2), 2026-10-17. Implemented: `feedback_loop_build` (PERF-ZAB), `metric_loop_pivot` (PERF-ZAB, from his 2020 3:4 tempo-modulation demo).

### James Hype — loop-based live edits

Signature: "Hype Loops" (grab a sound, twist it, build tension into the drop), brake tricks, multi-deck "combos" that restructure tracks live, acapella juggling. Footage: behind-the-decks clips, the 4-deck London Underground set (2020), Brooklyn Mirage 2022 transition clips, recent 16-deck rig demos (stem-strip/layering arrangement craft). The rare performer who also teaches: his Digital DJ Tips "James Hype's Mixing Skills" course is ground truth for calibrating extraction.
Provenance: edu-survey-G.md §4 (performer shortlist #1), 2026-10-17. Implemented: `loop_tightening_build` (GAP-02, Hype Loops).

### DJ EZ — CDJ-native speed mixing

31 tracks in 45 minutes: quick-cut frippery, CDJ loop beat-juggles — e.g. a tiny loop of Wookie's "Battle" used as a kick drum under Cleptomaniacs — long subtle blends alternating with hard cuts. Canonical footage: Boiler Room x RBMA London (Dec 2012, close camera); FabricLive 71 for studio-clean audio. The loop-as-instrument move (a fragment looped into a drum role under another track) is the extraction target not yet in the engine.
Provenance: edu-survey-G.md §4 (performer shortlist #7), 2026-10-17.

### The reverse-engineering pipeline (S0–S11)

From edu-survey-G.md §5: **S0** target selection & footage scouting → **S1** source acquisition (video + tracklist + owned source tracks, provenance log) → **S2** mix-to-track alignment → transition regions (ISMIR-2020 style subsequence DTW) → **S3** control-type triage (crossfader-only vs EQ+faders) → **S4** per-band gain-trajectory estimation (NIME-2021 convex optimization — the DJ's actual EQ/fader automation curves) → **S5** FX/loop/pitch signature analysis (pure DSP on the mix alone) → **S6** controller-cam gesture annotation → **S7** gesture↔parameter fusion → **S8** technique hypothesis drafting → **S9** re-render verification (render the hypothesis with this engine; it must match) → **S10** confidence scoring & verdict → **S11** bank entry. Most automatable: S4, S5, S2.
Provenance: edu-survey-G.md §5–§6, 2026-10-17.

### The confidence ladder (L0–L4)

Bank entries require ≥ L2. **L4 — performer-confirmed:** the performer teaches it (Hype's course, Zabiela's trick videos) — these sources validate the pipeline itself: run S2–S9 on an L4 module and the extraction must match what he teaches; if it doesn't, the pipeline is wrong, not the performer. L1 candidates live in `work/`, not the bank.
Provenance: edu-survey-G.md §7, 2026-10-17.

### What the literature recovers — and where it stops

ISMIR 2020 (Kim/Yang/Nam): transition regions, lengths in beats, tempo/key deltas — no gains, no FX. NIME 2021: per-band gain trajectories + control-type classification — FX appear only as reconstruction error. CMMR 2019 (Schwarz & Fourer): placement, time-stretch, fade curves on synthetic mixes (UnmixDB). The papers stop at gain curves; this library's pipeline adds the FX moves, loop/juggle events, the gesture layer, and the why/when-not interpretation.
Provenance: edu-survey-G.md §1, 2026-10-17.

### Mashup discovery (long-tail pairs)

Track pairs can still be found that work together decades later — e.g. Michael Gray "The Weekend" × Daft Punk "Voyager", discovered 20 years on.
Provenance: @djsfrenchcandy, https://www.instagram.com/reel/DeZkcAXB_ps/ (2026-10-12).

### Emotional contrast (lyric mood × key)

Mismatch lyric mood and key — sad lyrics in a major key, happy lyrics in a minor key — to unsettle the listener. A selection-time consideration for vocal overlays and duets.
Provenance: @morsbeats_, https://www.instagram.com/p/CmW84txN9eF/ (2022-12-19).

### The hook test

If you are not involuntarily singing the hook while doing everyday tasks, the hook is not strong enough and needs rewriting. (Selection relevance: this is the field test for "iconic vocal" status that gates T-038/T-025.)
Provenance: @morsbeats_, https://www.instagram.com/p/CmHjFFSNJ5L/ (2022-12-13).
