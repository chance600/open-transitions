# Knowledge — Mixing

Mix craft distilled from the user's saved clips and creator pages. Documented techniques with provenance (FRAMEWORK.md §1, layer 3) — not renderable DJ transitions. Paraphrases, never verbatim. DM source thread: `542187470506577`.

## From his saved clips

### Weeknd-style crisp vocal chain (Logic stock only)
In order: pitch correction → channel EQ → de-esser → studio VCA compressor → vintage tube EQ → parallel compression on an aux → delay throw → Space Designer → tape delay → pitch shifter for widening → EVOC-20 PolySynth as vocoder at the end.
Provenance: raffer, https://www.instagram.com/reel/DFqJL1FMEys/ , saved 2025-02-05. (DM-A05; banked as a mixing chain — the earlier "overlaps T-004" flag was about the delay-throw element only.)

### Sidechain saturation (Delta concept)
The sidechain signal is summed with the main signal inside the distortion stage, then subtracted from the audible output — the sidechain stays dry while the main source keeps its distorted character: crunch that retains headroom with less traditional ducking. Ten saturation models, multiband, envelope-following filters.
Provenance: NEST Acoustics, https://www.instagram.com/reel/DHEPZz9x_sy/ , saved 2025-03-15. (DM-A19)

### Flattenator return-track heat
Drop the stock Flattenator onto a return track and dial a few dB of send from any synth/instrument — the jacked-up compressor preset adds aggressive compression and "heat."
Provenance: Max & Dana (@maxanddana), https://www.instagram.com/reel/DLuz6DaA4v6/ , saved 2025-07-19. (DM-A25)

### Transient control with soft clipping (StandardCLIP)
Put StandardCLIP on a clashing snare/clap, lower the threshold to shave transient peaks without changing the snare's shape, then add gain for body and tone while retaining headroom. Works from hats to basslines; doubles as a mastering tool.
Provenance: Max & Dana, https://www.instagram.com/reel/DLso5CUvLsv/ , saved 2025-07-19. (DM-A26)

### Movement for flat chord stacks
Basic reverb + Auto Filter with LFO amount/rate, filter frequency lowered for a slow sweep, automation duplicated across the clip, slight Drive, LFO amount automated to rise over time. Static chords become rhythmic, evolving.
Provenance: ROYALTY-FREE VOCALS, https://www.instagram.com/reel/DZLd953yDAJ/ , saved 2026-06-30. (DM-A37)

### Vocal tuning with Auto Shift
Strength 100%, custom scale rooted on C with only C♯, D♯, F♯, G♯, A♯ enabled, Smooth on — the plugin tracks sung pitch in real time and pulls it to the allowed notes.
Provenance: Ido Levin, https://www.instagram.com/reel/Ddy9IDHoWE0/ , saved 2026-09-30. (DM-A40)

### "Lamborghini" stereo automation (IRKO)
Instead of leaving elements static on one side, automate their position across the stereo field — a hi-hat heavy on the left moves right at chosen moments, then back. Unexpected left-right shifts keep headphone listeners engaged. Used on Grammy-level mixes.
Provenance: IRKO, https://www.instagram.com/reel/DdCnxtqz8b6/ , saved 2026-10-07. (DM-A42) Note: the engine is mono; this is a documented technique, not an engine feature.

## From creator pages (backtrack)

### Stock-compressor sidechain ducking
Duck the bass with Ableton's stock compressor every time the kick hits — space, a cleaner mix, and the classic pumping effect, no third-party plugin.
Provenance: @marshalljamesmusic, https://www.instagram.com/reel/DZA6OkbhGs3/ (2026-05-31).

### Let post-processing do the stereo work
Stereo information gets enhanced by compression and distortion in post — better results than stacking many stereo effects inside the chain.
Provenance: @imtrvcy, https://www.instagram.com/reel/Dd928_CTpkL/ (2026-10-01).

### Comp the whole, not the takes
When comping vocals from multiple takes, judge the combined result as a whole — stitched takes must sound good together, not just individually.
Provenance: @morsbeats_, https://www.instagram.com/p/CmCXPKHtMYq/ (2022-12-11).

### Generate your own harmonies
If recording harmonies is hard, use Melodyne, Antares Throat, or Soundtoys Little AlterBoy to generate/shape them.
Provenance: @morsbeats_, https://www.instagram.com/p/CltuzcjNG_d/ (2022-12-03).

### Mic distance
Keep proper distance from the microphone when recording vocals — singing right up against it (proximity/mouth-on-mic) is a common beginner mistake.
Provenance: @morsbeats_, https://www.instagram.com/p/Cl1cOJCNWR9/ (2022-12-06).

### Mixing is writing, not fixing
Treat mix decisions as part of composition rather than repair work at the end.
Provenance: @illumizotti, https://www.instagram.com/reel/DVKngdljuHj/ (2026-02-24).

### Creative sidechaining
Use sidechaining as a creative sound-design/movement tool, not only kick-vs-bass ducking.
Provenance: @illumizotti, https://www.instagram.com/reel/DUmH4mSCbYh/ (2026-02-10).

### Don't forget the midrange
Neglected midrange is a recurring mix problem — actively check it.
Provenance: @illumizotti, https://www.instagram.com/reel/DURGhGtCYX6/ (2026-02-02).

