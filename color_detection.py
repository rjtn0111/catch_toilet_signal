# color_detection.py
import cv2
import numpy as np
import yt_dlp
import time
from datetime import datetime

def detect_color_change(url, monitor_area, color_change_threshold=50, min_change_for_notification=20, show=True):
	# yt-dlpで動画のストリーミングURLを取得
	ydl_opts = {
		'format': 'best',
		'quiet': True,
	}

	try:
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			info_dict = ydl.extract_info(url, download=False)
			video_url = info_dict['url']
	except Exception as e:
		print(f"動画の取得に失敗しました: {e}")
		return

	# OpenCVで動画を読み込み
	cap = cv2.VideoCapture(video_url)
	# 初期の基準色
	initial_color = None
	previous_color_diff = 0

	# フレーム処理
	try:
		while cap.isOpened():
			ret, frame = cap.read()
			if not ret:
				print("フレームの取得に失敗しました。接続を再試行します。")
				break

			# 監視エリアの色を取得
			x, y, w, h = monitor_area
			area = frame[y:y+h, x:x+w]
			avg_color = cv2.mean(area)[:3]  # BGRの平均値を取得

			# 初期色を設定
			if initial_color is None:
				initial_color = avg_color
				print(f"初期色: {initial_color}")

			# 色の変化を計算
			color_diff = np.sqrt(np.sum((np.array(avg_color) - np.array(initial_color)) ** 2))

			# 初期色の時cntの初期化
			if color_diff < 20:
				cnt = 0

			# 変化が閾値を超えたら通知
			if color_diff > color_change_threshold:
				if cnt == 0:
					current_datetime = datetime.now()
				if abs(color_diff - previous_color_diff) < min_change_for_notification: # 前回のcolor_diffと比べて変化が少なかった場合cntをあげる（色の安定化check）
					cnt += 1
					if cnt == 5:
						print("色の変化を検出しました！通知を送信します。")
						print(f"色変化量: {color_diff}")
						print(f"color: {ave_color}")
						print("検知した日時:", current_datetime)

			# color_diffの保持
			previous_color_diff = color_diff

			# 監視エリアの枠を表示
			if show:
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				cv2.imshow('Color Change Detection', frame)

				# 'q'キーで終了
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break

			# 処理速度の調整
			time.sleep(0.5)

	except KeyboardInterrupt:
		print("プログラムを終了します。")

	cap.release()
	if show:
		cv2.destroyAllWindows()
