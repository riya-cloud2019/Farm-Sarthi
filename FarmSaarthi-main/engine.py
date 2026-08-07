import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


CROP_DATA_PATH = Path(__file__).parent / "data" / "farm_data.json"
LOCATION_DATA_PATH = Path(__file__).parent / "data" / "india_districts.json"

SOIL_MAP = {
    "clay": 0,
    "loamy": 1,
    "black": 2,
    "sandy": 3
}

SEASON_MAP = {
    "kharif": 0,
    "rabi": 1,
    "zaid": 2
}

PEST_MAP = {
    "low": 0,
    "medium": 1,
    "high": 2
}

STATE_PROFILES = {
    "Andhra Pradesh": {"soils": ["black", "loamy"], "temperature": (27, 34), "humidity": (58, 82), "rainfall": (65, 120), "ph": (6.2, 7.8), "season": "kharif", "nitrogen": (62, 88), "phosphorus": (30, 52), "potassium": (34, 58)},
    "Arunachal Pradesh": {"soils": ["loamy", "clay"], "temperature": (16, 26), "humidity": (68, 90), "rainfall": (140, 260), "ph": (5.2, 6.8), "season": "kharif", "nitrogen": (56, 82), "phosphorus": (26, 46), "potassium": (32, 54)},
    "Assam": {"soils": ["loamy", "clay"], "temperature": (22, 31), "humidity": (72, 90), "rainfall": (120, 240), "ph": (5.1, 6.9), "season": "kharif", "nitrogen": (58, 84), "phosphorus": (28, 48), "potassium": (32, 52)},
    "Bihar": {"soils": ["loamy", "clay"], "temperature": (20, 33), "humidity": (55, 82), "rainfall": (70, 150), "ph": (6.3, 7.9), "season": "rabi", "nitrogen": (60, 82), "phosphorus": (30, 50), "potassium": (28, 48)},
    "Chandigarh": {"soils": ["loamy"], "temperature": (18, 32), "humidity": (45, 72), "rainfall": (55, 110), "ph": (6.7, 7.8), "season": "rabi", "nitrogen": (54, 76), "phosphorus": (28, 46), "potassium": (26, 42)},
    "Chhattisgarh": {"soils": ["black", "loamy"], "temperature": (23, 34), "humidity": (55, 80), "rainfall": (90, 170), "ph": (6.0, 7.4), "season": "kharif", "nitrogen": (58, 82), "phosphorus": (26, 46), "potassium": (32, 56)},
    "Dadra and Nagar Haveli and Daman and Diu": {"soils": ["sandy", "loamy"], "temperature": (24, 33), "humidity": (62, 86), "rainfall": (85, 170), "ph": (6.1, 7.5), "season": "zaid", "nitrogen": (56, 82), "phosphorus": (26, 44), "potassium": (30, 50)},
    "Goa": {"soils": ["sandy", "loamy"], "temperature": (24, 32), "humidity": (70, 88), "rainfall": (160, 280), "ph": (5.6, 6.8), "season": "kharif", "nitrogen": (52, 76), "phosphorus": (24, 42), "potassium": (28, 48)},
    "Gujarat": {"soils": ["black", "sandy"], "temperature": (24, 36), "humidity": (38, 72), "rainfall": (35, 120), "ph": (6.8, 8.2), "season": "zaid", "nitrogen": (48, 76), "phosphorus": (22, 42), "potassium": (34, 60)},
    "Haryana": {"soils": ["loamy", "sandy"], "temperature": (19, 34), "humidity": (38, 68), "rainfall": (35, 95), "ph": (6.9, 8.1), "season": "rabi", "nitrogen": (50, 74), "phosphorus": (24, 44), "potassium": (26, 46)},
    "Himachal Pradesh": {"soils": ["loamy", "clay"], "temperature": (10, 24), "humidity": (48, 76), "rainfall": (60, 130), "ph": (5.6, 7.0), "season": "rabi", "nitrogen": (54, 78), "phosphorus": (26, 44), "potassium": (28, 48)},
    "Jammu and Kashmir": {"soils": ["loamy", "clay"], "temperature": (9, 24), "humidity": (46, 74), "rainfall": (45, 105), "ph": (6.1, 7.5), "season": "rabi", "nitrogen": (50, 76), "phosphorus": (24, 44), "potassium": (26, 46)},
    "Jharkhand": {"soils": ["loamy", "sandy"], "temperature": (21, 33), "humidity": (52, 78), "rainfall": (80, 150), "ph": (5.4, 7.0), "season": "kharif", "nitrogen": (54, 80), "phosphorus": (24, 42), "potassium": (28, 48)},
    "Karnataka": {"soils": ["black", "sandy"], "temperature": (21, 33), "humidity": (44, 74), "rainfall": (45, 125), "ph": (6.0, 7.8), "season": "kharif", "nitrogen": (50, 76), "phosphorus": (24, 42), "potassium": (30, 52)},
    "Kerala": {"soils": ["clay", "loamy"], "temperature": (24, 32), "humidity": (74, 92), "rainfall": (160, 300), "ph": (5.0, 6.5), "season": "kharif", "nitrogen": (58, 82), "phosphorus": (24, 42), "potassium": (30, 52)},
    "Ladakh": {"soils": ["sandy", "loamy"], "temperature": (4, 19), "humidity": (20, 42), "rainfall": (10, 40), "ph": (7.0, 8.4), "season": "zaid", "nitrogen": (34, 56), "phosphorus": (18, 34), "potassium": (22, 38)},
    "Lakshadweep": {"soils": ["sandy"], "temperature": (26, 32), "humidity": (75, 90), "rainfall": (140, 240), "ph": (6.5, 7.8), "season": "zaid", "nitrogen": (44, 66), "phosphorus": (20, 36), "potassium": (24, 42)},
    "Madhya Pradesh": {"soils": ["black", "loamy"], "temperature": (20, 34), "humidity": (42, 72), "rainfall": (50, 135), "ph": (6.3, 7.9), "season": "kharif", "nitrogen": (54, 80), "phosphorus": (26, 46), "potassium": (30, 54)},
    "Maharashtra": {"soils": ["black", "loamy"], "temperature": (22, 34), "humidity": (46, 74), "rainfall": (45, 150), "ph": (6.2, 7.8), "season": "kharif", "nitrogen": (52, 80), "phosphorus": (24, 46), "potassium": (30, 56)},
    "Manipur": {"soils": ["clay", "loamy"], "temperature": (18, 28), "humidity": (64, 86), "rainfall": (95, 180), "ph": (5.2, 6.8), "season": "kharif", "nitrogen": (56, 80), "phosphorus": (24, 42), "potassium": (30, 48)},
    "Meghalaya": {"soils": ["clay", "loamy"], "temperature": (15, 25), "humidity": (72, 92), "rainfall": (180, 320), "ph": (4.8, 6.5), "season": "kharif", "nitrogen": (54, 78), "phosphorus": (22, 40), "potassium": (28, 46)},
    "Mizoram": {"soils": ["loamy", "clay"], "temperature": (17, 28), "humidity": (68, 88), "rainfall": (160, 260), "ph": (5.0, 6.6), "season": "kharif", "nitrogen": (54, 78), "phosphorus": (22, 40), "potassium": (28, 46)},
    "Nagaland": {"soils": ["loamy", "clay"], "temperature": (17, 28), "humidity": (64, 86), "rainfall": (120, 220), "ph": (5.2, 6.8), "season": "kharif", "nitrogen": (54, 78), "phosphorus": (22, 40), "potassium": (28, 46)},
    "National Capital Territory of Delhi": {"soils": ["loamy", "sandy"], "temperature": (18, 35), "humidity": (35, 70), "rainfall": (30, 95), "ph": (6.7, 8.0), "season": "rabi", "nitrogen": (46, 68), "phosphorus": (22, 40), "potassium": (24, 42)},
    "Odisha": {"soils": ["clay", "loamy"], "temperature": (23, 34), "humidity": (60, 86), "rainfall": (85, 180), "ph": (5.4, 7.1), "season": "kharif", "nitrogen": (56, 82), "phosphorus": (24, 42), "potassium": (28, 48)},
    "Puducherry": {"soils": ["clay", "loamy"], "temperature": (25, 33), "humidity": (68, 88), "rainfall": (75, 165), "ph": (6.0, 7.4), "season": "zaid", "nitrogen": (54, 76), "phosphorus": (24, 42), "potassium": (28, 48)},
    "Punjab": {"soils": ["loamy", "sandy"], "temperature": (18, 32), "humidity": (40, 68), "rainfall": (35, 95), "ph": (6.8, 8.0), "season": "rabi", "nitrogen": (52, 76), "phosphorus": (24, 46), "potassium": (24, 44)},
    "Rajasthan": {"soils": ["sandy", "loamy"], "temperature": (22, 38), "humidity": (22, 55), "rainfall": (12, 70), "ph": (7.0, 8.4), "season": "zaid", "nitrogen": (34, 58), "phosphorus": (16, 34), "potassium": (20, 40)},
    "Sikkim": {"soils": ["loamy", "clay"], "temperature": (10, 22), "humidity": (62, 84), "rainfall": (100, 220), "ph": (5.0, 6.6), "season": "kharif", "nitrogen": (52, 74), "phosphorus": (22, 40), "potassium": (28, 46)},
    "Tamil Nadu": {"soils": ["clay", "loamy"], "temperature": (24, 34), "humidity": (52, 78), "rainfall": (35, 110), "ph": (6.1, 7.7), "season": "zaid", "nitrogen": (52, 78), "phosphorus": (24, 44), "potassium": (30, 52)},
    "Telangana": {"soils": ["black", "loamy"], "temperature": (24, 35), "humidity": (42, 70), "rainfall": (45, 110), "ph": (6.4, 7.9), "season": "kharif", "nitrogen": (50, 76), "phosphorus": (24, 42), "potassium": (30, 56)},
    "Tripura": {"soils": ["clay", "loamy"], "temperature": (23, 31), "humidity": (70, 88), "rainfall": (120, 210), "ph": (5.2, 6.8), "season": "kharif", "nitrogen": (56, 80), "phosphorus": (22, 40), "potassium": (28, 46)},
    "Uttar Pradesh": {"soils": ["loamy", "clay"], "temperature": (19, 34), "humidity": (42, 74), "rainfall": (45, 120), "ph": (6.5, 8.0), "season": "rabi", "nitrogen": (50, 76), "phosphorus": (24, 44), "potassium": (24, 44)},
    "Uttarakhand": {"soils": ["loamy", "clay"], "temperature": (11, 24), "humidity": (48, 78), "rainfall": (70, 160), "ph": (5.4, 7.0), "season": "rabi", "nitrogen": (52, 76), "phosphorus": (22, 40), "potassium": (26, 44)},
    "West Bengal": {"soils": ["clay", "loamy"], "temperature": (22, 33), "humidity": (62, 86), "rainfall": (95, 210), "ph": (5.5, 7.2), "season": "kharif", "nitrogen": (56, 80), "phosphorus": (24, 42), "potassium": (28, 48)},
    "Andaman and Nicobar": {"soils": ["sandy", "clay"], "temperature": (25, 31), "humidity": (74, 90), "rainfall": (160, 290), "ph": (5.5, 7.0), "season": "zaid", "nitrogen": (50, 74), "phosphorus": (20, 38), "potassium": (26, 44)}
}

