import requests, re, os, sys, json
from html.parser import HTMLParser
from bs4 import BeautifulSoup

class Subject():
    def __init__(self, time, name, source):
        self.time = time
        self.name = name
        self.source = source

def get_group(groupId):
    url = 'https://table.nsu.ru/group/%d' % groupId
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse_group(groupId):
    soup = get_group(groupId)
    table = soup.find('table', { 'class' : 'time-table' })
    trs = table.find_all('tr')
    b = {}

    for tr in trs[1:]:
        tds = tr.find_all('td')
        if tds is not None:
            i = 0
            for td in tds:
                if tds[0].string not in b:
                    b[tds[0].string] = {}
                name = td.find('div', {'class' : 'cell'})
                if name is not None:
                    result = re.search(r'\w.*\w', name.find('div', { 'class' : 'subject'}).string)
                    b[tds[0].string][i] = Subject(tds[0].string, result.group(0), td)
                else:
                    b[tds[0].string][i] = Subject(tds[0].string, '', td)
                i = i + 1
    return b

def get_all_items(groupsArray):
    result = {}
    for groupId in groupsArray:
        result[groupId] = parse_group(groupId)
    return result

def get_table_by_item(itemName, allItems):
    result = {}
    for k1 in allItems:
        for k2 in allItems[k1]:
            for k3 in allItems[k1][k2]:
                if allItems[k1][k2][k3].name == itemName:
                    if k2 not in result:
                        result[k2] = {}
                    result[k2][k3] = allItems[k1][k2][k3] 
    return result

def delete_table_by_item(itemName, items):
    result = {}
    for k1 in items:
        for k2 in items[k1]:
            if items[k1][k2].name != itemName:
                if k1 not in result:
                    result[k1] = {}
                result[k1][k2] = items[k1][k2]
    return result

def merge_tables(priorityTable, slaveTable):
    for k1 in slaveTable:
        for k2 in slaveTable[k1]:
            if k1 not in priorityTable:
                priorityTable[k1] = {}
            if k2 not in priorityTable[k1] or priorityTable[k1][k2].name == '':
                priorityTable[k1][k2] = slaveTable[k1][k2]
    return priorityTable

def create_rasp_for_group(groupId, itemsToAdd, itemsToDelete, groupsArray):
    allItems = get_all_items(groupsArray)
    groupItems = parse_group(groupId)

    for deleteItem in itemsToDelete:
        groupItems = delete_table_by_item(deleteItem, groupItems)

    for addItem in itemsToAdd:
        tableForAdd = get_table_by_item(addItem, allItems)
        groupItems = merge_tables(groupItems, tableForAdd)

    return groupItems

def transponate_resp(items):
    result = {}
    for k1 in items:
        for k2 in items[k1]:
            if k2 != '' :
                if k2 not in result:
                    result[k2] = {}
                result[k2][k1] = items[k1][k2]
    return result

def create_fixed_rasp(groupId, sourceHtml, itemsToAdd, itemsToDelete, groupsArray):
    fixedRasp = create_rasp_for_group(groupId, itemsToAdd, itemsToDelete, groupsArray)

    table = sourceHtml.find('table', { 'class' : 'time-table' })
    trs = table.find_all('tr')

    for tr in trs[1:]:
        tds = tr.find_all('td')
        if tds is not None:
            i = 0
            timeNow = re.search(r'\w.*\w', tds[0].string).group(0)
            for td in tds:
                try:
                    newSource = fixedRasp[timeNow][i].source
                    td.replace_with(newSource)
                except KeyError:
                    td.replace_with(BeautifulSoup('<td></td>', 'html.parser'))
                i = i + 1
    
    return sourceHtml

def get_rasp_from_file(filePath):
    soup = BeautifulSoup(open(filePath), "html.parser")
    return soup

def save_rasp_in_file(filepath, rasp):
    with open(filepath, 'w') as output_file:
        output_file.write(rasp.prettify())

def create_group_rasp(configPath, sourcePath):
    return 0

def main(configPath):
    data = {}
    with open(configPath, "r") as read_file:
        data = json.load(read_file)
    
    groupId = data['group_id']
    htmlFilePath = data['html_path']
    itemsToAdd = data['items_to_add']
    itemsToDelete = data['items_to_delete']
    groupsArray = data['groups']

    sourceHtml = BeautifulSoup(open(htmlFilePath), "html.parser")
    fixedRasp = create_fixed_rasp(groupId, sourceHtml, itemsToAdd, itemsToDelete, groupsArray)
    save_rasp_in_file(htmlFilePath, fixedRasp)

def print_created_rasp(lalala):
    lululu = transponate_resp(lalala)
    for k1 in lululu:
        print(k1, ':')
        for k2 in lululu[k1]:
            print('\t|', k2, '|', lululu[k1][k2].name)

if __name__ == "__main__":
    configPath = "config.json"
    if len(sys.argv) >= 2:
        configPath = sys.argv[1]
    main(configPath)
