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

### The DnB pattern taxonomy — continuous drop, cut-in, valley, mountain (note.com)

A working DnB DJ's own transition-pattern taxonomy, stated as named patterns with bounds — the genre's native labels for what the performer corpus will find. **Continuous Drop**: the end of A's drop runs straight into the start of B's drop, the blend opening 8 bars before A's drop ends — no breakdown between drops; banked as the base `continuous_drop` (WEB-19). **Cut-in**: the surprise switch — at the drop moment after a buildup, change tracks wholesale with a crisp upfader move; the registry's T-030/T-014 family performed at drop scale, with the practitioner's cueing rule attached (cue by the kick waveform, not the app's grid, or the groove discrepancy shows). **Valley** ("create a bottom of valley"): lay B's intro on the first bar of the break after A's drop ends — or on A's outro — with the fader reaching max only at B's verse; the intro-over-break staging of `breakdown_transition` (T-023), also stated independently in the DJ TechTools forum ("start the intro alongside the break in the first track... as the break ends the main idea of the second kicks in"). **Running up a mountain**: align the two drops, set the mix start 8 or 16 bars before them, and land either as a double drop or by *converging* on B's drop alone — the converge outcome is banked as an axis on `double_drop` (T-024), and the same text's case study (Andy C: Sub Focus "Rock It" (Wilkinson Remix) + Camo & Krooked "Sientelo" + Sub Focus "Solar System") banks the triple-drop staging there. One accent completes the taxonomy: the **pre-drop fader dip** — with two tracks stacked, drop the *other* track's upfader for the 1/4-bar break just before the drop so the break stands out; a subtraction accent at the exact point the EDM arrangement doctrine independently deletes the last 1/4 bar before a drop (knowledge/producing, EDM Templates).
Provenance: kohadachan, "A Personal Drum and Bass DJ how to" (note.com, 2024), fetched first-hand in full 2026-10-22; DJ TechTools forum, "Transitions In a Mix" (2013), fetched 2026-10-22 (study program expansion tranche 2 / Phase 23, 2026-10-22).

### Long-layer EQ doctrine at 174 — the total-bass-constant rule (note.com)

DnB's long layers are held together by a stated EQ discipline, not taste. Before layering, the incoming track is staged: upfader at ~0% (or ~60% for a blend entry, 100% only for a cut-in), low EQ at 0 or 8 o'clock, mids at top, highs at ~10 o'clock. The low EQs are *switched* at the moment the next track "comes in earnest" — and the governing invariant is that **the total amount of bass does not change drastically** across the switch: replace completely or keep some of A's low, but hold the sum. Two corollaries: if one track is in a break while the other is in its intro, killing both lows makes the sound faint — carry low EQ on *both* tracks through that window (the one licensed exception to one-bass-at-a-time); and if the high shuffle feels off, take about half the highs from the non-main track — more blurs its contours. Where stems exist, an unwanted vocal is removed rather than EQ'd around, and a LowCut Echo covers the surgery's artifacts. The doctrine's registry shadow: it is the operating manual for `eq_blend` (T-001) and `bass_swap` (T-002) at DnB dwell times, and it prices why DnB entries in the pattern taxonomy can stage for 8–16 bars without mud.
Provenance: kohadachan, "A Personal Drum and Bass DJ how to" (note.com, 2024), "EQ manipulation to soften muddy sound" + "Processing of overlapping vocals", fetched first-hand 2026-10-22 (Phase 23).

### LowCut Echo — the DnB echo form, and the echo family's band axis (note.com)

The echo form DnB actually reaches for is the **LowCut Echo**: the echo's wet path carries no lows, so at 174 BPM the tail smears the hats and mids while the kick grid stays clean — stated in the taxonomy as "often used... when I want the end of the previous track to blend in better," knob at ~10 o'clock, and as the cover for stem-surgery artifacts. In registry terms this is a band axis on the echo family (`echo_out` T-004 and its blends): wet-path band = low-cut, beside Phase 22's per-deck assignment axis — the echo's repeats inherit the outgoing track's rhythm but not its bass weight, which is exactly what a one-bassline genre requires of a tail. The general principle travels: any tail effect staged under an incoming drop should be band-limited away from the band the drop is about to own.
Provenance: kohadachan, "A Personal Drum and Bass DJ how to" (note.com, 2024), "Frequently used effects", fetched first-hand 2026-10-22 (Phase 23).

