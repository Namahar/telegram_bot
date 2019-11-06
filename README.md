# telegram_bot
Telegram bot for personal group chat

html_reader.py scans through chat data exported from Telegram. html_reader.py takes all relevant data in a list. You must export the data to a txt file using the command >> 'output.txt'. html_reader.py uses a config file which stores personal information that I needed to remove. Remove the import statement or add your own clean_config.py file. 

reccurent_neural_network.py contains all the training and output functions for the neural network. telegram.py is where the output is taken from recurrent_neural_network.py and sent to the telegram chat. telegram.py uses a config file to store the telegram API key and other chat related IDs. Add your own config file or remove the import statement to run. 
