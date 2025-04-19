# Local storage utilities : Current deployment @Supabase
import os

# Store Generated Hashes to file
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SONGS_DIR_PATH: str = os.path.join(BASE_DIR, "songs")
RECORDINGS_DIR: str = os.path.join(BASE_DIR, "recordings")
SONGS_METADATA_PATH: str = os.path.join(BASE_DIR, "songsData.json")

def get_recorded_path(fileName: str) -> str:
    RECORDED_PATH = os.path.join(RECORDINGS_DIR, f"{fileName}.wav")
    return RECORDED_PATH

songs: list[dict] = [
    {
        "song": "Shayad",
        "artists": ["Arijit Singh"]
    },
    {
        "song": "Attention",
        "artists": ["Charlie Puth"]
    },
    {
        "song": "Die For You",
        "artists": ["The Weeknd", "Ariana Grande"]
    },
    {
        "song": "Khairiyat",
        "artists": ["Arijit Singh"]
    },
    {
        "song": "Save Your Tears",
        "artists": ["The Weeknd", "Ariana Grande"]
    },
    {
        "song": "We Don't Talk Anymore",
        "artists": ["Charlie Puth", "Selena Gomez"]
    }
]