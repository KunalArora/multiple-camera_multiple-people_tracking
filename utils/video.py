import logging as log
import cv2 as cv


class MulticamCapture:
    def __init__(self, sources):
        assert sources
        self.captures = []
        self.transforms = []

        try:
            sources = [int(src) for src in sources]
            mode = 'cam'
        except ValueError:
            mode = 'video'

        if mode == 'cam':
            for id in sources:
                log.info('Connection  cam {}'.format(id))
                cap = cv.VideoCapture(int(id))
                cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
                cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
                cap.set(cv.CAP_PROP_FPS, 30)
                cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
                assert cap.isOpened()
                self.captures.append(cap)
        else:
            for video_path in sources:
                log.info('Opening file {}'.format(video_path))
                cap = cv.VideoCapture(video_path)
                assert cap.isOpened()
                self.captures.append(cap)

    def add_transform(self, t):
        self.transforms.append(t)

    def get_frames(self):
        frames = []
        timestamps = []
        for capture in self.captures:
            has_frame, frame = capture.read()
            if has_frame:
                calc_timestamps = [0.0]
                fps = capture.get(cv.CAP_PROP_FPS)
                timestamp = capture.get(cv.CAP_PROP_POS_MSEC)
                calc_timestamps.append(calc_timestamps[-1] + 1000/fps)
                for t in self.transforms:
                    frame = t(frame)
                frames.append(frame)
                timestamps.append(timestamp)

        return len(frames) == len(self.captures), frames, timestamps

    def get_num_sources(self):
        return len(self.captures)

    def get_transforms(self):
        return self.transforms

    def get_source_parameters(self):
        frame_size = []
        fps = []
        for cap in self.captures:
            frame_size.append((int(cap.get(cv.CAP_PROP_FRAME_WIDTH)),
                               int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))
            fps.append(int(cap.get(cv.CAP_PROP_FPS)))
        return frame_size, fps


class NormalizerCLAHE:
    def __init__(self, clip_limit=.5, tile_size=16):
        self.clahe = cv.createCLAHE(clipLimit=clip_limit,
                                    tileGridSize=(tile_size, tile_size))

    def __call__(self, frame):
        for i in range(frame.shape[2]):
            frame[:, :, i] = self.clahe.apply(frame[:, :, i])
        return frame
