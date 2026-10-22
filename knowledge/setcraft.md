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
