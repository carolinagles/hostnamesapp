"""Hostname Generator - Streamlit app (Swiss minimalist design).

Run locally:   streamlit run app/streamlit_app.py
"""
import html
import json

import streamlit as st
import streamlit.components.v1 as components

import hostnames as hn

st.set_page_config(page_title="Hostname Generator", layout="centered",
                   initial_sidebar_state="collapsed")

ACCENT = "#1F4D33"
INK = "#111111"
MUTED = "#6E6E6A"
RULE = "#E4E4E0"
FONT = "'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace"
FONT_IMPORT = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700"
               "&family=JetBrains+Mono:wght@400;500&display=swap")

# --------------------------------------------------------------------------- styles
st.markdown(f"""
<style>
@import url('{FONT_IMPORT}');

html, body, .stApp, .stApp p, .stApp label, .stApp input, .stApp button,
.stApp h1, .stApp h2, .stApp h3, .stApp div {{ font-family: {FONT}; }}

header[data-testid="stHeader"], #MainMenu, footer,
[data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}

.block-container {{ max-width: 880px; padding-top: 4.5rem; padding-bottom: 6rem; }}

/* Typography */
.eyebrow {{ font-size: .72rem; font-weight: 600; letter-spacing: .14em;
           text-transform: uppercase; color: {ACCENT}; margin: 0 0 1.1rem; }}
.title {{ font-size: 3.1rem; font-weight: 700; line-height: 1.02; letter-spacing: -.035em;
          color: {INK}; margin: 0; }}
.lede {{ font-size: 1.02rem; line-height: 1.6; color: {MUTED}; max-width: 34rem;
         margin: 1.2rem 0 0; }}
.lede code {{ font-family: {MONO}; font-size: .92em; color: {INK};
              background: none; padding: 0; }}

.section {{ display: grid; grid-template-columns: 3rem 1fr; align-items: baseline;
            border-top: 2px solid {INK}; padding-top: .9rem; margin: 3.6rem 0 1.6rem; }}
.section .num {{ font-size: .75rem; font-weight: 600; color: {ACCENT};
                 font-variant-numeric: tabular-nums; }}
.section .name {{ font-size: .75rem; font-weight: 600; letter-spacing: .14em;
                  text-transform: uppercase; color: {INK}; }}

/* Form */
[data-testid="stForm"] {{ border: none; padding: 0; }}
.stApp label p {{ font-size: .72rem !important; font-weight: 600; letter-spacing: .1em;
                  text-transform: uppercase; color: {MUTED}; }}
.stApp input {{ font-size: 1rem !important; }}
[data-testid="stTextInputRootElement"], [data-testid="stNumberInputContainer"] {{
    height: 2.9rem; background: #fff !important; }}
[data-testid="stTextInputRootElement"] input, [data-testid="stNumberInputContainer"] input,
[data-testid="stNumberInputContainer"] button {{ background: #fff !important; }}
[data-testid="stTextInputRootElement"]:focus-within,
[data-testid="stNumberInputContainer"]:focus-within {{ border-color: {ACCENT} !important; }}
.stTextInput input {{ font-family: {MONO} !important; letter-spacing: .06em;
                      text-transform: uppercase; }}
.stTextInput input::placeholder {{ text-transform: none; letter-spacing: 0;
                                   font-family: {FONT}; color: #A9A9A4; }}
[data-testid="stWidgetLabel"] {{ min-height: 0; margin-bottom: .35rem; }}
[data-testid="stCaptionContainer"] p {{ color: {MUTED}; font-size: .8rem; }}

.stFormSubmitButton button, .stDownloadButton button {{
    height: 2.9rem; font-size: .78rem; font-weight: 600; letter-spacing: .12em;
    text-transform: uppercase; }}
.stFormSubmitButton button p, .stDownloadButton button p {{
    font-size: .78rem !important; font-weight: 600 !important; letter-spacing: .12em;
    text-transform: uppercase !important; }}
.stFormSubmitButton button {{ background: {ACCENT}; border-color: {ACCENT}; color: #fff; }}
.stFormSubmitButton button:hover {{ background: #163A26; border-color: #163A26; color: #fff; }}
.stDownloadButton button {{ background: #fff; color: {INK}; border: 1px solid {INK}; }}
.stDownloadButton button:hover {{ background: {INK}; color: #fff; border-color: {INK}; }}

/* Notices */
.notice {{ border-left: 2px solid {ACCENT}; padding: .2rem 0 .2rem 1rem; color: {INK};
           font-size: .92rem; margin: 1rem 0; }}
.notice.error {{ border-color: #B3261E; }}

/* Distribution */
.dist h4 {{ font-size: .72rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase;
            color: {MUTED}; margin: 0 0 1rem; padding: 0; }}
.bar-row {{ display: grid; grid-template-columns: 1fr auto; font-size: .86rem; color: {INK};
            margin-bottom: .2rem; }}
.bar-row span:last-child {{ font-variant-numeric: tabular-nums; color: {MUTED}; }}
.bar {{ height: 3px; background: {RULE}; margin-bottom: .85rem; }}
.bar > div {{ height: 3px; background: {ACCENT}; }}

.foot {{ margin-top: 5rem; padding-top: 1rem; border-top: 1px solid {RULE};
         font-size: .75rem; color: {MUTED}; }}
</style>
""", unsafe_allow_html=True)


