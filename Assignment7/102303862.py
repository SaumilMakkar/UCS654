#!/usr/bin/env python3
"""
YouTube Audio Mashup Program
Downloads N videos from a singer, converts to audio, cuts first Y seconds, and merges them.
"""

import sys
import os
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import ffmpeg_downloader as ffdl
import shutil
import time


def print_usage():
    """Print usage information"""
    print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
    print("Example: python 1015579.py \"Sharry Maan\" 11 21 1015579-output.mp3")


def validate_arguments(args):
    """
    Validate command line arguments
    Returns: (singer_name, num_videos, audio_duration, output_file) or None if invalid
    """
    if len(args) != 5:
        print("Error: Incorrect number of parameters.")
        print(f"Expected 4 parameters, got {len(args) - 1}")
        print_usage()
        return None
    
    singer_name = args[1]
    
    try:
        num_videos = int(args[2])
        if num_videos <= 10:
            print("Error: Number of videos must be greater than 10.")
            return None
    except ValueError:
        print("Error: NumberOfVideos must be a valid integer.")
        return None
    
    try:
        audio_duration = int(args[3])
        if audio_duration <= 20:
            print("Error: Audio duration must be greater than 20 seconds.")
            return None
    except ValueError:
        print("Error: AudioDuration must be a valid integer.")
        return None
    
    output_file = args[4]
    if not output_file.endswith('.mp3'):
        print("Warning: Output file should have .mp3 extension")
    
    return singer_name, num_videos, audio_duration, output_file