### DnB key moves — the +2 lift, the +6 "back code", the −3 float (note.com)

Harmonic practice stated as named moves at DnB tempo: for long mixes and mashups, same key (4A -> 4A); for slight change, one wheel step; for energy — "appears on lots of cut-ins" — a **+2 shift** (5A -> 7A, 12A -> 2A, one key up); a **+6 shift** (1A -> 7A, 12B -> 6B) the source names the **"back code"**, a tritone jump that reads as lift rather than clash at cut-in speed; and a **−3 shift** (7A -> 4A; arithmetically +9), used even into a deliberate bass replacement on an out-of-key pair for its "unique floating feeling." The registry's compatibility model already prices +1/+2 as the energy-boost band (select.py's key_move feature); the back code extends the named vocabulary to the far pole: at a cut-in, harmonic *distance* is spent as energy, where in a long blend it would be spent as clash — the same interval, two prices, decided by the transition's duration. That duration-dependence is the entry's claim: key-move acceptability is a function of how long the two keys must coexist.
Provenance: kohadachan, "A Personal Drum and Bass DJ how to" (note.com, 2024), "Harmonic mixing", fetched first-hand 2026-10-22 (Phase 23).

## From the Phase 24 enumeration (combinatorial pass)

### Named chains I — spinback into the drop-swap; brake into the drop

Two same-seam chains (§6 Sequence) whose second move fires inside the first's exit gesture. **Spinback → drop-swap** (`backspin` → `hotcue_drop_swap`): the rewind's snap lands the pair on a downbeat with the room's attention on the deck, and the swap spends that attention instantly — B's drop replaces A's at the exact point the spin dies, so the rewind reads as aim, not recovery. This is Class 3's own example chain from the V2 map, verified against the exit/entry graph (snap exit → cold entry). **Brake → drop** (`brake_stop` / `power_down` → `hotcue_drop_swap` or `double_drop`): the brake's contract already ends with "the caller drops the next track on the following downbeat" — the chain names what the contract implies, with the drop-swap preferred over a plain B start because the dive has already spent the pair's tempo relationship; a drop event forgives what a blend entry would expose.
Provenance: Phase 24 combinatorial enumeration (ENUMERATION.md Part B — 6,006 ordered pairs under same-seam scoping, 5,227 compatible; chains banked at the naming bar, compositions stated per FRAMEWORK §6 operator 3).

### Named chains II — echo, then rewind the deck

**Echo → rewind** (`echo_out` → `backspin`): A's throw is already ringing post-fader when the hand takes the (silent) deck back — the tail keeps the room while the rewind is pure theatre and reset, and B enters on the spin's snap or under the tail's last repeats. Distinct from the gesture-triggered echo (Smooth Echo / Fader Echo dispositions, where the gesture *fires* the tail): here the order is reversed, the tail is established first, and the gesture plays over it — the pair is a sequence, not a compound, and the exit/entry graph prices it clean (tail exit → any entry).
Provenance: Phase 24 combinatorial enumeration (ENUMERATION.md Part B).

### Named chains III — tease, then swap the basses

**Tease → bass-swap** (`filter_sweep` staged as a tease → `bass_swap`): across several phrases B is shown filtered — present, recognizable, weightless — and the basses trade only at the drop. The chain is the temporal reading of what `eq_blend` (T-001, composed of `filter_sweep` + `bass_swap`) does fused: the same two atoms, sequenced so the *reveal* and the *weight transfer* land as two separate events. DJs call the pair as one plan ("tease it, then swap on the drop"), which is what makes it a named chain and not just two transitions in a row.
Provenance: Phase 24 combinatorial enumeration (ENUMERATION.md Part B); Class 3's second example chain in EDUCATIONAL-SOURCES-V2.md.

### Named chains IV — the fake-out into the real double drop

**Fake-out → double drop** (`fake_drop` → `double_drop`): A's drop is withheld at the last moment (the fake), and the energy the room braced for is paid by *both* drops landing together a phrase later. The fake alone spends expectation; the chain refinances it — the double drop's collision is the payoff the fake promised, which is why the pair is called as one move in dubstep/open-format practice rather than programmed as two. Graph check: snap exit → cold entry, compatible at the same seam.
Provenance: Phase 24 combinatorial enumeration (ENUMERATION.md Part B).

### Named chains V — tighten the loop, then swap (the Hype chain)

