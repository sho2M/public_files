# ardupilotのログbinファイルをcsvファイルに変換したものに適用する。

from datetime import datetime, timedelta
import sys 
import csv


label_keywords = {
    'timestamp':'日にち・時刻',
    'TimeUS':'システムが起動してからの経過時間',
    # GPS
    'Status':'GPSの修正タイプ',
    'GMS':'GPS週の開始以来ミリ秒',
    'GWk':'1980年1月5日から何週間経っているか',
    'NSats':'取得した衛生の数',
    'HDop':'水平精度',
    'Lat':'緯度[deg]',
    'Lng':'経度[deg]',
    'Alt':'高度[mm]',
    'Spd':'地上速度[m/s]',
    'GCrs':'地域',
    'VZ':'垂直速度[m/s]',
    'Yaw':'ドローンのYaw',
    # IMU
    'GyrX':'X軸に関する回転速度[rad/s]',
    'GyrY':'Y軸に関する回転速度[rad/s]',
    'GyrZ':'Z軸に関する回転速度[rad/s]',
    'AccX':'X軸に関する加速度[m/s^2]',
    'AccY':'Y軸に関する加速度[m/s^2]',
    'AccZ':'Z軸に関する加速度[m/s^2]',
    'EG':'ジャイロスコープエラーエンカウント',
    'EA':'加速度計エラーエンカウント',
    'T':'IMUの温度',
    'GH':'ジャイロスコープの健康状態',
    'AH':'加速度計の健康状態',
    'GHz':'ジャイロスコープが測定を行う周波数',
    'AHz':'加速度計が測定を行う周波数'
}

def format_csv(csv_file_path):
    
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
        # csvファイルの数値データに行う処理
        for row in rows:
            try:
                # timestampを見やすく変換 日本時間に変換するために9時間足している あとcsv内のデータはすべてstring
                row[0] = str(datetime.utcfromtimestamp(float(row[0])) + timedelta(hours=9))  
            
                # TimeUSをわかりやすく秒に変換
                row[1] = str(round(float(row[1]) / 1000000, 3)) + "[sec]"
            
            except ValueError:  # 文字以外の場合はスキップ
                pass   
        
        # csvのラベルをわかりやすく変更
        for index,cell in enumerate(rows[0]):
            for key in label_keywords:
                if cell == key:
                    rows[0][index] = label_keywords[key]
                    break    
        
        # csvを書き出す処理
        writer = csv.writer(sys.stdout)  # オブジェクト作成
        writer.writerows(rows)  # 変換後のlistをcsvにて書き出し
        
if __name__ == "__main__":
    if len(sys.argv) != 2:  # 実行時に変換したいcsvファイルを指定しなかったとき
        print("Usage: python formatting_csv.py input_file_name > output_file_name")
        sys.exit(1)
        
    csv_file_path = sys.argv[1]
    format_csv(csv_file_path)
    
        
        