# -*- coding: utf-8 -*-
"""Untitled

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X3udpN6eIfnbpU17jGrv9O8j6LJsH7Rk
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import functools
import numpy as np

!pip install MechanicalSoup
import mechanicalsoup

browser = mechanicalsoup.StatefulBrowser()
browser.open("https://godvillegame.com/")
browser.select_form('form[action="/login/login"]')
browser["username"] = "Go24yWnHZ77wL2"
browser["password"] = "go24yWnHZ77wL2"
response = browser.submit_selected()
browser.follow_link("news")

soup = browser.get_current_page()
#link = urlopen('https://godvillegame.com/news').read()    
#soup = BeautifulSoup(html_doc, 'html.parser')

#print(soup.prettify())

across_comingup = 0
down_comingup = 0
word_incoming = 0
word_index_across = []
word_index_down = []
for string in soup.find("div", attrs={"class": "cross_q"}).stripped_strings:
  line = repr(string)
  line = line.replace('\\t', '')
  line = line.replace('\\n', ' ')
  line = line.replace('&nbsp', ' ')
  line = line.replace('.', '')
  line = line.replace('\'', '')
  if across_comingup:
    splitted = line.split()
    iter_number = len(splitted)
    for i in range(iter_number):
      if word_incoming:
        word_incoming = 0
      if splitted[i].isdigit():
        word_index_across.append(int(splitted[i]))
        word_incoming = 1  
  if down_comingup:
    splitted = line.split()
    iter_number = len(splitted)
    for i in range(iter_number):
      if word_incoming:
        word_incoming = 0
      if splitted[i].isdigit():
        word_index_down.append(int(splitted[i]))
        word_incoming = 1  
  if line == "Across:":
    across_comingup = 1
  elif line == "Down:":
    across_comingup = 0
    down_comingup = 1

across_words = [[] for i in range(len(word_index_across))]
down_words = [[] for i in range(len(word_index_down))]
list_of_unfilled_letter_positions = [[]]
counter = 0
for unknown_letters in soup.find_all("input", attrs={"autocomplete":"off"}):
  line = unknown_letters['aria-label']
  line = line.replace(',', '')
  line = line.replace('.', ' .')
  splitted = line.split()
  #print(splitted)
  if (splitted[1] == 'down'):
    down_words[word_index_down.index(int(splitted[0]))].append([])
    list_of_unfilled_letter_positions[counter].append(1)
    list_of_unfilled_letter_positions[counter].append(word_index_down.index(int(splitted[0])))
    list_of_unfilled_letter_positions[counter].append(int(splitted[splitted.index('letter') + 1]))
    list_of_unfilled_letter_positions[counter].append(unknown_letters['name'])
  if (splitted[1] == 'across'):
    across_words[word_index_across.index(int(splitted[0]))].append([])
    list_of_unfilled_letter_positions[counter].append(0)
    list_of_unfilled_letter_positions[counter].append(word_index_across.index(int(splitted[0])))
    list_of_unfilled_letter_positions[counter].append(int(splitted[splitted.index('letter') + 1]))
    list_of_unfilled_letter_positions[counter].append(unknown_letters['name'])
  if '.' in splitted :
    shifted_index = splitted.index('.') + 1
    counter += 1
    list_of_unfilled_letter_positions.append([])
    if (splitted[shifted_index + 1] == 'down'):
      down_words[word_index_down.index(int(splitted[shifted_index + 0]))].append([])
      list_of_unfilled_letter_positions[counter].append(1)
      list_of_unfilled_letter_positions[counter].append(word_index_down.index(int(splitted[shifted_index + 0])))
      list_of_unfilled_letter_positions[counter].append(int(splitted[splitted[shifted_index:].index('letter') + 1 + shifted_index]))
      list_of_unfilled_letter_positions[counter].append(unknown_letters['name'])
    if (splitted[shifted_index + 1] == 'across'):
      across_words[word_index_across.index(int(splitted[shifted_index + 0]))].append([])
      list_of_unfilled_letter_positions[counter].append(0)
      list_of_unfilled_letter_positions[counter].append(word_index_across.index(int(splitted[shifted_index + 0])))
      list_of_unfilled_letter_positions[counter].append(int(splitted[splitted[shifted_index:].index('letter') + 1 + shifted_index]))
      list_of_unfilled_letter_positions[counter].append(unknown_letters['name'])
  counter += 1
  list_of_unfilled_letter_positions.append([])
list_of_unfilled_letter_positions.pop()

for unknown_letters in soup.find_all("div", attrs={"class": "open"}):
  line = unknown_letters['aria-label']
  line = line.replace(',', '')
  line = line.replace('-', '')
  splitted = line.split()
  #print(splitted)
  if (splitted[1] == 'down'):
    down_words[word_index_down.index(int(splitted[0]))].append([])
  if (splitted[1] == 'across'):
    across_words[word_index_across.index(int(splitted[0]))].append([])

for unknown_letters in soup.find_all("div", attrs={"class": "open"}):
  line = unknown_letters['aria-label']
  line = line.replace(',', '')
  line = line.replace('-', '')
  splitted = line.split()
  #print(splitted)
  if splitted[-1].isdigit(): 
    if (splitted[1] == 'down'):
      down_words[word_index_down.index(int(splitted[0]))][int(splitted[splitted.index("letter") + 1]) - 1] = ' '
    elif (splitted[1] == 'across'):
      across_words[word_index_across.index(int(splitted[0]))][int(splitted[splitted.index("letter") + 1]) - 1] = ' '
  else:
    if (splitted[1] == 'down'):
      down_words[word_index_down.index(int(splitted[0]))][int(splitted[splitted.index("letter") + 1]) - 1] = splitted[-1]
    elif (splitted[1] == 'across'):
      across_words[word_index_across.index(int(splitted[0]))][int(splitted[splitted.index("letter") + 1]) - 1] = splitted[-1]

link_solution = urlopen('https://wiki.godvillegame.com/Omnibus_List').read()    
soup_solution = BeautifulSoup(link_solution, 'html.parser')

#print(soup_solution.prettify())

across_solution = [[] for i in range(len(word_index_across))]
down_solution = [[] for i in range(len(word_index_down))]
for i in range(len(across_words)):
  l_test = across_words[i]
  for string in soup_solution.find_all("li"):
    line = list(string.text.upper())
    count = np.where([ x == y for x, y in zip(line, l_test) ])[0].size
    if count == len(np.where([x != [] for x in l_test])[0]):
      print(line)
      across_solution[i] = line
for i in range(len(down_words)):
  l_test = down_words[i]
  for string in soup_solution.find_all("li"):
    line = list(string.text.upper())
    count = np.where([ x == y for x, y in zip(line, l_test) ])[0].size
    if count == len(np.where([x != [] for x in l_test])[0]) and len(line) == len(l_test):
      print(line)
      down_solution[i] = line

print(browser.get_url())
browser.select_form()

for positions in list_of_unfilled_letter_positions:
  if positions[0] == 0:
    browser[positions[3]] = across_solution[positions[1]][positions[2]-1]
  if positions[0] == 1:
    browser[positions[3]] = down_solution[positions[1]][positions[2]-1]

response = browser.submit_selected()

print(response.text)

git