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
Provenance: Mixed In Key, "Use Advanced Harmonic Mixing Techniques" (book chapter) + "Change DJ Set Energy With the Camelot Wheel" workflow, https://mixedinkey.com — mined 2026-10-21.

### Camelot diagonals and the +4 — far moves are not uniformly clash (Mixed In Key)

The wheel's diagonals are asymmetric: B→A with +1 (8B → 9A) and A→B with −1 (9A → 8B) share notes and work; the reverse diagonal (8B → 7A) contains dissonant intervals and does not. Separately, the +4 same-letter move (10B → 2B, Guetta via MIK) "sounds dissonant at first, but sometimes it works — tracks with simple melodies usually yield the best results." A flat distance ladder that scores every far or cross-letter move as clash erases both distinctions: the working diagonal, and the far move whose condition is melodic simplicity. Banked as selection knowledge; the `camelot_distance` refinement is a BUILD-LOG Phase 9 proposal, not implemented.
Provenance: Mixed In Key, "Use Advanced Harmonic Mixing Techniques" (book chapter), https://mixedinkey.com/book/use-advanced-harmonic-mixing-techniques/ — mined 2026-10-21.
