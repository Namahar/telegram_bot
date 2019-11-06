from bs4 import BeautifulSoup
import time
import os
import clean_config

def isTimeFormat(d):
    try:
        time.strptime(d, '%H:%M')
        return True
    except ValueError:
        return False

def output(data, vocabulary):

   for d in data:
      if d == 'Next messages':
         continue
      elif d == 'Previous messages':
         continue
      elif d == 'Exported Data':
         continue
      elif 'joined group by link' in d:
         continue
      elif d == 'K' or d == 'Kae':
         continue
      elif 'In reply to' in d:
         continue
      elif 'this message' in d:
         continue
      elif d == 'Not included, change data exporting settings to download.':
         continue
      elif d == 'Photo':
         continue
      elif d == 'Video file':
         continue
      elif 'http' in d:
         continue
      elif 'MB' in d or 'KB' in d:
         continue
      elif d == clean_config.name1:
         continue
      elif d == clean_config.name2 or d == 'A':
         continue
      elif clean_config.name3 in d or d == 'N':
         continue
      elif '@' in d:
         continue
      elif d == 'Sticker':
         continue
      elif d == clean_config.name4 or d == 'S':
         continue
      elif d == clean_config.name5 or d == 'T':
         continue
      elif d == 'Shadow':
         continue
      elif d == clean_config.name6 or d == 'ZR':
         continue
      elif d == clean_config.name10 or d == 'B':
         continue
      elif d == 'G' or d == 'Guava Goddess':
         continue
      elif d == 'TW' or d == 'The Wrath':
         continue
      elif d == 'ns' or d == clean_config.name7:
         continue
      elif d == 'E' or d == clean_config.name8:
         continue
      elif d == 'J' or d == clean_config.name9:
         continue
      elif d == 'Banned God' or d == 'BG':
         continue
      elif 'pinned' in d:
         continue
      elif isTimeFormat(d):
         continue
      elif '2019' in d:
         continue
      else:
         if not d in vocabulary:
            vocabulary.append(d)

   return

def singleFile(f):
   HtmlFile = open(f, 'r', encoding='utf-8')
   source_code = HtmlFile.read() 

   # close file
   HtmlFile.close()

   # parse html code
   soup = BeautifulSoup(source_code, 'html.parser')

   # prints properly formatted html code
   # print(soup.prettify())

   # gets stripped text
   data = soup.stripped_strings
   
   output(data) 
   return

def main():
   # get file name and open it
   files = os.listdir('chat_data')
   base = 'chat_data/'

   vocabulary = []
   
   start = time.time()

   for f in files:
      fname = base + f
      HtmlFile = open(fname, 'r', encoding='utf-8')
      source_code = HtmlFile.read() 
   
      # close file
      HtmlFile.close()

      # parse html code
      soup = BeautifulSoup(source_code, 'html.parser')

      # prints properly formatted html code
      # print(soup.prettify())

      # gets stripped text
      data = soup.stripped_strings

      output(data, vocabulary)   

   end = time.time()
   # print(end - start)
   # print(len(vocabulary))

   return


if __name__ == '__main__':
   main()