### Phase shifting as a mix tool
Phase shifting is a deliberate mix/sound tool worth learning (method in video).
Provenance: @illumizotti, https://www.instagram.com/reel/DUl1PpjiUqb/ (2026-02-10).

### Time-based FX inside a Drum Rack
Put time-based effects inside an Ableton Drum Rack for drum sound design.
Provenance: @illumizotti, https://www.instagram.com/reel/DdWyvqXypNE/ (2026-09-16).

### Pro vocal chain from stock plugins (Logic)
A professional-sounding vocal track can be built from any vocal using only stock Logic Pro plugins (chain demonstrated in video).
Provenance: @nest.acoustics, https://www.instagram.com/reel/C-S3LTyMoFe/ (2024-08-05).

### Tempo-synced tails — decay and pre-delay authored in beats (iZotope Learn)

iZotope's reverb curriculum states the tail as a rhythmic quantity: set pre-delay and decay to beat values at the track's tempo — their worked example puts pre-delay at exactly one 1/64 note (52 ms at 71 BPM) and decay at exactly one half note (1.69 s) — so the wash lines up with the rhythm, ends on the grid, and blends instead of smearing. The companion discipline is accumulation control: with busy material, bypass-automate the reverb so it retriggers per note or chord, and the sounding tail only ever belongs to the current harmony. Read against the registry, this is the authoring side of the SPACE family's hygiene rules (T-005 reverb_wash, the QC gate's tail_hygiene check): instruments in this repo measure tails in seconds, but they are *written* in beats, and a transition's tail is cleanest when its decay was a note value from the start. The same article's feed conditioning — band-limiting the reverb's input (the Abbey Road trick) and ghost-trigger carving of atonal transients out of the feed — sets the tail's spectral and tonal scope before the tail exists (study program tranche 13, 2026-10-22).
Provenance: iZotope Learn, "5 Essential Tips for Mixing Reverb", https://www.izotope.com/community/blog/essential-tips-for-mixing-reverb , read in full first-hand 2026-10-22; and "10 Common Delay Mistakes Mixing Engineers Make", https://www.izotope.com/en/learn/10-common-delay-mistakes-mixing-engineers-make , read first-hand 2026-10-22 (gate-before-delay feed gating; delay timing by ear).

### Out-point creep — the loop tightens past the metric grid (Hype, via DJ Carlo)

The documented anatomy of the Hype-style buildup loop adds a final tightening stage the halving ladder doesn't reach: the loop is set manually (In/Out buttons) on the *current* song and rides over the *next* track's build; its EQ is adjusted while it rides so it coheres with the build underneath; the length halves (2 beats → 1) via the 1/2x button; and once the loop is at one beat, tightening continues by re-pressing the Out button and turning the jog — moving the loop's out point *inside* the beat, so the loop length leaves the metric grid entirely (0.9, 0.75, 0.6 beats) and the repetition rate rises continuously instead of in octave steps. In registry terms this is an axis on GAP-02 `loop_tightening_build` — **out_point_creep**: after the last metric stage, a sub-beat end-point pull-in stage, rate set by jog turns rather than by the halving ladder. It matters because the ladder's last step (1 beat → 1/2 beat) is its coarsest doubling; the creep is how the performer keeps the acceleration smooth into the drop instead of arriving early and sitting at the tightest loop.
Provenance: DJ Carlo Atendido, "10 MUST KNOW DJ Mixing Techniques" — transcript fetched first-hand 2026-10-22 (youtubetotranscript.com), the buildup-loop section describing the Hype form; corroborates the GAP-02 compound banked in Phase 12 from the course-page doctrines (study program expansion tranche 1 / Phase 22, 2026-10-22).

### Two-copy offset jerk and the sampler-carry handoff (Recess practitioner texts)

Two vinyl-era moves from the Recess technique archive, stated by practitioners as recipes. (1) **The two-copy offset jerk** (contributor "Flash"): run two copies of the same record at the same point; pull copy B back so it sits 1/2 beat behind copy A — B's kick lands on A's offbeat — then jerk the crossfader A→B→A: the accent reads as a doubled, echoing kick hit, a manual flam at phrase scale. It is *not* the tempo double trick (DM-A21 ramps pitch 1x→2x) and not instant doubles as a loading convenience; the offset itself, held for a moment and fader-jerked, is the gesture — the two-copy phasing family at its smallest unit. (2) **The sampler-carry handoff**: pre-load 2 bars of the outgoing track into a sampler and run it under the track; at the mix, fade the sampler up as the real deck fades, then backspin the freed deck in one beat while the sampler carries the hook for one bar *past* the join — the deck is free for the spinback precisely because the hook no longer lives on it. The registry's form is GAP-16 `spare_deck_element_firing` × T-007 `backspin`; the text contributes the level-crossfade choreography (sampler rises as deck falls, so the hook's level never dips at the swap) that makes the compound invisible.
Provenance: Recess.co.uk technique archive (practitioner-contributed walkthroughs), fetched first-hand 2026-10-22 — the two-copies recipe and the sampler/backspin mix walkthrough (study program expansion tranche 1 / Phase 22, 2026-10-22).
