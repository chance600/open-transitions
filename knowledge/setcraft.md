# Knowledge — Setcraft

Set-level craft: energy planning, hosting moves, genre norms, and the library's documented exclusions. Provenance on every entry (FRAMEWORK.md §1, layer 3).

### Energy planning (bank T-016)

**The scale:** energy is scored 1–10 (spectral flux + RMS + onset density). Reference arcs: warm-up 3–6, peak 6±3.5 (a sine, not a plateau), after-hours 5→2. Transition planning keys off the delta: lateral (±1) → invisible handoffs (eq_blend); up (+2) → builds and collisions; down (−2) → washes and freezes — never fake-lift into a comedown. The T-037 selection rules encode thresholds on this scale (e.g. bass_swap requires energy ≥ 6).
**Calibration (Mixed In Key's published anchors for the same 1–10 scale, Phase 9):** level 2 = chill, no beat; 5 = lounge; 6 = the danceability threshold; 7 = upbeat; 9–10 = festival anthems. A +2 delta that crosses 5→6 or 8→9 changes kind, not just degree.
Provenance: technique bank TECHNIQUES.md (T-016), 2026-10-16; anchors: Mixed In Key founder interview, 1001tracklists, mined 2026-10-21.

### Genre transition norms (bank GAPS.md #10)

- **Hip-hop / open format:** quick cuts, stutter (T-019), wordplay (T-011), hard cuts (T-030).
- **House / techno:** long blends (T-001), filter sweeps (T-003), layered FX.
- **DnB / dubstep:** double drops (T-024), drop swaps (T-014).
- **Trance / progressive:** breakdown transitions (T-023), reverb wash (T-005).
- **Pop:** punchline snaps (T-025), genre bridges (T-026).
The selection engine (`engine/select.py`) encodes these as genre-norm scoring bonuses.
Provenance: technique bank GAPS.md #10, 2026-10-16.

### Siren / horn placement (bank T-036 — documented exclusion)

The airhorn is governed by a scarcity law: **once per set, maximum**, on the 1 of the biggest drop, 0.5–1.0 s, at unity, high-passed at 1 kHz, never over a vocal or a breakdown. The second blast halves the first's impact. Placement is a human hype decision — the library registers it as an exclusion (FRAMEWORK.md §9) so selection can explain its absence; it is never auto-deployed. (Reggae/dancehall sound-system culture treats the horn conversationally — a tradition, not a transition technique.)
Provenance: technique bank TECHNIQUES.md (T-036), 2026-10-16.

### Holding-pattern loop (documented exclusion)

An outro groove looped indefinitely as a set tool — buy time, recover, reset while the next track is prepared. The bank's T-027 discipline caps *transition* loops at 2 cycles, so the indefinite form lives here as a SET-level recovery plan, registered as an exclusion in `engine/meta.py`, not as a transition technique.
Provenance: Transition Gap Report 2026-10-19 (gap 3, flagged † deliberate exclusion).

### Mic talk-over reset (GAP-18)

Talking over the outgoing track's outro on the mic to reset the room, then dropping the next track cold. A hosting move, not an audio operation — specified as a planning entry (`mic_talkover_reset`, techniques/mic_talkover_reset.md), never ranked by the selection engine.
Provenance: Transition Gap Report 2026-10-19 (gap 18, open-format source).

### Extended-set philosophy

Long-form/open-to-close sets are where the musical statement happens (6 hours in Guadalajara, 10.5 hours recorded at Stereo Montreal) versus short slots; deep, melodic, emotional tracks as journeys that take their time unfolding rather than rushing to a payoff.
Provenance: @enamourmusic, https://www.instagram.com/p/DYxmbCTku5c/ (2026-05-25) and https://www.instagram.com/p/Deju63kEUMw/ (2026-10-16).

### Vary the set, don't repeat it

At Burning Man he deliberately chose sets that would each be a totally different vibe from one another, rather than repeating one set across camps.
Provenance: @enamourmusic, https://www.instagram.com/reel/Dce1du_vG16/ (2026-08-25).

### Less is more on the dancefloor

Just a few percussion elements plus an open hi-hat is enough to keep the dancefloor grooving.
Provenance: @mattstonedj, https://www.instagram.com/reel/DdgpkdcNv2o/ (2026-09-20).

### Arrange by contrast

Deliberately create a contrast moment so the track (and by extension the set) feels exciting and has somewhere to go.
Provenance: @marshalljamesmusic, https://www.instagram.com/reel/DZGGVE2B6fR/ (2026-06-02).

### Reps beat tutorials

Watching 100 bassline tutorials will not make you good at basslines — making 100 basslines will. Tutorials and lessons help; there are no shortcuts. Related: expect ~1,000 rejections/ignores before the first yes; copy other producers to learn their techniques without recreating every detail; and don't let AI learn the fundamentals for you — use it to speed up workflow, not to skip learning.
Provenance: @marshalljamesmusic, https://www.instagram.com/reel/Dd4EeueBWTa/ (2026-09-29).

### Capture the first take

A first-take solo played on an expressive instrument (Soma Terra) shaped the track "Won't Let You" — capturing a live first take as the core of a record.
Provenance: @enamourmusic, https://www.instagram.com/reel/DOgNGtAiK1P/ (2025-09-12).

### Energy Boost Mixing — key movement is an energy event (Mixed In Key)

Mixed In Key's named doctrine: mixing *up* in pitch lifts the floor independently of the tracks' energy levels. +2 Camelot numbers, same letter (two semitones up) is the standard boost — "the best mix," safer than one semitone; +7 numbers (= −5 the short way round; MIK's current workflow page names it the "-5 move") is one semitone up, the sharper boost. Conditions: mix a boost **quickly** — the keys are incompatible, melodies clash, it is not a long-blend move; time it across percussive sections; support it with a higher Energy Level; use in moderation or the set feels forced. The mirror (−2 counter-clockwise) is an energy drop: a deliberate wind-down / closing signal. Selection consequence: key distance is *directional* — the same wheel step reads as lift going up and release going down, which a symmetric distance score cannot express (select.py proposals, BUILD-LOG Phase 9).
**Implemented (Phase 10):** `engine/select.py` now derives a signed `key_move` feature (tonic semitone delta, −6..+5) and an `energy_boost` flag (key_move +1/+2 with energy_delta ≥ 0); snap/void exits earn a +1.0 preference on boost pairs via `_boost_bonus` — the quick-mix rule as scoring, while seamless/tail gates are untouched. Guarded by check_select Case 7.
Provenance: Mixed In Key, "Use Advanced Harmonic Mixing Techniques" (book chapter) + "Change DJ Set Energy With the Camelot Wheel" workflow, https://mixedinkey.com — mined 2026-10-21.

### Camelot diagonals and the +4 — far moves are not uniformly clash (Mixed In Key)

The wheel's diagonals are asymmetric: B→A with +1 (8B → 9A) and A→B with −1 (9A → 8B) share notes and work; the reverse diagonal (8B → 7A) contains dissonant intervals and does not. Separately, the +4 same-letter move (10B → 2B, Guetta via MIK) "sounds dissonant at first, but sometimes it works — tracks with simple melodies usually yield the best results." A flat distance ladder that scores every far or cross-letter move as clash erases both distinctions: the working diagonal, and the far move whose condition is melodic simplicity. Banked as selection knowledge; the `camelot_distance` refinement is a BUILD-LOG Phase 9 proposal, not implemented.
**Implemented (Phase 10):** the working diagonal scores 2 inside `camelot_distance` itself (check_select Case 6); the +4 gate is pair-level — an upward same-letter +4 move on a vocal-free pair (`vocal_pair == "neither"`, the interim simplicity proxy) reads an effective 3 in `derive_features`, with the raw ladder preserved as `camelot_raw` (Case 8). camelot_max ≤ 2 techniques stay closed to gated pairs.
Provenance: Mixed In Key, "Use Advanced Harmonic Mixing Techniques" (book chapter), https://mixedinkey.com/book/use-advanced-harmonic-mixing-techniques/ — mined 2026-10-21.

### Compatibility vs modulation — the two modes of key movement (Club Ready DJ School)

Club Ready's harmonic-mixing guide frames the same territory as two modes with different jobs: **compatibility mixing** (same key, ±1, A↔B switch) exists for smoothness — mashups, acapellas, long blends, extended layering — while **modulation mixing** (larger wheel jumps) exists for movement: energy, lift, impact, timed around drops. Their discipline matches the registry's split exactly: the ladder band governs long-overlap families, boosts are quick events. Two further data points, recorded at their evidentiary weight: (1) the guide lists +4 among the *least forgiving* relationships (+4/+6/+8/+10) — compatible with the simplicity-gated +4 exception above, not a contradiction of it: ungated +4 is dissonant, the gate is the condition; (2) the author's personal +9 note — the same-letter +9 move (a minor third up at the tonic, four of seven scale notes shared) "often sounds surprisingly good... fresh without feeling completely disconnected." Single-source personal preference, NOT adopted into the ladder — recorded here as a named modulation color for set-level use only. The guide's governing rule is also the program's: "the longer two songs overlap, the more important harmonic compatibility becomes" — quick outro swaps and drop replacements are explicitly exempt, which is the quick-mix rule stated from the teaching side.
Provenance: Club Ready DJ School, "How To Mix In Key: The Complete Guide To Harmonic Mixing For DJs" (Tribe Talk blog), https://www.clubreadydjschool.com/tribe-talk/mix-tips/how-to-mix-in-key-the-complete-guide-to-harmonic-mixing-for-djs — mined 2026-10-21.

### Trainwreck salvage (failure exits)

Every rendered transition has a failure state, and the practitioner's salvage repertoire is short: abort the blend to a single track (the cut is the universal abort — it cannot clash because only one track remains), re-cue the incoming track and re-attempt while the outgoing still has time, or mask the wreck socially (mic) while resetting. Selection consequence: hard-cut-class exits are the library's zero-clash-risk family precisely because they double as every other technique's failure exit — a failed blend degrades to a cut, never to a worse blend. A trainwreck's cost is reputational, not structural: "it's not the trainwreck itself but how you deal with it that really matters."
Provenance: Digital DJ Tips, "5 Ways To Salvage A Trainwreck" (digitaldjtips.com/5-tricks-to-recover-from-a-trainwreck/), mined 2026-10-21 (Phase 11, community-layer pass); the abort-to-one-track reading is the bank's.

### Tempo Master succession — whose tempo governs after the bridge (Traktor AUTO mode)

Every tempo move silently answers a question the render itself doesn't ask: once the transition completes, whose tempo is the set's tempo? Traktor's AUTO mode states the performance answer as a succession rule — when the Tempo Master deck's track ends or is stopped, the synced deck automatically becomes the new Tempo Master; when no deck remains synced, the Master Clock takes over as the standing reference. The Transport preferences refine it: only decks that can be master are eligible (Track/Stem, not Remix), and "only on-air decks" restricts succession to decks actually playing to the main output. Mapped onto the registry: a T-021 pair-ramp ends with authority on B by construction (the ramp's destination *is* the succession); a same-tempo blend has no succession event at all; and a ferryman/loop-held bridge defers succession to the layer's exit, which is why the neutral layer must be tempo-agnostic while it holds. Set-level rule, not a renderer: selection already encodes it implicitly in which side of a pair a technique treats as reference — this entry names it (study program tranche 7, 2026-10-21).
Provenance: Native Instruments, Traktor Pro 4 manual — Global Concepts, "Tempo Synchronization" (Automatic Tempo Master Assignment; Customizing Tempo Master Behavior), https://www.manua.ls/native-instruments/traktor-pro-4/manual , mined 2026-10-21.

### Tempo ≠ energy — the Tempo Rollercoaster (Laidback Luke)

Luke's course devotes a full section to performing big BPM and genre changes, and its first lesson separates the variables the rest of the section then exploits: "Understanding tempo vs energy." Tempo is a number; energy is the crowd's state, and the two are not locked — a set can move down in BPM while moving up in energy (density, register, familiarity all pay energy independently of the clock), which is what makes his "Tempo Rollercoaster" a ride rather than a series of accidents: large tempo moves in both directions, planned as energy events. This is the tempo-side counterpart of the Mixed In Key energy doctrine above (key movement as an energy event): selection should score a pair's tempo delta and its energy delta separately, because techniques exist for spending either while holding the other — the T-021 family spends tempo, the quick-mix/drop family spends neither and buys energy with density. Recorded as the performer's statement of a distinction the registry's `energy_delta` feature already assumes (study program tranche 7, 2026-10-21).
Provenance: Digital DJ Tips, "Laidback Luke Teaches Mixing" course curriculum, section iv "Performing Big BPM & Genre Changes" (lesson titles), https://milled.com/learn-to-dj-with-virtual-dj-home-online-video-course/54-mix-techniques-33-lessons-1-big-transformation-sgYpVB67ambzz-by — mined 2026-10-21.

### The throwback — a callback layer from earlier in the set (DJ Courses Online)

A set-level move stated in DJ TLM's school's performance-EQ teaching: partway through the set, bring back an earlier track — "cut the highs and let it run for 32 bars over your next track" — using a distinctive, recognizable bassline or mid figure the crowd has already been primed by, then plough on with the mix. It is not a transition between the current pair; it is a third source whose identity is *the set's own history*, layered briefly (the teaching is explicit: an easter egg, never the whole song again). In registry terms it is the layer family (T-020 `three_deck_layer`, GAP-16 `spare_deck_element_firing`) with the layer's source axis set to *previously played*: selection gains nothing renderable — no pair feature predicts it — but the move explains a class of long-set moments no pair model produces, and it is the positive form of the trainwreck-salvage entry's premise that a set is a sequence with memory, not a chain of independent pairs (study program tranche 8, 2026-10-21).
Provenance: John Bartmann, "The Performance Approach To EQing" (Bringing it back), DJ Courses Online DJ Blog — DJ TLM's school, https://djcoursesonline.com/dj-blog , read first-hand 2026-10-21.

### Fuzzy key sync — the sync target is a compatibility set, not a key (Engine DJ)

Engine DJ 3.2 splits Key Sync into two modes and names the difference: **Strict** syncs to the same key; **"Fuzzy"** syncs "to the closest compatible key instead of the same key," explicitly to avoid "potentially large jumps in pitch when key syncing 2 or more tracks." The doctrine hiding in the feature is that key identity is the wrong target for a sync operation: the compatible neighborhood (the registry's distance ladder — same, relative, ±1, the working diagonals) is a set of acceptable destinations, and the correct sync is the *cheapest move into the set*, not the exact match at any pitch cost. This is Club Ready's compatibility mode (above) stated as a vendor default rather than a teacher's preference, and it is the performance form of what select.py's `camelot_distance` already scores: a pair is not in-or-out of key, it is at a distance, and the distance is a price. Recorded as the third first-party anchor for the compatibility model (MIK's ladder, Club Ready's modes, Engine's sync) (study program tranche 8, 2026-10-21).
Provenance: Engine DJ, "Engine DJ v3.2.0 Now Available" (Fuzzy Key Mixing), https://enginedj.com/news/articles/engine-dj-v3-2-0-now-available-day-mode-fuzzy-key-mixing-flex-gate-fx-and , read first-hand 2026-10-21.

### Restraint — energy headroom is a set-level resource (Passionate DJ)

David Michael's restraint doctrine (Passionate DJ, "Restraint & Patience", Podcast #075) prices the warm-up failure as an energy-budget error: the impatient opener is "advancing the energy of the night too quickly (how can you find room to ebb-and-flow when you're already starting at 10?)" — peak energy spent early cannot be spent again, so the set's arc flattens no matter what follows. The mechanism-level claims: the value-subtractors are density moves played as decoration ("overuse of effects and filters, looping 12 tracks on top of each other"), and what survives every technology shift is selection, crowd-reading, and story — "the ability to play the right tracks at the right time, and the ability to tell a story through the presentation of recorded music." In this repo's terms it is the floor discipline between Luke's density doctrine (how much technique per minute) and A-Trak's risk rule (how much ambition per set): the energy curve itself is a budgeted resource, and restraint is how it is saved for when the room can use it (study program tranche 9, 2026-10-21).
Provenance: David Michael, "Restraint & Patience: The DJ's Lost Virtues", Passionate DJ Podcast #075, 2017-01-16, https://passionatedj.com/restraint-as-a-dj-when-less-is-more/ , read first-hand 2026-10-21.

### Key Sync's candidate set — least change over six named relatives (Pioneer CDJ-3000)

The CDJ-3000's manual body states its Key Sync rule as a set-membership test with a price: on [KEY SYNC], "the key is adjusted to the key with the least change among the following — Same key, Dominant key, Subdominant key, Relative key, Relative key of dominant key, Relative key of subdominant key." The six candidates are not an arbitrary list: in wheel terms they are the same position, the two fifth-neighbors (dominant/subdominant), the relative (mode flip at the same position), and the relatives of the two fifth-neighbors — the two diagonals. That is precisely the neighborhood this repo's `camelot_distance` treats as cheap since the Phase 10 P1 refinement scored the working diagonals at 2: Pioneer's hardware charges a diagonal exactly what it charges a fifth-neighbor when the semitone cost ties, and picks whichever member of the set costs the least pitch shift. Read beside Engine's Fuzzy mode (above), the two vendors implement the same doctrine at different grains — Engine names the set ("closest compatible"), Pioneer enumerates it — and both refine the rekordbox software chapter's exact-target statement (Phase 14): the sync target is a compatibility set with a least-cost rule, and the set's boundary is the distance-2 neighborhood. Fourth first-party anchor for the compatibility model, and the first stated by the player hardware rather than the software (study program tranche 12, 2026-10-22).
Provenance: Pioneer DJ, CDJ-3000 Instruction Manual, "Key Sync" (p.69), https://www.manualsdir.com/manuals/855416/pioneer-dj-cdj-3000-high-resolution-pro-dj-multiplayer-black.html?page=69 , read first-hand 2026-10-22.

### Key stability is the default — energy from arrangement, not key change (EDM Tips)

Will Darling's arrangement doctrine, read first-hand, states the producer-side premise the compatibility model assumes: one micro progression (two to four chords, a single key) carries the whole track, and "the energy comes from melody, automation, and arrangement of elements" — the stuck producer's named wrong turns are adding more chords, changing key, and writing multiple progressions. A second progression, when used at all, is bounded by three rules: stay in the same key, reuse chords from the main progression, keep it short — "the goal is contrast — not confusion." In this repo's terms: the unmarked pair is *no key move at all*, and the move is a priced, marked event — which is why the ladder can charge distance at all, why Club Ready's compatibility mode is the default and modulation the exception (above), and why select.py's P3 gate lets only simple material pay the +4 price. The doctrine's macro half (vary which part of the progression plays, which elements play it, and the density) is the layer family's arrangement form, and its study method — mapping a reference track's macro arrangement — is the same element-inventory move Oscar teaches (study program tranche 14, 2026-10-22).
Provenance: Will Darling, "THE Fastest Way to Arrange a Track", EDM Tips, https://edmtips.com/fastest-way-to-arrange-a-track/ , read first-hand 2026-10-22.

### Composite-track staging — one perceived track, three or four sources (Zabiela, Balance 029)

Zabiela's Balance 029 (58 tracks across two acts, assembled over a year in a DDJ-RZ + Ableton back-and-forth) states its method in his own words: songs chosen to have "'conversations' with each other", focus "very heavily on melody", and a microcosmic layering in which what sounds like one track is the bones of one record carrying specific elements of others — the review of record names the peak instance: Redlight's "City Jams" "perfectly blending with elements of three other tracks". At set scale this is the layer family's staging doctrine: the unit of setcraft is not the track but the *composite*, and transitions inside a composite are element swaps, not joins — which is why his ratio reads ~15 tracks/hr while the gesture rate runs 30+/hr. The same mix supplies the set-ending form: Act 1 closes with a sudden halt designed to mimic running out of tape — the tape-stop exit (DM-A05) promoted to a *set-level* gesture, the whole journey cut as if the medium failed. Caveat stated in place: Balance is a produced mix CD, not a live set — the composites are evidence for the staging doctrine and for what the layering can carry, not for live feasibility at that density.
Provenance: We Own The Nite NYC, "LISTEN: James Zabiela mixes Balance 029" — full Act 1/Act 2 tracklists + his mission statement, fetched first-hand 2026-10-22, https://weownthenitenyc.com/listen-james-zabiela-mixes-balance-029/ (study program expansion tranche 1 / Phase 22, 2026-10-22).

### Density modulation — cut passages and long holds as alternating modes (DJ EZ)

EZ's documented sets run two densities as deliberate alternating modes, not one style: the Boiler Room x RBMA set (Dec 2012) cuts 31 tracks in 45 minutes (≈41/hr, quick-cut frippery, CDJ loop juggles), while FABRICLIVE 71 (32 tracks / 75.5 min ≈ 25/hr) is built with documented long-hold blends — and fabric's own style statement names both halves in one sentence: "hard and fast cutting, volume manipulation, loops, effects and drops *with long subtle mixes*". The setcraft point: transition density is a *variable the set modulates* — cut-dense passages spend attention, long holds bank it — and a performer's tracks/hr figure is meaningless without its mode split. For selection this prices density as a set-level arc decision made before any pair is chosen; inside a passage, the mode is the constraint the pair-level pick must satisfy.
Provenance: Mixmag, "The 20 Best DJ Mixes of the Decade" (Boiler Room 31/45 count), via BCR001 Five Mixes Rewind, fetched 2026-10-22; fabriclondon.com, FABRICLIVE 71 newsflash + full 32-track listing via Clash/Resident Advisor, fetched 2026-10-22 (study program expansion tranche 1 / Phase 22, 2026-10-22).

### DnB dwell arithmetic — 44, 66, or 88 seconds a track (note.com)

DnB set construction has stated numbers. At ~174 BPM the sections run ~16 bars; 8 bars is ~11 seconds, and the counted dwell per track lands in three quanta: **44 seconds** (shortest — drop excerpt plus seam), **1:06** (slightly longer), **1:28** (longer); beyond that a track is being held deliberately, for a break-led energy change or a closer played to the end. A 60-minute set therefore runs a little over 50 tracks, and the taxonomy's author structures the hour in five parts — opening (~3 tracks), Part A (~15, steady key/pace, one short break), Part B (~8 vocal/different-taste tracks layered from a break), Part C (~20, the mash-up game at full rate), closing (~4, the last track chosen first and the approach arranged backwards from it). The setcraft claim: in high-rate genres the *dwell quantum* is the unit of arc design — energy changes are scheduled in counts of tracks-at-44-seconds, and "density" (Phase 22's EZ entry) is just the dwell distribution's other name.
Provenance: kohadachan, "A Personal Drum and Bass DJ how to" (note.com, 2024), "Sense of Time" + "My personal idea of how to assemble a set list", fetched first-hand 2026-10-22 (Phase 23).

### NUKG short-blend doctrine — a few bars, peak picture over narrative (RA on Conducta)

The new UK garage school states its mixing doctrine by contrast: Conducta's blends are "fast and precise, normally just a few bars long," the set "less concerned with crafting a narrative than... painting a picture of a garage rave at its peak, spin-backs, gun fingers and all" — 38 tracks sequenced at few-bar dwell with the energy held at peak throughout, where the older UKG master (EZ, Phase 22) alternates cut passages with long holds. The doctrine's elements: vocal-led 2-step sequencing, chart-hit remixes deployed as recognition events ("garage DJs are often not afraid of deploying a well-timed hit"), and the rewind as furniture — the mix's own tracklist carries a tune titled "Wheel Up," the pull-up having become repertoire, not just gesture. For the registry this is the UKG staging bound: blends of 2–4 bars are the genre's default seam, and long-blend bases are the exception that must justify itself — the inverse of the house default. It also closes the map's UKG cell honestly: no UKG transition *educator* exists in text; the tradition's doctrine is carried by its performed mixes and their reviewers.
Provenance: Resident Advisor, review of Conducta, *The Kiwi Sound* (2020), fetched first-hand 2026-10-22 (Phase 23).

### Alignment-measured calibration — Digweed, Transitions 1150 (Phase 25)

The bank's first mix-to-track alignment (subsequence DTW of source tracks against the full mix; record: repo ALIGNMENT.md) measured John Digweed's Guerilla Records special (21 tracks / 2 h) at five solid positions, and the numbers calibrate two things the registry previously took on statement. First, the artist's own published timestamps are cue-approximate: measured track starts deviate 0.0, −2.1, +33.5, −38.6, −17.5 s from the listing (RMS ≈26 s on a 15 s-quantised list) — alignment work must search ±60 s windows around published timestamps, not trust them. Second, every measured tempo adjustment sits inside Kim et al.'s corpus band: +1.65 %, −0.50 %, −0.02 %, −1.85 %, +3.66 % (5/5 under 5 %, vs the corpus's 86.1 % of 20,765 transitions), and each track's per-half DTW slope is constant (e.g. 1.0188/1.0188) — the moves are pitch rides set once at the deck, not drift. One-sided overlap bounds from the same run: Body Medusa's audio persists ≥~102 s past the next track's listed start (a long-blend lower bound), while Schudelfloss ends within ~2 s of its successor's listed start (a tight handover) — the same set runs both dwell extremes, at track tenures of ~6 min.
Provenance: Phase 25 S2 alignment tranche, measured first-hand 2026-10-22 (alignment-measured confidence; full per-track table + method in repo ALIGNMENT.md). Corpus comparison: Kim et al., ISMIR 2020 (1,557 mixes / 20,765 transitions).

### A measured crossfader-class opener — and alignment's same-song blind spot (Phase 25)

The one fully measured blend of the Phase 25 alignment (Transitions 1150, Fuzzy Logic — Obsession → Spooky — Little Bullet) is crossfader-class by the NIME-2021 recovery method's own test: per-band 50 %-share crossover times inside the 9.2 s endpoint overlap land at mid 3.7 s / low 5.5 s / high 5.5 s — a 1.8 s spread, all bands handing over together with the mid marginally first, against the corpus's 28 % crossfader-only / 72 % EQ-blend split (Kim/Yang/Nam, 3,930 transitions). The two-source model leaves almost no unexplained energy in mid (0.011) and high (0.009); the low band's 0.092 residual is recorded as bass-management-scale, not a third source. The same run marks the method's limit, which future alignment tranches inherit: adjacent mixes of the *same song* (positions 02/03, 13/14 in this set) cannot be separated by chroma — a rerub file of Intoxication aligned at both Leftfield positions at near-clean cost — so same-song boundaries bank positionally at best, and a fetched file whose DTW optimum lands inside a different position's window (this run's track 06) is an identity failure to record, never a placement to bank.
Provenance: Phase 25 S2 alignment tranche, measured first-hand 2026-10-22 (alignment-measured; method + full record in repo ALIGNMENT.md). Method kin: Kim, Yang & Nam, NIME 2021 (sub-band gain recovery, low <180 Hz / mid / high >3 kHz).

### Feeler tracks (PulseDJ)

An open-format set does not commit to its direction up front — it probes. A feeler track is a short, low-commitment deployment whose purpose is information, not payoff: drop a genre, a tempo, or an era for a verse and read whether the room follows. If it follows, the set pivots toward it; if it doesn't, the feeler costs one track, not the night. The doctrine pairs with the BPM-barrier law (the feeler lands on a structural anchor) and with energy tagging (the feeler's tag tells the DJ what it tested). A set without feelers is a set that guesses its room once, at the first track.
Provenance: PulseDJ blog, open-format guide, fetched first-hand 2026-10-24. (Phase 27.)

### Energy tagging 1–5 (PulseDJ)

Tag every track 1–5 on energy before the set, and the set becomes plannable: the DJ sees the night's altitude curve on paper instead of feeling for it mid-mix. The tags do three jobs at once — they sequence the arc (no 5-after-5 without a dip), they ration the boosts (an energy-boost lift spends a tag step, not just a key step), and they make the pivot legible (a feeler that tests a 4-tag direction is a different bet from one that tests a 2-tag direction). Tagging is setcraft infrastructure, not metadata decoration: the registry's energy_delta feature is the per-transition form of the same number.
Provenance: PulseDJ blog, open-format guide, fetched first-hand 2026-10-24. (Phase 27.)

### Room-reading and the pivot doctrine (PulseDJ)

The set's plan is a hypothesis and the room is the evidence. PulseDJ's pivot doctrine: read the room continuously (movement, attention, the feelers' returns) and pivot the plan when the evidence turns — change genre, tempo, or era at a structural anchor rather than defending a plan the room has stopped following. The pivot is not failure; it is the job. The failure is the opposite: a DJ who plays the planned set to an emptying floor because the plan was good on paper. The pivot's mechanics are the registry's reset and bed bases (WEB-31, WEB-32) — the doctrine tells the DJ WHEN to reach for them.
Provenance: PulseDJ blog, open-format guide, fetched first-hand 2026-10-24. (Phase 27.)

### Power block mixing — a set plan, not a base (Mixed In Key)

MIK's power block is a SET plan with full parameters, and it is banked here rather than as a registry base because no single transition renders it: rapid 20–30 s hook-to-hook cycling through compatible keys at matched energy, rhythm never broken, with a dip rule after several bangers (the block earns its rest). The parameters are the entry: segment length 20–30 s, key compatibility required across the whole block (not per-transition), energy matched or rising within the block, dip after the block, never inside it. As a base it would be unnameable (a block is a sequence, not a seam); as setcraft it is a complete, performable plan.
Provenance: Mixed In Key wiki, "5 mixing techniques every DJ should know" (power block mixing), fetched first-hand 2026-10-24. (Phase 27.)

### Transition-track selection rule (Crossfader + PulseDJ)

A transition track is chosen by its internal structure, not its genre label. The rule, stated identically from both sources: the track must contain a natural internal BPM shift (an intro that builds through tempos, a breakdown that re-enters at a new pace) or an energy/BPM mismatch with its neighbours that makes the switch itself non-jarring. A track without either property is just a track — it bridges nothing, and deploying it as a bridge strands the set mid-tempo. The rule is the selection gate for GAP-07's transition-track edit family: the edit can stage a bridge, but only a track that already shifts can BE one.
Provenance: Crossfader, "How To Mix Hip Hop" (transition-track selection) + PulseDJ blog, open-format guide (transition track row), fetched first-hand 2026-10-24. (Phase 27.)
