# Knowledge — Workflows

Prep, library, and business workflows with provenance (FRAMEWORK.md §1, layer 3). These feed selection (e.g. key/energy data, hot cues) but are procedures, not renderable transitions. DM source thread: `542187470506577`.

### Mixed In Key → Rekordbox XML workflow (DM-A32)

Export the Rekordbox library as XML → import into Mixed In Key to analyze key/tempo/energy → set preferences to export cue points to Rekordbox (check "Overwrite existing cue points") → export → reimport the XML in Rekordbox (Preferences > Advanced > Import to Collection). Tracks then display keys plus auto hot cues at good mix-in points without losing custom cues. This is the data pipeline that feeds the library's harmonic layer (T-015) and selection features.
Provenance: MASSIMO, https://www.instagram.com/reel/DV83pi3kUly/ , saved 2026-04-13. (DM-A32)

### 60-second remix workflow (stems-first)

Pick a song, secure stems (YouTube MP3 + vocal-separation tools like LALALAI, official multitrack sites, free multitrack sources), import into the DAW, then use a vocoder to lock the vocal's tempo to the project BPM; repeat per element (drums, bass, others). Speed comes from stems-first, not from shortcuts in the mix.
Provenance: MARSHALL JAMES, https://www.instagram.com/reel/DGlNQ17RFdX/ , saved 2025-02-26. (DM-A16)

### Public-MIDI remix shortcut

Grab a public MIDI file of the target song (e.g. bitmidi.com), drag it into the DAW — the full arrangement loads across multiple tracks, saving hours of reconstruction while leaving room for creative editing.
Provenance: WARN, https://www.instagram.com/reel/Dd2jS4LtJtz/ , saved 2026-09-30. (DM-A41)

### Instagram acapella sampling hack (Ableton Move)

Search Reels for "sample this acapella", capture the vocal video on iPhone, import into Ableton, pitch the sample up, automate the drum sampler's built-in effects, and slice-to-MIDI to generate a new beat. Works with Push 2/3.
Provenance: carter (@dnksaus), https://www.instagram.com/reel/DBlteHKJzpe/ , saved 2025-02-02. (DM-A04)

### Beatport hype-chart strategy

Stop demoing major labels; target smaller "hype" labels. Master the track, upload privately to SoundCloud with downloads enabled, email a concise pitch with the demo link. Once signed, negotiate a two-week Beatport exclusive pre-sale and push friends to buy 10–15 copies to crack the hype charts.
Provenance: Max & Dana (@maxanddana), https://www.instagram.com/reel/DF_3arLMFLx/ , saved 2025-02-14. (DM-A10)

### Versioning discipline (34-version lesson)

A track tuned halfway between Dm and D♯m, mixed for 8 months across 34 versions, ended up going back to the original mix — versioning preserves the option to return; found sounds (his water bottle) became SFX and melodic elements.
Provenance: @dnksaus, https://www.instagram.com/p/CeMGMcvl7xb/ (2022-05-30).

### Self-release over waiting

Stop waiting months for labels to reply or for the "perfect" release home — self-release, and teach/show how the music is made instead.
Provenance: @imtrvcy, https://www.instagram.com/p/C8kmRBePQDZ/ (2024-06-23).

### Serato Flip — recorded cue automation as a track edit

Flip records a performance — hot-cue triggers and censor actions, in time — into an automation lane saved in the track file's own metadata, then replays that automation on playback: the track edits itself. Serato's named uses are transition-shaped: extend intros, breakdowns or outros for better mixing; create transition sections inside a song for changing tempo or beat structure; auto-skip verses/choruses; clean (censor) edits; tone play. Loop Snap quantizes the recorded Flip's length to the track's BPM so a looped Flip cycles in time. This is the authoring model behind the registry's premade-edit family (T-028 beat_jump's playhead arithmetic, T-014 hotcue_drop_swap, GAP-07 premade tempo-bridge edit): the moves are performed once, then stored *with the track* rather than re-performed nightly — prep-layer, not a renderer, so it lives here in the knowledge layer (study program tranche 2, 2026-10-21).
Provenance: Serato Support, Serato Flip User Guide, https://support.serato.com/hc/en-us/articles/203157550-Serato-Flip-User-Guide , mined 2026-10-21.

### Release FX — the chain-terminator operator (rekordbox)

