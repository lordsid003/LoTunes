## 🎵LoTunes

Have you ever been at a café, club, or party and suddenly a tune plays that strikes a nostalgic chord? You *know* you've heard it before, but the name just slips away... frustrating, right?
<b><i>LoTunes</i></b> is a browser-based music recognition app that listens, thinks, and tells you exactly what song is playing — all within seconds. No installations, no fuss. Just open, record, and rediscover the music you love. Implemented using <b><i>Shazam's Algorithm</i></b> from scratch!

---

Try it live: https://lotunes.streamlit.app

---

## 🚀 Features

* 🎤 **Real-Time Audio Capture** via your browser
* 🧠 **Shazam-like Audio Fingerprinting** using constellation maps
* 🔍 **Hash-based Song Matching** for fast, accurate recognition
* 📡 **Supabase Cloud Database** for storing song fingerprints
* 🎨 **Streamlit UI** – clean, fast, and interactive
* 🖼️ **Song Metadata & Cover Art** display on successful match

---
## Workflow

<img src="https://github.com/user-attachments/assets/0ea81a4e-f916-4487-b9ab-333b2bfbb6de?raw=true" width="50%"/>

## 🎬 Gallery

<img src="https://github.com/user-attachments/assets/e3f28c62-f7f1-4607-b319-fe82ef213aa6?raw=true" width="50%" />
<img src="https://github.com/user-attachments/assets/dd8d9bf2-51e8-4014-b948-e8249b12a9b4?raw=true" width="50%" />




---

## 🛠️ Tech Stack

| Layer            | Technology                                |
| ---------------- | ----------------------------------------- |
| Frontend         | Streamlit                                 |
| Audio Capture    | `st_audiorec`                             |
| Audio Processing | NumPy, SciPy, Librosa                     |
| Fingerprinting   | Custom hash-based algorithm (like Shazam) |
| Database         | Supabase (PostgreSQL + REST API)          |
| Deployment       | Streamlit Cloud (or localhost)            |

---

## 📁 Folder Structure

```
LoTunes/
│
├── fingerprints/         # Fingerprinting and hashing logic
├── database/             # Supabase interaction scripts
├── streamlit_app.py      # Streamlit UI logic
├── utils.py              # Audio utils (FFT, filtering, plotting)
├── add_songs.py          # Add songs to fingerprint DB
├── requirements.txt      # All dependencies
└── README.md             # You're here!
```

---

## 🧪 How It Works

1. **Record 20 seconds** of audio in the browser.
2. Convert to spectrogram → detect peaks → generate *constellation map*.
3. Hash pairs of peaks into fingerprints.
4. Compare hashes to those in the Supabase DB.
5. Find the best match using **offset-vote matching**.
6. Boom! 🎶 Song title, artist, album art, and playback link delivered.

---

## 💻 Installation

Clone the repo:

```bash
git clone https://github.com/your-username/LoTunes.git
cd LoTunes
```

Create a virtual environment and install requirements:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run streamlit_app.py
```

---

## 🧠 Inspiration

Inspired by the magic of **Shazam**, we wanted to build a lightweight, open-source alternative that works entirely in the browser. Whether you’re a music lover, a techie, or both — this project combines sound science with a love for soundtracks.

---

## 🧩 Want to Add Songs?

1. Place `.mp3` or `.wav` files in your `songs/` directory.
2. Run:

```bash
python add_songs.py
```

3. Songs will be processed and fingerprints stored in your Supabase DB.

---

## 🌍 Roadmap

* [x] Real-time audio recognition
* [x] Supabase fingerprint storage
* [x] UI with Streamlit
* [ ] Upload and recognize from local files
* [ ] Deploy publicly
* [ ] Add community support for song contributions

---

## 👨‍💻 Author

Made by Siddharth Verma [LordSid003]

---

## 📜 License

MIT License – free to fork, build, and remix your own sonic sleuth!

---
