# Deploying the Hostname Generator with Streamlit

## Project structure
```
Hostnames_app/
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
- Sidebar: number of hostnames (100–10,000), optional seed for reproducible results, regenerate button.
- **Data**: table with filters by OS, environment, and country, plus CSV download.
- **Charts**: the notebook charts, plus an expected-vs-observed percentage table.
- **Decode**: type a hostname (e.g. `AIGER789`) to see its OS, environment, country, and node.
- **Rules**: the hostname composition table.

## Troubleshooting
- `ModuleNotFoundError` on Streamlit Cloud → check that `requirements.txt` is inside `app/`, next to `streamlit_app.py`.
- `ModuleNotFoundError: hostnames` → `hostnames.py` must be in the same folder as `streamlit_app.py`.
- Port already in use locally → `streamlit run app/streamlit_app.py --server.port 8502`.