def download_videos(singer_name, num_videos):
    """
    Download videos from YouTube for the specified singer
    Returns: list of downloaded video file paths
    """
    print(f"\n[1/4] Searching and downloading {num_videos} videos for '{singer_name}'...")
    
    # Create downloads directory
    download_dir = "downloads"
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir)
    
    # YouTube search query
    search_query = f"ytsearch{num_videos}:{singer_name}"

    # yt-dlp requires an external JS runtime for full YouTube support.
    # In the Python API, js_runtimes must be a dict: {runtime: {config}}.
    js_runtimes = None
    if shutil.which('node'):
        js_runtimes = {'node': {}}
        print("Using JavaScript runtime: node (required for YouTube extraction).")
    elif shutil.which('deno'):
        js_runtimes = {'deno': {}}
        print("Using JavaScript runtime: deno (default).")
    else:
        print("WARNING: No JavaScript runtime found (node/deno). YouTube downloads may fail.")
    
    # Try manual cookie file FIRST if it exists (most reliable)
    # Check in current directory and script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cookie_file = None
    for path in ["cookies.txt", os.path.join(script_dir, "cookies.txt"), os.path.join(os.getcwd(), "cookies.txt")]:
        if os.path.exists(path):
            cookie_file = path
            break
    
    if cookie_file:
        print(f"\nUsing manual cookie file ({cookie_file})...")
        print(f"Cookie file found at: {os.path.abspath(cookie_file)}")
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                # Use safe ASCII filenames to avoid encoding/locking issues
                'outtmpl': f'{download_dir}/%(id)s.%(ext)s',
                'restrictfilenames': True,
                'quiet': False,
                'no_warnings': False,
                **({'js_runtimes': js_runtimes} if js_runtimes else {}),
                'cookiefile': cookie_file,
                'retries': 3,
                'fragment_retries': 3,
                # Use 'web' client with cookies (Android doesn't support cookies)
                'extractor_args': {
                    'youtube': {
                        'player_client': ['web'],  # Web client supports cookies
                    }
                },
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=True)
                
                downloaded_files = []
                if info and 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            title = entry.get('title', 'video')
                            for file in os.listdir(download_dir):
                                if file.startswith(title[:50]):
                                    downloaded_files.append(os.path.join(download_dir, file))
                                    break
                
                if downloaded_files:
                    print(f"Successfully downloaded {len(downloaded_files)} videos using cookie file")
                    return downloaded_files
                else:
                    all_files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) 
                                if os.path.isfile(os.path.join(download_dir, f))]
                    if all_files:
                        print(f"Successfully downloaded {len(all_files)} videos using cookie file")
                        return all_files
        except Exception as e:
            error_msg = str(e).lower()
            if "format is not available" in error_msg or "requested format" in error_msg:
                print(f"Web client with cookies failed: Format not available.")
                print("Trying without specifying player client (let yt-dlp choose)...")
                # Try without specifying client - let yt-dlp choose the best one
                try:
                    ydl_opts_no_client = {
                        'format': 'bestaudio/best',
                        'outtmpl': f'{download_dir}/%(id)s.%(ext)s',
                        'restrictfilenames': True,
                        'quiet': False,
                        'no_warnings': False,
                        **({'js_runtimes': js_runtimes} if js_runtimes else {}),
                        'cookiefile': cookie_file,
                        'retries': 3,
                        'fragment_retries': 3,
                    }
                    with YoutubeDL(ydl_opts_no_client) as ydl:
                        info = ydl.extract_info(search_query, download=True)
                        all_files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) 
                                    if os.path.isfile(os.path.join(download_dir, f))]
                        if all_files:
                            print(f"Successfully downloaded {len(all_files)} videos using cookies (auto client)")
                            return all_files
                except Exception as e2:
                    print(f"Auto client selection also failed: {str(e2)[:150]}")
            elif "bot" in error_msg or "sign in" in error_msg:
                print(f"Cookie file failed: Still detected as bot.")
                print("Trying with different player clients...")
                
                # Try with different clients using the same cookie file
                for client in ['ios']:
                    try:
                        print(f"  Trying {client} client with cookies...")
                        ydl_opts['extractor_args'] = {
                            'youtube': {
                                'player_client': [client],
                            }
                        }
                        with YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(search_query, download=True)
                            all_files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) 
                                        if os.path.isfile(os.path.join(download_dir, f))]
                            if all_files:
                                print(f"Successfully downloaded {len(all_files)} videos using {client} client with cookies")
                                return all_files
                    except Exception as e2:
                        print(f"  {client} client also failed: {str(e2)[:100]}")
                        continue
                
                print("\nAll methods with cookies failed. Possible reasons:")
                print("  1. Cookies may be expired - export fresh cookies from browser")
                print("  2. YouTube is temporarily blocking - wait 10-15 minutes and try again")
                print("  3. Need to be logged into YouTube when exporting cookies")
            else:
                # Avoid printing full exception message to sidestep Unicode console issues
                print("Cookie file method failed (see yt-dlp logs above for details).")
                # Try one more time without specifying client
                try:
                    print("Retrying without specifying player client...")
                    ydl_opts_simple = {
                        'format': 'bestaudio/best',
                        'outtmpl': f'{download_dir}/%(id)s.%(ext)s',
                        'restrictfilenames': True,
                        'quiet': False,
                        **({'js_runtimes': js_runtimes} if js_runtimes else {}),
                        'cookiefile': cookie_file,
                        'retries': 3,
                    }
                    with YoutubeDL(ydl_opts_simple) as ydl:
                        info = ydl.extract_info(search_query, download=True)
                        all_files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) 
                                    if os.path.isfile(os.path.join(download_dir, f))]
                        if all_files:
                            print(f"Successfully downloaded {len(all_files)} videos")
                            return all_files
                except:
                    pass
    
    # If cookie file doesn't exist or failed, try browser cookies
    browsers_to_try = ['firefox', 'edge', 'chrome']
    
    for browser in browsers_to_try:
        print(f"\nTrying with {browser} browser cookies...")
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{download_dir}/%(id)s.%(ext)s',
                'restrictfilenames': True,
                'quiet': False,
                'no_warnings': False,
                'extract_flat': False,
                **({'js_runtimes': js_runtimes} if js_runtimes else {}),
                'cookiesfrombrowser': (browser,),
                'retries': 3,
                'fragment_retries': 3,
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=True)
                
                downloaded_files = []
                if info and 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            title = entry.get('title', 'video')
                            for file in os.listdir(download_dir):
                                if file.startswith(title[:50]):
                                    downloaded_files.append(os.path.join(download_dir, file))
                                    break
                
                if downloaded_files:
                    print(f"Successfully downloaded {len(downloaded_files)} videos using {browser} cookies")
                    return downloaded_files
                else:
                    all_files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) 
                                if os.path.isfile(os.path.join(download_dir, f))]
                    if all_files:
                        print(f"Found {len(all_files)} downloaded files")
                        return all_files
        except Exception as e:
            error_msg = str(e).lower()
            if "cookie" in error_msg or "could not copy" in error_msg:
                print(f"  {browser} cookies unavailable, trying next browser...")
                continue
            elif "bot" in error_msg or "sign in" in error_msg:
                print(f"  {browser} cookies failed: Still detected as bot")
                continue
            else:
                all_files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) 
                            if os.path.isfile(os.path.join(download_dir, f))]
                if all_files:
                    print(f"Found {len(all_files)} downloaded files despite error")
                    return all_files
    
    # Last resort: Try different player clients without cookies
    print("\nTrying player clients without cookies...")
    player_clients = ['android', 'ios']
    
    for client in player_clients:
        print(f"\nTrying with {client} client...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{download_dir}/%(id)s.%(ext)s',
            'restrictfilenames': True,
            'quiet': False,
            'no_warnings': False,
            **({'js_runtimes': js_runtimes} if js_runtimes else {}),
            'extractor_args': {
                'youtube': {
                    'player_client': [client],
                }
            },
            'retries': 3,
            'fragment_retries': 3,
        }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=True)
                all_files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) 
                            if os.path.isfile(os.path.join(download_dir, f))]
                if all_files:
                    print(f"Successfully downloaded {len(all_files)} videos using {client} client")
                    return all_files
        except Exception as e:
            error_msg = str(e).lower()
            if "bot" in error_msg or "sign in" in error_msg:
                print(f"  {client} client failed: Bot detection")
                continue
    
    # All methods failed
    print("\n" + "="*70)
    print("All download methods failed due to YouTube bot detection.")
    print("="*70)
    print("\nSOLUTION: Export cookies from your browser manually:")
    print("\nMethod 1 - Using Browser Extension (Easiest):")
    print("  1. Install 'Get cookies.txt LOCALLY' extension in Chrome/Firefox")
    print("  2. Go to youtube.com and log in")
    print("  3. Click the extension icon -> Export -> Save as 'cookies.txt'")
    print("  4. Place cookies.txt in the same folder as this script")
    print("  5. Run the script again")
    print("\nMethod 2 - Using yt-dlp command:")
    print("  Run: yt-dlp --cookies-from-browser firefox --print-to-file url cookies.txt")
    print("\nMethod 3 - Wait and retry:")
    print("  YouTube may be temporarily blocking. Wait 10-15 minutes and try again.")
    print("\nMethod 4 - Install Node.js:")
    print("  Download from https://nodejs.org/ and install")
    print("  This helps yt-dlp bypass some YouTube restrictions")
    print("="*70)
    
    return []