STATE_LANGUAGES = {
    "Andhra Pradesh": ["en", "hi", "te"],
    "Arunachal Pradesh": ["en", "hi"],
    "Assam": ["en", "hi", "as", "bn"],
    "Bihar": ["en", "hi"],
    "Chandigarh": ["en", "hi", "pa"],
    "Chhattisgarh": ["en", "hi"],
    "Dadra and Nagar Haveli and Daman and Diu": ["en", "hi", "gu"],
    "Goa": ["en", "hi", "mr", "kn"],
    "Gujarat": ["en", "hi", "gu"],
    "Haryana": ["en", "hi"],
    "Himachal Pradesh": ["en", "hi"],
    "Jammu and Kashmir": ["en", "hi", "ur"],
    "Jharkhand": ["en", "hi"],
    "Karnataka": ["en", "hi", "kn"],
    "Kerala": ["en", "hi", "ml"],
    "Ladakh": ["en", "hi"],
    "Lakshadweep": ["en", "ml"],
    "Madhya Pradesh": ["en", "hi"],
    "Maharashtra": ["en", "hi", "mr"],
    "Manipur": ["en", "hi"],
    "Meghalaya": ["en", "hi"],
    "Mizoram": ["en", "hi"],
    "Nagaland": ["en", "hi"],
    "National Capital Territory of Delhi": ["en", "hi", "pa", "ur"],
    "Odisha": ["en", "hi", "or"],
    "Puducherry": ["en", "ta"],
    "Punjab": ["en", "hi", "pa"],
    "Rajasthan": ["en", "hi"],
    "Sikkim": ["en", "hi"],
    "Tamil Nadu": ["en", "hi", "ta"],
    "Telangana": ["en", "hi", "te"],
    "Tripura": ["en", "hi", "bn"],
    "Uttar Pradesh": ["en", "hi"],
    "Uttarakhand": ["en", "hi"],
    "West Bengal": ["en", "hi", "bn"],
    "Andaman and Nicobar": ["en", "hi", "bn"]
}