def section(num: str, name: str) -> None:
    st.markdown(f'<div class="section"><span class="num">{num}</span>'
                f'<span class="name">{name}</span></div>', unsafe_allow_html=True)


def notice(text: str, error: bool = False) -> None:
    cls = "notice error" if error else "notice"
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)


def results_list(rows: list[dict], keyword: str) -> None:
    """Hostname list with a Copy button per row, rendered as an HTML component."""
    row_h, head_h, max_h = 57, 92, 640
    height = min(head_h + row_h * len(rows) + 4, max_h)
    data = json.dumps(rows)
    kw = json.dumps(keyword)
    components.html(f"""
<!doctype html><html><head>
<link href="{FONT_IMPORT}" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: {FONT}; color: {INK}; background: #fff; }}
  .bar {{ display: flex; justify-content: space-between; align-items: center;
          padding: 0 0 1rem; border-bottom: 1px solid {INK}; }}
  .count {{ font-size: .86rem; color: {MUTED}; }}
  .count b {{ color: {INK}; font-weight: 600; font-variant-numeric: tabular-nums; }}
  .head, .row {{ display: grid; grid-template-columns: 2.6rem 8.4rem 1fr 5.6rem;
                 align-items: center; column-gap: 1rem; }}
  .head {{ font-size: .68rem; font-weight: 600; letter-spacing: .12em; text-transform: uppercase;
           color: {MUTED}; padding: .9rem 0 .6rem; border-bottom: 1px solid {RULE}; }}
  .list {{ overflow-y: auto; max-height: {max_h - head_h}px; }}
  .row {{ height: {row_h}px; border-bottom: 1px solid {RULE}; }}
  .row:hover {{ background: #FAFAF8; }}
  .idx {{ font-size: .75rem; color: #A9A9A4; font-variant-numeric: tabular-nums; }}
  .host {{ font-family: {MONO}; font-size: 1rem; font-weight: 500; letter-spacing: .04em; }}
  .host mark {{ background: none; color: {ACCENT}; font-weight: 600;
                border-bottom: 2px solid {ACCENT}; }}
  .meta {{ font-size: .82rem; color: {MUTED}; white-space: nowrap; overflow: hidden;
           text-overflow: ellipsis; }}
  .meta .sep {{ color: #C9C9C4; margin: 0 .45rem; }}
  button {{ font-family: {FONT}; font-size: .68rem; font-weight: 600; letter-spacing: .12em;
            text-transform: uppercase; height: 2rem; padding: 0 .9rem; cursor: pointer;
            background: #fff; color: {INK}; border: 1px solid #CFCFCA;
            transition: background .12s, color .12s, border-color .12s; }}
  button:hover {{ border-color: {INK}; }}
  button:focus-visible {{ outline: 2px solid {ACCENT}; outline-offset: 2px; }}
  button.done {{ background: {ACCENT}; border-color: {ACCENT}; color: #fff; }}
  .row button {{ justify-self: end; width: 5.6rem; }}
  .primary {{ border-color: {INK}; }}
  .sr {{ position: absolute; left: -9999px; }}
  @media (max-width: 560px) {{
    .head, .row {{ grid-template-columns: 2rem 1fr 5rem; }}
    .meta, .head .m {{ display: none; }}
    .row button {{ width: 5rem; }}
  }}
</style></head><body>
<div class="bar">
  <span class="count"><b id="n"></b> hostnames</span>
  <button class="primary" id="all" aria-label="Copy all hostnames">Copy all</button>
</div>
<div class="head"><span>No.</span><span>Hostname</span><span class="m">OS / Environment / Country</span><span></span></div>
<div class="list" id="list" role="list"></div>
<div class="sr" aria-live="polite" id="live"></div>
<script>
const rows = {data}; const kw = {kw};
const esc = s => s.replace(/[&<>"]/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
function mark(h) {{
  if (!kw) return esc(h);
  const i = h.indexOf(kw);
  if (i < 0) return esc(h);
  return esc(h.slice(0, i)) + '<mark>' + esc(kw) + '</mark>' + esc(h.slice(i + kw.length));
}}
document.getElementById('n').textContent = rows.length.toLocaleString('en-US');
document.getElementById('list').innerHTML = rows.map((r, i) => `
  <div class="row" role="listitem">
    <span class="idx">${{String(i + 1).padStart(2, '0')}}</span>
    <span class="host">${{mark(r.hostname)}}</span>
    <span class="meta">${{r.os}}<span class="sep">/</span>${{r.environment}}<span class="sep">/</span>${{r.country}}</span>
    <button data-h="${{r.hostname}}" aria-label="Copy ${{r.hostname}}">Copy</button>
  </div>`).join('');

function fallbackCopy(text) {{
  const t = document.createElement('textarea');
  t.value = text; t.style.position = 'fixed'; t.style.opacity = '0';
  document.body.appendChild(t); t.select();
  let ok = false; try {{ ok = document.execCommand('copy'); }} catch (e) {{}}
  document.body.removeChild(t); return ok;
}}
async function copy(text, btn, label) {{
  let ok = false;
  try {{ await navigator.clipboard.writeText(text); ok = true; }}
  catch (e) {{ ok = fallbackCopy(text); }}
  btn.textContent = ok ? 'Copied' : 'Failed';
  btn.classList.toggle('done', ok);
  document.getElementById('live').textContent = ok ? 'Copied to clipboard' : 'Copy failed';
  setTimeout(() => {{ btn.textContent = label; btn.classList.remove('done'); }}, 1400);
}}
document.getElementById('list').addEventListener('click', e => {{
  const b = e.target.closest('button'); if (b) copy(b.dataset.h, b, 'Copy');
}});
document.getElementById('all').addEventListener('click', e =>
  copy(rows.map(r => r.hostname).join('\\n'), e.currentTarget, 'Copy all'));
</script></body></html>
""", height=height, scrolling=False)


