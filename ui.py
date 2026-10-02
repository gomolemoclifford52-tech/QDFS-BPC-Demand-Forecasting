"""Visual layer for QDFS.

All custom CSS and the HTML for the dashboard hero and cards live here,
so app.py keeps the forecasting logic and Streamlit layout only.

The builders return plain HTML strings. They have no Streamlit
dependency, which keeps them easy to test and preview.
"""

from html import escape

import matplotlib.pyplot as plt


# ============================================================
# Design tokens
# ============================================================

INK = "#1C201D"
MUTED = "#6B706B"
LINE = "#D6D8D0"
ORANGE = "#EC6A24"   # Moving Average
OLIVE = "#6F7A45"    # Exponential Smoothing
OLIVE_CARD = "#A3AA84"

SERIES_COLORS = {
    "actual": INK,
    "ma": ORANGE,
    "es": OLIVE,
}


# ============================================================
# Global CSS
# ============================================================

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&display=swap');

:root {
    --q-canvas: #E6E7E2;
    --q-card: rgba(255, 255, 255, 0.72);
    --q-card-edge: rgba(255, 255, 255, 0.95);
    --q-ink: #1C201D;
    --q-muted: #6B706B;
    --q-line: #D6D8D0;
    --q-track: #D3D5CC;
    --q-orange: #EC6A24;
    --q-orange-soft: #F8D8C3;
    --q-olive: #6F7A45;
    --q-olive-card: #A3AA84;
    --q-olive-ink: #262B16;
    --q-shadow: 0 1px 0 rgba(0, 0, 0, 0.03),
                0 18px 40px -24px rgba(38, 43, 22, 0.35);
    --q-font: "Archivo", "Helvetica Neue", Arial, sans-serif;
}

/* ---------- App shell ---------- */