DEFAULT_PROFILE = {
    "soils": ["loamy", "clay"],
    "temperature": (20, 32),
    "humidity": (48, 78),
    "rainfall": (50, 140),
    "ph": (6.0, 7.5),
    "season": "kharif",
    "nitrogen": (52, 78),
    "phosphorus": (24, 44),
    "potassium": (28, 48)
}


class FarmSaarthiEngine:
    def __init__(self):
        with CROP_DATA_PATH.open("r", encoding="utf-8") as file:
            self.crop_data = json.load(file)["crops"]
        with LOCATION_DATA_PATH.open("r", encoding="utf-8") as file:
            self.location_data = json.load(file)["districts"]

        self.training_data = self._build_training_dataset()
        self.model_accuracy = 0.0
        self.model = self._train_model()

    def list_states(self):
        return sorted({item["state"] for item in self.location_data})

    def list_districts(self):
        return self.location_data

    def get_district(self, district_name, state_name=None):
        for district in self.location_data:
            if district["district"].lower() == district_name.lower():
                if state_name and district["state"] != state_name:
                    continue
                return district
        return None

    def recommend(self, district_name, preferred_language, crop_interest="", state_name=None):
        raw_district = self.get_district(district_name, state_name)
        if not raw_district:
            return {"error": "District not found for the selected state."}

        district = self._build_district_context(raw_district)
        features = self._district_features(district)
        probabilities = self.model.predict_proba(pd.DataFrame([features]))[0]
        classes = self.model.classes_
        prediction_rows = []

        for crop_name, probability in zip(classes, probabilities):
            crop_profile = self._get_crop_profile(crop_name)
            score = self._blend_score(district, crop_profile, float(probability), crop_interest)
            prediction_rows.append(
                {
                    "crop": crop_name,
                    "score": score,
                    "reasons": self._build_reasons(district, crop_profile, crop_interest)
                }
            )

        prediction_rows.sort(key=lambda item: item["score"], reverse=True)
        top_crops = prediction_rows[:3]

        return {
            "district": district,
            "language": preferred_language,
            "top_crops": top_crops,
            "irrigation_advice": self._irrigation_advice(district),
            "fertilizer_advice": self._fertilizer_advice(district),
            "alerts": self._generate_alerts(district),
            "decision_score": self._decision_score(district, preferred_language, top_crops[0]["score"]),
            "model_summary": {
                "algorithm": "Random Forest Classifier",
                "training_rows": int(len(self.training_data)),
                "accuracy": round(self.model_accuracy * 100, 1),
                "districts_loaded": len(self.location_data)
            }
        }

    def _build_training_dataset(self):
        rows = []
        rng = np.random.default_rng(42)

        for crop in self.crop_data:
            for _ in range(150):
                rows.append(
                    {
                        "nitrogen": int(rng.integers(crop["nitrogen"][0], crop["nitrogen"][1] + 1)),
                        "phosphorus": int(rng.integers(crop["phosphorus"][0], crop["phosphorus"][1] + 1)),
                        "potassium": int(rng.integers(crop["potassium"][0], crop["potassium"][1] + 1)),
                        "temperature": round(float(rng.uniform(crop["temp_min"], crop["temp_max"])), 1),
                        "humidity": round(float(rng.uniform(crop["humidity_min"], crop["humidity_max"])), 1),
                        "ph": round(float(rng.uniform(crop["ph_min"], crop["ph_max"])), 1),
                        "rainfall": round(float(rng.uniform(crop["rainfall_min"], crop["rainfall_max"])), 1),
                        "soil_code": SOIL_MAP[crop["primary_soil"]],
                        "season_code": SEASON_MAP[crop["primary_season"]],
                        "label": crop["name"]
                    }
                )

        return pd.DataFrame(rows)

    def _train_model(self):
        features = self.training_data.drop(columns=["label"])
        labels = self.training_data["label"]

        X_train, X_test, y_train, y_test = train_test_split(
            features,
            labels,
            test_size=0.2,
            random_state=42,
            stratify=labels
        )

        model = RandomForestClassifier(
            n_estimators=240,
            max_depth=12,
            min_samples_split=4,
            random_state=42
        )
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        self.model_accuracy = accuracy_score(y_test, predictions)
        return model

    def _build_district_context(self, raw_district):
        profile = STATE_PROFILES.get(raw_district["state"], DEFAULT_PROFILE)
        seed = sum(ord(char) for char in f"{raw_district['state']}-{raw_district['district']}")

        soil = profile["soils"][seed % len(profile["soils"])]
        temperature = self._spread(profile["temperature"], seed, 1)
        humidity = self._spread(profile["humidity"], seed, 2)
        rainfall = self._spread(profile["rainfall"], seed, 3)
        ph = round(self._spread(profile["ph"], seed, 4, decimal=True), 1)
        nitrogen = int(self._spread(profile["nitrogen"], seed, 5))
        phosphorus = int(self._spread(profile["phosphorus"], seed, 6))
        potassium = int(self._spread(profile["potassium"], seed, 7))
        market_price_index = int(62 + (seed % 27))

        humidity_risk = humidity >= 80 or rainfall >= 140
        if humidity_risk and temperature > 28:
            pest_risk = "high"
        elif humidity > 62 or rainfall > 85:
            pest_risk = "medium"
        else:
            pest_risk = "low"

        return {
            "name": raw_district["district"],
            "state": raw_district["state"],
            "state_code": raw_district["stateCode"],
            "district_code": raw_district["districtCode"],
            "soil": soil,
            "temperature": int(round(temperature)),
            "rainfall_forecast": int(round(rainfall)),
            "humidity": int(round(humidity)),
            "season": profile["season"],
            "market_price_index": market_price_index,
            "pest_risk": pest_risk,
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "potassium": potassium,
            "ph": ph,
            "languages": STATE_LANGUAGES.get(raw_district["state"], ["en", "hi"])
        }

    def _spread(self, bounds, seed, offset, decimal=False):
        low, high = bounds
        span = high - low
        value = low + ((seed * (offset * 13 + 7)) % 1000) / 1000 * span
        return round(value, 1) if decimal else value

    def _district_features(self, district):
        return {
            "nitrogen": district["nitrogen"],
            "phosphorus": district["phosphorus"],
            "potassium": district["potassium"],
            "temperature": district["temperature"],
            "humidity": district["humidity"],
            "ph": district["ph"],
            "rainfall": district["rainfall_forecast"],
            "soil_code": SOIL_MAP[district["soil"]],
            "season_code": SEASON_MAP[district["season"]]
        }

    def _get_crop_profile(self, crop_name):
        for crop in self.crop_data:
            if crop["name"] == crop_name:
                return crop
        return None

    def _compatibility_score(self, district, crop_profile):
        score = 0
        if district["soil"] in crop_profile["soil"]:
            score += 12
        if crop_profile["temp_min"] <= district["temperature"] <= crop_profile["temp_max"]:
            score += 10
        if crop_profile["ph_min"] <= district["ph"] <= crop_profile["ph_max"]:
            score += 8
        if crop_profile["rainfall_min"] * 0.65 <= district["rainfall_forecast"] <= crop_profile["rainfall_max"] * 1.15:
            score += 10
        if crop_profile["humidity_min"] <= district["humidity"] <= crop_profile["humidity_max"]:
            score += 8
        return score

    def _blend_score(self, district, crop_profile, probability, crop_interest):
        score = probability * 62 + self._compatibility_score(district, crop_profile)
        if crop_interest and crop_interest.lower() in crop_profile["name"].lower():
            score += 8
        return round(min(score, 99.5), 1)

    def _build_reasons(self, district, crop_profile, crop_interest):
        reasons = []

        if district["soil"] in crop_profile["soil"]:
            reasons.append(f"{crop_profile['name']} fits {district['soil']} soil.")
        if crop_profile["temp_min"] <= district["temperature"] <= crop_profile["temp_max"]:
            reasons.append("Temperature is within the recommended range.")
        if crop_profile["ph_min"] <= district["ph"] <= crop_profile["ph_max"]:
            reasons.append("Soil pH supports healthy growth.")
        if crop_profile["rainfall_min"] * 0.65 <= district["rainfall_forecast"] <= crop_profile["rainfall_max"] * 1.15:
            reasons.append("Rainfall conditions are favorable.")
        if crop_interest and crop_interest.lower() in crop_profile["name"].lower():
            reasons.append("Matches the farmer's stated crop interest.")

        if not reasons:
            reasons.append("Model confidence is driven mainly by similar crop-climate patterns in training data.")

        return reasons[:3]

    def _irrigation_advice(self, district):
        if district["rainfall_forecast"] < 45:
            return "Low rainfall is expected. Use drip irrigation, mulching, and early-morning watering to reduce moisture loss."
        if district["rainfall_forecast"] < 95:
            return "Moderate rainfall is expected. Schedule irrigation after checking field moisture and avoid unnecessary watering."
        return "High rainfall is expected. Reduce extra irrigation and keep field drainage channels clear to prevent waterlogging."

    def _fertilizer_advice(self, district):
        tips = []

        if district["nitrogen"] < 55:
            tips.append("Nitrogen is on the lower side, so split nitrogen application can improve vegetative growth.")
        if district["phosphorus"] < 30:
            tips.append("Phosphorus is limited. Basal phosphorus placement near roots may improve crop establishment.")
        if district["potassium"] < 35:
            tips.append("Potassium is low. Add potash support to strengthen stress tolerance and grain filling.")
        if district["ph"] > 7.6:
            tips.append("Soil is slightly alkaline. Organic compost can improve micronutrient availability.")
        if district["ph"] < 5.6:
            tips.append("Soil is mildly acidic. Liming may help balance soil reaction for sensitive crops.")

        if not tips:
            tips.append("NPK balance looks stable. Prefer soil-test-based micronutrient correction and avoid over-application.")

        return " ".join(tips[:2])

    def _generate_alerts(self, district):
        alerts = []

        if district["temperature"] >= 34:
            alerts.append("Heat alert: protect young plants, avoid afternoon spraying, and irrigate during cooler hours.")
        if district["rainfall_forecast"] < 35:
            alerts.append("Dry spell alert: conserve water and improve soil moisture retention.")
        if district["rainfall_forecast"] > 150:
            alerts.append("Heavy rainfall alert: monitor drainage and prevent root-zone waterlogging.")
        if district["humidity"] > 82:
            alerts.append("Disease alert: humidity is high, so fungal risk may increase.")
        if PEST_MAP[district["pest_risk"]] >= 1:
            alerts.append("Pest alert: inspect leaves and stems regularly for early infestation signs.")
        if district["market_price_index"] >= 84:
            alerts.append("Market alert: local price conditions are favorable for near-term selling.")
        if not alerts:
            alerts.append("No major risk flag today. Continue normal crop monitoring.")

        return alerts

    def _decision_score(self, district, preferred_language, top_score):
        score = 48
        if preferred_language in district["languages"]:
            score += 18
        if district["market_price_index"] >= 76:
            score += 8
        if district["pest_risk"] == "low":
            score += 10
        elif district["pest_risk"] == "medium":
            score += 5
        if top_score >= 78:
            score += 10
        elif top_score >= 62:
            score += 6
        if self.model_accuracy >= 0.9:
            score += 5
        return min(score, 100)
