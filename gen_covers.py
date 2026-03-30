import requests, base64, json, os, time

API_KEY = "AIzaSyD38LKBJXFTVLzDiM0pbQn70fCJ7uwfAHI"
MODEL   = "gemini-3.1-flash-image-preview"
URL     = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

OUTPUT_DIR = r"C:\Users\kamel\projets\amazi\covers"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TRACKS = [
    ("adrar",   "Photorealistic Atlas mountains Morocco at golden hour, dramatic clouds, Berber village on mountain slope with terracotta houses, cinematic warm light, no text"),
    ("agadir",  "Photorealistic ancient Berber kasbah walls at sunset, warm terracotta tones, Moroccan mud-brick architecture, dramatic orange-purple sky, North Africa, no text"),
    ("akal",    "Photorealistic Kabylie Berber mountain village Algeria, terraced stone houses on rocky hillside, olive trees, golden afternoon Mediterranean light, no text"),
    ("andalus", "Photorealistic ornate Moroccan Andalusian arch with intricate zellige tiles and arabesque plaster carvings at night, moonlight, blue and gold tones, no text"),
    ("anzar",   "Photorealistic Sahara desert sand dunes with hot wind creating ripple patterns, golden sand waves, dramatic long shadows, no people, Morocco Erg Chebbi, no text"),
    ("imesli",  "Photorealistic Gnawa musician playing darbouka drum in Moroccan medina at night, colorful qmaja costume with pompoms, warm lantern light, no text"),
    ("izuran",  "Photorealistic Tuareg nomad on camel silhouette crossing Sahara dunes at sunset, epic orange sky, traditional blue boubou robes, dramatic desert landscape, no text"),
    ("layla",   "Photorealistic Milky Way and stars over ancient Moroccan kasba ruins in Sahara, blue-purple cosmic night sky, silhouette of kasbah walls, no text"),
    ("maqam",   "Photorealistic Moroccan riad inner courtyard with central fountain, intricate geometric zellige tiles, carved white plaster walls, lemon tree, warm lantern light, no text"),
    ("qanun",   "Photorealistic traditional Moroccan tea ceremony, ornate engraved silver teapot pouring tea, colorful glass cups, geometric patterns table, warm amber candlelight, no text"),
    ("tafat",   "Photorealistic Tenere desert Niger at golden hour, vast flat golden sand with isolated rock formations, dramatic light shafts from clouds, epic empty horizon, no text"),
    ("tasusmi", "Photorealistic Gnawa musicians in spiritual ceremony in Marrakech Djemaa el Fna, colorful qmaja costumes, playing guembri bass lute, night atmosphere, mystical, no text"),
]

total = len(TRACKS)
for idx, (filename, prompt) in enumerate(TRACKS, 1):
    out_path = os.path.join(OUTPUT_DIR, f"{filename}.jpg")
    if os.path.exists(out_path):
        print(f"[{idx}/{total}] SKIP: {filename}.jpg")
        continue

    print(f"[{idx}/{total}] Generating {filename}...")

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]}
    }

    try:
        resp = requests.post(URL, json=payload, timeout=90)
        resp.raise_for_status()
        data = resp.json()

        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        saved = False
        for part in parts:
            if "inlineData" in part:
                img_bytes = base64.b64decode(part["inlineData"]["data"])
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
                print(f"  OK Saved {len(img_bytes)//1024} KB -> {out_path}")
                saved = True
                break
        if not saved:
            print(f"  FAIL No image in response")
            print(f"    {json.dumps(data, indent=2)[:600]}")

    except Exception as e:
        print(f"  FAIL Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"    {e.response.text[:400]}")

    time.sleep(3)

print("\nDone! Covers saved to:", OUTPUT_DIR)