.stApp {
    background:
        radial-gradient(1100px 560px at 72% -8%, #F6F6F2 0%, rgba(246, 246, 242, 0) 70%),
        var(--q-canvas);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stMainBlockContainer"],
.block-container {
    max-width: 1380px;
    padding-top: 1.4rem;
}

[data-testid="stSidebar"] {
    border-right: 1px solid var(--q-line);
}

/* ---------- Pill tab navigation ---------- */

[role="tablist"] {
    gap: 4px;
    width: fit-content;
    max-width: 100%;
    margin: 0 auto 1.6rem auto;
    padding: 5px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.55);
    border: 1px solid var(--q-card-edge);
    box-shadow: var(--q-shadow);
    overflow-x: auto;
}

[role="tab"] {
    height: auto;
    padding: 0.5rem 1.1rem;
    border-radius: 999px;
    border: none;
    background: transparent;
    color: var(--q-muted);
}

[role="tab"] p {
    font-size: 0.92rem;
    font-weight: 500;
}

[role="tab"][aria-selected="true"] {
    background: #FFFFFF;
    color: var(--q-ink);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

[role="tab"]:focus-visible {
    outline: 2px solid var(--q-orange);
    outline-offset: 2px;
}

[data-baseweb="tab-highlight"],
[data-baseweb="tab-border"] {
    display: none;
}

/* ---------- Streamlit elements as cards ---------- */

[class*="st-key-card"] {
    background: var(--q-card);
    border: 1px solid var(--q-card-edge);
    border-radius: 22px;
    padding: 1.25rem 1.4rem 1.4rem 1.4rem;
    box-shadow: var(--q-shadow);
}

[data-testid="stMetric"] {
    background: var(--q-card);
    border: 1px solid var(--q-card-edge);
    border-radius: 16px;
    padding: 0.9rem 1.1rem;
}

[class*="st-key-card"] [data-testid="stMetric"] {
    background: transparent;
    border: none;
    padding: 0;
}

[data-testid="stMetricValue"] {
    font-variant-numeric: tabular-nums;
    font-weight: 600;
    letter-spacing: -0.01em;
}

[data-testid="stMetricLabel"] p {
    color: var(--q-muted);
}

[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

[data-testid="stAlert"] {
    border-radius: 14px;
}

[data-testid="stExpander"] details {
    border-radius: 16px;
    background: var(--q-card);
    border-color: var(--q-card-edge);
}

h2, h3 {
    letter-spacing: -0.01em;
}

/* ---------- Custom HTML components ---------- */

.q-root {
    font-family: var(--q-font);
    color: var(--q-ink);
    font-variant-numeric: tabular-nums;
}

.q-root *,
.q-root *::before,
.q-root *::after {
    box-sizing: border-box;
}

.q-root h1,
.q-root h2,
.q-root h3,
.q-root p,
.q-root dl,
.q-root dd {
    margin: 0;
    padding: 0;
    font-family: var(--q-font);
}

.q-root h1,
.q-root h2,
.q-root h3 {
    color: inherit;
}

/* Top bar */

.q-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1.1rem;
}

.q-brand {
    display: flex;
    align-items: center;
    gap: 0.65rem;
}

.q-mark {
    display: grid;
    place-items: center;
    width: 38px;
    height: 38px;
    border-radius: 12px;
    background: var(--q-ink);
}

.q-mark svg {
    width: 18px;
    height: 18px;
}

.q-brand-name {
    font-size: 1.15rem;
    font-weight: 750;
    font-stretch: 118%;
    letter-spacing: 0.01em;
}

.q-brand-sub {
    color: var(--q-muted);
    font-size: 0.9rem;
}

.q-source {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.45rem 0.9rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.6);
    border: 1px solid var(--q-card-edge);
    color: var(--q-muted);
    font-size: 0.85rem;
}

.q-source strong {
    color: var(--q-ink);
    font-weight: 600;
}

/* Hero */

.q-hero {
    display: grid;
    grid-template-columns: minmax(0, 1.55fr) minmax(300px, 1fr);
    gap: 2rem;
    align-items: stretch;
    margin-bottom: 1.25rem;
}

.q-hero-main {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 1.6rem;
    padding-top: 0.4rem;
}

.q-root .q-title {
    font-size: clamp(2.1rem, 4.1vw, 3.55rem);
    font-weight: 760;
    font-stretch: 116%;
    line-height: 0.98;
    letter-spacing: -0.012em;
    text-transform: uppercase;
    max-width: 18ch;
}

.q-lede {
    margin-top: 0.9rem !important;
    max-width: 52ch;
    color: var(--q-muted);
    font-size: 1rem;
    line-height: 1.5;
}

.q-kpis {
    display: flex;
    flex-wrap: wrap;
    gap: 1.2rem 2.6rem;
}

.q-kpi-value {
    font-size: clamp(1.5rem, 2.3vw, 2rem);
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1.1;
}

.q-unit {
    margin-left: 0.25rem;
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--q-muted);
    letter-spacing: 0;
    vertical-align: 0.65em;
}

.q-kpi-label {
    margin-top: 0.25rem;
    color: var(--q-muted);
    font-size: 0.85rem;
}

.q-segbar {
    display: flex;
    gap: 3px;
    height: 20px;
}

.q-seg {
    flex: 1 1 0;
    border-radius: 3px;
    background: var(--q-track);
}

.q-seg.is-on {
    background: var(--q-orange);
}

.q-segbar-legend {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-top: 0.5rem;
    color: var(--q-muted);
    font-size: 0.8rem;
}

.q-segbar-legend span:first-child,
.q-segbar-legend span:last-child {
    white-space: nowrap;
}

.q-segbar-legend .q-mid {
    color: var(--q-ink);
    text-align: center;
}

/* Surfaces */

.q-panel,
.q-card {
    background: var(--q-card);
    border: 1px solid var(--q-card-edge);
    border-radius: 22px;
    box-shadow: var(--q-shadow);
}

.q-panel {
    padding: 1.3rem 1.4rem;
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
}

.q-panel.is-empty {
    align-self: start;
}

.q-panel .q-note {
    margin-top: auto !important;
}

.q-panel-head,
.q-card-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
}

.q-root .q-panel-head h2 {
    font-size: 1.05rem;
    font-weight: 650;
}

.q-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.22rem 0.65rem;
    border-radius: 999px;
    background: rgba(28, 32, 29, 0.06);
    font-size: 0.78rem;
    font-weight: 500;
    white-space: nowrap;
}

