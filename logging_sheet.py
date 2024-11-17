import gspread
import os

dir_path = os.path.dirname(__file__) # 作業フォルダの取得
credentials_file_path=os.path.join(dir_path, "client_secret.json") # 認証用のJSONファイル
authorized_user_file_path=os.path.join(dir_path, "authorized_user.json") # 証明書の出力ファイル
sheet_url = "https://docs.google.com/spreadsheets/d/1lEYKDamoCxxGrjGxAPgFOCnPAYoEFbt6_kl_lkvmneI/edit?gid=0#gid=0"

row_data = [0, -11, '2023/05/04', '単行書き込み']

def append_row_to_sheet(sheet_url, row_data, credentials_file_path, authorized_user_file_path):
	gc = gspread.oauth(
		credentials_filename=credentials_file_path, # 認証用のJSONファイル
		authorized_user_filename=authorized_user_file_path, # 証明書の出力ファイル
	)

	wb = gc.open_by_url(sheet_url)
	ws = wb.get_worksheet(0)
	ws.append_row(row_data)

# append_row_to_sheet(sheet_url, row_data, credentials_file_path, authorized_user_file_path)