def distribution(df) -> None:
    cols = st.columns(3, gap="large")
    for col, (field, title, codes) in zip(cols, [
            ("os", "Operating system", hn.OS_CODES),
            ("environment", "Environment", hn.ENV_CODES),
            ("country", "Country", hn.COUNTRY_CODES)]):
        counts = df[field].value_counts()
        total = len(df)
        rows = []
        for name, _ in sorted(codes.values(), key=lambda v: -counts.get(v[0], 0)):
            c = int(counts.get(name, 0))
            pct = 100 * c / total if total else 0
            rows.append(f'<div class="bar-row"><span>{html.escape(name)}</span>'
                        f'<span>{pct:.0f}%</span></div>'
                        f'<div class="bar"><div style="width:{pct:.1f}%"></div></div>')
        col.markdown(f'<div class="dist"><h4>{title}</h4>{"".join(rows)}</div>',
                     unsafe_allow_html=True)


# --------------------------------------------------------------------------- header
st.markdown("""
<p class="eyebrow">Infrastructure naming</p>
<h1 class="title">Hostname<br>Generator</h1>
<p class="lede">Eight characters, four parts: operating system, environment, country and node.
<code>AIGER789</code> reads as AIX, Integration, Germany, node 789.</p>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------- 01 generate
section("01", "Generate")
with st.form("generate", border=False, enter_to_submit=True):
    c1, c2, c3 = st.columns([3.2, 1.4, 1.4], vertical_alignment="bottom")
    keyword = c1.text_input("Keyword", max_chars=8, placeholder="Optional, e.g. IRL, LP or 007")
    quantity = c2.number_input("Quantity", min_value=1, max_value=5000, value=20, step=10)
    submitted = c3.form_submit_button("Generate", type="primary", width="stretch")
st.caption("The keyword is placed inside every hostname. Leave it empty for fully random names.")

if submitted:
    kw = hn.clean_keyword(keyword)
    if not hn.is_possible(kw):
        st.session_state.pop("result", None)
        st.session_state.error = (f"No valid hostname can contain <b>{html.escape(kw)}</b>. "
                                  "Try an OS or environment letter, a country code such as GER, or a node number.")
    else:
        st.session_state.pop("error", None)
        st.session_state.result = {"df": hn.build_dataframe(int(quantity), kw),
                                   "keyword": kw, "requested": int(quantity)}

if "error" in st.session_state:
    notice(st.session_state.error, error=True)

# --------------------------------------------------------------------------- 02 results
result = st.session_state.get("result")
if result:
    df, kw = result["df"], result["keyword"]
    section("02", "Results")
    if len(df) < result["requested"]:
        notice(f"Only {len(df)} unique hostnames can contain <b>{html.escape(kw)}</b>; "
               f"all of them are listed.")
    results_list(df.to_dict(orient="records"), kw)

    _, dl = st.columns([3, 1.4])
    dl.download_button("Download CSV", df.to_csv(index=False).encode(),
                       file_name=f"hostnames{'_' + kw if kw else ''}.csv",
                       mime="text/csv", width="stretch")

    section("03", "Distribution")
    distribution(df)
else:
    section("02", "Results")
    st.markdown(f'<p style="color:{MUTED};font-size:.92rem">No hostnames yet. '
                'Set a keyword or leave it empty, then press Generate.</p>',
                unsafe_allow_html=True)

st.markdown('<div class="foot">Probabilities: OS L 40, S 30, A 20, H 10 &nbsp;/&nbsp; '
            'Environment D 10, I 10, T 25, S 25, P 30 &nbsp;/&nbsp; '
            'Country NOR 6, FRA 9, ITA 16, ESP 16, GER 23, IRL 30 &nbsp;/&nbsp; Node 001–999 uniform.</div>',
            unsafe_allow_html=True)
