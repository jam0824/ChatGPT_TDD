import re
import sys

class ConvertTop:
    def get_time(self, input_string):
        # 時間を抽出する正規表現
        time_pattern = r"\b(\d{2}:\d{2}:\d{2})\b"
        # 稼働時間を抽出するための正規表現（"up 6 min" および "up  2:37" の両方に対応）
        uptime_pattern = r"up\s+((\d+):)?(\d+)( min)?,"

        # 時間を検索して抽出
        time_match = re.search(time_pattern, input_string)
        if time_match:
            time = time_match.group(1)
        else:
            time = "00:00:00"  # 時間が見つからない場合のデフォルト値

        # 稼働時間を検索して抽出
        uptime_match = re.search(uptime_pattern, input_string)
        if uptime_match:
            uptime_hours = int(uptime_match.group(2)) if uptime_match.group(2) else 0
            uptime_minutes = int(uptime_match.group(3))
            uptime_formatted = f"{uptime_hours:02}:{uptime_minutes:02}"
        else:
            uptime_formatted = "00:00"  # 稼働時間が見つからない場合のデフォルト値

        return [time, uptime_formatted]
    
    def get_cpu(self,string):
        US_INDEX = 0
        SY_INDEX = 1
        NI_INDEX = 2
        parts = string.split(',')
        # Extract the 'us', 'sy', and 'ni' values
        us = parts[US_INDEX].split()[1]
        sy = parts[SY_INDEX].strip().split()[0]
        ni = parts[NI_INDEX].strip().split()[0]

        return [us, sy, ni]
    
    def get_mem(self, mem_info):
        # 文字列から必要な値を抽出
        parts = mem_info.split(',')
        total = int(parts[0].split()[3])
        used = int(parts[2].strip().split()[0])  # 'used' 値を正しく取得

        # パーセンテージを計算
        used_percentage = (used / total) * 100

        # 小数第一位で四捨五入し、改行文字を加える
        formatted_percentage = f"{used_percentage:.1f}\n"

        return [formatted_percentage]
    
    def get_data(self, string):
        # 入力された文字列に応じて適切なメソッドを呼び出す
        if string.startswith("top"):
            return self.get_time(string)
        elif string.startswith("%Cpu(s)"):
            return self.get_cpu(string)
        elif string.startswith("KiB Mem"):
            return self.get_mem(string)
        else:
            return []
        
    def get_top_all(self, string_array):
        # 保存用の文字列配列
        saved_strings = []

        # 配列を1つずつ順次読み込む
        for string in string_array:
            # get_dataメソッドを呼び出す
            returned_strings = self.get_data(string)

            # get_dataから帰ってきた文字列配列が空ではない場合、保存用の文字列配列にextendする
            if returned_strings:
                saved_strings.extend(returned_strings)

        # 保存用の文字列配列を返す
        return saved_strings
    
    def convert_csv(self, string_array):
        # 改行文字がある場合はそのまま、なければカンマを追加する
        return ''.join(s + (',' if not s.endswith('\n') else '') for s in string_array).strip(',')
    
    def read_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return ["Error: File not found."]
        except Exception as e:
            return [f"Error: {e}"]

    def process_file(self, file_name):
        lines = self.read_file(file_name)

        # Check if the first string in the array contains 'Error'
        if 'Error' in lines[0]:
            print(lines[0])
            sys.exit(1)

        processed_lines = self.get_top_all(lines)
        return self.convert_csv(processed_lines)

