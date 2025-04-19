from collections import Counter
from utils.fingerprints import get_spectrogram, get_peaks, generate_hashes
from utils.paths import get_recorded_path
from config import SUPABASE_TABLE, client

def load_fingerprints_from_supabase():
    print("🗄️ Fetching fingerprints from Supabase...")
    response = client.table(SUPABASE_TABLE).select("song_name", "hashes", "song_artists", "song_poster_URL").execute()

    if not response.data:
        raise ValueError("❌ No fingerprint data found in Supabase!")
    
    db = {}
    for entry in response.data:
        song_name = entry["song_name"]
        hashes = entry["hashes"]
        song_artists = entry["song_artists"]  # This should be an array
        song_poster_URL = entry["song_poster_URL"]
        db[song_name] = {
            "hashes": hashes,
            "song_artists": song_artists,
            "song_poster_URL": song_poster_URL
        }

    print(f"✅ Loaded fingerprints for {len(db)} songs.")
    return db

def match_clip_to_song(recorded_hashes, database):
    scores = {}
    song_details = {}
    
    for song, song_data in database.items():
        song_hashes = song_data["hashes"]
        offset_deltas = Counter()
        song_hash_map = {}
        
        # Build map: hash => [timestamps in song]
        for h, t in song_hashes:
            song_hash_map.setdefault(h, []).append(t)
        
        # Match against recorded clip
        for h, t_rec in recorded_hashes:
            if h in song_hash_map:
                for t_song in song_hash_map[h]:
                    offset_deltas[t_song - t_rec] += 1
        
        if offset_deltas:
            best_offset, count = offset_deltas.most_common(1)[0]
            print(f"🎼 Matching against: {song} | Top offset: {best_offset}, Matches: {count}")
            scores[song] = count
            song_details[song] = {
                "score": count,
                "artists": song_data["song_artists"],
                "poster_url": song_data["song_poster_URL"]
            }
        else:
            scores[song] = 0
    
    if not scores:
        return None, 0, None, None
    
    best_match = max(scores, key=scores.get)
    return best_match, scores[best_match], song_details[best_match]["artists"], song_details[best_match]["poster_url"]

def recognize(RECORDED_PATH: str):
    print("🎧 Matching recorded clip...")
    
    spec, _ = get_spectrogram(RECORDED_PATH)
    peaks = get_peaks(spec)
    print(f"🔍 Extracted {len(peaks)} peaks from recorded audio.")
    
    hashes = generate_hashes(peaks)
    print(f"🔗 Generated {len(hashes)} hashes from recorded audio.")
    
    database = load_fingerprints_from_supabase()
    best_match, match_score, _, _ = match_clip_to_song(hashes, database)

    if match_score == 0:
        print("😞 No matching song found.")
    else:
        print(f"✅ Match found: {best_match} ({match_score} matching hashes)")

if __name__ == "__main__":
    fileName: str = str(input("File name for matching: "))
    RECORDED_PATH = get_recorded_path(fileName=fileName)
    recognize(RECORDED_PATH=RECORDED_PATH)