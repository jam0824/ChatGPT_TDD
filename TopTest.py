import unittest
from unittest.mock import patch
import sys

# ConvertTopクラスをインポートします（または実装します）
from ModuleConvertTop import ConvertTop

class TestGetTime(unittest.TestCase):

    def test_get_time(self):
        input_string = "top - 13:52:54 up 6 min,  0 users,  load average: 0.01, 0.07, 0.03"
        expected_result = ["13:52:54", "00:06"]
        # ConvertTopクラスのインスタンスを作成してメソッドを呼び出します
        convert_top_instance = ConvertTop()
        self.assertEqual(convert_top_instance.get_time(input_string), expected_result)

    def test_get_time_additional(self):
        input_string = "top - 00:47:32 up  2:37,  2 users,  load average: 3.01, 1.52, 0.47"
        expected_result = ["00:47:32", "02:37"]
        convert_top_instance = ConvertTop()
        self.assertEqual(convert_top_instance.get_time(input_string), expected_result)

class TestGetCpu(unittest.TestCase):
    def test_get_cpu(self):
        input_string = "%Cpu(s):  16.2 us,  20.3 sy,  5.0 ni,63.5 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st"
        expected_result = ["16.2", "20.3", "5.0"]
        result = ConvertTop().get_cpu(input_string)
        self.assertEqual(result, expected_result)

class TestGetMem(unittest.TestCase):
    def test_get_mem(self):
        test_input = "KiB Mem : 40979980 total, 37696840 free,  1050480 used,  2232660 buff/cache"
        expected_output = ["2.6\n"]
        
        # ConvertTop インスタンスを作成
        converter = ConvertTop()
        
        # get_mem 関数を呼び出して結果を取得
        result = converter.get_mem(test_input)
        
        # 期待される結果と比較
        self.assertEqual(result, expected_output)

    def test_get_mem_with_different_data(self):
        test_input = "KiB Mem : 40979980 total, 37696840 free,  1040480 used,  2232660 buff/cache"
        expected_output = ["2.5\n"]
        
        # ConvertTop インスタンスを作成
        converter = ConvertTop()
        
        # get_mem 関数を呼び出して結果を取得
        result = converter.get_mem(test_input)
        
        # 期待される結果と比較
        self.assertEqual(result, expected_output)

class TestConvertTop(unittest.TestCase):

    @patch('ModuleConvertTop.ConvertTop.get_time', return_value=["13:52:54", "00:06"])
    def test_get_data(self, mock_get_time):
        test_string = "top - 13:52:54 up 6 min,  0 users,  load average: 0.01, 0.07, 0.03"
        result = ConvertTop().get_data(test_string)
        self.assertEqual(result, ["13:52:54", "00:06"])

    @patch('ModuleConvertTop.ConvertTop.get_cpu', return_value=["16.2", "20.3", "5.0"])
    def test_get_cpu(self, mock_get_cpu):
        test_string = "%Cpu(s):  16.2 us,  20.3 sy,  5.0 ni,63.5 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st"
        result = ConvertTop().get_data(test_string)
        self.assertEqual(result, ["16.2", "20.3", "5.0"])

    @patch('ModuleConvertTop.ConvertTop.get_mem', return_value=["2.6\n"])
    def test_get_mem(self, mock_get_mem):
        test_string = "KiB Mem : 40979980 total, 37696840 free,  1050480 used,  2232660 buff/cache"
        result = ConvertTop().get_data(test_string)
        self.assertEqual(result, ["2.6\n"])

    def test_get_other(self):
        test_string = "Tasks:   2 total,   1 running,   1 sleeping,   0 stopped,   0 zombie"
        result = ConvertTop().get_data(test_string)
        self.assertEqual(result, [])
    
    def test_get_blank(self):
        test_string = ""
        result = ConvertTop().get_data(test_string)
        self.assertEqual(result, [])

class TestGetTopAll(unittest.TestCase):
    def test_get_top_all(self):
        test_data = ["top - 13:52:54 up 6 min,  0 users,  load average: 0.01, 0.07, 0.03",
                    "Tasks:   2 total,   1 running,   1 sleeping,   0 stopped,   0 zombie",
                    "",
                    "%Cpu(s):  16.2 us,  20.3 sy,  5.0 ni,63.5 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st",
                    "KiB Mem : 40979980 total, 37696840 free,  1050480 used,  2232660 buff/cache",
                    "",
                    "KiB Swap: 10485760 total, 10485760 free,        0 used. 39463640 avail Mem"]
        expected =  ["13:52:54","00:06","16.2","20.3","5.0","2.6\n"]
        result = ConvertTop().get_top_all(test_data)
        self.assertEqual(result, expected)

class TestConvertCSV(unittest.TestCase):
    def test_convert_csv(self):
        input_data = ["13:52:54", "00:06", "16.2", "20.3", "5.0", "2.6\n", "13:52:54", "00:06", "16.2", "20.3", "5.0", "2.6\n"]
        expected_output = "13:52:54,00:06,16.2,20.3,5.0,2.6\n13:52:54,00:06,16.2,20.3,5.0,2.6\n"
        result = ConvertTop().convert_csv(input_data)
        self.assertEqual(result, expected_output)

class TestReadFile(unittest.TestCase):
    def setUp(self):
        self.convert_top = ConvertTop()

    def test_read_file(self):
        file_name = "test_file.txt"
        expected_result = [
            "top - 13:52:54 up 6 min,  0 users,  load average: 0.01, 0.07, 0.03",
            "Tasks:   2 total,   1 running,   1 sleeping,   0 stopped,   0 zombie",
            "%Cpu(s):  16.2 us,  20.3 sy,  5.0 ni,63.5 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st"
        ]
        result = self.convert_top.read_file(file_name)
        self.assertEqual(result, expected_result)
    
    def test_read_file_not_found(self):
        # ファイルが見つからない場合のテスト
        result = self.convert_top.read_file("nonexistent_file.txt")
        self.assertEqual(result, ["Error: File not found."])

    def test_read_file_general_exception(self):
        # 一般的な例外をテストする
        with patch("builtins.open", side_effect=Exception("General error")):
            result = self.convert_top.read_file("some_file.txt")
            self.assertEqual(result, ["Error: General error"])

class TestProcessFile(unittest.TestCase):
    def test_process_file(self):
        # テストデータと期待される結果を定義
        test_data = "test_file.txt"
        expected_result = "13:52:54,00:06,16.2,20.3,5.0"

        # ConvertTopクラスのインスタンスを作成
        converter = ConvertTop()

        # process_fileメソッドを呼び出して実際の結果を取得
        result = converter.process_file(test_data)

        # 期待される結果と実際の結果を比較
        self.assertEqual(result, expected_result)

    def test_process_file_error(self):
        # テストデータと期待されるエラーメッセージを定義
        test_data = "test_file.txt"
        expected_error_message = "Error: General error"

        # ConvertTopクラスのインスタンスを作成
        converter = ConvertTop()

        # read_fileメソッドをモックしてエラーメッセージを返すように設定
        with patch('ModuleConvertTop.ConvertTop.read_file', return_value=["Error: General error"]):
            # sys.exitが呼ばれることを確認するためのコンテキストマネージャを設定
            with self.assertRaises(SystemExit) as cm:
                # process_fileメソッドを呼び出し、sys.exit(1)が発生することを期待
                converter.process_file(test_data)

            # sys.exitの引数が1であることを確認
            self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()