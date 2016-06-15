import datetime
import grapher_gen_results as grapher
import os
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

def run_report():
	env = Environment(loader = FileSystemLoader('.'))
	template = env.get_template("my_report.html")
	
	main_figures = pd.read_pickle("results")
	
	#get current dir for printing images
	current_dir = os.getcwd()
	
	#Introduction data
	num_total_test = len(main_figures)
	grouped_date = main_figures.groupby(main_figures["date"])
	date_num_more_prac = datetime.datetime.strptime(grouped_date.size().idxmax(), '%d-%m-%Y' ).strftime("%A %d %b")
	num_more_prac = grouped_date.size().max()
	
	
	#Overall correct
	per_overall_correct = str(round(main_figures["correct"].sum() / len(main_figures), 4) * 100) + "%"
	
	
	# Gender right wrong reporting
	grouped_best_gen = (main_figures["correct"]==True).groupby(main_figures["article"])
	correct_gen = grouped_best_gen.mean()
	strong_gender = correct_gen.idxmax()
	num_correct_strong_gen = str(round(correct_gen.max(), 4)*100) + "%"
	weak_gender = correct_gen.idxmin()
	num_correct_weak_gen = str(round(correct_gen.min(), 4)*100) + "%"
	
	# Historically right wrong reporting
	grouped_date = (main_figures["correct"]==True).groupby(main_figures["date"])
	correct_by_date = grouped_date.mean()
	date_max_correct = datetime.datetime.strptime(correct_by_date.idxmax(), '%d-%m-%Y' ).strftime("%A %d %b")
	qt_date_max_correct = str(round(correct_by_date.max(), 4)*100) + "%"
	
	# Historical results per gender
	grouped_gen_date = (main_figures["correct"]==True).groupby(
	            [main_figures["date"], main_figures["article"]])
	correct_gender_date = grouped_gen_date.mean().reset_index()
	correct_gender_date["pct_change"] =  (correct_gender_date.groupby("article").pct_change())*100
	more_once = len(pd.unique(correct_gender_date["date"])) > 1
	last_date = correct_gender_date[correct_gender_date["date"] == max(correct_gender_date.date)]
	biggest_change_gen_date = str(round(max(last_date["pct_change"]), 2)) + "%"
	gender_big_change = last_date.loc[[last_date["pct_change"].idxmax()]]["article"].to_string(index=False)
	lowest_change_gen_date = str(round(min(last_date["pct_change"]), 2)) + "%"
	gender_lowest_change_gen_date = last_date.loc[[last_date["pct_change"].idxmin()]]["article"].to_string(index=False)
	
	
	
	
	template_vars = {"current_dir": current_dir,
					"num_total_test": num_total_test,
					"date_num_more_prac": date_num_more_prac,
					"num_more_prac": num_more_prac, 
					"per_overall_correct": per_overall_correct,
					"strong_gender": strong_gender,
					"num_correct_strong_gen": num_correct_strong_gen,
					"weak_gender": weak_gender,
					"num_correct_weak_gen": num_correct_weak_gen,
					"date_max_correct": date_max_correct,
					"qt_date_max_correct": qt_date_max_correct,
					"more_once": more_once,
					"gender_big_change": gender_big_change,
					"biggest_change_gen_date": biggest_change_gen_date,
					"lowest_change_gen_date": lowest_change_gen_date,
					"gender_lowest_change_gen_date": gender_lowest_change_gen_date
					}
	
	
	html_out = template.render(template_vars)
	
	with open("results_report", 'w') as f:
	    html_out = template.render(template_vars)
	    f.write(html_out)
	
	pdf_report = HTML(string=html_out).write_pdf("report.pdf")

	return(pdf_report)




