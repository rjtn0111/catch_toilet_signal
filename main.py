# やること
# 色変化中の安定化
# 接続切れの対策
# スプレットシートへの書き込み機能
# 閾値などのハイパラ調整
# 色の範囲を定める
from color_detection import detect_color_change

# YouTubeの動画URL
url = 'https://www.youtube.com/live/bPh0zpkiu74?si=iypxldiINNlMpaRo'

# 監視エリアの位置とサイズ（例：左上の位置、50x50ピクセル）
monitor_area = (950, 700, 100, 50)  # (x, y, width, height)

# detect_color_change関数を呼び出す
detect_color_change(
    url=url,
    monitor_area=monitor_area,
    color_change_threshold=50,
    min_change_for_notification=20,
    show=False
)