rekordbox's Release FX (DDJ-RZX manual, "Using the release FX"; XDJ-RX3 pad assignments) is an operator, not an effect: it "enables you to turn off the beat FX that was on up until now simultaneously with the adding of an effect — the playing track and effect sound can be smoothly connected by using release FX." One release FX per effect unit, fired by the lever/pad release at the moment the running FX dies. Its members are all registry bases — Vinyl Brake → T-006 brake_stop, Echo → T-004 echo_out, Back Spin → T-007 backspin (each in SHORT/LONG duration voicings on the RX3 pads), ECHO OUT ("playing a 1-Beat Loop and fading out the sound") → T-004's loop-form, BUILD UP ("creates a Build Up by gradually reducing the loop length") → GAP-02 loop_tightening_build confirmed verbatim by the first party, MUTE → T-030 hard_cut, DUCKING ("changes the volume according to the beat and fades out the sound by adding a ducking-like effect") → the beat-ducking exit, WEB-13 pumper_exit's mechanism in exit form (Denon's Pumper is the other vendor). In FRAMEWORK §6 terms it is the chain-terminator: whatever chain is running, the release FX is how it ends — an authoring/sequencing rule for chains, not a renderer, so it lives here in the knowledge layer (study program tranche 3, 2026-10-21). **Second-hardware confirmation (tranche 4, 2026-10-21):** Pioneer's RMX-1000 RELEASE FX lever does the same move in dedicated hardware — its three members are VINYL BRAKE → T-006, ECHO → T-004, BACK SPIN → T-007, and the manual (p.14) states that moving the lever turns the release effect on *and turns off any SCENE FX, ISOLATE FX or X-PAD FX effects that were on before*: the terminator semantics are the platform's own, on two independent hardware lines.
Provenance: Pioneer DJ rekordbox — DDJ-RZX manual, "Using the release FX"; XDJ-RX3 manual, Release FX pad assignments, https://rekordbox.com , mined 2026-10-21.

### Smooth Echo — trigger-coupled echo tails (Pioneer DJM-S11)

Pioneer's Smooth Echo (DJM-S11 product copy) assigns a T-004 echo_out throw to a control of the performer's choice — a fader, a pad — so "the echo will be triggered as soon as you move the relevant control": the tail is fired *by the cut gesture itself*, not by a separate FX action. The performance consequence is the point: scratch and fader work leave echo tails without a free hand for the FX lever, so the exit throw and the cut become one motion. As a model it is a trigger-semantics layer over T-004 (and over its pitch-riding sibling WEB-01 spiral_echo): any renderer whose tail is currently "thrown at the seam" can be re-read as thrown by whatever gesture makes the seam — fader cut, backspin, brake. Knowledge-class: it changes when tails fire, not what they are (study program tranche 3, 2026-10-21).
Provenance: Pioneer DJ, DJM-S11 product page — Smooth Echo, https://www.manua.ls/pioneer/djm-s11/manual (manual body pp.55–61 for the Beat FX it couples to), mined 2026-10-21.

### Fade-marker pair — declarative transition authoring (Traktor Cruise Mode)

Traktor's Fade In / Fade Out Cue Points are a transition stored as two annotations, one in each track: "The Fade Out and Fade In Cue Points are used for the automated Cue/Play of tracks. For this to work, you have to set a Fade Out Cue Point in one track and a Fade In Cue Point in another track." Cruise Mode then performs the pair — the next track loads into the opposite deck, starts a few seconds before the current track's end, and the authored points shape the crossfade; the DJ can also fire the transition manually at any moment by pulling the playing channel's fader down. This is Serato Flip's authoring model (tranche 2, above) in its second vendor form, with the division of labour inverted: Flip stores a *performance* (cue choreography) in the track, the fade-marker pair stores a *handoff* (exit point + entry point) split across the pair. Both say the same thing about where transitions live in a prepared library — in the tracks' metadata, decided at prep time, executed at play time — which is the authoring premise behind the registry's premade-edit family (T-028, GAP-07) and behind this repo's own spec format: a transition is a stored object, not an improvisation (study program tranche 7, 2026-10-21).
Provenance: Native Instruments, Traktor Pro 4 manual — Advanced Usage Tutorials, "Working with Cue Points" (Cue Point Types); Advanced Operation, "Using Cruise Mode for Automatic Mixing", https://www.manua.ls/native-instruments/traktor-pro-4/manual , mined 2026-10-21.
