# S2 MIX-TO-TRACK ALIGNMENT — RECORD

Phase 25 (2026-10-22): the staged HÖR Berlin / Boiler Room S2 alignment
tranche from EDUCATIONAL-SOURCES-V2's ranked queue (item 3's staging
note). Method: S0–S11 pipeline (transition-lab/OPEN-SOURCE-LANDSCAPE-
EDUCATION.md §5) at stages S1–S5 + S8–S11 — subsequence DTW mix-to-track
alignment (Kim et al., ISMIR 2020), sub-band gain estimation in the
NIME-2021 band split (low <180 Hz / mid 180 Hz–3 kHz / high >3 kHz),
residual analysis for FX/loop gestures. Gesture stages S6/S7 are out of
scope for this tranche (audio-first); every banked claim carries its
confidence on the landscape ladder: alignment-measured (L1-grade audio
evidence) > tracklist-inferred > watcher-described.

Status: COMPLETE for this tranche (2026-10-22). Sets attempted 3,
aligned 1 (Digweed Transitions 1150). Of its 21 positions: 9 tracks
carried into DTW alignment — 5 solid alignments, 3 proxy alignments
(wrong-mix files of the right song, flagged in place), 1 excluded as
ambiguous. Transitions: 2 adjacent-pair records extracted, 1 fully
measured blend (01→02); the rest bounded or unmeasurable, stated per
pair below. Scratch artifacts (audio, features, paths, alignment.json)
retained under ~/workspace/scratch/s2-alignment/.

## Set selection (S0)

Corpus named by the map (V2 Class 1F/1C): HÖR Berlin + Boiler Room
archives, ground truth = 1001tracklists timestamped tracklists with
`w/` layering notation.

