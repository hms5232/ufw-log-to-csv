#!/usr/bin/python3
# file encoding=utf-8

"""
author: hms5232
source code on https://github.com/hms5232/ufw-log-to-csv
Contact, report bugs or ask questions: https://github.com/hms5232/ufw-log-to-csv/issues

Windows users can download .exe file on https://github.com/hms5232/ufw-log-to-csv/releases
"""


import datetime


def main():
	# try...expect...finally...
	# 用 with 資源會自動釋放
	# TODO: 將路徑及檔案名稱放在這邊做成變數方便使用者修改使用
	# ※※ >>>  ↓↓↓↓↓↓↓ change input filename or path here if you want <<< ※※
	with open('ufw.log', 'r', encoding='UTF-8') as f:
		ufw_logs = f.readlines()  # 逐行讀取並存入 list
		now_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # 取得現在時間並格式化
		# ※※ >>>  ↓↓↓↓↓↓↓↓↓↓↓ change output filename or path here if you want <<< ※※
		with open("ufw"+now_time+".csv", 'a', encoding='UTF-8') as o:  # o of "output"
			# TODO: 改用 csv 模組來做寫入的動作＆import
			csv_title = '"月","日","時間","主機名稱","kernel 時間","動作","IN","OUT","MAC", "來自(src)", "DST", "LEN","TOS","PREC","TTL","ID","協定(PROTO)","來源埠(SPT)","DPT","WINDOW","RES","Control Bits / flags","URGP"\n'
			fieldnames = ['月', '日', '時間', '主機名稱', 'kernel 時間', '動作', 'IN', 'OUT', 'MAC', 'SRC', 'DST', 'LEN', 'TOS', 'PREC', 'TTL', 'ID', 'DF', 'PROTO', 'SPT', 'DPT', 'WINDOW', 'RES', 'Control Bits / flags', 'URGP']  # 欄位名稱
			output = csv_title  # 輸出到 csv 的內容
			csv.DictWriter(o, fieldnames=fieldnames)  # 寫入標題
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
				output = output + get_expect_time(ufw_logs[i])  # TODO: dict

			o.write(output)  # 寫入csv
			print(end='\n\n')  # 讓之前 print 出來的東西不會被覆蓋（\r\n）順便排版


# 抓取 kernel 之後的部分
def get_expect_time(log_string):
	log_string = log_string[16:]  # 把前面已經擷取的時間部分切掉
	result = ''  # 擷取出來的內容
	isDF = False  # 這筆紀錄是否為DF（don't fragment）的判斷
	isUDP = False  # 判斷是不是UDP協定（如果是UDP協定會有些欄位沒有資料）
	while log_string.find('[') != -1:  # 這筆紀錄還沒跑完
		# Re:從零開始
		starttag = 0
		endtag = 0
		if log_string.find('[') != -1:  # 先抓有[]的
			starttag = log_string.find('[')
			endtag = log_string.find(']')
			result = result + '"' + log_string[starttag+1:endtag] + '",'  # TODO: 改用 csv 模組來做寫入的動作
			log_string = log_string[endtag+1:]  # 去掉]後從空格開始
	log_string = log_string[1:]  # 去掉開頭空格
	# 中括號（方括號）抓完後 split 以空格為分隔符號切割剩下的字串
	result = result + get_after_brackets(log_string)  # TODO: 改用 csv 模組來做寫入的動作——改接 dict

	# 	elif log_string.find(' ') != -1:  # 再抓剩下的
	# 		starttag = log_string.find(' ')
	# 		log_string_tmp = log_string[starttag+1:]
	# 		endtag = log_string_tmp.find(' ') + 1
	# 		# 如果是有=的話就只抓=後面的部分
	# 		ptr_equal = log_string[starttag+1:endtag].find('=')
	# 		# 因為在RES之後flag有可能不只一個，所以在RES之後到URGP之間通通抓出來
	# 		isRES = False
	# 		if ptr_equal != -1:  # 有=
	# 			if log_string[starttag+1:ptr_equal+1] == "RES":
	# 				isRES = True
	# 			starttag = log_string.find('=')
	#
	# 		if log_string[starttag+1:endtag] == 'UDP':  # 如果是UDP
	# 			isUDP = True
	#
	# 		if log_string[starttag+1:endtag] == 'DF':  # 如果是DF
	# 			isDF = True
	# 			log_string = log_string[endtag:]  # 保留空格不切掉
	# 			continue
	#
	# 		result = result + '"' + log_string[starttag+1:endtag] + '",'
	#
	# 		log_string = log_string[endtag:]  # 保留空格不切掉
	# 		if isRES:
	# 			# 抓取RES後面剩下的項目到URPG之前(control flags)
	# 			tmp_index = 0
	# 			# 擷取control flags和之後的內容
	# 			tmp = log_string[1:].split(" ")  # 將剩下的字串用空格來分割並放進list
	# 			while True:
	# 				if tmp[tmp_index].find("=") >= 0:  # 如果發現=，代表已經擷取完畢了
	# 					break
	# 				tmp_index += 1
	# 			S = ""
	# 			for s in tmp[:tmp_index]:  # 開始拿出每個control flags
	# 				S += s+"|"
	# 			S = S[:-1]  # 拿掉最後一個|
	# 			result = result + '"' + S + '",'
	# 			# 將剩下的部分依照原本的邏輯處理
	# 			ptr = log_string.find("=")
	# 			while True:
	# 				ptr -= 1
	# 				if log_string[ptr] == " ":
	# 					break
	# 			log_string = log_string[ptr:]
	#
	#
	# if isDF :  # 如果有DF就在最後面加上
	# 	if isUDP:  # 如果是UDP封包則要補齊空出來的欄位
	# 		result = result + '"","","","DF",'  # 補漏洞
	# 	else:
	# 		result = result + '"DF",'  # 一般情況下直接加在最後面即可

	# TODO: return dict
	result = result + '\n'  # 一筆紀錄處理完了記得換行
	return result


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
	log_dict = dict()
	orig_log_list = log_list

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
				log_dict['DF'] = '*'
			else:
				log_dict['DF'] = ''
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
