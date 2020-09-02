# Multi Camera Multi Person Python Demo

This demo demonstrates how to run Multi Camera Multi Person demo using OpenVINO<sup>TM</sup>.

## Run the following command line after switching into the cloned directory 

```
python multi_camera_multi_person_tracking.py \
    -i datasets/HallWayTracking/videos/001.avi datasets/HallWayTracking/videos/002.avi datasets/HallWayTracking/videos/005.avi \
    -m model/intel/person-detection-retail-0013/FP32-INT8/person-detection-retail-0013.xml \
    --m_reid model/intel/person-reidentification-retail-0031/FP32-INT8/person-reidentification-retail-0031.xml \
    --config config.py

```

## How It Works

The demo expects the next models in the Intermediate Representation (IR) format:

   * Person detection model (or person instance segmentation model)
   * Person re-identification model

As input, the demo application takes:
* paths to several video files specified with a command line argument `--videos`
* indexes of web cameras specified with a command line argument `--cam_ids`

The demo workflow is the following:

1. The demo application reads tuples of frames from web cameras/videos one by one.
For each frame in tuple it runs person detector
and then for each detected object it extracts embeddings using re-identification model.
2. All embeddings are passed to tracker which assigns an ID to each object.
3. The demo visualizes the resulting bounding boxes and unique object IDs assigned during tracking.

## Running

### Installation of dependencies

To install required dependencies run

```bash
pip3 install -r requirements.txt
```

### Command line arguments
```
Minimum command examples to run the demo:

```
# videos
python multi_camera_multi_person_tracking.py \
    -i path/to/video_1.avi path/to/video_2.avi \
    --m_detector path/to/person-detection-retail-0013.xml \
    --m_reid path/to/person-reidentification-retail-0103.xml \
    --config config.py

# web-cameras
python multi_camera_multi_person_tracking.py \
    -i 0 1 \
    --m_detector path/to/person-detection-retail-0013.xml \
    --m_reid path/to/person-reidentification-retail-0103.xml \
    --config config.py
```

<!-- # videos with instance segmentation model
python multi_camera_multi_person_tracking.py \
    -i path/to/video_1.avi path/to/video_2.avi \
    --m_segmentation path/to/instance-segmentation-security-0050.xml \
    --m_reid path/to/person-reidentification-retail-0107.xml \
    --config config.py
 -->
<!-- The demo can use a JSON file with detections instead of a person detector.
The structure of this file should be as follows:
```json
[
    [  # Source#0
        {
            "frame_id": 0,
            "boxes": [[x0, y0, x1, y1], [x0, y0, x1, y1], ...],  # N bounding boxes
            "scores": [score0, score1, ...],  # N scores
        },
        {
            "frame_id": 1,
            "boxes": [[x0, y0, x1, y1], [x0, y0, x1, y1], ...],
            "scores": [score0, score1, ...],
        },
        ...
    ],
    [  # Source#1
        {
            "frame_id": 0,
            "boxes": [[x0, y0, x1, y1], [x0, y0, x1, y1], ...],  # N bounding boxes
            "scores": [score0, score1, ...],  # N scores
        },
        {
            "frame_id": 1,
            "boxes": [[x0, y0, x1, y1], [x0, y0, x1, y1], ...],
            "scores": [score0, score1, ...],
        },
        ...
    ],
    ...
]
```
Such file with detections can be saved from the demo. Specify the argument
`--save_detections` with path to an output file.
 -->
## Demo Output

The demo displays bounding boxes of tracked objects and unique IDs of those objects.
To save output video with the result please use the option  `--output_video`,
to change configuration parameters please open the `config.py` file and edit it.

Also demo can dump resulting tracks to a json file. To specify the file use the
`--history_file` argument.

## Quality measuring

The demo provides tools for measure quality of the multi camera multi person tracker:
* Evaluation MOT metrics
* Visualize the demo results from a history file

For MOT metrics evaluation we use [py-motmetrics](https://github.com/cheind/py-motmetrics) module.
It is necessary to have ground truth annotation file for the evaluation.
The annotation must includes the following labels and attributes:
```json
[
  {
    "frame_id": 0,
    "attributes": [
      {
        "id": 0,
        "name": "bbox",
        "type": "person",
        "values": [345,210,178,70]
      },
      {
        "id": 1,
        "name": "bbox",
        "type": "person",
        "values": [124,567,165,100]
      }
    ]
  }
]
```

To run evaluation MOT metrics use the following command:
```bash
python run_evaluate.py \
    --history_file path/to/history/file.json \
    --gt_files \
      path/to/ground/truth/annotation/for/source_0.xml \
      path/to/ground/truth/annotation/for/source_1.xml \
```
Number of ground truth files depends on the number of used video sources.

For the visualization of the demo results please use the next command:
```
python run_history_visualize.py \
    -i path/to/video_1.avi path/to/video_2.avi \
    --history_file path/to/history/file.json \
```
This a minimum arguments set for the script. To show all available arguments
run the command:

## Process analysis

During the demo execution are available two options for analysis the process:
1. Visualize distances between embeddings that are criterion for matching tracks.
2. Save and visualize embeddings.

By default these options are disabled.
To enable the first one please set in configuration file for `analyzer` parameter
`enable` to `True`, for the second one for `embeddings` specify parameter `path`
that is a directory where data related to embeddings will be saved
(if it is an empty string the option is disabled). In `embeddings` is a parameter
`use_images`. If it is `True` for every embedding will be drawn an image with a person
instead a point.
