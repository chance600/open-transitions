# DRAFT: chopped_screwed_slowdown_chop

Status: DRAFT — not a registry entry. Requires human review before
implementation, demo, or merge. APPLICABLE future research (user
direction 2026-10-29 via style lab): a remix method that transfers
across songs. This draft is technique analysis only — no build.

- Source: screwlab-guide (https://screwlab.com/help/what-is-chopped-and-screwed/)
- Supporting source: minatrix-dj-screw (https://minatrix.fm/en/artists/name/dj_screw/)
- License note: Public articles — learn-from and link only; no license claimed
- Summary: Chopped and screwed remix method: screw tempo and pitch
  down together (~60–75% of the original, classic 60–70 BPM), then
  chop phrases into repeated, skipped, or rearranged segments; the
  vocal survives as a deep, syrupy drawl over thickened bass.

## Evidence (mechanism confirmed)

Chopped and screwed, verified first-hand 2026-10-29 against the
registered sources (public articles, learn-from and link only):

- Screwed (Screwlab): slowing a track's tempo AND pitch down
  together, rather than isolating one or the other the way a modern
  time-stretch tool can. DJ Screw did this by hand, dragging a
  record on two turntables and alternating between them to keep the
  sound continuous as it slowed. The effect drops the vocals into a
  deep, syrupy drawl and thickens the bass — the foundation every
  chopped and screwed track is built on.
- Chopped (Screwlab): the editing side — taking a phrase, verse, or
  hook and cutting it into smaller pieces, then repeating, skipping,
  or rearranging them. A chop might stutter a single word, double a
  line back on itself, or drop a beat out before it lands again. Done
  well, it changes the rhythm and feel of a section without changing
  what is actually being said.
- Two-copy mechanics (Minatrix): working with two turntables and two
  copies of the same track, Screw would significantly reduce playback
  speed (rhythm heavier and more stretched, voices lower), then use
  the mixer and crossfader to repeat individual words, lines, or drum
  fragments by switching back and forth between the two records.
  Cassette transfer could process the finished recording further:
  long spaces between beats, voices dropped in pitch, phrases
  repeated, time radically stretched.
- Tempo rule (Screwlab): classic chopped and screwed lands around
  60–70 BPM, but screwing works by dragging speed down by a
  percentage rather than targeting a fixed BPM — most screwed mixes
  end up around 60–75% of the original tempo (a typical ~90 BPM
  hip-hop track lands close to 60–70 BPM once screwed).
- What it replaces / where chops land: the tight radio edit is
  replaced by a looser, looped arrangement — heavier, slower, more
  hypnotic, built for driving slow rather than the dance floor.
  Scratches, record stops, and DJ tags are common touches layered
  on top. Chops land on phrases, verses, and hooks (word stutters,
  doubled lines, dropped beats), not on arbitrary grid points.
- What it is NOT: "slowed" / "slowed + reverb" tracks borrow the
  tempo drop but usually stop there (a digital pitch and tempo edit
  with reverb, no hand chop). The chop — rearranging and repeating
  sections — is what slowed edits skip.
- Generalization (Minatrix): Screw did not work exclusively with rap
  — his collection spanned artists from across the US and a wide
  variety of genres, incorporated into his mixes. The method is a
  percentage slowdown plus phrase chopping, so it transfers across
  songs rather than belonging to one song's arrangement.

OPEN QUESTION — "crunch": the user's framing describes the style as
"making it a little crunchier," but neither source names a
crunch/distortion stage as part of the technique. What the sources
do describe is thickening (bass), the syrupy drawl, and tape/vinyl
transfer texture. Whether "crunch" means the pitch-down + transfer
texture itself, or an added distortion stage, is UNCONFIRMED — no
distortion mechanism is asserted here. Do not present a crunch unit
as part of this technique until a source states one.

## Applicability (selector fields)

- Tempo: source gives a percentage rule (60–75% of original), not a
  fixed target BPM; classic landing zone 60–70 BPM. No BPM-gap cap
  is stated (this is a whole-track remix, not a pair blend).
- Key/harmonic: source gives no key applicability; pitch drops with
  tempo (linked, not independent), so the whole track transposes
  down together.
- Energy: source gives no energy scale; the result is lower urgency,
  more hypnotic, driving-slow rather than dance-floor.
- Sections: chops land on phrases, verses, and hooks; arrangement
  becomes looser and looped rather than tight.
- Vocals: the vocal survives the slowdown as a deep, syrupy drawl;
  chops stutter words, double lines, and rearrange phrases. The
  vocal is the most exposed element of the method.
- Genre families: Houston hip-hop origin; sources state the method
  was applied across genres (Minatrix), so no single-genre limit is
  asserted.
- Use when: a whole-track remix is wanted that re-weights a song
  toward weight, space, and repetition — slower, heavier, looped —
  with phrase-level chops that change rhythm without changing what
  is said.
- Avoid when: the track's identity depends on its original tempo
  and tight arrangement; the vocal must stay intelligible at
  original pitch; a dance-floor energy level must be preserved.

BUILD GATE (carried, not lifted): chopped-VOCAL builds — any build
that uses a chopped vocal as a hook — still need the user's explicit
word before anyone builds one (style lab will-NOT list: "no vocal
chop as hook"; the 2026-10-29 research direction does not lift it).
Research and analysis need no such word; builds do. This draft is
analysis only.

## Registry fit (META schema)

Mapping to the META schema (engine/meta.py), as a proposal for a
future META entry — not an entry itself.

- Preconditions (requires): a whole source track (not a pair);
  tempo+pitch linked slowdown to ~60–75% of original; phrase-level
  chop points (words, lines, hooks); two-copy or DAW equivalent for
  crossfader-style repeats. No camelot_max, vocal_ok, or genre_pair_ok
  threshold is asserted — the sources state none.
- Energy/exit profile: lateral-to-down energy (urgency drops,
  weight and space rise); exit: the remix IS the track, not a seam
  between two tracks — no handover profile applies.
- Evidence reference: Screwlab, "What Is Chopped and Screwed?"
  (https://screwlab.com/help/what-is-chopped-and-screwed/),
  screwed + chopped definitions, tempo percentage rule, and
  slowed-vs-screwed distinction, read first-hand 2026-10-29;
  Minatrix DJ Screw biography
  (https://minatrix.fm/en/artists/name/dj_screw/), two-copy
  crossfader mechanics and cross-genre application, read first-hand
  2026-10-29. Learn-from and link only; no preset, sample, hook, or
  melody copied.

## Demo + verification checklist (all must pass before merge)

- [ ] Implementation added as an engine function + META entry
- [ ] Demo rendered and listed in demos/out/verification.json
      with render_ok, silence_ok, and headroom_ok all true
- [ ] Technique named in a shipped render and heard by a human
- [ ] Promotion gate passed (see learning/verdicts.py):
      human PASS/heart verdict required; machine metrics never promote
- [ ] Build gate cleared separately if any build uses a chopped
      vocal as a hook (user's explicit word required)

## Provenance

Mined from screwlab-guide + minatrix-dj-screw. Public articles:
learn-from only — reimplement, never copy code or prose verbatim.
No sample, hook, or melody lifted; technique + implementation only.
