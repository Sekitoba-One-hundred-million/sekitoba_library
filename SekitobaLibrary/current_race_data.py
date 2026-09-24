import numpy as np

from SekitobaLibrary.constants import *
import SekitobaLibrary.feature_value as fv

CHANGE_CURRENT_KEY_DATA = {}
CHANGE_CURRENT_KEY_DATA["日付"] = "day"
CHANGE_CURRENT_KEY_DATA["天気"] = "weather"
CHANGE_CURRENT_KEY_DATA["開催"] = "held"
CHANGE_CURRENT_KEY_DATA["R"] = "race_num"
CHANGE_CURRENT_KEY_DATA["レース名"] = "race_name"
CHANGE_CURRENT_KEY_DATA["頭数"] = "all_horce_nunm"
CHANGE_CURRENT_KEY_DATA["枠番"] = "flame_number"
CHANGE_CURRENT_KEY_DATA["馬番"] = "horce_number"
CHANGE_CURRENT_KEY_DATA["オッズ"] = "odds"
CHANGE_CURRENT_KEY_DATA["人気"] = "popular"
CHANGE_CURRENT_KEY_DATA["着順"] = "rank"
CHANGE_CURRENT_KEY_DATA["騎手"] = "jockey"
CHANGE_CURRENT_KEY_DATA["斤量"] = "burden_weight"
CHANGE_CURRENT_KEY_DATA["距離"] = "dist"
CHANGE_CURRENT_KEY_DATA["馬場"] = "baba"
CHANGE_CURRENT_KEY_DATA["馬場指数"] = "baba_index"
CHANGE_CURRENT_KEY_DATA["タイム指数"] = "time_index"
CHANGE_CURRENT_KEY_DATA["タイム"] = "time"
CHANGE_CURRENT_KEY_DATA["着差"] = "diff"
CHANGE_CURRENT_KEY_DATA["通過"] = "passing_rank"
CHANGE_CURRENT_KEY_DATA["ペース"] = "pace"
CHANGE_CURRENT_KEY_DATA["上り"] = "up3"
CHANGE_CURRENT_KEY_DATA["馬体重"] = "weight"
CHANGE_CURRENT_KEY_DATA["賞金"] = "money"


