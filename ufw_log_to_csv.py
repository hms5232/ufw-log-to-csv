#!/usr/bin/python3
# file encoding=utf-8

"""
author: hms5232
source code on https://github.com/hms5232/ufw-log-to-csv
Contact, report bugs or ask questions: https://github.com/hms5232/ufw-log-to-csv/issues

Windows users can download .exe file on https://github.com/hms5232/ufw-log-to-csv/releases
"""


import datetime
import csv


def main():
	# TODO: 將路徑及檔案名稱放在這邊做成變數方便使用者修改使用
	# try...expect...finally...
	# 用 with 資源會自動釋放
	# ※※ >>>  ↓↓↓↓↓↓↓ change input filename or path here if you want <<< ※※
	with open('ufw.log', 'r', encoding='UTF-8') as f:
		ufw_logs = f.readlines()  # 逐行讀取並存入 list
		now_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # 取得現在時間並格式化
		# ※※ >>>  ↓↓↓↓↓↓↓↓↓↓↓ change output filename or path here if you want <<< ※※
		# 為了讓換行字元可以被正確解析，需要加上 newline='' 參數
		with open("ufw"+now_time+".csv", 'a', encoding='UTF-8', newline='') as o:  # o of "output"
			csv_title = '"月","日","時間","主機名稱","kernel 時間","動作","IN","OUT","MAC", "來自(src)", "DST", "LEN","TOS","PREC","TTL","ID","協定(PROTO)","來源埠(SPT)","DPT","WINDOW","RES","Control Bits / flags","URGP"\n'

			# You can change order of fieldnames here
			fieldnames = ['月', '日', '時間', '主機名稱', 'kernel 時間', '動作', 'IN', 'OUT', 'MAC', 'SRC', 'DST', 'LEN', 'TOS', 'PREC', 'TTL', 'ID', 'DF', 'PROTO', 'SPT', 'DPT', 'WINDOW', 'RES', 'Control Bits / flags', 'URGP', 'TC', 'HOPLIMIT', 'FLOWLBL', 'TYPE', 'CODE', 'SEQ', 'MTU', 'MARK', '??']  # 欄位名稱
			writer = csv.DictWriter(o, fieldnames=fieldnames)
			writer.writeheader()  # 寫入標題

			# 讀取每一筆紀錄
			for i in range(len(ufw_logs)):
				record = dict()
				print("正在處理第", i+1, "筆紀錄...", end='\r')
				# 時間
				record['月'] = ufw_logs[i][0:3]
				record['日'] = ufw_logs[i][4:6]
				record['時間'] = ufw_logs[i][7:16]
				# kernel 名稱
				record['主機名稱'] = get_kernel_name(ufw_logs[i])
				# 剩下的部份
				for j in get_expect_time(ufw_logs[i]).items():
					record[j[0]] = j[1]

				try:
					writer.writerow(record)  # 寫入一列
				except ValueError:
					print()  # 避免第幾筆紀錄的輸出被覆蓋掉
					print("紀錄中出現了程式碼中沒有的欄位！請複製錯誤紀錄及該筆原始 log 發起 issue 或自行更新後發 Pull request。\n")
					print("\thttps://github.com/hms5232/ufw-log-to-csv/issues")
					print("\n===== 以下錯誤紀錄 =====\n")
					raise
				except:
					raise

			print(end='\n\n')  # 讓之前 print 出來的東西不會被覆蓋（\r\n）順便排版


# 抓取 kernel 之後的部分
def get_expect_time(log_string):
	log_string = log_string[16:]  # 把前面已經擷取的時間部分切掉
	after_time_dict = dict()  # kernel 之後的部分
	which_brackets = 1  # 第幾個中括號的資料囉

	# 先抓中括號的部份
	while log_string.find('[') != -1:  # 這筆紀錄中括號的部份還沒抓完
		# Re:從零開始
		starttag = 0
		endtag = 0
		if log_string.find('[') != -1:  # 先抓有[]的
			starttag = log_string.find('[')
			endtag = log_string.find(']')
			# 抓取內容
			if which_brackets == 1:
				after_time_dict['kernel 時間'] = log_string[starttag+1:endtag]
			elif which_brackets == 2:
				after_time_dict['動作'] = log_string[starttag+1:endtag]
			else:  # 以防萬一我也不知道會不會哪天更新就多一個中括號的項目
				after_time_dict['??'] = log_string[starttag+1:endtag]
			which_brackets += 1
			log_string = log_string[endtag+1:]  # 去掉]後從空格開始
	log_string = log_string[1:]  # 去掉開頭空格

	# 中括號（方括號）抓完後 split 以空格為分隔符號切割剩下的字串
	# 逐一放入字典
	for i in get_after_brackets(log_string).items():
		after_time_dict[i[0]] = i[1]

	return after_time_dict


# 擷取 kernel 的名字
def get_kernel_name(log_string):
	kernel_name = ''
	kernel_tag = 0
	if log_string.find('kernel') != -1:
		kernel_name = log_string[16:log_string.find('kernel')]
	return kernel_name


# 抓取中括號之後的部份並切割處理
def get_after_brackets(log_string):
	log_list = log_string.split(' ')  # 用空格去分割紀錄個每個項目
	log_list.remove('\n')  # 檔案裡面有換行符號先移除掉
	log_dict = dict()  # 這筆紀錄中方括號後面分割好的部份
	orig_log_list = log_list.copy()  # 複製請加上 copy 否則 reference 會指向同一個位址

	for i in orig_log_list:  # 處理每一個項目
		# 用等號分割
		log_item = i.split('=')  # 個別項目內容的 list
		if len(log_item) == 2:  # 有等號
			# 將等號前作為 key ，等號後作為 value
			log_dict[log_item[0]] = log_item[1]
		else:  # 沒等號
			# 直接給定 key 後設定 value
			# Control Bits / flags 另外處理不在這邊弄
			if log_item[0] == 'DF':
				log_dict['DF'] = '＊'
			else:
				if not 'DF' in log_dict:  # 避免前面已經加上＊被覆蓋
					log_dict['DF'] = ''  # 避免找不到 key 的問題
				# 除此之外大概就是 Control Bits / flags 的部份，直接跳過不移除
				continue
		log_list.remove(i)  # 跑完之後就移除項目

	# 處理 Control Bits / flags
	if len(log_list) > 0:  # 理論上剩下 Control Bits / flags
		control_flag = ''  # 全部的 Control Bits / flags
		for j in log_list:
			control_flag = control_flag + j + ' '
		log_dict['Control Bits / flags'] = control_flag
	return log_dict


if __name__ == '__main__':
	main()
