"""
open-transitions engine — clip verification.

Three checks per rendered transition clip:
  (a) silence gaps: no digital-silence (>50 ms below -60 dBFS) except where
      the plan explicitly allows them (allowed_silence spans, in seconds).
  (b) headroom: peak < 0 dBFS (render normalizes to -1 dBFS; this re-checks
      the written file).
  (c) timbre continuity: spectral-centroid track over +/-2 s around the
      handoff point; flags brick-wall jumps (adjacent-window delta > 1500 Hz
      sustained over <100 ms is reported, not failed — some techniques like
      riser drops are *supposed* to snap).

Produces a PNG with the centroid plot + an RMS overview, saved next to the
clip. Returns a dict summary (also written to verification.json by render.py).
"""

import numpy as np
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _HAS_MPL = True
except Exception:
    # numpy 2.x vs system matplotlib 3.6 incompatibility: plots are
    # nice-to-have; verification numerics always run.
    _HAS_MPL = False
    plt = None

from . import dsp


SILENCE_DB = -60.0
MIN_GAP_S = 0.05


def check_silence_gaps(x, sr, allowed=()):
    """Return list of (t0, t1) silence gaps not covered by allowed spans."""
    times, rms = dsp.rms_envelope(x, sr, win_s=MIN_GAP_S)
    db = dsp.gain_to_db(rms)
    silent = db < SILENCE_DB
    gaps = []
    i = 0
    while i < len(silent):
        if silent[i]:
            j = i
            while j < len(silent) and silent[j]:
                j += 1
            gaps.append((float(times[i]), float(times[j - 1]) + MIN_GAP_S))
            i = j
        else:
            i += 1

    def covered(g):
        return any(a0 <= g[0] and g[1] <= a1 for a0, a1 in allowed)

    return [g for g in gaps if not covered(g)]


def check_headroom(x):
    peak = float(np.max(np.abs(x)))
    return {"peak": peak, "peak_dbfs": float(dsp.gain_to_db(peak)),
            "ok": peak < 1.0}


def centroid_continuity(x, sr, handoff_s, window_s=4.0):
    """Centroid track around the handoff; returns (times, cents, max_jump_hz)."""
    if handoff_s is None:
        return None
    i0 = max(0, int((handoff_s - window_s / 2) * sr))
    i1 = min(len(x), int((handoff_s + window_s / 2) * sr))
    seg = x[i0:i1]
    times, cents = dsp.spectral_centroid_track(seg, sr, win_s=0.1, hop_s=0.05)
    times = times + i0 / sr
    jump = float(np.max(np.abs(np.diff(cents)))) if len(cents) > 1 else 0.0
    return {"times": times, "cents": cents, "max_adjacent_jump_hz": jump,
            "handoff_s": handoff_s}


def verify_clip(x, sr, handoff_s=None, allowed_silence=(),
                plot_path=None, clip_id="clip"):
    x = np.asarray(x, dtype=np.float64)
    gaps = check_silence_gaps(x, sr, allowed_silence)
    head = check_headroom(x)
    cc = centroid_continuity(x, sr, handoff_s)

    summary = {
        "clip": clip_id,
        "duration_s": round(len(x) / sr, 2),
        "silence_gaps_s": [(round(a, 2), round(b, 2)) for a, b in gaps],
        "silence_ok": len(gaps) == 0,
        "peak_dbfs": round(head["peak_dbfs"], 2),
        "headroom_ok": head["ok"],
    }
    if cc is not None:
        summary["handoff_s"] = handoff_s
        summary["centroid_max_jump_hz"] = round(cc["max_adjacent_jump_hz"], 1)

    if plot_path and _HAS_MPL:
        _plot(x, sr, cc, gaps, plot_path, clip_id)
    elif plot_path and not _HAS_MPL:
        print(f"    verify: (plot skipped — matplotlib unavailable)", flush=True)

    print(f"    verify: silence_gaps={summary['silence_gaps_s']} "
          f"peak={summary['peak_dbfs']} dBFS "
          + (f"centroid_jump={summary.get('centroid_max_jump_hz')} Hz"
             if cc else ""), flush=True)
    return summary


def _plot(x, sr, cc, gaps, plot_path, clip_id):
    fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=False)

    # Top: RMS overview of the whole clip
    times, rms = dsp.rms_envelope(x, sr, win_s=0.1)
    axes[0].plot(times, dsp.gain_to_db(rms), lw=0.8)
    axes[0].set_ylim(-70, 5)
    axes[0].set_ylabel("RMS (dBFS)")
    axes[0].set_title(f"{clip_id} — level overview")
    axes[0].grid(alpha=0.3)
    for g0, g1 in gaps:
        axes[0].axvspan(g0, g1, color="red", alpha=0.25)

    # Bottom: spectral centroid around handoff
    if cc is not None:
        axes[1].plot(cc["times"], cc["cents"], lw=1.0)
        axes[1].axvline(cc["handoff_s"], color="red", ls="--",
                        label="handoff")
        axes[1].set_ylabel("centroid (Hz)")
        axes[1].set_xlabel("time (s)")
        axes[1].set_title("spectral centroid ±2 s around handoff")
        axes[1].legend()
        axes[1].grid(alpha=0.3)
    else:
        axes[1].text(0.5, 0.5, "no handoff specified", ha="center")

    fig.tight_layout()
    fig.savefig(plot_path, dpi=100)
    plt.close(fig)