- **Set 1 — Nitepunk @ HÖR Berlin, 2026-10-15** (the Phase 22 proof
  item). 1001tracklists sv3bwh1: 22 positions, 2 `w/` layer events
  (19 w/ Nitepunk & Soh Soh — Conjure; 22 w/ Skrillex — REDLINE DASH),
  6 ID–ID positions (04, 06, 07, 08, 11, 15, 19 — seven counting
  position 18's unreleased Nitepunk ID), 16 identified released
  tracks. Tracklist carries NO timestamps → all positions must come
  from alignment itself. 1 h studio set, fixed-camera HÖR recording
  (clean audio — the gain-trajectory-friendly end of the corpus).
  Track tenure ≈2.7 min/track — the longest in the high-rate class,
  hence the primary alignment target.
- **Set 2 — Andy C @ Moon Stage, Rampage Open Air, 2022-07-01**
  (1001tracklists 1kr297g9). 50 numbered positions + ~25 `w/` layers,
  timestamps to the second (stream-clock 7:05:01→8:02:26+), new layers
  every 30–90 s. The performed counterpart to Phase 23's DnB texts.
  Caveats recorded up front: festival crowd audio; a large minority of
  positions are VIP/bootleg/Patreon-only versions whose source audio
  may be unobtainable — those stay tracklist-inferred, never silently
  upgraded. **Status: mix audio NOT acquired (see Failures) —
  attempted, failed on the YouTube media wall; no alternate public
  audio source (SoundCloud/Mixcloud) carries this set.**

- **Set 3 (substitute primary) — John Digweed, Transitions 1150
  (Guerilla Records Special), 2026-09-11.** Mixcloud official upload
  (mixcloud.com/johndigweed/transitions-1150) — the route that works
  (see Failures for YouTube). Full timestamped tracklist from the
  artist's own listing: 21 tracks / 2 h, timestamps at 15 s
  quantization, all identified, all released (Guerilla Records
  catalogue, 1992–94 progressive house). Track tenure ≈5.7 min — the
  long-blend end of Class 1E, the map's "purest sub-band trajectory
  data". Source tracks: SoundCloud carries full-length uploads of
  most of the catalogue (incl. the label-era mixes); per-track
  identity verified at acquisition (duration + alignment fit), never
  assumed. Structural caveat: six positions are second mixes of a
  song already played (02/03, 07/08, 13/14 same-song pairs; 05/17,
  10/16, 12/21 same-song returns) — chroma alone cannot separate
  same-song remixes; those boundaries bank at the confidence the
  band/gain evidence supports, stated per transition.

## Failures / route findings (S1)

- **YouTube media download is walled from both egress points**
  (this VM and MAC-1, 2026-10-22): every player client probed
  (android, ios, web, tv, tv_embedded, mweb, web_safari, android_vr,
  visionos, mediaconnect, android_creator) returns either the
  SABR-only-streaming error or "Sign in to confirm you're not a bot";
  format listings show m3u8 audio that will not fetch. Metadata
  (search, tracklist pages) works; media does not. This kills the
  Nitepunk mix (HÖR's only public audio home is YouTube) and the
  Andy C set audio, and all YouTube-sourced tracks. Recorded as an
  environment failure, not a corpus failure — both sets remain valid
  targets whenever a route exists. No bypass attempted (no cookie
  scraping, no PO-token tooling, no mirror/ripping sites).
- **Mixcloud works** via yt-dlp (DASH, slow ≈50 KB/s through the
  egress proxy, ~22 MB for a 1 h set at stream bitrate) — Boiler Room
  and Digweed official uploads both fetch. Honey Dijon @ Boiler
  Room Sugar Mountain (Mixcloud) was downloaded as a route proof;
  no timestamped tracklist for it could be confirmed on 1001/MixesDB,
  so it is NOT carried into alignment (kept as an unworked asset,
  scratch only).
- **SoundCloud works** via yt-dlp search + download, fast. Fan
  uploads of catalogue tracks are the availability risk; identity is
  verified per track (below).

## Method (as run)

Set 3 pipeline, as actually executed (deviations from the landscape
design recorded in place):

- **Acquisition (S1).** Mix: Digweed's official SoundCloud upload
  (`soundcloud.com/john-digweed/john-digweed-transitions1150-2`),
  AAC 7201.4 s — duration verified against the 2 h listing. The
  Mixcloud official upload was abandoned mid-download (superseded by
  the SoundCloud route). Tracks: SoundCloud search + direct URLs,
  token-overlap identity gate ≥0.45 at fetch, then ffprobe duration
  check; every fetched file decode-verified (ffprobe) before use.
  Files that failed identity on inspection were replaced or excluded
  in place (see per-track notes) — never silently upgraded.
- **Features (S2).** All audio → mono 22,050 Hz WAV (libsndfile
  cannot read the AAC-in-MP4 containers; ffmpeg converts). Chunked
  STFT chroma (n_fft 4096, hop 2048 ≈ 10.77 fps, L2-normalised) + RMS
  band amplitudes in the NIME-2021 split (low <180 Hz / mid
  180 Hz–3 kHz / high >3 kHz), computed in 600 s chunks.
  **Deviation:** chroma_stft replaces chroma_cqt — CQT over the 2 h
  mix was OOM-killed; STFT chroma is a standard DTW alignment feature
  and the substitution is recorded here rather than hidden.
- **Alignment (S3–S5).** Subsequence DTW (librosa, cosine distance,
  steps [1,1]/[1,2]/[2,1], weights [0,0.4,0.4]) of each track's full
  chroma against the mix window official−240 s … official+900 s.
  Zero-norm (silent) frames sanitised before the cosine metric.
  Per track recorded: aligned start/end, span, start deviation vs the
  official timestamp, tempo ratio (track time ÷ mix time, overall +
  per-half), mean DTW cost, Krumhansl key estimate from mean chroma.
- **Transitions (S8–S11).** For position-adjacent pairs with both
  sides aligned: endpoint overlap; per-band gain trajectories by
  warping each track's band amplitudes through its DTW path,
  normalising by solo-region gains, and solving a per-1 s-block 2×2
  non-negative system per band; per-band 50 %-share crossover times;
  control classification (crossfader_like if crossover spread ≤
  max(3 s, 15 % of overlap), else eq_blend_staggered); residual share
  per band (unexplained energy → FX/third-source flag).

## Results

### Set 1 — Nitepunk @ HÖR Berlin
FAILED at S1: mix audio not acquired (YouTube media wall, above).
No alignment attempted; nothing banked from description.

### Set 2 — Andy C @ Rampage Open Air
FAILED at S1: no acquirable public audio (YouTube walled; no
SoundCloud/Mixcloud source). No alignment attempted.

### Set 3 — John Digweed, Transitions 1150 (21 positions)

Mix audio acquired and verified; 12 of 21 source tracks acquired,
9 carried into DTW (05 excluded on identity, 13/14/16 as flagged
proxies). Not acquired: 03, 04, 07, 08, 10 (correct mix), 12, 15,
17, 18, 20, 21 — SoundCloud official uploads for several are
DRM-flagged ("This video is DRM protected": Spooky and Chameleon
Project catalogue), the rest have no full-length public upload
found; Bandcamp and archive.org routes were probed and are dead
ends for this catalogue.

Per-track alignment (mix seconds; cost = mean DTW cosine cost,
clean-track median ≈0.027):

| # | Track | Start (dev vs official) | Span | Tempo ratio | Cost | Verdict |
|---|-------|------------------------|------|-------------|------|---------|
| 01 | Fuzzy Logic — Obsession (Orbit Quantum Loop) | 0.0 (0.0) | 367.1 | 0.9838 | 0.029 | aligned |
| 02 | Spooky — Little Bullet (Gargantuan) | 357.9 (−2.1) | 411.7 | 1.0050 | 0.026 | aligned |
| 06 | React 2 Rhythm — I Know You Like It (file as fetched) | 2035.9 (+580.9) | 210.7 | 1.0000 | 0.029 | **ambiguous — excluded** |
| 09 | Supereal — Body Medusa (Leftfield Rmx) | 2343.5 (+33.5) | 428.3 | 0.9998 | 0.026 | aligned |
| 11 | Dr. Atomic — Schudelfloss (Spooky Hedonism) | 3021.4 (−38.6) | 385.3 | 1.0188 | 0.017 | aligned (best fit) |
| 13 | R2R — Intoxication [PROXY: HUD Rerub file] | 3802.3 (+22.3) | 251.7 | 1.0007 | 0.027 | proxy-aligned |
| 14 | R2R — Intoxication [PROXY: same file] | 4264.8 (+49.8) | 251.8 | 1.0004 | 0.030 | proxy-aligned |
| 16 | D.O.P. — Groovy Beat [PROXY: Apetzu remix] | 5105.1 (+170.1) | 242.1 | 1.0019 | 0.077 | proxy, weak |
| 19 | Lemon Sol — Aquamarine (Deep Blue) | 5952.5 (−17.5) | 405.6 | 0.9647 | 0.034 | aligned |

Findings, at the confidence each carries:

1. **Official timestamps are cue-approximate (alignment-measured).**
   Start deviations for the five solid tracks: 0.0, −2.1, +33.5,
   −38.6, −17.5 s (RMS ≈26 s) against a listing quantised to 15 s.
   Any future alignment against artist-published timestamps needs
   search windows of at least ±60 s; treating them as exact would
   misplace three of five tracks.
2. **Tempo adjustments all inside Kim et al.'s <5 % band
   (alignment-measured).** Mix-vs-source tempo moves: 01 +1.65 %,
   02 −0.50 %, 09 −0.02 %, 11 −1.85 %, 19 +3.66 % — 5/5 under 5 %,
   agreeing with the corpus stat (86.1 % of 20,765 transitions
   adjust <5 %). Per-half ratios are near-identical within each
   track (e.g. 11: 1.0188/1.0188; 19: 0.9625/0.9669) — these are
   constant pitch rides set at the deck, not drift or warping.
3. **Track 06 is an identity failure, recorded not resolved.** The
   fetched file (titled as the Fabio Paras Remix of I Know You
   Like It) aligns at full length, ratio 1.0000, cost 0.029 — but
   at 2035.9 s, inside position 08's window, which contradicts the
   published order given anchors 02 and 09. Either the upload is
   mislabelled (its content is a different position's track) or the
   DTW locked onto same-family loop material; the record cannot
   distinguish, so 06 banks nothing and its neighbours' transitions
   stay unmeasured.
4. **Same-song positions confirm positionally, not by mix
   (proxy-measured).** One HUD Rerub file of Intoxication aligns at
   BOTH Leftfield positions (13 and 14) at near-clean cost —
   rerub/remix audio of a song cannot identify which mix plays,
   exactly the stated structural caveat. Position 16's proxy fits
   at 2.7× clean cost with +170 s deviation: tentative placement
   only.
5. **Transition 01→02 — the tranche's one fully measured blend
   (alignment-measured).** Endpoint overlap 9.2 s. Per-band 50 %
   crossover times inside the overlap: mid 3.7 s, low 5.5 s, high
   5.5 s — spread 1.8 s → crossfader-like control (all bands hand
   over together, mid marginally first), B-share 0→1 in every
   band. Residual share: mid 0.011, high 0.009 (the two-source
   model explains the blend almost completely there), low 0.092
   (a small unexplained low-band remainder — consistent with bass
   management or rumble, not enough to claim a third source).
   Against Kim/Yang/Nam's corpus split (28 % crossfader-only /
   72 % EQ-blend), this set-opener sits in the crossfader minority.
   n=1: knowledge-grade, not a new base.
6. **One-sided overlap bounds (alignment + tracklist).** 09's
   audio persists to 2771.8 s vs position 10's listed start
   2670 s → ≥~102 s of coexistence past the listed cue (≥~62 s
   allowing the ±40 s timestamp error) — a long-blend lower bound
   for 09→10. 11 ends 3406.6 s vs 12's listed start 3405 s →
   11→12 handover is tight (overlap ≈0–40 s). 02's apparent end
   (769.6 s) vs 03's listed start (615 s) is NOT banked: 02/03 are
   two mixes of the same song and chroma cannot separate them —
   the span is an artefact of same-song similarity.
7. **Key estimates (low confidence, corroboration only).**
   Krumhansl on mean chroma: 01 A major (r 0.62), 02 A# minor
   (0.86), 09 F major (0.54), 11 F# minor (0.82), 19 D# major
   (0.57). No transposition-scale key moves are evidenced; nothing
   banked on keys beyond this note.

Banked from this tranche: 3 knowledge entries (setcraft ×2,
workflows ×1). New bases: none — no measured gesture was
mechanism-distinct from the existing crossfade/EQ families.
Axes/variants: none — a single measured transition does not
justify re-staging an existing base. Both zeros are deliberate:
the tranche banks what the measurements support, and the
measurements support calibration, not new technique claims.