def convert_to_audio(video_files):
    """
    Convert video files to audio (mp3)
    Returns: list of audio file paths
    """
    print(f"\n[2/4] Converting {len(video_files)} videos to audio...")

    # Ensure ffmpeg/ffprobe are available for pydub
    try:
        ffmpeg_path = ffdl.ffmpeg_path
        ffprobe_path = ffdl.ffprobe_path
        if ffmpeg_path and ffprobe_path:
            # Make sure ffmpeg/ffprobe are discoverable via PATH (pydub uses `which("ffprobe")`)
            ffmpeg_bin_dir = os.path.dirname(ffmpeg_path)
            current_path = os.environ.get("PATH", "")
            if ffmpeg_bin_dir and ffmpeg_bin_dir not in current_path.split(os.pathsep):
                os.environ["PATH"] = os.pathsep.join([ffmpeg_bin_dir, current_path])

            AudioSegment.converter = ffmpeg_path
            AudioSegment.ffmpeg = ffmpeg_path
            AudioSegment.ffprobe = ffprobe_path
            print(f"Using ffmpeg at: {ffmpeg_path}")
        else:
            print("Warning: ffmpeg binaries not found via ffmpeg-downloader; conversion may fail.")
    except Exception as e:
        print(f"Warning: Could not configure ffmpeg for pydub: {e}")
    
    audio_dir = "audio_files"
    if os.path.exists(audio_dir):
        shutil.rmtree(audio_dir)
    os.makedirs(audio_dir)
    
    audio_files = []
    
    for i, video_file in enumerate(video_files):
        try:
            print(f"Converting {i+1}/{len(video_files)}: {os.path.basename(video_file)}")
            
            # Load audio from video file
            audio = AudioSegment.from_file(video_file)
            
            # Export as mp3
            audio_filename = f"audio_{i+1}.mp3"
            audio_path = os.path.join(audio_dir, audio_filename)
            audio.export(audio_path, format="mp3")
            
            audio_files.append(audio_path)
            
        except Exception as e:
            print(f"Error converting {video_file}: {e}")
            continue
    
    print(f"Successfully converted {len(audio_files)} files to audio")
    return audio_files


