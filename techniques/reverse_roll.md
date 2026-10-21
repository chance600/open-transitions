# reverse_roll

**Bank:** Web-mined 2026-10-21 (WEB-03) — Pioneer REV ROLL beat FX (reversed loop sampler) as an exit build · **Automatability:** High · **Confidence:** High

**Source:** Pestrela DJ Knowledge Base, Effects — REV ROLL: loop sampler reversed

## Signature

`reverse_roll` — family TIME, exit snap, energy delta +1 (rising).

## Spec

Reverse roll: A's last beat loops backwards, tightening, into B.

    The Pioneer REV ROLL beat FX grabs a beat fraction and loops it
    reversed. As a transition: `a` plays clean, then its final beat is
    grabbed and tiled backwards across the last `roll_bars` — the tile
    length halves every two tiles (1 beat -> 1/2 -> 1/4 -> 1/8), so the
    reversed suck inward accelerates — and `b` releases on the downbeat
    the roll was consuming. Output is len(a) + len(b).

    Parameters
    ----------
    a : outgoing segment (mono float64); its final beat is the grabbed
        material, its final `roll_bars` are the roll zone.
    b : incoming segment (mono float64), entered at len(a).
    sr : sample rate, Hz.
    bar_s : seconds per bar.
    roll_bars : roll zone length in bars (default 2).

    Why it works: forward rolls (T-008) build by insistence — the same
    hit harder and faster. Reversed tiles build by *inhalation*: every
    transient sucks back into the deck instead of punching out, the
    phrase feels vacuumed away, and B's first downbeat exhales. It is
    the mirror mechanism of the backspin (T-007) — but where a backspin
    is one continuous spin of the whole tail, the reverse roll stays on
    the grid, so B can land beat-locked.