**Tighten → swap** (`loop_tightening_build` → `hotcue_drop_swap`): the buildup loop halves toward the metric grid's floor (GAP-02, with the out-point-creep axis from Phase 22), and at maximum tightness the drop-swap fires — B's drop replaces the loop the crowd has been locked into. This is James Hype's signature sequence stated as a chain: the tightening supplies the tension curve, the swap supplies the event, and neither move carries the moment alone (a swap without the tighten is a trick; a tighten without the swap is a stall).
Provenance: Phase 24 combinatorial enumeration (ENUMERATION.md Part B); the tightening atom and its creep axis from Phases 4/22 (Hype's buildup-loop craft).

### Processing the return — the FX-return compound pattern

The enumeration's largest compound class (69 surviving pairs) is one pattern: **a tail is generated, and the tail — not the track — is processed.** Gate the reverb return with a transform pattern and the wash pulses (the gated tail); duck the echo return against the incoming kick and the tail breathes around B (`pumper_exit`'s duck pointed at a return; the ducked FX return's full named form is Phase 17's); filter or formant-morph the return and the tail changes character as it dies (Engine's Filter Dub Echo names the filter case; the X1850's Hall Echo names echo-into-reverb). The pattern's rule: return processing is *staging of an existing tail*, expressible with the registry's send/return and stack machinery — knowledge-class, not a base — with one exception the enumeration did promote: conditioning that lives *inside* a feedback loop (repeat k is processed k times) is a mechanism, and its tone form is built as `aging_echo` (CMP-01). The line the pattern draws: process the tail once, it's staging; process it per-repeat, it's a mechanism.
Provenance: Phase 24 combinatorial enumeration (ENUMERATION.md Part B); instances from the bank's vendor dispositions (Engine Touch FX / X1850, Phases 6–8) and Phase 17 (Produce Like A Pro's ducked return).

### Dry+Wet — the additive mix law, and the pre-filtered send (Mixxx)
Two mix laws govern every wet effect, and naming the wrong one mis-renders the transition: Dry/Wet *substitutes* (the wet series replaces the dry as the control turns), while Mixxx's Dry+Wet mode *adds* — "in Dry+Wet mode, the dry signal is always at full volume," so the tail is layered over an unducked dry. The worked example that proves the send-side topology: an effect chain Filter → Echo in Dry+Wet removes bass from the echoed signal without touching the unechoed signal (the basis of `pre_filtered_echo` WEB-22). Corollaries from the same chapter: a phase-shifting filter (phaser/flanger class) blended about halfway against dry produces comb filtering — a QC fact for any parallel FX blend; reverb is the sole tempo-sync exemption in the architecture (every other effect can sync, including delay times at fixed subdivisions); and the famous Ping Pong mode is invisible on mono material — it redistributes repeats between L and R only, so on a mono render it is identical to a plain echo (a duplicate, banked as such). What Ch. 11 does NOT contain: any per-effect parameter list — the manual defers every range/default to in-app hover tooltips, and the legacy 2.0 manual (§10.5) gives parameter *names* for Echo/Reverb/Flanger/BitCrusher/Filter only; Phaser and Tremolo parameters are undocumented in both (named gap).
Provenance: Mixxx 2.5 Manual Ch. 11 (Effects) + legacy 2.0 §10.5, manual.mixxx.org, fetched 2026-10-23. (Phase 26, software/hardware tranche A.)

### Stem-scoped FX is routing infrastructure, not a technique family (VirtualDJ + djay)
Both stem platforms converge on the same doctrine: an FX scoped to a stem is the *scope* doing the work, the effect stays the registry's existing base. VirtualDJ's Stem FX is a global routing mode with exactly three scope groups (Vocal / Melody / Rhythm) applying the unit's effect to the chosen group only; djay documents the same per-stem routing ("add echo only to the vocals, filter just the drums, or apply reverb to the melody"). This confirms and bounds the GAP-08 precedent the bank already applies (stem-scoped echo = `echo_out` staged on a stem, not a new base). djay's Mute FX is the sharpest form: muting or soloing a stem fires a quantised echo tail on that stem alone (1 / ¾ / ½ beat — banked as an axis on `echo_out`). The general render pattern is `<base>__<stem>_only`; minting a base per (effect × stem) pair would multiply the registry without adding a mechanism.
Provenance: VirtualDJ Manual (Stems 2.0 / Effects pages) + djay Pro help (Neural Mix / Mute FX pages), fetched 2026-10-23. (Phase 26.)

