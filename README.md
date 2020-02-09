# Custom timetable

## Description

Custom timetable project is provide functional for creating custom timetable for NSU students which want to delete unused lessons and add used one.

## Installation

1. Clone this repository.

2. You will need following dependencies to build project:
   1. python3+
   2. python-pip3
   3. pip3 beautifulsoup4
   4. pip3 lxml

3. Download your timetable from "https://table.nsu.ru/group/your_group_number" in project directory(with chrome you should use save as)

## Usage
1. Change config.json file:
   1. Put your group number
   2. Put name of downloaded html file
   3. Change itemsToAdd and itemsToDelete whatever you want

2. Run python script:
   python3 parser.py config.json
3. Enjoy your new timetable!

## Example
   config.json:
	{
		"group_id":17202,
		"html_path":"rasp.html",
		"items_to_add":
		[
			"АСМиМ", 
			"ЭПСМиМ", 
			"ЛМИЗ"
		],
		"items_to_delete":
		[
			"МиМИИ",
			"Теор. автоматов", 
			"Учеб. практика, НИР",
			"ТООИ",
			"Инж. и комп. графика",
			"СММО"
		]
	}
