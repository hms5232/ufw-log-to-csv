# ufw-log-to-csv

## 緣起　Introduction
在啟用[UFW（Uncomplicated Firewall）](https://zh.wikipedia.org/wiki/Uncomplicated_Firewall)後有時候會打開防火牆產生的日誌看看，但看幾次總覺得原生出來的不太容易閱讀或統計之類的，因此動手寫了一個小程式來幫忙轉成csv。

## 需求　Requirements
Python 3.6 以上或更新（Python2使用者可將程式碼中的兩個`, encoding='UTF-8'`刪掉亦可執行和輸出csv）
  
Python 3.6 or or latest version (For Python2, you can delete `, encoding='UTF-8'` from code to execute.)

## 使用說明　Manual
※關於紀錄中各項目代表的意思可參見 https://askubuntu.com/questions/1116145/understanding-ufw-log 。  
請將`ufw_log_to_csv.py`和`ufw.log`放在同個目錄下（可將log複製出來或將`ufw_log_to_csv.py`放進去，推薦前者）後執行：  

    cd [檔案所在位置]
    py ufw_log_to_csv.py  # Windows user
    python3 ufw_log_to_csv.py  # Linux user

之後程式會自己尋找`ufw.log`這個檔案並輸出成`[YYYYMMDD_HHMMSS].csv`（可自行替換程式碼中輸出和輸入的檔名以符合自己需求），如果有不正確的地方請調整設定：編碼為**UTF-8**、資料有標題、分隔符號為**逗號**。

## 已知問題　Known issues
1. 當協定為ICMP時有奇怪的紀錄會破壞整個邏輯，詳細見 [issue4](https://github.com/hms5232/ufw-log-to-csv/issues/4)


## 許可　License
請見 [LICENSE](https://github.com/hms5232/ufw-log-to-csv/blob/master/LICENSE) 頁面。
  
See [LICENSE](https://github.com/hms5232/ufw-log-to-csv/blob/master/LICENSE).
