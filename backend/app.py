import os
import tempfile
import streamlit as st
from utils.paths import songs
from audio_recorder_streamlit import audio_recorder
from match import match_clip_to_song, load_fingerprints_from_supabase
from utils.fingerprints import get_spectrogram, get_peaks, generate_hashes

# Page configuration with custom theme
st.set_page_config(
    page_title="LoTunes | Music Identifier",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

database = load_fingerprints_from_supabase()

with st.sidebar:
    st.subheader("Available Songs")

    st.markdown("""
    <style>
        .song-poster-image {
            width: 100%;
            height: 120px;
            object-fit: cover;
            border-radius: 8px;
        }
        
        .song-container {
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid rgba(250, 250, 250, 0.2);
        }
    </style>
    """, unsafe_allow_html=True)

    for songName, songData in database.items():
        st.markdown("<div class='song-container'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"""
                <img src="{songData['song_poster_URL']}" class="song-poster-image" alt="{songName}"/>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="song-name-header">
                🎶 {songName}
            </div>
            """, unsafe_allow_html=True)
            for artist in songData["song_artists"]:
                st.markdown(f"""
                <p class="song-artists" style="font-size: 0.7rem;">
                    {artist}   
                </p>
                """, unsafe_allow_html=True)
        st.markdown("""<div></div>""", unsafe_allow_html=True)

# Custom CSS for styling with theme compatibility
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
    }
    
    /* Header styling - works with both themes */
    .app-header {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
        padding: 2.5rem 1rem 1.5rem 1rem;
        border-radius: 1rem;
        color: white !important; /* Force white text regardless of theme */
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
            
    .song-name-header {
        background-color: #FF4B4B;
        color: white !important;
        border-radius: 0.3rem;
        font-size: 0.85rem;
        padding: 0.5rem;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Content containers with theme-aware backgrounds */
    .content-section {
        background-color: rgba(248, 249, 250, 0.05); /* Very light background that works in both themes */
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(233, 236, 239, 0.2); /* Subtle border that works in both themes */
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        height: 3rem;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    /* Identify button */
    .identify-button > button {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    
    .identify-button > button:hover {
        background-color: #45a049 !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* New recording button */
    .new-recording-button > button {
        background-color: #3f51b5 !important;
        color: white !important;
    }
    
    .new-recording-button > button:hover {
        background-color: #303f9f !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Result message for identified song */
    .song-identified {
        background-color: rgba(13, 110, 253, 0.2); /* Semi-transparent blue */
        border-left: 4px solid #0d6efd;
        color: inherit; /* Use the theme's text color */
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* Result message for no match */
    .no-match {
        background-color: rgba(255, 193, 7, 0.2); /* Semi-transparent yellow */
        border-left: 4px solid #ffc107;
        color: inherit; /* Use the theme's text color */
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* Tips section with theme awareness */
    .tips-section {
        background-color: rgba(0, 123, 255, 0.1); /* Semi-transparent blue */
        border-left: 4px solid #0d6efd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    
    /* Footer styling with theme awareness */
    .footer {
        text-align: center;
        opacity: 0.8; /* Slightly muted but visible in both themes */
        padding-top: 1rem;
        border-top: 1px solid rgba(233, 236, 239, 0.2); /* Subtle line */
        margin-top: 2rem;
    }
    
    /* Audio player styling */
    audio {
        width: 100%;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    
    /* Song result card */
    .song-result-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1.5rem 0;
        background: linear-gradient(145deg, #4481eb 0%, #04befe 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .song-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .song-name {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .match-score {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Loading animation for identification */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .identifying-animation {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1.5rem 0;
    }
    
    .identifying-animation span {
        margin: 0 0.5rem;
        font-size: 2rem;
        animation: bounce 1s infinite;
    }
    
    .identifying-animation span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .identifying-animation span:nth-child(3) {
        animation-delay: 0.4s;
    }
            
    .song-poster {
        margin-bottom: 1rem;
        display: flex;
        justify-content: center;
    }

    .song-poster img {
        max-width: 200px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }

    .song-poster img:hover {
        transform: scale(1.02);
    }

    .song-artists {
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for recording status
if 'recording_complete' not in st.session_state:
    st.session_state.recording_complete = False
if 'temp_path' not in st.session_state:
    st.session_state.temp_path = None
if 'identified_song' not in st.session_state:
    st.session_state.identified_song = None
if 'match_score' not in st.session_state:
    st.session_state.match_score = 0
if 'identification_attempted' not in st.session_state:
    st.session_state.identification_attempted = False
if 'recording_in_progress' not in st.session_state:
    st.session_state.recording_in_progress = False
if 'song_artists' not in st.session_state:
    st.session_state.song_artists = None
if 'song_poster_url' not in st.session_state:
    st.session_state.song_poster_url = None
if 'audio_bytes' not in st.session_state:  
    st.session_state.audio_bytes = None

# App header with animated gradient - theme-compatible
st.markdown("""
<div class="app-header">
    <h1>🎵 LoTunes</h1>
    <p>Identify any song by recording a short snippet</p>
</div>
""", unsafe_allow_html=True)

# Information card - theme-compatible
with st.container():
    st.markdown("""
    <div class="content-section">
        <h4>🎯 How It Works</h4>
        <p>Record a snippet of music playing around you, and LoTunes will identify the song using audio fingerprinting technology similar to Shazam.</p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "View sidebar for songs in Database",
        icon=":material/info:"
    )

# Function to reset the app state
def reset_app():
    st.session_state.recording_complete = False
    st.session_state.identified_song = None
    st.session_state.match_score = 0
    st.session_state.song_artists = None
    st.session_state.song_poster_url = None
    st.session_state.identification_attempted = False
    st.session_state.recording_in_progress = False
    st.session_state.audio_bytes = None

    if st.session_state.temp_path and os.path.exists(st.session_state.temp_path):
        os.remove(st.session_state.temp_path)
        st.session_state.temp_path = None

# Display identification results if available
if st.session_state.identification_attempted and st.session_state.identified_song:
    if st.session_state.match_score > 0:
        # Display song match result
        st.markdown(f"""
        <div class="song-result-card">
            <div class="song-poster">
                <img src="{st.session_state.song_poster_url}" alt="Album art" style="max-width: 200px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            </div>
            <div class="song-icon">🎵</div>
            <div class="song-name">{st.session_state.identified_song}</div>
            <div class="song-artists">{"Artist(s): " + ", ".join(st.session_state.song_artists) if st.session_state.song_artists else ""}</div>
            <div class="match-score">Match confidence: {st.session_state.match_score} fingerprint matches</div>
        </div>
        """, unsafe_allow_html=True)
        
        # New recording button
        st.markdown('<div class="new-recording-button">', unsafe_allow_html=True)
        if st.button("🔄 Identify Another Song"):
            reset_app()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # No need to show any other UI elements after successful identification
elif st.session_state.identification_attempted:
    # No match found
    st.markdown("""
    <div class="no-match">
        <h3>😕 No Match Found</h3>
        <p>We couldn't identify this song. Try again with a clearer recording or a more prominent section of the song.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Suggestions for better results
    st.markdown("""
    <div class="tips-section">
        <h4>Suggestions for Better Results:</h4>
        <ul>
            <li>Record during the chorus or most recognizable part</li>
            <li>Move closer to the audio source</li>
            <li>Reduce background noise</li>
            <li>Try a longer recording duration</li>
            <li>Make sure the song is in our database</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # New recording button
    st.markdown('<div class="new-recording-button">', unsafe_allow_html=True)
    if st.button("🔄 Try Again"):
        reset_app()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
# Only show recording UI if no successful identification yet
elif not st.session_state.identification_attempted:
    if not st.session_state.recording_complete:
        with st.container():
            st.markdown("#### 🎚️ Recording Settings")
            duration = st.slider(
                "Recording Duration (seconds)",
                min_value=5,
                max_value=30,
                value=10,
                step=1,
                help="Select how long you want to record. 10-15 seconds is usually enough for song identification."
            )
            # Display selected settings - theme compatible
            st.info(
                f"Current Settings: Recording for {duration} seconds",
                icon=":material/settings:"
            )
            st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        # Starts recording button with custom styling
        if not st.session_state.recording_complete and not st.session_state.recording_in_progress:
            wav_audio_data = audio_recorder(
                text="Click 🎙️ to start recording: ",
                icon_size="2x",
                recording_color="#ff5252",
                neutral_color="#764ba2",
                energy_threshold=(-1.0, 1.0),
                pause_threshold=duration,
            )

            # Displays animation while waiting for recording
            if wav_audio_data is None:
                st.markdown("""
                <div class="recording-animation">
                    <h3>🎧 Waiting for recording...</h3>
                </div>
                """, unsafe_allow_html=True)

            # If recording is done, set session states
            if wav_audio_data is not None and not st.session_state.recording_complete:
                # Save temp WAV file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    tmp_file.write(wav_audio_data)
                    tmp_path = tmp_file.name

                # Save to session state
                st.session_state.temp_path = tmp_path
                st.session_state.audio_bytes = wav_audio_data
                st.session_state.recording_complete = True
                st.session_state.recording_in_progress = False

                st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        
        # Displays audio player and identify button if recording is complete
        if st.session_state.recording_complete and st.session_state.temp_path and not st.session_state.identification_attempted:
            st.success("✅ Recording saved successfully!")
            # Creates playback section with some visual enhancement
            st.markdown("""
            <h4>🔊 Playback Your Recording</h4>
            <p>Listen to make sure your recording captured the music clearly:</p>
            """, unsafe_allow_html=True)
            
            # Audio player
            st.audio(st.session_state.audio_bytes, format="audio/wav")
            
            # Identification button
            st.markdown('<div class="identify-button">', unsafe_allow_html=True)
            identify_song = st.button("🔍 Identify Song")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if identify_song:
                # Show identification animation
                st.markdown("""
                <div class="identifying-animation">
                    <h3>Identifying Song</h3>
                    <span>🎵</span>
                    <span>🔍</span>
                    <span>🎧</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Run identification directly within the Streamlit context
                with st.spinner("Analyzing audio fingerprint..."):
                    try:
                        spec, _ = get_spectrogram(st.session_state.temp_path)
                        peaks = get_peaks(spec)
                        hashes = generate_hashes(peaks)
                        
                        best_match, match_score, artists, poster_url = match_clip_to_song(hashes, database)

                        # Store results in session state
                        st.session_state.identified_song = best_match
                        st.session_state.match_score = match_score
                        st.session_state.song_artists = artists
                        st.session_state.song_poster_url = poster_url
                        st.session_state.identification_attempted = True
                    except Exception as e:
                        st.error(f"Error during identification: {str(e)}")
                        st.session_state.identification_attempted = True
                
                # Force rerun to update UI with results and clear previous elements
                st.rerun()
        
        # Display tips when not recording and no recording has been completed
        elif not st.session_state.recording_complete and not st.session_state.recording_in_progress:
            # Tips for better recording when not recording - theme compatible
            st.markdown("""
            <div class="tips-section">
                <h4>📝 Tips for Best Results:</h4>
                <ul>
                    <li>Hold your device close to the music source</li>
                    <li>Reduce background noise if possible</li>
                    <li>Try to capture a chorus or distinctive part of the song</li>
                    <li>10-15 seconds of clear audio is usually enough</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Footer with additional information - theme compatible
st.markdown("""
<div class="footer">
    <p>🎵 LoTunes uses advanced audio fingerprinting similar to Shazam</p>
    <p>Version 1.0.0 | © 2025 LoTunes</p>
</div>
""", unsafe_allow_html=True)