.q-chip::before {
    content: "";
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--q-muted);
}

.q-chip.is-ok::before { background: #4E8A3E; }
.q-chip.is-stale::before { background: var(--q-orange); }
.q-chip.is-plain::before { display: none; }

.q-rows {
    display: flex;
    flex-direction: column;
}

.q-row {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.7rem 0;
    border-top: 1px solid var(--q-line);
}

.q-row:first-child {
    border-top: none;
}

.q-row-label {
    color: var(--q-muted);
    font-size: 0.9rem;
}

.q-row-value {
    font-weight: 600;
    text-align: right;
    white-space: nowrap;
}

.q-row-sub {
    display: block;
    margin-top: 0.15rem;
    color: var(--q-muted);
    font-size: 0.78rem;
    font-weight: 500;
}

.q-swatch {
    display: inline-block;
    width: 9px;
    height: 9px;
    margin-right: 0.45rem;
    border-radius: 3px;
    vertical-align: 0.05em;
}

.q-note {
    color: var(--q-muted);
    font-size: 0.8rem;
    line-height: 1.45;
}

.q-empty {
    color: var(--q-muted);
    line-height: 1.5;
}

.q-empty strong {
    color: var(--q-ink);
}

/* Card grid */

.q-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 1rem;
    margin-bottom: 1.25rem;
}

.q-card {
    padding: 1.15rem 1.2rem 1.2rem 1.2rem;
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
    min-height: 250px;
}

.q-card.span-3 {
    grid-column: span 3;
}

.q-card-head.is-stacked {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.2rem;
}

.q-root .q-card-head h3 {
    font-size: 0.98rem;
    font-weight: 650;
}

.q-big {
    font-size: 1.85rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1;
}

/* Forecast range on a shared scale */

.q-range-track {
    position: relative;
    height: 10px;
    border-radius: 999px;
    background: var(--q-track);
}

.q-range-band {
    position: absolute;
    top: 0;
    bottom: 0;
    border-radius: 999px;
    opacity: 0.45;
}

.q-range-dot {
    position: absolute;
    top: 50%;
    width: 14px;
    height: 14px;
    margin-left: -7px;
    margin-top: -7px;
    border-radius: 50%;
    border: 2px solid #FFFFFF;
}

.q-range-scale {
    display: flex;
    justify-content: space-between;
    margin-top: 0.35rem;
    color: var(--q-muted);
    font-size: 0.72rem;
}

.q-stats {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 0.35rem 1rem;
    font-size: 0.86rem;
    margin-top: auto !important;
}

.q-stats dt {
    color: var(--q-muted);
}

.q-stats dd {
    text-align: right;
    font-weight: 600;
}

/* Olive history card */

.q-card.is-olive {
    background: var(--q-olive-card);
    border-color: rgba(255, 255, 255, 0.35);
    color: var(--q-olive-ink);
}

.q-card.is-olive .q-sub {
    color: rgba(38, 43, 22, 0.75);
}

.q-sub {
    color: var(--q-muted);
    font-size: 0.8rem;
}

.q-bars {
    display: flex;
    align-items: flex-end;
    gap: 3px;
    height: 112px;
    flex: 1 1 auto;
}

.q-bar {
    flex: 1 1 0;
    min-width: 2px;
    border-radius: 3px 3px 1px 1px;
    background: rgba(38, 43, 22, 0.78);
}

.q-bar.is-latest {
    background: #F7F7F2;
}

.q-history-foot {
    display: flex;
    justify-content: space-between;
    gap: 0.75rem;
    font-size: 0.8rem;
}

.q-history-foot b {
    display: block;
    font-size: 0.95rem;
    font-weight: 650;
}

/* MAPE columns */

.q-cols {
    display: flex;
    gap: 0.8rem;
    flex: 1 1 auto;
    align-items: stretch;
}

.q-col {
    flex: 1 1 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
}

.q-col-value {
    font-weight: 650;
    font-size: 0.95rem;
}

.q-col-track {
    position: relative;
    width: 100%;
    max-width: 64px;
    flex: 1 1 auto;
    min-height: 96px;
    border-radius: 16px;
    background: rgba(28, 32, 29, 0.06);
    overflow: hidden;
}

