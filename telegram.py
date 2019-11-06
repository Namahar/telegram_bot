import requests
import recurrent_neural_network as rnn
import config

url = "https://api.telegram.org/bot" + config.tele + '/'
weather_url = 'http://api.openweathermap.org/data/2.5/weather?'

# print dictionary function
def printDict(dictionary, f):
   for key, val in dictionary.items():
      # print(str(key) + " = " + str(val))
      f.write(str(key) + " = " + str(val) + "\n")

   return

# used for debugging
# prints data from message object
# can print to console or file "datalog.txt"
def messagePrint(message, f):

   # message is dictionary wrapped in list
   # need to access dictionary using 0 index in list
   for key, val in message[0].items():

      # print data if value is not a dict
      if not isinstance(val, dict):
         # print(str(key) + " = " + str(val))
         f.write(str(key) + " = " + str(val) + "\n")

      # print sub dictionary
      else:
         # print("\n" + key)
         f.write("\n" + str(key) + "\n")
         for ke, va in val.items():
            if not isinstance(va, dict):
               # print(str(ke) + " = " + str(va))
               f.write(str(ke) + " = " + str(va) + "\n")
            
            # prints sub dictionary of sub dictionary
            else:
               # print("\n" + ke)
               f.write("\n" + str(ke) + "\n")
               printDict(va, f)

   # print("\n")
   f.write("\n\n")
   return

def sayHi(message_id, chat_id):             
   if message_id in config.users:
      chat_params = {'chat_id': chat_id,
                     'text': "Hi " + config.users[message_id],
                     'disable_notifaction': True}

   else:
      chat_params = {'chat_id': chat_id,
                     'text': "Hi",
                     'disable_notifaction': True}
   
   requests.get(url = url + 'sendMessage', params = chat_params)

   return

# turns off bot
def sayGoodbye(chat_id):
   chat_params = {'chat_id': chat_id,
                  'text': 'Goodbye',
                  'disable_notifaction': True}
   requests.get(url = url + 'sendMessage', params = chat_params)

   return

# scans messages f
def scanMessage(message_data, message_id, chat_id):
   message_data = message_data['text'].lower().split(" ")
   length = len(message_data)

   # looks for weather information
   if 'weather' in message_data and '@' in message_data[0]:
      index = message_data.index('weather')
      city = ''
      for i in range(index+2, len(message_data)):
         city = city + ' ' + message_data[i] 

      city = city[1:len(city)]
      country = 'us'

      complete_url = weather_url + "q=" + city + "," + country + "&appid=" + config.weather + "&units=imperial"
      data = requests.get(complete_url).json()

      if 'cod' in data and data['cod'] == '404':
         chat_params = {'chat_id': chat_id,
                     'text': "this city has no weather data",
                     'disable_notifaction': True}
   
         requests.get(url = url + 'sendMessage', params = chat_params)

      else:
         temp = data['main']['temp']

         # if temp is wanted in celsius 
         # temp = (temp - 273.15) * 9/5 + 32
         # temp = round(temp, 1)
         
         chat_params = {'chat_id': chat_id,
                     'text': "The current temperature is: " + str(temp) + " degrees Fahrenheit",
                     'disable_notifaction': True}
   
         requests.get(url = url + 'sendMessage', params = chat_params)
   
   # looks to respond hi or exit chat
   else:

      for i in range(0, length):
         if message_data[i] == 'hi' and length == 1:
            sayHi(message_id, chat_id)

         elif '@' in message_data[i] and message_data[i].index('@') == 0 and message_data[0] == '@joaquin_the_bot':
            if message_data[i] == 'hi' and length == 2:
               sayHi(message_id, chat_id)
            elif length == 1:
               sayHi(message_id, chat_id)

         if message_data[i] == 'goodbye' and i + 1 < length and message_data[i+1] == 'joaquin' and length == 2:
            sayGoodbye(chat_id)
            return True

   return False

def botMessage(message_data, message_id, chat_id, lines, maxlen, word_id, id_word):
   message_data = message_data['text'].lower().split(" ")
   length = len(message_data)

   for i in range(length):
      if message_data[i] == '@joaquin_the_bot':
         message_input = message_data[i+1:]
         message_input = ' '.join(message_input)
         # print(message_input)
         
         bot_val = rnn.output(lines, maxlen, word_id, id_word, message_input)
         # print(bot_val)

         chat_params = {'chat_id': chat_id,
                  'text': bot_val,
                  'disable_notifaction': True}
         requests.get(url = url + 'sendMessage', params = chat_params)

   return False

def main():

   # setup for rnn
   lines, maxlen, word_id, id_word = rnn.startup()

   # file to log data
   f = open("datalog.txt", "w")

   # get information about bot
   data = requests.get(url = url + 'getMe').json()['result']
   printDict(data, f)

   # update id used to keep track of new messages
   update_id = -1
   end = False

   while (1):
      # set parameters for update function
      message_params = {'offset': update_id+1, 'limit': 1000, 'timeout': 100, 'allowed_updates': ["message"]}
      
      # get new message
      message = requests.get(url = url + 'getUpdates', params = message_params).json()['result']

      # check to stop program
      if end:
         break
      
      # if a new message is received, update message counter
      if (message):
         messagePrint(message, f)

         # get update id of message
         update_id = message[0]['update_id']

         # get message data of message object
         # check if message is edited
         if not 'edited_message' in message[0]:
            message_data = message[0]['message']

         # currently skips over edited messages
         else:
            continue

         
         # check that message object has a text entry
         if 'text' in message_data:

            # get message id to respond and chat id to respond in
            message_id = message_data['from']['id']
            chat_id = message_data['chat']['id']

            # end = scanMessage(message_data, message_id, chat_id)
            end = botMessage(message_data, 
                              message_id, 
                              chat_id, 
                              lines, maxlen, word_id, id_word)

   f.close()
   return

if __name__ == '__main__':
   main()