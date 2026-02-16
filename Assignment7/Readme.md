# YouTube Audio Mashup - Assignment

**Roll Number:** 102303862

## Assignment Overview

Create a command-line Python program that downloads YouTube videos of a singer, extracts audio, cuts segments, and merges them into a single mashup file.

## Requirements

### Program Functionality
1. Download N videos of a specified singer from YouTube (N > 10)
2. Convert all videos to audio format
3. Cut the first Y seconds from each audio file (Y > 20)
4. Merge all audio clips into a single output file

### Command Line Usage
```bash
python 102303862.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>
```

**Example:**
```bash
python 102303862.py "Sharry Maan" 20 20 102303862-output.mp3
```

### Input Validation
The program must check for:
- Correct number of parameters (4 required)
- NumberOfVideos > 10
- AudioDuration > 20
- Appropriate error messages for invalid inputs
- Exception handling

## Setup & Installation

### Prerequisites
1. Python 3.7 or higher
2. FFmpeg (for audio processing)

### Install Dependencies
```bash
pip install yt-dlp pydub
```

### Install FFmpeg
- **Ubuntu/Debian:** `sudo apt install ffmpeg`
- **macOS:** `brew install ffmpeg`
- **Windows:** Download from ffmpeg.org and add to PATH

## How It Works

1. **Search & Download:** Searches YouTube for the singer and downloads N videos
2. **Convert:** Extracts audio from each video file
3. **Cut:** Takes the first Y seconds from each audio
4. **Merge:** Combines all clips into one final mashup file
5. **Cleanup:** Removes temporary files

## Technologies Used

- **yt-dlp** (from pypi.org) - YouTube video downloading
- **pydub** (from pypi.org) - Audio processing, cutting, and merging
- **Python sys** - Command-line argument handling
- **Python os/shutil** - File management

## Sample Output

```
Configuration:
  Singer: Sharry Maan
  Number of videos: 20
  Audio duration per clip: 20 seconds
  Output file: 102303862-output.mp3

[1/4] Downloading videos...
[2/4] Converting to audio...
[3/4] Cutting audio clips...
[4/4] Merging clips...

✓ Successfully created mashup: 102303862-output.mp3
```

## Error Handling

- Validates parameter count
- Checks numeric constraints (N > 10, Y > 20)
- Handles download failures
- Manages audio conversion errors
- Provides clear error messages

## Notes

- Requires active internet connection
- Processing time depends on number of videos
- Temporary files are auto-cleaned after completion