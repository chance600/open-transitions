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