.q-col-fill {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 16px;
}

.q-col-name {
    color: var(--q-muted);
    font-size: 0.8rem;
}

/* Workflow (empty state) */

.q-steps {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 1rem;
}

.q-step .q-step-n {
    display: inline-grid;
    place-items: center;
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: var(--q-ink);
    color: #FFFFFF;
    font-size: 0.78rem;
    font-weight: 600;
    margin-bottom: 0.55rem;
}

.q-step b {
    display: block;
    margin-bottom: 0.2rem;
}

.q-step span {
    color: var(--q-muted);
    font-size: 0.88rem;
    line-height: 1.45;
}

/* Page header for the non-dashboard tabs */

.q-page {
    margin-bottom: 1.1rem;
}

.q-root .q-page h2 {
    font-size: 1.6rem;
    font-weight: 740;
    font-stretch: 114%;
    text-transform: uppercase;
    letter-spacing: -0.005em;
    line-height: 1.05;
}

.q-page p {
    margin-top: 0.45rem !important;
    color: var(--q-muted);
    max-width: 70ch;
}

/* ---------- Responsive ---------- */

@media (max-width: 1100px) {
    .q-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .q-card.span-3 { grid-column: span 1; }
    .q-steps { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media (max-width: 900px) {
    .q-hero { grid-template-columns: minmax(0, 1fr); }
}

@media (max-width: 640px) {
    .q-grid { grid-template-columns: minmax(0, 1fr); }
    .q-steps { grid-template-columns: minmax(0, 1fr); }
    .q-kpis { gap: 1rem 1.6rem; }
    .q-card { min-height: 0; }
}
</style>
"""


# ============================================================
# Formatting helpers
# ============================================================

def mwh(value):
    """Whole-number MWh with thousands separators."""
    return f"{value:,.0f}"


def compact(value):
    """Short scale label, e.g. 1.19M or 840k."""
    magnitude = abs(value)

    if magnitude >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    if magnitude >= 1_000:
        return f"{value / 1_000:.0f}k"

    return f"{value:,.0f}"


def _pct(value, low, high):
    if high <= low:
        return 50.0

    return max(0.0, min(100.0, (value - low) / (high - low) * 100))


def _join(parts):
    """Join HTML fragments without blank lines or indentation."""
    return "".join(part.strip() for part in parts)


BOLT_SVG = (
    '<svg viewBox="0 0 24 24" aria-hidden="true">'
    '<path d="M13.2 2 4.5 13.6h6.1L9.9 22l8.6-11.6h-6.1L13.2 2Z" '
    'fill="#EC6A24"/></svg>'
)


# ============================================================
# Components
# ============================================================

def topbar(data_source, first_quarter, last_quarter):
    return _join([
        '<div class="q-root q-topbar">',
        '<div class="q-brand">',
        f'<span class="q-mark">{BOLT_SVG}</span>',
        '<span class="q-brand-name">QDFS</span>',
        '<span class="q-brand-sub">Quarterly demand forecasting</span>',
        '</div>',
        '<div class="q-source">',
        f'<strong>{escape(str(data_source))}</strong>',
        f'<span>{escape(str(first_quarter))} to {escape(str(last_quarter))}</span>',
        '</div>',
        '</div>',
    ])


def page_header(title, description=""):
    description_html = (
        f"<p>{escape(description)}</p>" if description else ""
    )

    return _join([
        '<div class="q-root q-page">',
        f'<h2>{escape(title)}</h2>',
        description_html,
        '</div>',
    ])


def _segbar(n_quarters, highlight_last, first_quarter, last_quarter, caption):
    segments = []

    for index in range(n_quarters):
        is_on = highlight_last and index >= n_quarters - highlight_last
        css_class = "q-seg is-on" if is_on else "q-seg"
        segments.append(f'<span class="{css_class}"></span>')

    return _join([
        f'<div class="q-segbar" role="img" aria-label="{escape(caption)}">',
        "".join(segments),
        '</div>',
        '<div class="q-segbar-legend">',
        f'<span>{escape(str(first_quarter))}</span>',
        f'<span class="q-mid">{escape(caption)}</span>',
        f'<span>{escape(str(last_quarter))}</span>',
        '</div>',
    ])


def _forecast_panel(f):
    if f is None:
        return ""

    status_class = "is-ok"
    status_text = "Up to date"

    def versus_latest(value):
        change = (value - f["latest"]) / f["latest"] * 100
        sign = "+" if change >= 0 else "\u2212"
        return (
            f'<span class="q-row-sub">{sign}{abs(change):.1f}% vs '
            f'{escape(str(f["latest_quarter"]))}</span>'
        )

    rows = [
        (
            f'<span class="q-swatch" style="background:{ORANGE}"></span>'
            f'Moving average, {f["ma_window"]} quarters',
            f'{mwh(f["ma_next"])} MWh{versus_latest(f["ma_next"])}',
        ),
        (
            f'<span class="q-swatch" style="background:{OLIVE}"></span>'
            f'Exponential smoothing, α {f["alpha"]:.1f}',
            f'{mwh(f["es_next"])} MWh{versus_latest(f["es_next"])}',
        ),
        (
            "Gap between the two forecasts",
            f'{mwh(abs(f["ma_next"] - f["es_next"]))} MWh',
        ),
        (
            "Lower historical MAPE",
            escape(f["lower_mape_label"]),
        ),
    ]

    row_html = "".join(
        '<div class="q-row">'
        f'<span class="q-row-label">{label}</span>'
        f'<span class="q-row-value">{value}</span>'
        '</div>'
        for label, value in rows
    )

    return _join([
        '<aside class="q-panel">',
        '<div class="q-panel-head">',
        f'<h2>Forecast for {escape(f["next_quarter"])}</h2>',
        f'<span class="q-chip {status_class}">{status_text}</span>',
        '</div>',
        f'<div class="q-rows">{row_html}</div>',
        '<p class="q-note">Ranges on the cards below are forecast ± MAD. '
        'They are error-based ranges, not confidence intervals.</p>',
        '</aside>',
    ])


def _empty_panel(next_quarter, stale=False):
    if stale:
        chip = '<span class="q-chip is-stale">Out of date</span>'
        message = (
            'The data or parameters changed since the last run. Select '
            '<strong>Run forecast</strong> in the sidebar to refresh.'
        )
    else:
        chip = '<span class="q-chip">Not run</span>'
        message = (
            'Set the moving-average window and α in the sidebar, then '
            'select <strong>Run forecast</strong>. Both models and their '
            'accuracy will appear here.'
        )

    return _join([
        '<aside class="q-panel is-empty">',
        '<div class="q-panel-head">',
        f'<h2>Forecast for {escape(next_quarter)}</h2>',
        chip,
        '</div>',
        f'<p class="q-empty">{message}</p>',
        '</aside>',
    ])


def hero(dataset, forecast=None, next_quarter="Next quarter", stale=False):
    """Dashboard hero: headline, dataset figures, quarter strip, forecast panel.

    dataset: dict with n, latest, latest_quarter, average,
             first_quarter, last_quarter
    forecast: dict from forecast_summary(), or None before a run
    """
    kpis = [
        (mwh(dataset["latest"]), "MWh",
         f'Latest quarter, {dataset["latest_quarter"]}'),
        (mwh(dataset["average"]), "MWh", "Quarterly average"),
        (f'{dataset["n"]}', "", "Quarters of data"),
    ]

    kpi_html = "".join(
        '<div class="q-kpi">'
        f'<div class="q-kpi-value">{value}'
        + (f'<span class="q-unit">{unit}</span>' if unit else "")
        + '</div>'
        f'<div class="q-kpi-label">{escape(label)}</div>'
        '</div>'
        for value, unit, label in kpis
    )

    if forecast is not None:
        window = forecast["ma_window"]
        caption = f"Last {window} quarters feed the moving-average forecast"
        highlight = window
        panel = _forecast_panel(forecast)
    else:
        caption = f'{dataset["n"]} quarters loaded'
        highlight = 0
        panel = _empty_panel(next_quarter, stale)

    segbar = _segbar(
        dataset["n"],
        highlight,
        dataset["first_quarter"],
        dataset["last_quarter"],
        caption,
    )

    return _join([
        '<section class="q-root q-hero">',
        '<div class="q-hero-main">',
        '<div>',
        '<h1 class="q-title">Quarterly electricity demand forecast</h1>',
        '<p class="q-lede">Moving average and exponential smoothing, '
        'compared on Botswana Power Corporation distribution data. '
        'Distribution is used as a proxy for demand.</p>',
        '</div>',
        f'<div class="q-kpis">{kpi_html}</div>',
        f'<div>{segbar}</div>',
        '</div>',
        panel,
        '</section>',
    ])


def _model_card(title, chip, color, point, lower, upper, mad, mape,
                scale_low, scale_high):
    band_left = _pct(lower, scale_low, scale_high)
    band_right = _pct(upper, scale_low, scale_high)
    dot = _pct(point, scale_low, scale_high)

    return _join([
        '<article class="q-card">',
        '<div class="q-card-head">',
        f'<h3>{escape(title)}</h3>',
        f'<span class="q-chip is-plain">{escape(chip)}</span>',
        '</div>',
        f'<div class="q-big">{mwh(point)}<span class="q-unit">MWh</span></div>',
        '<div>',
        '<div class="q-range-track" role="img" '
        f'aria-label="Forecast {mwh(point)} MWh, range {mwh(lower)} to {mwh(upper)} MWh">',
        f'<span class="q-range-band" style="left:{band_left:.2f}%;'
        f'width:{band_right - band_left:.2f}%;background:{color}"></span>',
        f'<span class="q-range-dot" style="left:{dot:.2f}%;background:{color}"></span>',
        '</div>',
        '<div class="q-range-scale">',
        f'<span>{compact(scale_low)}</span>',
        '<span>Shared scale, both models</span>',
        f'<span>{compact(scale_high)}</span>',
        '</div>',
        '</div>',
        '<dl class="q-stats">',
        f'<dt>Range ± MAD</dt><dd>{mwh(lower)} to {mwh(upper)}</dd>',
        f'<dt>MAD</dt><dd>{mwh(mad)} MWh</dd>',
        f'<dt>MAPE</dt><dd>{mape:.2f}%</dd>',
        '</dl>',
        '</article>',
    ])


def _history_card(quarters, values):
    peak_index = max(range(len(values)), key=lambda i: values[i])
    low_index = min(range(len(values)), key=lambda i: values[i])
    top = max(values) if max(values) > 0 else 1

    bars = []

    for index, (quarter, value) in enumerate(zip(quarters, values)):
        height = value / top * 100
        css_class = "q-bar is-latest" if index == len(values) - 1 else "q-bar"
        bars.append(
            f'<span class="{css_class}" style="height:{height:.2f}%" '
            f'title="{escape(str(quarter))}: {mwh(value)} MWh"></span>'
        )

    return _join([
        '<article class="q-card is-olive">',
        '<div class="q-card-head is-stacked">',
        '<h3>Quarterly distribution</h3>',
        f'<span class="q-sub">{escape(str(quarters[0]))} to '
        f'{escape(str(quarters[-1]))}</span>',
        '</div>',
        '<div class="q-bars" role="img" aria-label="Quarterly distribution '
        f'from {escape(str(quarters[0]))} to {escape(str(quarters[-1]))}">',
        "".join(bars),
        '</div>',
        '<div class="q-history-foot">',
        f'<span><b>{mwh(values[peak_index])}</b>'
        f'<span class="q-sub">Peak, {escape(str(quarters[peak_index]))}</span></span>',
        f'<span style="text-align:right"><b>{mwh(values[low_index])}</b>'
        f'<span class="q-sub">Low, {escape(str(quarters[low_index]))}</span></span>',
        '</div>',
        '</article>',
    ])


def _mape_card(f):
    top = max(f["ma_mape"], f["es_mape"]) or 1

    columns = [
        ("MA", f["ma_mape"], ORANGE),
        ("ES", f["es_mape"], OLIVE),
    ]

    col_html = "".join(
        '<div class="q-col">'
        f'<span class="q-col-value">{value:.2f}%</span>'
        '<div class="q-col-track">'
        f'<span class="q-col-fill" style="height:{value / top * 100:.2f}%;'
        f'background:{color}"></span>'
        '</div>'
        f'<span class="q-col-name">{name}</span>'
        '</div>'
        for name, value, color in columns
    )

    return _join([
        '<article class="q-card">',
        '<div class="q-card-head">',
        '<h3>Historical MAPE</h3>',
        '<span class="q-chip is-plain">Lower is better</span>',
        '</div>',
        f'<div class="q-cols">{col_html}</div>',
        f'<p class="q-note">MA scored on {f["ma_eval_n"]} quarters, '
        f'ES on {f["es_eval_n"]}. Different periods, so treat the gap '
        'with care.</p>',
        '</article>',
    ])


def _workflow_card():
    steps = [
        ("Load data", "Use the built-in BPC dataset or upload a CSV or Excel file."),
        ("Set parameters", "Choose the moving-average window and smoothing α."),
        ("Run forecast", "Generate historical and next-quarter forecasts."),
        ("Review and export", "Compare MAD and MAPE, then download the report."),
    ]

    step_html = "".join(
        '<div class="q-step">'
        f'<span class="q-step-n">{number}</span>'
        f'<b>{escape(title)}</b>'
        f'<span>{escape(text)}</span>'
        '</div>'
        for number, (title, text) in enumerate(steps, start=1)
    )

    return _join([
        '<article class="q-card span-3">',
        '<div class="q-card-head"><h3>How it works</h3></div>',
        f'<div class="q-steps">{step_html}</div>',
        '</article>',
    ])


def dashboard_cards(quarters, values, forecast=None):
    """Card row under the hero."""
    history = _history_card(list(quarters), [float(v) for v in values])

    if forecast is None:
        return _join([
            '<div class="q-root q-grid">',
            history,
            _workflow_card(),
            '</div>',
        ])

    low = min(forecast["ma_lower"], forecast["es_lower"])
    high = max(forecast["ma_upper"], forecast["es_upper"])
    pad = (high - low) * 0.12 or abs(high) * 0.05 or 1
    scale_low, scale_high = low - pad, high + pad

    ma_card = _model_card(
        "Moving average",
        f'{forecast["ma_window"]} quarters',
        ORANGE,
        forecast["ma_next"],
        forecast["ma_lower"],
        forecast["ma_upper"],
        forecast["ma_mad"],
        forecast["ma_mape"],
        scale_low,
        scale_high,
    )

    es_card = _model_card(
        "Exponential smoothing",
        f'α {forecast["alpha"]:.1f}',
        OLIVE,
        forecast["es_next"],
        forecast["es_lower"],
        forecast["es_upper"],
        forecast["es_mad"],
        forecast["es_mape"],
        scale_low,
        scale_high,
    )

    return _join([
        '<div class="q-root q-grid">',
        ma_card,
        history,
        es_card,
        _mape_card(forecast),
        '</div>',
    ])


# ============================================================
# Matplotlib styling
# ============================================================

def style_axes(fig, ax, title, x_label, y_label):
    """Apply the QDFS look to a Matplotlib chart."""
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)

    ax.spines["bottom"].set_color(LINE)
    ax.tick_params(colors=MUTED, labelsize=9, length=0, pad=6)
    if "MWh" in y_label:
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda value, _: f"{value:,.0f}")
        )
    ax.grid(axis="y", color=LINE, linewidth=0.8)
    ax.grid(axis="x", visible=False)
    ax.set_axisbelow(True)

    has_legend = bool(ax.get_legend_handles_labels()[0])

    ax.set_title(title, loc="left", fontsize=12, fontweight="semibold",
                 color=INK, pad=34 if has_legend else 14)
    ax.set_xlabel(x_label, color=MUTED, fontsize=9, labelpad=8)
    ax.set_ylabel(y_label, color=MUTED, fontsize=9, labelpad=8)

    if has_legend:
        legend = ax.legend(frameon=False, fontsize=9, loc="lower left",
                           ncol=4, bbox_to_anchor=(0, 1.0),
                           borderaxespad=0.3, handlelength=2.2)
        for text in legend.get_texts():
            text.set_color(INK)