### Stem taxonomy is unstable — and bleed is a fidelity parameter (VirtualDJ)
VirtualDJ's own pages disagree about the stem set: the headline and Stems+FX pads use four stems; the 5-knob Stems EQ claims five it never names in text (image-only — a named gap); ModernEQ splits drums into kick + hihat; EZRemix collapses to three groups. Any stem render must state which taxonomy it stages (the registry's surrogate set is four, six under the kick/hihat axis on GAP-08). More consequential for the mixing lane: the FAST separation mode's parameter is literally called **bleed** — a cross-stem leakage coefficient — so separation quality is a *render parameter*, not a fixed property of the source; prepared stems cost ≈4× the original file size, and realtime separation is tiered by GPU. When a blend sounds muddy, bleed is a knob, not a fate.
Provenance: VirtualDJ Manual (Stems 2.0, Mixer, Help/Stems pages), fetched 2026-10-23. (Phase 26.)

### The tails-only break — a void where only the wet tail sounds (SP-404MKII)
MUTE BUS ([SHIFT]+[BUS FX]) mutes the *input* to a running wet bus: "only the reverberations or delay sound are heard." Roland frames the gesture as performance technique — "an effective performance technique" for "expressive breaks" — and its release semantics are part of the move: input returns and the effect switches off simultaneously, so the re-entry is clean dry with a reset chain. Banked as an axis on `reverb_freeze` (T-034), whose freeze sustains the tail; the mute-bus break lets it *decay* in the void instead. The same doctrine appears independently in Pioneer's DJM-V10 footnotes ("only the effect sound remains if you set the channel fader to the [0] position") — two vendors, one staging: cut the input, keep the tail, mind the re-entry.
Provenance: SP-404MKII Reference v5.5 (BUS FX pages) + DJM-V10 manual via manua.ls (p65 footnote), fetched 2026-10-23. (Phase 26.)

