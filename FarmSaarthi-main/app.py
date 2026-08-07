from flask import Flask, jsonify, render_template, request

from engine import FarmSaarthiEngine


app = Flask(__name__)
engine = FarmSaarthiEngine()

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "mr": "Marathi",
    "kn": "Kannada",
    "pa": "Punjabi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "ml": "Malayalam"
}


TRANSLATIONS = {
    "en": {
        "title": "FarmSaarthi",
        "subtitle": "AI crop intelligence for vernacular farmer support",
        "state": "State",
        "district": "District",
        "language": "Language",
        "crop_interest": "Crop interest",
        "analyze": "Analyze Farm Conditions",
        "voice": "Use Voice Input",
        "results": "Recommendation Results",
        "top_crops": "Top Crop Suggestions",
        "irrigation": "Irrigation Advice",
        "fertilizer": "Fertilizer Advice",
        "alerts": "Alerts",
        "impact": "Decision Accuracy Score",
        "placeholder": "Example: cotton, rice, maize",
        "loading": "Analyzing district conditions...",
        "model": "Model Insights",
        "overview": "Field Overview",
        "select_state": "Select a state",
        "select_district": "Select a district",
        "success": "Analysis completed successfully."
    },
    "hi": {
        "title": "फार्मसारथी",
        "subtitle": "क्षेत्रीय किसान सहायता के लिए एआई फसल विश्लेषण",
        "state": "राज्य",
        "district": "जिला",
        "language": "भाषा",
        "crop_interest": "फसल रुचि",
        "analyze": "खेती की स्थिति जांचें",
        "voice": "आवाज़ इनपुट उपयोग करें",
        "results": "सिफारिश परिणाम",
        "top_crops": "मुख्य फसल सुझाव",
        "irrigation": "सिंचाई सलाह",
        "fertilizer": "उर्वरक सलाह",
        "alerts": "अलर्ट",
        "impact": "निर्णय सटीकता स्कोर",
        "placeholder": "उदाहरण: cotton, rice, maize",
        "loading": "जिले की खेती की स्थिति का विश्लेषण हो रहा है...",
        "model": "मॉडल जानकारी",
        "overview": "क्षेत्र सारांश",
        "select_state": "राज्य चुनें",
        "select_district": "जिला चुनें",
        "success": "विश्लेषण सफलतापूर्वक पूरा हुआ।"
    },
    "te": {
        "title": "ఫార్మ్‌సారథి",
        "subtitle": "ప్రాంతీయ రైతు సహాయానికి ఏఐ పంట విశ్లేషణ",
        "state": "రాష్ట్రం",
        "district": "జిల్లా",
        "language": "భాష",
        "crop_interest": "పంట ఆసక్తి",
        "analyze": "వ్యవసాయ స్థితి విశ్లేషణ",
        "voice": "వాయిస్ ఇన్‌పుట్ ఉపయోగించండి",
        "results": "సిఫారసు ఫలితాలు",
        "top_crops": "ప్రముఖ పంట సూచనలు",
        "irrigation": "పారుదల సూచన",
        "fertilizer": "ఎరువు సూచన",
        "alerts": "అలర్ట్స్",
        "impact": "నిర్ణయ ఖచ్చితత్వ స్కోర్",
        "placeholder": "ఉదాహరణ: cotton, rice, maize",
        "loading": "జిల్లా పరిస్థితులను విశ్లేషిస్తున్నాము...",
        "model": "మోడల్ సమాచారం",
        "overview": "క్షేత్ర అవలోకనం",
        "select_state": "రాష్ట్రాన్ని ఎంచుకోండి",
        "select_district": "జిల్లాను ఎంచుకోండి",
        "success": "విశ్లేషణ విజయవంతంగా పూర్తైంది."
    },
    "ta": {
        "title": "பார்ம்சாரதி",
        "subtitle": "மொழி ஆதரவு விவசாயிக்கு ஏஐ பயிர் பகுப்பாய்வு",
        "state": "மாநிலம்",
        "district": "மாவட்டம்",
        "language": "மொழி",
        "crop_interest": "பயிர் விருப்பம்",
        "analyze": "விவசாய நிலை பகுப்பாய்வு",
        "voice": "குரல் உள்ளீடு பயன்படுத்தவும்",
        "results": "பரிந்துரை முடிவுகள்",
        "top_crops": "முக்கிய பயிர் பரிந்துரைகள்",
        "irrigation": "நீர்ப்பாசன ஆலோசனை",
        "fertilizer": "உர ஆலோசனை",
        "alerts": "எச்சரிக்கைகள்",
        "impact": "முடிவு துல்லிய மதிப்பெண்",
        "placeholder": "உதாரணம்: cotton, rice, maize",
        "loading": "மாவட்ட நிலை பகுப்பாய்வு செய்யப்படுகிறது...",
        "model": "மாதிரி தகவல்",
        "overview": "புல நிலை சுருக்கம்",
        "select_state": "மாநிலத்தைத் தேர்ந்தெடுக்கவும்",
        "select_district": "மாவட்டத்தைத் தேர்ந்தெடுக்கவும்",
        "success": "பகுப்பாய்வு வெற்றிகரமாக முடிந்தது."
    },
    "mr": {
        "title": "फार्मसारथी",
        "subtitle": "प्रादेशिक शेतकरी सहाय्यासाठी एआय पीक विश्लेषण",
        "state": "राज्य",
        "district": "जिल्हा",
        "language": "भाषा",
        "crop_interest": "पिकाची आवड",
        "analyze": "शेती स्थिती तपासा",
        "voice": "आवाज इनपुट वापरा",
        "results": "शिफारस निकाल",
        "top_crops": "मुख्य पीक सूचना",
        "irrigation": "सिंचन सल्ला",
        "fertilizer": "खत सल्ला",
        "alerts": "सूचना",
        "impact": "निर्णय अचूकता गुण",
        "placeholder": "उदाहरण: cotton, rice, maize",
        "loading": "जिल्हा परिस्थितीचे विश्लेषण सुरू आहे...",
        "model": "मॉडेल माहिती",
        "overview": "शेत सारांश",
        "select_state": "राज्य निवडा",
        "select_district": "जिल्हा निवडा",
        "success": "विश्लेषण यशस्वीरीत्या पूर्ण झाले."
    },
    "kn": {
        "title": "ಫಾರ್ಮ್‌ಸಾರಥಿ",
        "subtitle": "ಪ್ರಾದೇಶಿಕ ರೈತ ಸಹಾಯಕ್ಕಾಗಿ ಎಐ ಬೆಳೆ ವಿಶ್ಲೇಷಣೆ",
        "state": "ರಾಜ್ಯ",
        "district": "ಜಿಲ್ಲೆ",
        "language": "ಭಾಷೆ",
        "crop_interest": "ಬೆಳೆ ಆಸಕ್ತಿ",
        "analyze": "ಕೃಷಿ ಸ್ಥಿತಿ ವಿಶ್ಲೇಷಿಸಿ",
        "voice": "ಧ್ವನಿ ಇನ್‌ಪುಟ್ ಬಳಸಿ",
        "results": "ಶಿಫಾರಸು ಫಲಿತಾಂಶಗಳು",
        "top_crops": "ಮುಖ್ಯ ಬೆಳೆ ಸಲಹೆಗಳು",
        "irrigation": "ನೀರಾವರಿ ಸಲಹೆ",
        "fertilizer": "ರಸಗೊಬ್ಬರ ಸಲಹೆ",
        "alerts": "ಎಚ್ಚರಿಕೆಗಳು",
        "impact": "ನಿರ್ಧಾರ ನಿಖರತಾ ಅಂಕೆ",
        "placeholder": "ಉದಾಹರಣೆ: cotton, rice, maize",
        "loading": "ಜಿಲ್ಲಾ ಪರಿಸ್ಥಿತಿಯನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...",
        "model": "ಮಾದರಿ ಮಾಹಿತಿ",
        "overview": "ಕ್ಷೇತ್ರ ಅವಲೋಕನ",
        "select_state": "ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "select_district": "ಜಿಲ್ಲೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "success": "ವಿಶ್ಲೇಷಣೆ ಯಶಸ್ವಿಯಾಗಿ ಪೂರ್ಣಗೊಂಡಿದೆ."
    },
    "pa": {
        "title": "ਫਾਰਮਸਾਰਥੀ",
        "subtitle": "ਖੇਤਰੀ ਕਿਸਾਨ ਸਹਾਇਤਾ ਲਈ ਏਆਈ ਫਸਲ ਵਿਸ਼ਲੇਸ਼ਣ",
        "state": "ਰਾਜ",
        "district": "ਜ਼ਿਲ੍ਹਾ",
        "language": "ਭਾਸ਼ਾ",
        "crop_interest": "ਫਸਲ ਰੁਚੀ",
        "analyze": "ਖੇਤੀ ਹਾਲਤ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ",
        "voice": "ਆਵਾਜ਼ ਇਨਪੁੱਟ ਵਰਤੋ",
        "results": "ਸਿਫਾਰਸ਼ ਨਤੀਜੇ",
        "top_crops": "ਮੁੱਖ ਫਸਲ ਸੁਝਾਅ",
        "irrigation": "ਸਿੰਚਾਈ ਸਲਾਹ",
        "fertilizer": "ਖਾਦ ਸਲਾਹ",
        "alerts": "ਚੇਤਾਵਨੀਆਂ",
        "impact": "ਫੈਸਲਾ ਸ਼ੁੱਧਤਾ ਸਕੋਰ",
        "placeholder": "ਉਦਾਹਰਨ: cotton, rice, maize",
        "loading": "ਜ਼ਿਲ੍ਹਾ ਹਾਲਤ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ...",
        "model": "ਮਾਡਲ ਜਾਣਕਾਰੀ",
        "overview": "ਖੇਤ ਝਲਕ",
        "select_state": "ਰਾਜ ਚੁਣੋ",
        "select_district": "ਜ਼ਿਲ੍ਹਾ ਚੁਣੋ",
        "success": "ਵਿਸ਼ਲੇਸ਼ਣ ਸਫਲਤਾਪੂਰਵਕ ਪੂਰਾ ਹੋਇਆ।"
    },
    "bn": {
        "title": "ফার্মসারথি",
        "subtitle": "আঞ্চলিক কৃষক সহায়তার জন্য এআই ফসল বিশ্লেষণ",
        "state": "রাজ্য",
        "district": "জেলা",
        "language": "ভাষা",
        "crop_interest": "ফসল পছন্দ",
        "analyze": "চাষের অবস্থা বিশ্লেষণ করুন",
        "voice": "ভয়েস ইনপুট ব্যবহার করুন",
        "results": "সুপারিশ ফলাফল",
        "top_crops": "প্রধান ফসল পরামর্শ",
        "irrigation": "সেচ পরামর্শ",
        "fertilizer": "সার পরামর্শ",
        "alerts": "সতর্কতা",
        "impact": "সিদ্ধান্ত নির্ভুলতা স্কোর",
        "placeholder": "উদাহরণ: cotton, rice, maize",
        "loading": "জেলার অবস্থা বিশ্লেষণ করা হচ্ছে...",
        "model": "মডেল তথ্য",
        "overview": "ক্ষেত্র সারাংশ",
        "select_state": "রাজ্য নির্বাচন করুন",
        "select_district": "জেলা নির্বাচন করুন",
        "success": "বিশ্লেষণ সফলভাবে সম্পন্ন হয়েছে।"
    },
    "gu": {
        "title": "ફાર્મસારથી",
        "subtitle": "પ્રાદેશિક ખેડૂત સહાય માટે એઆઈ પાક વિશ્લેષણ",
        "state": "રાજ્ય",
        "district": "જિલ્લો",
        "language": "ભાષા",
        "crop_interest": "પાક રસ",
        "analyze": "ખેતી સ્થિતિ વિશ્લેષણ કરો",
        "voice": "વોઈસ ઇનપુટ વાપરો",
        "results": "ભલામણ પરિણામો",
        "top_crops": "મુખ્ય પાક સૂચનો",
        "irrigation": "સિંચાઈ સલાહ",
        "fertilizer": "ખાતર સલાહ",
        "alerts": "ચેતવણીઓ",
        "impact": "નિર્ણય ચોકસાઈ સ્કોર",
        "placeholder": "ઉદાહરણ: cotton, rice, maize",
        "loading": "જિલ્લાની સ્થિતિનું વિશ્લેષણ થઈ રહ્યું છે...",
        "model": "મોડલ માહિતી",
        "overview": "ખેતર સારાંશ",
        "select_state": "રાજ્ય પસંદ કરો",
        "select_district": "જિલ્લો પસંદ કરો",
        "success": "વિશ્લેષણ સફળતાપૂર્વક પૂર્ણ થયું."
    },
    "ml": {
        "title": "ഫാംസാരഥി",
        "subtitle": "പ്രാദേശിക കർഷക സഹായത്തിനായുള്ള എഐ വിള വിശകലനം",
        "state": "സംസ്ഥാനം",
        "district": "ജില്ല",
        "language": "ഭാഷ",
        "crop_interest": "വിള താൽപ്പര്യം",
        "analyze": "കൃഷിസ്ഥിതി വിശകലനം ചെയ്യുക",
        "voice": "വോയ്സ് ഇൻപുട്ട് ഉപയോഗിക്കുക",
        "results": "ശുപാർശ ഫലങ്ങൾ",
        "top_crops": "പ്രധാന വിള നിർദേശങ്ങൾ",
        "irrigation": "ജലസേചന ഉപദേശം",
        "fertilizer": "വള ഉപദേശം",
        "alerts": "അറിയിപ്പുകൾ",
        "impact": "തീരുമാന കൃത്യത സ്കോർ",
        "placeholder": "ഉദാഹരണം: cotton, rice, maize",
        "loading": "ജില്ലാ സാഹചര്യങ്ങൾ വിശകലനം ചെയ്യുന്നു...",
        "model": "മോഡൽ വിവരങ്ങൾ",
        "overview": "വയൽ അവലോകനം",
        "select_state": "സംസ്ഥാനം തിരഞ്ഞെടുക്കുക",
        "select_district": "ജില്ല തിരഞ്ഞെടുക്കുക",
        "success": "വിശകലനം വിജയകരമായി പൂർത്തിയായി."
    }
}


@app.route("/", methods=["GET"])
def index():
    districts = engine.list_districts()
    states = engine.list_states()
    selected_language = request.args.get("language", "en")
    labels = TRANSLATIONS.get(selected_language, TRANSLATIONS["en"])

    return render_template(
        "index.html",
        districts=districts,
        states=states,
        labels=labels,
        languages=TRANSLATIONS,
        language_names=LANGUAGE_NAMES,
        selected_language=selected_language
    )


@app.post("/analyze")
def analyze():
    payload = request.get_json(silent=True) or request.form
    state = payload.get("state", "")
    district = payload.get("district", "")
    language = payload.get("language", "en")
    crop_interest = payload.get("crop_interest", "")

    result = engine.recommend(district, language, crop_interest, state)
    if result.get("error"):
        return jsonify(result), 400
    return jsonify(result)


if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
