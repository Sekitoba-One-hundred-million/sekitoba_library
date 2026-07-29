import SekitobaLibrary.lib as lib


class SelectHorce:
    def __init__(self, horce_list, model_key_list, revrse_list, odds_data):
        self.horce_list = horce_list
        self.model_key_list = model_key_list
        self.revrse_list = revrse_list
        self.odds_data = odds_data
        self.index_create()

    def index_create(self):
        for key in self.model_key_list:
            self.horce_list = sorted(self.horce_list, key=lambda x: x[key + "_score"], reverse=key in self.revrse_list)

            for i in range(0, len(self.horce_list)):
                self.horce_list[i][key + "_score_index"] = i + 1

    def exacta(self, base_key):
        get_money = lib.escapeValue
        sort_result = sorted(
            self.horce_list, key=lambda x: x[base_key + "_score"], reverse=base_key in self.revrse_list
        )

        if sort_result[0]["odds"] < 3.5:
            return get_money

        for key in self.model_key_list:
            if sort_result[0][key + "_score_index"] > 2:
                return get_money

        get_money = -1
        one_horce = sort_result[0]
        second_horce = {}
        rank_sort_result = sorted(self.horce_list, key=lambda x: x["rank_score"], reverse=True)

        for i in range(0, len(rank_sort_result)):
            if one_horce["horce_id"] == rank_sort_result[i]["horce_id"]:
                continue

            if int(rank_sort_result[i]["odds"]) < 3.5:
                continue

            second_horce = rank_sort_result[i]
            break

        if one_horce["rank"] == 1 and second_horce["rank"] == 2:
            get_money = self.odds_data["馬単"] / 100

        return get_money