### FX returns are full channels — and the DJM-V10 SEND bounds (Xone:96 + DJM-V10)
The Phase 24 ruling stands — the FX-return pattern is one doctrine, not a family of bases — and the two flagship mixers refine it the same way: the wet return lands on a *full channel strip* (TRIM/EQ/FILTER/fader on the V10; channel EQ + VCF assignment on the 96's A/B returns, against flat C/D-style direct injection), so the transition is performed by fading and EQ'ing the wet stem against the dry channel. V10 specifics worth banking exactly: the SEND section holds only FOUR built-in effects (Short Delay, Long Delay, Dub Echo, Reverb — there is no Ping Pong in SEND; Ping Pong exists only as a Beat FX); TONE is a filter on the built-in wet sound, not a per-effect parameter; one built-in plus EXT1 plus EXT2 can run simultaneously and even sum into a single return channel; external units are level-only (SIZE/FEEDBACK, TIME and TONE do not apply). Negative ruling: the V10's per-channel COMP is a one-knob static compressor with no sidechain, key input or tempo link — it does NOT ground a `pumper_exit` variant; it is channel glue only.
Provenance: Xone:96 User Guide (official support HTML) + DJM-V10 manual via manua.ls (pp26–27, 44–50), fetched 2026-10-23. (Phase 26.)

### Band-selective FX — the modifier that composes with everything (DJM-V10)
The V10's Beat FX can be assigned to one frequency band only — FX FREQUENCY selects LOW, MID or HI, the selected band is processed and the rest passes dry. This is a *routing modifier*, composable with every band-processable base (`<base>__low_band_only` etc.), rendered as a 3-way crossover split with the chosen band processed and summed back. It shares its split with `eq_blend` and its band-as-element thinking with GAP-08, but minting per-effect band bases would triple-count one routing fact. Crossover frequencies are stated nowhere in the manual (named gap); renders use registry-standard crossovers and say so.
Provenance: DJM-V10 manual via manua.ls (p56), fetched 2026-10-23. (Phase 26.)

### Crunch is not crush — and the Xone:96 ground-truth corrections (Xone:96)
CRUNCH (Xone:96, 0–10 per VCF) is pre-filter *harmonic addition*: analogue-style saturation generated from the signal just before the filter, level-dependent (optimum drive ±6 dB). `crush_degrade` (WEB-04) is the opposite physics — quantisation and sample-rate reduction, information *removed* (the SP-404's Crusher says so explicitly: its RATE is sample-rate reduction). Confusing the two mis-renders both. Corrections the guide forces on prior assumptions: the 96 has NO master isolator, limiter or compressor of any kind (a negative fact — master processing is the DJM-V10's axis, not a shared flagship trait); RES runs MILD→WILD "just short of self-oscillation" with no numeric Q anywhere (the response curves are graphs only, not text-extractable); channel fader curves are a named vocabulary (constant power / dipped / fast-cut); and soft-switching makes even filter-type and assignment changes click-free mid-performance, which is what licenses downbeat type-switch stagings inside the filter bases. Monitoring doctrine (dual independent cue systems, split cue) is unrenderable and lives in the workflows scheme-gap entry.
Provenance: Xone:96 User Guide (official support HTML, read end-to-end), fetched 2026-10-23. (Phase 26.)

### Compatibility mixing vs modulation mixing (Club Ready)

Two different harmonic operations share the name "harmonic mixing" and must not be conflated. Compatibility mixing chooses keys that agree (the Camelot wheel's legal moves, T-015) so two tracks can overlap without clash. Modulation mixing CHANGES key mid-set as a device — a deliberate lift or shift staged as an energy event, with FX and arrangement doing the work of selling the move. The registry's T-015 is the compatibility function; modulation moves (the +7 lift, the +9 jump, the +2 boost) are staged events on top of it, not alternative readings of the same wheel. A set that modulates without ever establishing compatibility has no home key to lift from; a set that only ever matches never lifts at all.
Provenance: Club Ready DJ School, harmonic-mixing guide, fetched first-hand 2026-10-24. (Phase 27.)

### The overlap-duration law (Club Ready)

The farther the key move, the shorter the overlap that survives it. Same-key and ±1 moves tolerate long blends; +2 energy boosts want short, staged overlaps; the unforgiving set (+4/+6/+8/+10) survives only as a timing-critical hit, if at all. The law is the reason the registry's far-move bases are exits and snaps, not blends: duration is a harmonic parameter, not just a structural one. MIK's +2 caution is the same law from the other side — a +2 "may clash in long overlap," so the DJ keeps a smoother alternative ready rather than committing the blend.
Provenance: Club Ready DJ School, harmonic-mixing guide + Mixed In Key wiki, harmonic mixing explained, fetched first-hand 2026-10-24. (Phase 27.)

### Energy-boost staging and quota (Mixed In Key + Club Ready)

A key lift is not just a wheel move — it is staged. FX are laid around the lift (a riser into it, a wash or impact on it), and the lifts are rationed: "one or two per set" (MIK). The quota is the doctrine: an energy boost spent every transition stops being a boost and becomes the set's default altitude, after which nothing can lift further. Key-lock rehearsal belongs here too — MIK's doctrine is to rehearse the lift with key-lock on before performing it, so the staged lift is a practiced gesture, not a discovered accident.
Provenance: Mixed In Key wiki, harmonic mixing explained + 5 mixing techniques; Club Ready DJ School, harmonic-mixing guide, fetched first-hand 2026-10-24. (Phase 27.)

### The BPM-barrier structural-anchor doctrine (PulseDJ)

Tempo barriers are crossed at structural points, not at arbitrary bars. The open-format table's doctrine: anchor the switch on a verse, a chorus, a drop — a point the room already hears as a boundary — and the tempo change reads as arrangement, not error. The same doctrine governs the strategy table's cut law (exact 1-beat of the new verse/chorus, ±5 BPM band) and its reset law (WEB-31's tail erases the old metronome before any-BPM drops). A tempo switch placed mid-phrase fights two grids at once; the same switch placed on a structural anchor fights none, because the room's attention is already at a boundary.
Provenance: PulseDJ blog, open-format guide (strategy table + BPM-barrier doctrine), fetched first-hand 2026-10-24. (Phase 27.)

### Phase cancellation multiplies with three-plus decks — and the mono test (DJ Gym)

With two decks, phase problems are occasional; with three or more, they multiply — every added deck adds pairwise interactions, and low-end cancellation is the first casualty. DJ Gym's doctrine is procedural, not hopeful: EQ/ISO discipline (frequency slotting, T-020's pyramid), transient sculpting (transients carry the phase information that cancels), frequency slotting per deck, and a MONO COMPLIANCE TEST — sum the stack to mono and listen, because a stack that sounds wide in stereo and hollow in mono is cancelling, and most rooms are effectively mono at the floor. A three-deck stack that fails the mono test is not mixed yet, however good it sounds in headphones.
Provenance: DJ Gym, "The Ultimate Guide to Multi-Deck Mixing," fetched first-hand 2026-10-24. (Phase 27.)

### Balance and "not overcooked" — orchestration, not stacking (Pioneer + DJ Gym)

Techno's multi-deck heat has a ceiling, and the veterans name it. Sharpe (via Pioneer DJ's guide): the craft is balance — "not overcooked." DJ Gym states the same doctrine as a positive law: "the art of multi-deck mixing isn't about filling every frequency slot — it's about orchestration." The failure mode is additive: each added layer feels small on its own deck and the stack arrives muddy, loud, and flat. The corrective is subtractive — mute, carve, or drop a layer before adding the next — and the test is the room, not the meters: if the stack's energy stopped rising when the last layer arrived, that layer was overcooking, not orchestration.
Provenance: Pioneer DJ blog, "A complete guide to multi-deck mixing" (Sharpe) + DJ Gym, "The Ultimate Guide to Multi-Deck Mixing," fetched first-hand 2026-10-24. (Phase 27.)

### The hip-hop 8-bar chorus blend law (Serato forum)

Hip-hop's blend window is one 8-bar chorus, not a house-length runway — and the law follows from the window. The incoming track drops its bass only (not its highs, not its mids) and raises it with the crossfader as A leaves; the full-chorus blend exits by straight cut or spinback, never by a long tail, because there is no long tail to spend. A hip-hop blend that borrows house timing — 32 bars of overlap, gradual everything — runs past the chorus into the next verse with two vocals stacked, which is the genre's characteristic failure. The window is the technique: short, bass-gated, exited decisively.
Provenance: Serato forum, "EQing for Blends in Hip Hop" + "How do you transition from song to song?" (full-chorus blend, spinback exit), fetched first-hand 2026-10-25. (Phase 28.)

### EQ-as-sculpture vs fader-as-volume (DJTechTools forum, djproben)

EQs fit sounds together; faders manage loudness — and confusing the two jobs is the beginner's blend defect. The doctrine, stated exactly: use gains to level-match tracks recorded at different levels, EQs to keep sounds from clashing, and volume faders to bring a track in (e.g. highs first, fader to 100% over 4 bars, then bass and mids over 4–8 bars). The extreme form is legitimate: both tracks at 100% on the faders, the whole transition ridden on gains and EQs alone. A blend that rides loudness on the EQs (turning knobs to get louder) or sculpts on the faders (fading to fix a clash) has the jobs backwards, and no amount of practice fixes a backwards job assignment.
Provenance: DJTechTools forum, djproben, "need advice in mixing technique," fetched first-hand 2026-10-25. (Phase 28.)

### The three-knob blend routine, staged (SetFlow)

The house/techno blend has a canonical knob order, and the order is the routine: lows — one bass at a time, swapped in one move on a phrase as the outgoing track winds down; highs — incoming highs start down and open gradually, fully open BY the bass swap, so two hi-hat patterns never fizz together and the incoming hats never give the game away early; mids — outgoing mids ease back over the first half of the blend, making room for the new track's chords and vocals. Moves stay gradual (a slow turn over the first half sounds like the music changing; a sudden one sounds like a knob). Cuts are the exception — a cut drops on the beat at full volume with nothing to EQ — and so are clash blends: key clashes and two vocals on top of each other cap the blend at 8 bars.
Provenance: SetFlow, "How to EQ a DJ Transition," fetched first-hand 2026-10-25. (Phase 28.)

### The clash-window law: 8 bars maximum (SetFlow + Serato)

A blend that clashes — wrong key, two vocals — does not get fixed by length; it gets capped by it. SetFlow's Mix view caps clash blends at 8 bars, and the Serato hip-hop threads converge on the same number from the other side (one 8-bar chorus). The law generalizes: overlap duration is a function of compatibility, not ambition. Compatible pairs earn long blends; clashing pairs earn short ones, and a long clash blend is not a braver blend — it is a longer announcement of the clash.
Provenance: SetFlow, "How to EQ a DJ Transition" (8-bar clash cap) + Serato forum hip-hop threads, fetched first-hand 2026-10-25. (Phase 28.)

### The beatless-break cross-BPM law (Thomann)

Tracks at irreconcilable tempos still mix — at their beatless sections. Thomann's law: if beatmatching is impossible (different tempos, imprecise sync), pick a section without a beat in at least one track; beatless breaks mix together cleanly even at completely different BPMs, and the new track must continue with a strong groove after the transition so the previous track's absence reads as arrival, not dropout. The law is the low-tech counterpart to WEB-32's bed: where the bed covers a jump with a third element, the beatless break covers it with nothing — the absence of rhythm is itself the bridge.
Provenance: Thomann blog, "The 5 most important DJ transitions" (Fading), fetched first-hand 2026-10-25. (Phase 28.)

### The +2 energy-boost law, with its caution (DJ Mag + Mixed In Key)

Jump two places on the Camelot wheel for a transpose effect that is "jarring to the dance floor but when done correctly has an uplifting effect" (DJ Mag) — and the caution travels with it (MIK, already in T-015's evidence): a +2 "may clash in long overlap," so the DJ keeps a smoother alternative ready. Banked here as a law, not an engine move (unlike Phase 27's +7/+9, which shipped as a harmonic_mix extension): the +2 is a staged event with a short-overlap requirement, and the overlap-duration law above is what enforces it. A +2 held long is not a bolder boost; it is the caution, ignored.
Provenance: DJ Mag, "Tips & Tricks for DJs" (+2 jump) + Mixed In Key wiki (already in T-015 evidence), fetched first-hand 2026-10-25. (Phase 28.)

### The Kim tempo band: 86.1% of real tempo moves stay under 5% (Kim et al., ISMIR 2020)

Across 20,765 matched transitions (1,557 mixes, 13,728 tracks, House/Trance-heavy), tempo adjustments follow a double-exponential distribution skewed hard to zero: 86.1% under 5%, 94.5% under 10%, 98.6% under 20%. The calibration write-back for the registry: a pair needing more than 5% is the exception (13.9%), more than 10% is rare (5.5%), more than 20% is near-absent (1.4%) — and the registry's selection gates that allow 10% are permissive relative to practice, not descriptive of it. Banked as a law, not an engine change: the gates stay where they are, but a build that plans a >10% move should know it is planning an outlier move, and a >20% move needs a dedicated device (a bed, a brake, a cut), not a blend. The same paper's method note matters for reuse: beat-synchronous chroma + MFCC subsequence DTW, key-invariant by circular chroma shift — the alignment method the S0–S11 pipeline already uses.
Provenance: Kim, Choi, Sacks, Yang & Nam, "A Computational Analysis of Real-World DJ Mixes using Mix-To-Track Subsequence Alignment," ISMIR 2020, https://arxiv.org/pdf/2008.10267 (§6.1, Fig. 4) + project site https://mir-aidj.github.io/djmix-analysis/ (tempo histogram), fetched first-hand 2026-10-25. (Phase 29.)

### The Kim key law: transposition is a deliberate act, not a habit (Kim et al., ISMIR 2020)

Only 2.5% of the 24,202 played tracks are transposed at all, and 94.3% of those move exactly one semitone. The paper's reading is the registry's: DJs leave master tempo / key lock on by default, and key change happens only when the DJ intentionally wants it. The write-back: a build that transposes by more than a semitone is not "harmonic mixing," it is a marked effect, and should be staged as one (a pitch-play device, a riser, a declared key move) rather than slipped inside a blend as if it were neutral. The 2.5% figure also bounds the harmonic_mix extension work: the +7/+9 axes from Phase 27 are effect moves for the rare deliberate case, not everyday blend settings.
Provenance: Kim et al., ISMIR 2020, https://arxiv.org/pdf/2008.10267 (§6.2, Fig. 5), fetched first-hand 2026-10-25. (Phase 29.)

### The Kim phrase law: transition lengths peak every 32 beats (Kim et al., ISMIR 2020)

Transition lengths in beats peak at every phrase — dotted lines every 32 beats in the paper's histogram, with the peaks landing on phrase multiples. DJs consider the repetitive structure of the dominant genres when they place transitions and cue points; a blend length that is not a phrase multiple is fighting the music's own grid. The write-back: the registry's blend-bar presets (8/16/32/64) already sit on this grid, and a custom blend length should be justified against it — a 24-bar blend is a deliberate off-phrase choice, not a neutral one. Combined with the cue-agreement law (setcraft), this is the empirical ground under "phrase-aligned" as a selection requirement rather than a taste preference.
Provenance: Kim et al., ISMIR 2020, https://arxiv.org/pdf/2008.10267 (§6.3, Fig. 6), fetched first-hand 2026-10-25. (Phase 29.)

### The DJtransGAN pairing law: BPM ≤5, key ≤2, 8 bars, phrase downbeats (Chen et al., ICASSP 2022)

The synthetic pairing pipeline that trains DJtransGAN — the only data-driven transition generator in the academic set — pairs tracks under three hard constraints: BPM difference ≤5, key difference ≤2 semitones, and a transition region fixed at 8 bars with cues at phrase downbeats (C_in = first downbeat of A's last 8 bars, C_out = last downbeat of B's first 8 bars). Real-data side: 284 livetracklist mixes segmented into 7,064 transition sections (sections under 1 minute discarded). The generator itself is a differentiable EQ + fader per sub-band — a learned version of the registry's eq_blend mechanism, not a new mechanism: per-sub-band fade curves are what eq_blend renders by hand. The write-back is a constraint set, not a base: pairs outside BPM ≤5 / key ≤2 need a bridging device, and the 8-bar figure is a training constraint, not evidence that 8 bars is optimal — it must not be quoted as "the ideal blend length" against Kim's 32-beat phrase peaks.
Provenance: Chen, Hsu, Liao, Martínez Ramírez, Mitsufuji & Yang, "Automatic DJ Transitions with Differentiable Audio Effects and GANs," arXiv:2110.06525 (§3.1), fetched first-hand 2026-10-25. (Phase 29.)

### The switch-point feature ranking: energy, harmony, timbre, drum onsets (Zehren et al., 2024)

On EDM-150 (150 tracks, 1987–2016, 99–148 BPM, 625 expert-annotated switch points, mean 4.2 per track), the features that most effectively mark a switch point are changes in energy, harmony, and timbre, plus drum-onset density — and the experience-driven model built on just two of them (bass-register energy novelty via RMS + bass-drum onset novelty via drum transcription, both on 2-beat windows with a 32-beat checkerboard kernel) reaches 89% precision at 30% recall, on par with the trained models. The precision/recall split is the lesson: two features find switch points you can trust but miss most of them (one model returns often only one point per track) — novelty peaks are sufficient evidence for a switch point, not a complete inventory of them. For the registry, this ranks cue-candidate features: an energy-novelty peak at a period downbeat outranks a timbre-only or harmony-only candidate, and a candidate with no novelty in any of the four is not a switch point at all, however convenient its position.
Provenance: Zehren et al., "Interpretability of Methods for Switch Point Detection in Electronic Dance Music," https://www.mdpi.com/2624-6120/5/4/36/html (§§3.3, 5), fetched first-hand 2026-10-25. (Phase 29.)

### The Bittner transition-point cost law: hierarchy, costs, pruning windows (Bittner et al., ISMIR 2017)

Transition points are restricted to downbeats and heavily weighted to section boundaries, in a strict hierarchy: drop points outrank section boundaries, which outrank plain downbeats. The cost that picks between candidates combines timbre distance and chroma distance over the overlap (similar = cheaper), inverse loudness (loud-in-both = cheaper), vocalness sum (vocals-in-both = expensive — overlapping vocals and mid-sentence cuts are the failure the cost exists to prevent), and boundary-miss penalties (2 if neither region end lands on a boundary, 1 if only one does). Pruning windows: A's point inside its last 25%, B's inside its first 20%. Two evaluation facts travel with the law: 15% of rendered transitions were rated "Bad" for beats not aligning (beat-estimation error, not taste), while key clash was flagged by no curator in either transition type — on a pop corpus, with tempo pairs constrained to ≤5 BPM. The write-back: the hierarchy and the vocalness cost are selection law for the registry's downbeat-restricted bases; the key-clash non-finding does NOT generalize to EDM blends, where the corpus differs and the clash-window law (Phase 28) already says otherwise.
Provenance: Bittner et al., "Automatic Playlist Sequencing and Transitions," ISMIR 2017, https://rachelbittner.weebly.com/uploads/3/2/1/8/32182799/bittner_ismir-playlist_2017.pdf (§4.1–4.3), fetched first-hand 2026-10-25. (Phase 29.)
