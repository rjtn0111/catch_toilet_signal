import cv2
import torch
import numpy as np
import yt_dlp
from ultralytics import YOLO
import tempfile

# YOLOv10モデルをロード
model = YOLO("yolov10m.pt")

# YouTubeの動画URLを指定
url = 'https://www.youtube.com/watch?v=TUd7JORZeWo&ab_channel=ANNnewsCH'

# yt-dlpで動画の情報を取得
ydl_opts = {
    'format': 'best',
    'quiet': True,
}

# 動画のストリーミングURLを取得
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(url, download=False)
    video_url = info_dict['url']

# OpenCVで動画を読み込み
cap = cv2.VideoCapture(video_url)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # フレームをYOLOv10に渡して推論を実行
    results = model(frame)

    # 推論結果をフレームに描画
    for result in results:
        for det in result.boxes:
            x1, y1, x2, y2 = det.xyxy[0].cpu().numpy()
            conf = det.conf.item()
            cls = int(det.cls.item())
            label = f"{model.names[cls]} {conf:.2f}"
            color = (0, 255, 0)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow('YOLOv10 Object Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()