# Knowledge — Setcraft

Set-level craft: energy planning, hosting moves, genre norms, and the library's documented exclusions. Provenance on every entry (FRAMEWORK.md §1, layer 3).

### Energy planning (bank T-016)

**The scale:** energy is scored 1–10 (spectral flux + RMS + onset density). Reference arcs: warm-up 3–6, peak 6±3.5 (a sine, not a plateau), after-hours 5→2. Transition planning keys off the delta: lateral (±1) → invisible handoffs (eq_blend); up (+2) → builds and collisions; down (−2) → washes and freezes — never fake-lift into a comedown. The T-037 selection rules encode thresholds on this scale (e.g. bass_swap requires energy ≥ 6).
Provenance: technique bank TECHNIQUES.md (T-016), 2026-10-16.

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
