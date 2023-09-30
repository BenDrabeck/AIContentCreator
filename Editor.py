import random
import os
from moviepy.editor import VideoFileClip, vfx, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.VideoClip import *

def make_video_format1(main_path, bkg_path="SubwaySurfers001.mp4", bkg_cutoff=0.45, main_ypan=0.15):
    # Create clips from file paths
    main_clip = VideoFileClip(main_path)
    bkg_clip = VideoFileClip(bkg_path)

    # Select a random portion of the background clip equal to the length of the main clip
    start = random.randint(0, int(bkg_clip.duration - 1) - int(main_clip.duration))
    bkg_clip = bkg_clip.subclip(start, start + main_clip.duration)

    # Resize the portion of the clip above to match bkg_cutoff
    percent = main_clip.h * bkg_cutoff / bkg_clip.h
    bkg_clip = vfx.resize(bkg_clip, percent)
    
    # Composite clips together and pan main clip by main_ypan parameter
    final = CompositeVideoClip([main_clip.set_position((0, -main_ypan), relative=True),
                                bkg_clip.set_position("bottom")]).set_audio(main_clip.audio)

    # Generate a unique output file name based on the input filename
    filename = os.path.basename(main_path)
    filename_without_extension = os.path.splitext(filename)[0]
    output = f"ready/{filename_without_extension}_processed.mp4"

    # Output file to the dynamically generated destination
    final.write_videofile(output,
                          codec='libx264',
                          audio_codec='aac',
                          temp_audiofile='temp-audio.m4a',
                          remove_temp=True)

def process_all_videos_in_folder(downloaded):
    for filename in os.listdir(downloaded):
        if filename.endswith(".mp4"):
            file_path = os.path.join(downloaded, filename)
            make_video_format1(file_path)

if __name__ == '__main__':
    process_all_videos_in_folder("downloaded")

