# wordplay

**Bank:** T-011 · **Automatability:** ADAPT · **Confidence:** high

**Source:** Crossfader '12 DJ Transitions' Wordplay; rustlarpdj lyric-based wordplay selection; needs word-level lyric timestamps

## Signature

```python
wordplay(a, b, sr, bpm, a_word_t, b_word_t, word_len_s=0.5, exit='hard_cut', exit_beats=4.0)
```

## Spec

Chain two tracks through a shared lyric word.

a plays until its shared-word onset (a_word_t); b's matching word
(at b_word_t, length word_len_s) triggers in rhythmic unison — the
crowd hears the word "answered" by the new track. After the word
completes, the transition finishes via `exit`.

Parameters
----------
a : outgoing segment; must contain the shared word at a_word_t.
b : incoming segment; must contain the matching word at b_word_t.
a_word_t / b_word_t : word onset times in seconds within a / b.
    From WhisperX-class word alignment in production; caller-supplied.
    Trigger must land within ~±50 ms or the illusion breaks.
word_len_s : duration of the shared word (both tracks).
exit : "hard_cut" (default) — a dies at word end, b continues;
       "echo_out" — a gets a 1/2-beat echo tail while b takes over.

Returns the rendered mix. Handoff point = a_word_t.
