random_seed = 100

mct_config = dict(
    time_window=20,
    global_match_thresh=0.2,
    bbox_min_aspect_ratio=1.2 # The less the better performance in terms of people detection
)

sct_config = dict(
    time_window=10,
    continue_time_thresh=2, # This is the time after which we continue the tracking of person
    track_clear_thresh=3000,
    match_threshold=0.25, # This is the threshold that two people match in different frames
    merge_thresh=0.15,
    n_clusters=4,
    max_bbox_velocity=0.2, # This is the velocity by which a person is moving and shifting
    detection_occlusion_thresh=0.7, # This is the occlusion threshold, when to merge two objects together 
    track_detection_iou_thresh=0.5,
    process_curr_features_number=0,
    interpolate_time_thresh=10,
    detection_filter_speed=0.6,
    rectify_thresh=0.1,
    manniquen_thresh=2
)

normalizer_config = dict(
    enabled=False,
    clip_limit=.5,
    tile_size=8
)

visualization_config = dict(
    show_all_detections=True,
    max_window_size=(1920, 1080),
    stack_frames='horizontal'
)

analyzer = dict(
    enable=True,
    show_distances=False,
    save_distances='',
    concatenate_imgs_with_distances=True,
    plot_timeline_freq=0,
    save_timeline='',
    crop_size=(32, 64)
)

embeddings = dict(
    save_path='',
    use_images=True,  # Use it with `analyzer['enable'] = True` to save crops of objects
    step=0  # Equal to subdirectory for `save_path`
)
