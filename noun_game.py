import pandas as pd
import random
import datetime
import os.path
import time

class Gender_guess:
    """"Implements the main game. A word in German is chosen and the user is asked for the gender."""

    def __init__(self, csvfile):
        """Takes csv values that contains nouns and generates a pandas data frame to collect results."""
        self.noun_list = csvfile
        self.data_base = pd.DataFrame(index=range(0),
                                      columns=['date', 'time', 'input','article', 'wort', 'word', 'correct'])
        
    def file_to_data_frame(self, csvfile):
        """Passes csv file with Vocabulary to pandas data frame."""
        data_nouns = pd.read_csv('final_data.csv', delimiter= ",", index_col=0)
        return data_nouns
    
    def pick_word(self, data_frame):
        """Randomly picks an index to select word to be tested."""
        random_pick = random.randint(0, len(data_frame.index) -1)
        return random_pick

    def eng_ger_word(self, random_pick, data_frame):
        """Select the words in German and English according to the random selection."""
        german = data_frame.ix[random_pick]["Wort"]
        english = data_frame.ix[random_pick]["Word"]
        return german, english
    
    def print_words(self, german, english):
        """Prints the set of instructions and words for the user."""
        german_spacing = int(len(german)/2)
        english_spacing = int(len(english)/2)
        total_spacing = (german_spacing + english_spacing)*2 + len("Deutsch"+"English") + 2
        print("{0}{1}{2}|| {3}{4}{5} \n {6} ".format
              (" "*german_spacing  ,"Deutsch", " "*german_spacing ," "*english_spacing
               ,"English" , " "*english_spacing, '='* total_spacing))
        print(" {0}{1}{2}\n\n".format(german," "*(german_spacing + 4) , english))
 
    def take_input(self):
        """Takes input of user. Prechecks input values."""
        gender = input("Der, die oder das? ... \n\n").lower()
        while gender not in ["der", "die", "das"]:
            print("\n\nPlease, make sure to enter a valid gender.")
            gender = input("Der, die oder das? ... \n\n").lower()
        return gender
    
    def print_input(self, gender_input, german_word):
        """Prints user's input.""" 
        print("\n\n{} {}".format(gender_input , german_word))
        
    def word_gender(self, random_pick, data_frame):
        """Chooses the article corresponding to word randomly chosen."""
        german_gen = data_frame.ix[random_pick]["Article"]
        return german_gen.strip()  
    
    def checker(self, german_gender, gender_input):
        """Checks if gender is right."""
        if german_gender == gender_input:
            print("Das stimmt! :)\n\n")
            return True
        else:
            print("Das ist nicht richtig :( --> {} \n\n ".format(german_gender))
            return False
    
    def gen_data_base(self, gender_input, german_gender, german_wort, english_word, correct):
        """Updates previously generated data base with results from tests."""
        to_add = pd.DataFrame({'date': [datetime.date.today().strftime("%d-%m-%Y")], 'time': [datetime.datetime.now().time().strftime("%H:%M:%S")], 
                               'input': [gender_input],'article': [german_gender], 
                               'wort': [german_wort], 'word': [english_word], 'correct': [correct]})
        self.data_base = self.data_base.append(to_add, ignore_index=True)
    
    def run_program(self, number_of_words):
        """Main logic of program. Stores results to a pandas data frame for time series tracking."""
        data = self.file_to_data_frame('nouns_german')
        for round in range(number_of_words):
            time.sleep(1)
            ran_pick = self.pick_word(data)
            german = self.eng_ger_word(ran_pick, data)[0]
            english = self.eng_ger_word(ran_pick, data)[1]
            german_gender = self.word_gender(ran_pick, data)
            self.print_words(german, english)
            gender_input = self.take_input()
            self.print_input(gender_input, german)
            correct = self.checker(german_gender, gender_input)
            self.gen_data_base(gender_input, german_gender, german, english, correct)
        if os.path.isfile("results"):
            previous_data = pd.read_pickle("results")
            previous_data = previous_data.append(self.data_base, ignore_index=True)
            previous_data.to_pickle("results")
        else: 
            self.data_base.to_pickle("results")


prueba_1 = Gender_guess('final_data.csv')
prueba_1.run_program(20)
