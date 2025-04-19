# For loading songs from local directory to supabase
import os
import json
# Progress bars
from tqdm import tqdm
from mimetypes import guess_type
from config import client, SUPABASE_BUCKET, SUPABASE_TABLE
from utils.paths import SONGS_DIR_PATH, SONGS_METADATA_PATH
from utils.fingerprints import get_peaks, get_spectrogram, FAN_VALUE, get_remote_audio_fileName

ARTISTS: str = "artists"
POSTER_URL: str = "posterURL"

with open(SONGS_METADATA_PATH) as f:
    songs_metaData = json.load(f)

def generate_hashes(peaks):
    hashes = []
    for i in tqdm(range(len(peaks)), desc="⛓ Generating Hashes", leave=False):
        for j in range(1, FAN_VALUE):
            if i + j < len(peaks):
                f1, t1 = peaks[i]
                f2, t2 = peaks[i + j]
                delta_t = t2 - t1
                if 0 <= delta_t <= 200:
                    h = hash((f1, f2, delta_t))
                    hashes.append((int(h), int(t1)))
    return hashes

def process_songs():
    song_files = [f for f in os.listdir(SONGS_DIR_PATH) if f.endswith(".mp3")]

    for file in tqdm(song_files, desc = "🎼 Processing songs"):
        filePath: str = os.path.join(SONGS_DIR_PATH, file)

        # Examine match with songsData.json file
        matching_entry = None
        for key, meta in songs_metaData.items():
            remote_audio_fileName = get_remote_audio_fileName(key, meta[ARTISTS])
            if remote_audio_fileName == file:
                matching_entry = (key, meta)
                break

        if not matching_entry:
            print(f"❌ MetaData missing for file: {file}")
            continue

        # Extract song information for processing and database insertion
        song_title, meta_data = matching_entry
        artists = meta_data[ARTISTS]
        poster_url = meta_data[POSTER_URL]

        # Hashing and fingerprinting
        print(f"\n🎧 Fingerprinting file: {file}")
        try:
            spectrogram, _ = get_spectrogram(audio_path = filePath)
            peaks = get_peaks(spectrogram = spectrogram)
            hashes = generate_hashes(peaks = peaks)
            print(f"✅ Generated {len(hashes)} hashes for file: {file}")
        except Exception as e:
            print(f"❌ Fingerprinting failed for {file}: {e}")
            continue

        # Upload to supabase storage
        remote_path = file
        mime_type, _ = guess_type(filePath)
        try:
            with open(filePath, "rb") as audio_file:
                client.storage.from_(SUPABASE_BUCKET).upload(
                    path = remote_path,
                    file = audio_file,
                    file_options = {
                        "content-type": mime_type or "audio/mpeg",
                        "cache-control": "3600",
                    }
                )
            print(f"📩 Uploaded file: {file} to Bucket.")
        except Exception as e:
            print(f"❌ Upload failed for {file}: {e}")
            continue

        existing = client.table(SUPABASE_TABLE).select("song_name").eq("song_name", song_title).execute()
        if existing.data:
            print(f"⚠️ Entry already exists for: {song_title}")
            continue

        # Insertion to supabase SQL table
        db_entry = {
            "song_name": song_title,
            "hashes": hashes,
            "song_artists": artists,
            "song_poster_URL": poster_url
        }

        try:
            client.table(SUPABASE_TABLE).insert(db_entry).execute()
            print(f"🗃️ Inserted DB entry for: {song_title}")
        except Exception as e:
            print(f"❌ Supabase insert failed: {e}")

    print("\n✅ All songs processed successfully!")

# Execution
if __name__ == "__main__":
    process_songs()