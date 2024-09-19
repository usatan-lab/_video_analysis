import cv2
import numpy as np


def process_video(video_path, output_file):
    # 動画の読み込み
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # 背景差分を用いて動きを検出
    fgbg = cv2.createBackgroundSubtractorMOG2()

    # 日記の内容を保存するリスト
    diary_entries = []

    # 動きのメッセージ
    messages = [
        "飼い猫は今日も元気に遊んでいた",
        "飼い猫がソファでくつろいでいる",
        "飼い猫が窓辺で外を眺めている",
    ]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # フレームの前処理
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgmask = fgbg.apply(gray)

        # 動きがある部分を検出
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 500:  # 動きの大きさの閾値
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # 動きに基づいてメッセージを生成
                message = np.random.choice(messages)
                diary_entries.append(f"フレーム {int(cap.get(cv2.CAP_PROP_POS_FRAMES))}: {message}")

        # 結果を表示（デバッグ用）
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # 日記の内容をファイルに保存
    with open(output_file, 'w') as f:
        for entry in diary_entries:
            f.write(f"{entry}\n")

    print(f"Diary entries have been saved to {output_file}")


# 動画ファイルのパスと出力ファイル名を指定
process_video('s_test.MP4', 'diary.txt')