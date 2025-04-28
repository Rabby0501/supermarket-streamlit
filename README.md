# 🛒 Supermarket Management System

A modern web-based supermarket management system built with Streamlit.

![Dashboard Screenshot](./assets/screenshot.png)

## Features ✨

- 📦 Product Management (Add/View)
- 📈 Real-time Stock Management
- 💰 Sales Recording & Tracking
- 📊 Interactive Analytics Dashboard
- 🔄 Automatic Data Persistence
- 🎨 Professional UI/UX Design

## Tech Stack 💻

- **Frontend**: Streamlit
- **Data Storage**: JSON files
- **Visualization**: Altair
- **Deployment**: Streamlit Sharing

## Installation ⚙️

1. Clone repository:
```bash this repo link use SSH link 
git clone git@github.com:Rabby0501/supermarket-streamlit.git (
cd supermarket-streamlit
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage 🚀

1. Start the application:
```bash
streamlit run app.py
```

2. Access the web interface at `http://localhost:8501`

## Deployment ☁️

1. Create GitHub repository
2. Push code (excluding `venv/` and `data/`)
3. Deploy to Streamlit Sharing:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect GitHub repository
   - Set main file to `app.py`

## Configuration ⚙️

- Edit `.gitignore` to exclude sensitive files
- Modify `data/` path in `app.py` for custom storage
- Update styles in CSS section of `app.py`

## License 📄
MIT License - See [LICENSE](./LICENSE) for details