def cut_audio_clips(audio_files, duration_seconds):
    """
    Cut first Y seconds from each audio file
    Returns: list of cut audio segments
    """
    print(f"\n[3/4] Cutting first {duration_seconds} seconds from each audio file...")
    
    cut_clips = []
    duration_ms = duration_seconds * 1000  # Convert to milliseconds
    
    for i, audio_file in enumerate(audio_files):
        try:
            print(f"Processing {i+1}/{len(audio_files)}: {os.path.basename(audio_file)}")
            
            # Load audio
            audio = AudioSegment.from_mp3(audio_file)
            
            # Cut first Y seconds
            cut_audio = audio[:duration_ms]
            
            cut_clips.append(cut_audio)
            
        except Exception as e:
            print(f"Error cutting audio {audio_file}: {e}")
            continue
    
    print(f"Successfully cut {len(cut_clips)} audio clips")
    return cut_clips


def merge_audio_clips(audio_clips, output_file):
    """
    Merge all audio clips into a single output file
    """
    print(f"\n[4/4] Merging {len(audio_clips)} audio clips into '{output_file}'...")
    
    try:
        # Combine all clips
        merged_audio = AudioSegment.empty()
        
        for i, clip in enumerate(audio_clips):
            print(f"Merging clip {i+1}/{len(audio_clips)}")
            merged_audio += clip
        
        # Export merged audio
        merged_audio.export(output_file, format="mp3")
        
        print(f"\n✓ Successfully created mashup: {output_file}")
        print(f"  Total duration: {len(merged_audio) / 1000:.2f} seconds")
        print(f"  File size: {os.path.getsize(output_file) / (1024*1024):.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"Error merging audio clips: {e}")
        return False


def cleanup_temp_files():
    """Clean up temporary directories"""
    print("\nCleaning up temporary files...")
    
    for directory in ["downloads", "audio_files"]:
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory)
            except Exception as e:
                # Avoid printing full exception (may contain non-encodable chars on Windows)
                print(f"Warning: Could not remove {directory}.")


def main():
    """Main program execution"""
    print("=" * 70)
    print("YouTube Audio Mashup Creator")
    print("=" * 70)
    
    # Validate arguments
    result = validate_arguments(sys.argv)
    if result is None:
        sys.exit(1)
    
    singer_name, num_videos, audio_duration, output_file = result
    
    print(f"\nConfiguration:")
    print(f"  Singer: {singer_name}")
    print(f"  Number of videos: {num_videos}")
    print(f"  Audio duration per clip: {audio_duration} seconds")
    print(f"  Output file: {output_file}")
    
    try:
        # Step 1: Download videos
        video_files = download_videos(singer_name, num_videos)
        if not video_files:
            print("\nError: No videos were downloaded. Exiting.")
            sys.exit(1)
        
        # Step 2: Convert to audio
        audio_files = convert_to_audio(video_files)
        if not audio_files:
            print("\nError: No audio files were created. Exiting.")
            sys.exit(1)
        
        # Step 3: Cut audio clips
        cut_clips = cut_audio_clips(audio_files, audio_duration)
        if not cut_clips:
            print("\nError: No audio clips were cut. Exiting.")
            sys.exit(1)
        
        # Step 4: Merge audio clips
        success = merge_audio_clips(cut_clips, output_file)
        if not success:
            print("\nError: Failed to create mashup. Exiting.")
            sys.exit(1)
        
        # Clean up temporary files
        cleanup_temp_files()
        
        print("\n" + "=" * 70)
        print("Mashup creation completed successfully!")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
        cleanup_temp_files()
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        cleanup_temp_files()
        sys.exit(1)


if __name__ == "__main__":
    main()