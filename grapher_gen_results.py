import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os.path

class Graphs:
    def __init__(self, data_base):
        self.data_base = data_base
    
    def overall_results_per(self):
        correct = self.data_base["correct"].sum() / len(self.data_base)
        wrong = (self.data_base["correct"]==False).sum() / len(self.data_base)
        results = [correct, wrong]
        outcome = (0.30, 0.50)
        fig, ax = plt.subplots()
        ax.grid(axis="y", zorder=0, color="#9698A1")
        width = 0.15 
        bars = ax.bar(outcome, results, width, zorder=3)
        bars[0].set_color('lightseagreen')
        bars[1].set_color('coral')
        ax.set_xticks((0.375, 0.575))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_xticklabels(('Right','Wrong'))
        fig.suptitle("Percentage Right/Wrong", fontsize=15)
        #plt.show()

    def results_per_gen(self):
        grouped = (self.data_base["correct"]==True).groupby(self.data_base["article"])
        correct = grouped.mean()
        incorrect = 1 - grouped.mean()
        gender_track = correct.append(incorrect)
        fig, ax = plt.subplots()
        ind_der = (1, 1.25)
        ind_die = (1.75, 2)
        ind_das = (2.50, 2.75)
        width = 0.25
        ax.grid(axis="y", zorder=0, color="#9698A1")
        bars_der = ax.bar(ind_der, gender_track["der"], width)
        bars_der[0].set_color('lightseagreen')
        bars_der[1].set_color('coral')
        bars_die = ax.bar(ind_die, gender_track["die"], width)
        bars_die[0].set_color('lightseagreen')
        bars_die[1].set_color('coral')
        bars_das = ax.bar(ind_das, gender_track["das"], width)
        bars_das[0].set_color('lightseagreen')
        bars_das[1].set_color('coral')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_xticks((1.25, 2, 2.75))
        ax.set_xticklabels(('der','die', 'das'))
        ax.set_xlim([0.9, 3.1])
        fig.suptitle("Percentage Right/Wrong by Gender", fontsize=15)
        # plt.show()

    def results_per_date(self):
        grouped = (self.data_base["correct"]==True).groupby(self.data_base["date"])
        correct = grouped.mean()
        wrong = 1 - grouped.mean()
        data_date = correct.append(wrong)
        fig, ax = plt.subplots()  
        x_loc = np.array([0, 0.15])
        ax.grid(axis="y", zorder=0, color="#9698A1")
        ticks = []
        dates_played = []
        for date in pd.unique(data_date.index):
            width = 0.15
            x_loc += 0.75
            bars_date = ax.bar(x_loc, data_date[date], width, zorder=3)
            bars_date[0].set_color('lightseagreen')
            bars_date[1].set_color('coral')
            ticks.append((width+x_loc)[0])
            dates_played.append(datetime.datetime.strptime(date, '%d-%m-%Y' ).strftime("%d %b"))
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_xticks(ticks)
        ax.set_xticklabels(dates_played)
        fig.suptitle("Right/Wrong by date", fontsize=15)
        ax.set_xlim([ax.get_xlim()[0], ax.get_xlim()[1]+0.15])
        # plt.show()

    def wrong_rank(self):
        wrong_words = self.data_base[self.data_base["correct"]==False]
        wrong_by_word = wrong_words.groupby(wrong_words["wort"])
        func = {"correct": "count", "article": lambda x: x.iloc[0]} ## "article": Getting the first value of entry
        wrong_by_word =  wrong_by_word.agg(func).rename(columns = {"correct": "wrong"})
        wrong_by_word = wrong_by_word.reset_index()
        wrong_ones_sort = wrong_by_word.sort_values(['wrong', 'wort'], ascending = [0, 0])
        first_twenty_wrong = wrong_ones_sort[0:20]
        col_num = np.arange(first_twenty_wrong.shape[0])
        fig, ax = plt.subplots(figsize=(8, 6))
        width = 0.65
        bars_worng = ax.bar(col_num, first_twenty_wrong["wrong"], width, color= 'powderblue'
                           , linewidth=0.5)
        ax.set_xlim([-0.5, ax.get_xlim()[1]])
        ax.set_ylim([0, ax.get_ylim()[1] +1])
        ax.set_title('Ranking of wrong words', fontsize=15)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis="y", zorder=0, color="#9698A1")
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_yticks(np.arange(first_twenty_wrong.iloc[-1]["wrong"], first_twenty_wrong.iloc[0]["wrong"]+2, 1.0))
        ax.set_xticks(col_num + 0.325)
        ax.set_xticklabels(list(first_twenty_wrong['wort']))
        plt.setp(ax.get_xticklabels(), rotation=90)
        
        for article in range(len(list(first_twenty_wrong['article']))):
            ax.text(article + 0.4, 0.15 , list(first_twenty_wrong['article'])[article], rotation= 90,
                   horizontalalignment='center',
                verticalalignment='center', fontsize=12) 
        # plt.tight_layout()
        # plt.show()

    def daily_stats(self):
        grouped = (self.data_base["correct"]==True).groupby(self.data_base["date"])
        correct = grouped.mean().reset_index()
        correct["wrong"] =  1 - correct["correct"]
        fig, ax = plt.subplots()
        dates = [datetime.datetime.strptime(date, '%d-%m-%Y' ).date() for date in correct["date"] ]
        left_limit = (datetime.datetime.strptime(pd.unique(self.data_base["date"])[0], '%d-%m-%Y' )  - 
                      datetime.timedelta(days= 1)).date() 
        right_limit = (datetime.datetime.strptime(pd.unique(self.data_base["date"])[-1], '%d-%m-%Y' )  
                       + datetime.timedelta(days=1)).date()
        ax.plot(dates, correct['correct'], marker = '.', color='lightseagreen',
                                           ms = 15, lw = 2, linestyle= '-' , label="correct" )
        ax.plot(dates, correct['wrong'], color='coral', marker = '.',
                                           ms = 15, lw = 2, linestyle= '-', label="wrong"  )
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.grid(axis="y", zorder=0, color="#9698A1")
        ax.set_xticks((dates))
        ax.set_xlim([left_limit, right_limit])
        ax.set_ylim([0., 1.])
        ax.legend(loc='upper right').get_frame().set_alpha(0.3)
        ax.set_title('Daily Stats', fontsize=15)
        ax.set_xticklabels([date.strftime("%d %b") for date in dates])
        # plt.show()

    def daily_stats_per_gender(self):
        grouped = (self.data_base["correct"]==True).groupby([self.data_base["date"], self.data_base["article"]])
        correct_gender = grouped.mean().reset_index()
        correct_gender["wrong"] = 1 - correct_gender["correct"] 
        correct_gender = correct_gender.set_index(["date", "article"]).unstack().reset_index()
        dates = [datetime.datetime.strptime(date, '%d-%m-%Y' ).date() 
                 for date in correct_gender["date"] ]
        left_limit = (datetime.datetime.strptime(pd.unique(self.data_base["date"])[0], '%d-%m-%Y' )  - 
                      datetime.timedelta(days= 1)).date() 
        right_limit = (datetime.datetime.strptime(pd.unique(self.data_base["date"])[-1], '%d-%m-%Y' )  
                       + datetime.timedelta(days=1)).date()
        fig= plt.figure()
        ax = fig.add_axes([0.1, 0.2, 0.85, 0.70])
        lab_desc, lab_chars = [], []
        gen_spec = {"der":"#6191C5" , "die":"#D56054" , "das": "#69B17D"}
        for gender, color_gen in gen_spec.items():
            ax.plot(dates, correct_gender["correct"][gender], color= color_gen, marker = '.', 
                    ms = 12, lw = 2, linestyle= '-' )
            ax.plot(dates, correct_gender["wrong"][gender], color= color_gen, marker = '.', 
                    ms = 12, lw = 2, linestyle= '--')
            leg_char_corr = plt.Line2D((0,1),(0,0), color=color_gen, marker='.', linestyle='-')
            leg_char_wrong = plt.Line2D((0,1),(0,0), color=color_gen, marker='.', linestyle='--')
            lab_chars.extend([leg_char_corr, leg_char_wrong])
            lab_desc.extend([gender + " right", gender + " wrong"])
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.grid(axis="y", zorder=0, color="#9698A1")
        ax.set_xticks((dates))
        ax.set_xlim([left_limit, right_limit])
        ax.set_ylim([-0.05, 1.1])
        ax.set_title('Daily Stats per gender', fontsize=15)
        ax.set_xticklabels([date.strftime("%d %b") for date in dates])
        ax.legend(lab_chars, lab_desc, loc='upper center', 
                  bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=3)
        # plt.show()

    def generate_report(self): 
        if not os.path.exists("img"):
            os.makedirs("img")
        self.overall_results_per()
        plt.savefig('img/overall_results_per', bbox_inches='tight')
        self.results_per_gen()
        plt.savefig('img/results_per_gen', bbox_inches='tight')
        self.results_per_date()
        plt.savefig('img/results_per_date', bbox_inches='tight')
        self.wrong_rank()
        plt.savefig('img/wrong_rank', bbox_inches='tight')
        self.daily_stats()
        plt.savefig('img/daily_stats', bbox_inches='tight')
        self.daily_stats_per_gender()
        plt.savefig('img/daily_stats_per_gender', bbox_inches='tight')


graph_test = Graphs(pd.read_pickle("results"))
graph_test.generate_report()
