#! /user/bin/env python3.5

import argparse
import random
import numpy as np
import moviepy.editor as moved


def parse_args():
    desc = "Random movie slicer."
    parser = argparse.ArgumentParser(
        description=desc,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--duration', '-d', help='', default=30, type=float)
    parser.add_argument('--seconds-per-clip', '-s', help='', default=1,
                        type=float)
    parser.add_argument('--output', '-o', help='output.avi', default=1, type=str)
    parser.add_argument('--shuffle', action='store_true')
    parser.add_argument('input_vid_file_names', nargs='+', help='', type=str)

    return parser.parse_args()

if __name__ == '__main__':

    # parse the args
    args = parse_args()

    input_vids = [moved.VideoFileClip(vid_file)
                  for vid_file in args.input_vid_file_names]
    min_resolution = min((vid.w, vid.h) for vid in input_vids)
    print('min_resolution: {}'.format(min_resolution))

    # get number of clips per video
    segments_per_input_vid = int(args.duration /
                                 len(args.input_vid_file_names) /
                                 args.seconds_per_clip
                                 + 2)  # since we skip the first/last segments

    # for input_vid in input vids, grab a random segment and append to movie
    # being created
    all_clips = []
    for vid in input_vids:

        # break into evenly sized chunks
        # vid = moved.VideoFileClip(input_vid_file)
        segment_interval_size = int(vid.duration) / segments_per_input_vid
        segment_intervals = [(i*segment_interval_size + 1,
                              (i + 1)*segment_interval_size)
                             for i in range(segments_per_input_vid)][1:-1]

        for start, end in segment_intervals:
            clip_start = start + random.random() * (segment_interval_size - 1)
            clip_end = clip_start + args.seconds_per_clip
            all_clips.append(vid.subclip(clip_start, min(clip_end, vid.duration)).resize(min_resolution))
            print('.', end='', flush=True)

    if args.shuffle:
        np.random.shuffle(all_clips)

    final_clip = moved.concatenate_videoclips(all_clips)
    final_clip.write_videofile("myHolidays_edited_2.avi",fps=24, codec='mpeg4')