class CurrentData:
    def __init__(self, data):
        self.race_data = data
        self.dev_odds = escapeValue
        self.dev_popular = escapeValue

    def setting_odds(self, odds):
        self.dev_odds = odds

    def setting_popular(self, popular):
        self.dev_popular = popular

    def place(self):  # 場所
        try:
            return fv.place_num(self.race_data["held"])
        except:
            return escapeValue

    def all_horce_num(self):
        try:
            return fv.data_check(self.race_data["all_horce_nunm"])
        except:
            return escapeValue

    def flame_number(self):  # 枠番
        try:
            return fv.data_check(self.race_data["flame_number"])
        except:
            return escapeValue

    def horce_number(self):  # 馬番
        try:
            return fv.data_check(self.race_data["horce_number"])
        except:
            return escapeValue

    def weight(self):
        try:
            return float(self.race_data["weight"].split("(")[0])
        except:
            return escapeValue

    def id_weight(self):  # 馬体重の増減
        try:
            return fv.weight(self.race_data["weight"])
        except:
            return escapeValue

    def weather(self):  # 天気
        try:
            return fv.weather(self.race_data["weather"])
        except:
            return escapeValue

    def rank(self):
        try:
            return fv.data_check(self.race_data["rank"])
        except:
            return escapeValue

    def popular(self):
        if self.dev_popular == escapeValue:
            try:
                return fv.data_check(self.race_data["popular"])
            except:
                return escapeValue

        return self.dev_popular

    def race_num(self):
        try:
            return fv.data_check(self.race_data["race_num"])
        except:
            return escapeValue

    def diff(self):
        try:
            return fv.data_check(self.race_data["diff"])
        except:
            return escapeValue

    def odds(self):
        if self.dev_odds == escapeValue:
            try:
                return fv.data_check(self.race_data["odds"])
            except:
                return escapeValue

        return self.dev_odds

    def up_time(self):
        try:
            return fv.data_check(self.race_data["up3"])
        except:
            return escapeValue

    def money(self):
        try:
            return fv.data_check(self.race_data["money"])
        except:
            return escapeValue

    def passing_rank(self):
        try:
            return self.race_data["passing_rank"]
        except:
            return ""

    def first_last_diff(self):
        first = -1
        last = -1

        try:
            split_rank = self.passing_rank().split("-")
            first = int(split_rank[0])
            last = int(split_rank[-1])
        except:
            return escapeValue

        return first - last

    def first_result_diff(self):
        first = -1

        try:
            split_rank = self.passing_rank().split("-")
            first = int(split_rank[0])
        except:
            return escapeValue

        return first - self.rank()

    def last_result_diff(self):
        last = -1

        try:
            split_rank = self.passing_rank().split("-")
            last = int(split_rank[-1])
        except:
            return escapeValue

        return last - self.rank()

    def pace(self):
        try:
            data = self.race_data["pace"].split("-")
            return float(data[0]), float(data[1])
        except:
            return escapeValue, escapeValue

    def birthday(self):
        try:
            return self.race_data["day"]
        except:
            return ""

    def ymd(self):
        try:
            return self.race_data["day"].split("/")
        except:
            return []

    def year(self):
        try:
            y = self.birthday().split("/")
            return int(y[0])
        except:
            return escapeValue

    def dist(self):  # 距離(kmで表す)
        str_dist = ""

        try:
            str_dist = self.race_data["dist"]
        except:
            return escapeValue

        str_math_dist = ""
        d = 0.0

        for i in range(0, len(str_dist)):
            if str.isdecimal(str_dist[i]):
                str_math_dist += str_dist[i]

        if not len(str_math_dist) == 0:
            d = float(str_math_dist) / 1000

        return d

    def key_dist(self):
        try:
            return self.race_data["dist"]
        except:
            return ""

    def baba_status(self):  # 馬場状態
        try:
            return fv.baba(self.race_data["baba"])
        except:
            return escapeValue

    def burden_weight(self):  # 斤量
        try:
            return fv.data_check(self.race_data["burden_weight"])
        except:
            return escapeValue

    def race_kind(self):
        try:
            _, t = fv.dist(self.race_data["dist"])
            return t
        except:
            return escapeValue

    def dist_kind(self):
        try:
            d, _ = fv.dist(self.race_data["dist"])
            return d
        except:
            return escapeValue

    def jockey_name_get(self):
        try:
            return self.race_data["jockey"].replace(" ", "")
        except:
            return ""

    def race_id(self):
        result = ""
        day = ""
        num = ""
        birthday = self.birthday()

        if len(birthday) == 0:
            return ""

        year = birthday.split("/")[0]
        race_place_num = str(int(self.place()))
        str_held = ""

        try:
            str_held = self.race_data["held"]
        except:
            return ""

        s = ""
        str_list = []

        for n in str_held:
            if n.isdecimal():
                s += n
            elif not len(s) == 0:
                str_list.append(s)
                s = ""

        if not len(s) == 0:
            str_list.append(s)

        if not len(str_list) == 2:
            return result

        if len(str_list[0]) == 1:
            day = "0" + str_list[0]
        else:
            day = str_list[0]

        if len(str_list[1]) == 1:
            num = "0" + str_list[1]
        else:
            num = str_list[1]

        if len(race_place_num) == 1:
            race_place_num = "0" + race_place_num

        race_num = str(int(self.race_num()))

        if len(race_num) == 1:
            race_num = "0" + race_num

        result = year + race_place_num + day + num + race_num

        return result

    def jockey_data(self, jockey_data_stprage):
        err_result = [escapeValue] * 5
        jockey_name = self.jockey_name_get()

        if len(jockey_name) == 0:
            return err_result

        year = ""
        before_year = ""

        if self.year() == escapeValue:
            return err_result

        year = str(self.year())
        before_year = str(int(year) - 1)
        current_jockey = {}

        try:
            current_jockey = jockey_data_stprage[jockey_name]
        except:
            return err_result

        result = np.zeros(5)

        try:
            result = np.array(current_jockey[before_year])
        except:
            return err_result

        return result

    def race_time(self):
        try:
            return fv.time(self.race_data["time"]) * 60
        except:
            return escapeValue

    def speed(self):
        race_time = self.race_time()

        if race_time == escapeValue:
            return escapeValue

        dist = self.dist()

        return race_time / dist

    def race_check(self):
        if self.popular() == escapeValue:
            return False
        elif self.place() == escapeValue:
            return False
        elif not self.race_kind() == 1 and not self.race_kind() == 2:
            return False
        elif self.rank() == escapeValue:
            return False
        elif len(self.ymd()) == 0:
            return False

        return True

    def new_check(self):
        race_name = ""
        check = False

        try:
            race_name = self.race_data["race_name"]
        except:
            return check

        word = "新馬"
        count = 0

        for i in range(0, len(race_name)):
            if count != 2 and word[count] == race_name[i]:
                count += 1

        if count == 2:
            check = True

        return check
