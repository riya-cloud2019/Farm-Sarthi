# FarmSaarthi Working Model

This is a lightweight working prototype of **FarmSaarthi**, a vernacular-enabled digital agricultural ecosystem.

## Features
- Regional language interface support for English, Hindi, Telugu, and Tamil
- Voice-enabled crop-interest input using browser speech recognition
- Integrated crop, soil, weather, nutrient, and market dataset
- ML-based crop recommendation engine using a Random Forest classifier
- Smart alerts for heat, dry spell, humidity, pests, and market conditions
- Decision accuracy score to demonstrate impact evaluation

## Project Structure
- `app.py` - Flask web application and JSON analysis endpoint
- `engine.py` - ML training, prediction, and advisory logic
- `data/farm_data.json` - sample agricultural dataset
- `templates/index.html` - UI template
- `static/styles.css` - interface styling

## Run the Project
```powershell
python -m pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Demo Flow
1. Select a language.
2. Select a district.
3. Type or speak a crop interest.
4. Click the analysis button.
5. View crop suggestions, alerts, advisory outputs, and model insights.

## Notes
- The current version trains a local Random Forest model from the in-app agricultural dataset.
- It is designed as a functional academic prototype and can be extended with live APIs, larger datasets, database storage, and production speech services.
