"""Generate techniques/<name>.md spec files from engine docstrings + bank metadata.

Usage: python3 demos/gen_technique_docs.py
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "engine", "techniques.py")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "techniques")

# bank_id, automatability verdict, confidence, source note
META = {
    "eq_blend": ("T-001", "ADOPT", "high",
                 "null-set-ai-dj Transition Cookbook (MIT), MusicRadar, mixingguide.com"),
    "bass_swap": ("T-002", "ADOPT", "high",
                  "null-set-ai-dj (MIT); the single most important 1-beat move in dance mixing"),
    "filter_sweep": ("T-003", "ADOPT", "high",
                     "null-set-ai-dj (MIT), MusicRadar"),
    "echo_out": ("T-004", "ADOPT", "high",
                 "null-set-ai-dj (MIT), DJ Carlo Atendido, MusicRadar"),
    "echo_out_blend": ("T-004b", "ADOPT", "high",
                       "engine original; field-tested on blend 02/03 work"),
    "layered_emergence": ("T-004c", "ADOPT", "high",
                          "engine original; field-tested on blend 02/03 work"),
    "reverb_wash": ("T-005", "ADOPT", "high",
                    "null-set-ai-dj (MIT), MusicRadar"),
    "brake_stop": ("T-006", "ADOPT", "high",
                   "Virtual Clubbing Life (rekordbox brake dial), Cassette Transport"),
    "backspin": ("T-007", "ADAPT", "medium",
                 "null-set-ai-dj (MIT); flick force is feel — 1-beat default"),
    "loop_roll_build": ("T-008", "ADOPT", "high",
                        "null-set-ai-dj (MIT), Crossfader"),
    "acapella_overlay": ("T-010", "ADAPT", "medium",
                         "null-set-ai-dj (MIT); phrase selection + fader riding are human"),
    "power_down": ("T-013", "ADOPT", "high",
                   "standard turntablist technique; curve shape is the tuning parameter"),
    "hotcue_drop_swap": ("T-014", "ADOPT", "high",
                         "Virtual Clubbing Life (4-beats-before-the-drop)"),
    "harmonic_mix": ("T-015", "ADOPT", "high",
                     "Camelot wheel; pure decision function over key codes"),
    "layered_fx_stack": ("T-017", "ADOPT", "high",
                         "VirtualDJ mapping community, ProDJ School, Club Ready"),
    "noise_echo_buildup": ("T-018", "ADOPT", "high",
                           "ProDJ School (Noise color FX + empty channel + Echo 1/2)"),
    "stutter_transition": ("T-019", "ADAPT", "medium",
                           "null-set-ai-dj (MIT); hot-cue transient placement needs onset detection"),
    "tempo_bridge": ("T-021", "ADOPT", "high",
                     "null-set-ai-dj (MIT); the engine's authorized time-stretch primitive"),
    "drum_bridge": ("T-022", "ADOPT", "high",
                    "null-set-ai-dj (MIT); strip is a full-mix approximation — stems are exact"),
    "breakdown_transition": ("T-023", "ADOPT", "high",
                             "null-set-ai-dj (MIT)"),
    "double_drop": ("T-024", "ADAPT", "medium",
                    "null-set-ai-dj (MIT); drop-pair complementarity is curatorial"),
    "vocal_punchline_snap": ("T-025", "ADOPT", "high",
                             "null-set-ai-dj (MIT)"),
    "genre_bridge": ("T-026", "ADAPT", "medium",
                     "null-set-ai-dj (MIT); the bridge leap is a taste decision"),
    "loop_transition": ("T-027", "ADOPT", "high",
                        "null-set-ai-dj (MIT); 2-cycle cap is the discipline"),
    "fake_drop": ("T-029", "ADAPT", "medium",
                  "null-set-ai-dj (MIT); human-triggered weapon, never auto-deployed"),
    "hard_cut": ("T-030", "ADOPT", "high",
                 "null-set-ai-dj (MIT); selection belongs to the framework (T-037)"),
    "loop_juggle_replace": ("T-031", "ADAPT", "medium",
                            "djwes/ausdjforums (The Replace); digital hot-cue adaptation"),
    "vocal_chop_build": ("T-033", "ADOPT", "high",
                         "MusicRadar, DJ Carlo cue-drumming lineage"),
    "reverb_freeze": ("T-034", "ADOPT", "high",
                      "DJM-V10 freeze translated to software parameters; first written recipe"),
    "riser_drop": ("—", "ADOPT", "medium",
                   "engine original: riser synth + HP thinning into a tempo-jump drop"),
    "select_technique": ("T-037", "ADOPT", "high",
                         "bank synthesis: rejection rules prune first, decision table picks"),
    "hook_drop_handoff": ("T-038", "ADOPT", "field-tested",
                          "original — distilled from blend 01 workshopping (v9-v18); "
                          "v14 = user-approved keeper, v17 = 'Awesome, yes'"),
    "wordplay": ("T-011", "ADAPT", "high",
                 "Crossfader '12 DJ Transitions' Wordplay; rustlarpdj lyric-based "
                 "wordplay selection; needs word-level lyric timestamps"),
    "build_to_drop": ("T-009", "ADAPT", "high",
                      "null-set-ai-dj (MIT); build-boundary detection is the "
                      "caller's job (ADAPT caveat)"),
    "three_deck_layer": ("T-020", "ADAPT", "medium",
                         "null-set-ai-dj (MIT); glue-layer selection is curatorial; "
                         "Garrix / Andy C practitioners"),
    "beat_jump": ("T-028", "ADOPT", "high",
                  "null-set-ai-dj (MIT); Coach Hapa 4-step; planning primitive — "
                  "pure playhead arithmetic"),
    "beat_jump_transition": ("T-028", "ADOPT", "high",
                             "rendered demo of the beat_jump repair primitive"),
    "pitch_play": ("T-032", "ADOPT", "high",
                   "Virtual Clubbing Life Acapella Pitch Play; |semitones| <= 2 "
                   "bank rule; not formant-preserving"),
    "screwed_treatment": ("T-039", "ADOPT", "high",
                          "DJ Screw canon (pitch-coupled slowdown + chops); "
                          "'slowed + reverb' variant; note ideas #20, #27, #39"),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    tree = ast.parse(open(SRC).read())
    made = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in META:
            doc = ast.get_docstring(node) or "(no docstring)"
            bank_id, verdict, conf, source = META[node.name]
            args = [a.arg for a in node.args.args]
            defaults = [ast.unparse(d) for d in node.args.defaults]
            sig = ", ".join(
                args[:len(args) - len(defaults)] +
                [f"{a}={d}" for a, d in zip(args[len(args) - len(defaults):],
                                            defaults)])
            md = (f"# {node.name}\n\n"
                  f"**Bank:** {bank_id} · **Automatability:** {verdict} · "
                  f"**Confidence:** {conf}\n\n"
                  f"**Source:** {source}\n\n"
                  f"## Signature\n\n```python\n{node.name}({sig})\n```\n\n"
                  f"## Spec\n\n{doc}\n")
            path = os.path.join(OUT, node.name + ".md")
            open(path, "w").write(md)
            made.append(node.name)
    # index
    idx = "# Technique Specs\n\n" + "\n".join(
        f"- [{n}]({n}.md) — {META[n][0]}" for n in sorted(made)) + "\n"
    open(os.path.join(OUT, "INDEX.md"), "w").write(idx)
    print(f"wrote {len(made)} technique specs + INDEX.md")
    missing = set(META) - set(made)
    if missing:
        print("WARNING: no function found for:", sorted(missing))


if __name__ == "__main__":
    main()
