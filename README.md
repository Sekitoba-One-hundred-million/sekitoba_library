# 赤兎馬ライブラリ
## 説明
赤兎馬の作成で使用するライブラリ  
基本的に共通で使える文字列に対する数値の振り分けなどはここに記載する。  
sekitoba_libraryとsekitoba_data_manageの二つの便利ツールが存在する。

## インストール
```
python setup.py develop
```

## アンインストール
```
python setup.py develop -u
```


## sekitoba_library
### lib.py
様々な計算ツールや共通するチェック機能などが記載されている。  
race_check( file_name, year, day, num, race_place_num )で返されるデータをcurrent_race_data.pyとpast_race_data.pyで使用する。

### feature_value.py
文字列を数値変換するための関数が記載されている。

### current_race_data.py
現レースに関するデータを処理するクラスが記載されている。  
クラスを呼び出す際にrace_checkの第一の返り値を引数として使用する。

### past_race_data.py
過去レースに関するデータを処理するクラスが記載されている。  
クラスを呼び出す際にrace_checkの第二の返り値を引数として使用する。

### connect.py
タイムアウトを加味したhttp通信とChromeDriverを用いた通信の関数が記載されている。  
基本的にスクレイピングで使用する。

### thread_scraping.py
http通信でスクレイピングする際にスレッド処理を行うクラスが記載されている。  
ChromeDriverを用いたものはまだ存在しない。


## sekitoba_data_manage
### s3_data_manage.py
AWSのS3からデータのロードとアップロードを行う関数が記載されている。  
アップロードは同じファイル名が存在する場合上書きされる。  
存在しないファイルをロードする際は*None*が返り値として返ってくる。

### thred_load.py
スレッド処理を用いて高速で複数のファイルをロードするクラスが記載されている。  
複数のファイルをS3からロードする際に使用する。(2,3個なら普通にロードした方が楽)  
最初にロードする全てのファイルをセットする。最初に呼び出す際にデータのロードが行われる。  
セットし忘れたファイル名でgetを行った際も存在するファイルならばロードしてくれる。

```
import sekitoba_data_manage as dm
dm.dl.file_set( file_name1 )
dm.dl.file_set( file_name2 )
dm.dl.file_set( file_name3 )
dm.dl.file_set( file_name4 )

data1 = dm.dl.data_get( file_name1 )
data2 = dm.dl.data_get( file_name2 )
```

### data_name.py
学習データを作成する際に使用するクラスが記載されている。  
appendで使用するデータの説明を投入してwriteで記載を行い出力する。  
データの順番も一緒に記載されるので学習データを作成する際は使用した方があとでわかりやすい。

```
import sekitoba_data_manage as dm

t_list = []
dm.dn.append( t_list, data1, "データの説明1" )
dm.dn.append( t_list, data2, "データの説明2" )
dm.dn.append( t_list, data3, "データの説明3" )

dm.dn.write( file_name )
```
