# Deploying the Hostname Generator with Streamlit

## Project structure
```
Hostnames_app/
├── .streamlit/
│   └── config.toml        # theme: white, forest green accent, square corners
├── app/
│   ├── streamlit_app.py   # Streamlit interface
│   ├── hostnames.py       # generator logic (from the notebook)
│   └── requirements.txt   # libraries for Streamlit Cloud
├── Hostnames_Generator.ipynb
├── hosts.csv
├── README.md
└── .gitignore
```

## 1. Run it locally (Mac)
```bash
cd ~/path/to/Hostnames_app
python3 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
streamlit run app/streamlit_app.py
```
The app opens automatically at http://localhost:8501. Stop it with `Ctrl + C`.

## 2. Upload the project to GitHub
Create an empty **public** repository on github.com (e.g. `hostnames-app`), then:
```bash
git init
git add .
git commit -m "Hostname generator Streamlit app"
git branch -M main
git remote add origin https://github.com/YOUR_USER/hostnames-app.git
git push -u origin main
```

## 3. Deploy on Streamlit Community Cloud (free)
1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **Create app** → **Deploy a public app from GitHub**.
3. Fill in:
   - Repository: `YOUR_USER/hostnames-app`
   - Branch: `main`
   - Main file path: `app/streamlit_app.py`
   - (Optional) App URL: e.g. `hostnames-generator`
4. Click **Deploy**. After 1–3 minutes you get a public link like
   `https://hostnames-generator.streamlit.app`.

Every `git push` to `main` updates the published app automatically.

## App features
- Swiss minimalist layout: one column, numbered sections, generous white space, forest green (#1F4D33) accent.
- **Keyword** (optional): fixed inside every hostname, e.g. `IRL`, `LP`, `007`. Impossible keywords show a clear message; very specific ones list every unique match.
- **Quantity** (1–5,000) and **Generate** (Enter also works).
- **Results**: numbered list with the keyword highlighted, a decoded description, a **Copy** button per row, **Copy all**, and **Download CSV**.
- **Distribution**: share of each OS, environment, and country in the current result.

## Troubleshooting
- The theme is not applied → `.streamlit/config.toml` must be at the repository root (inside `Hostnames_app/`, not inside `app/`).
- `ModuleNotFoundError` on Streamlit Cloud → check that `requirements.txt` is inside `app/`, next to `streamlit_app.py`.
- `ModuleNotFoundError: hostnames` → `hostnames.py` must be in the same folder as `streamlit_app.py`.
- Port already in use locally → `streamlit run app/streamlit_app.py --server.port 8502`.
