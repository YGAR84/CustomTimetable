# Custom timetable

## Description

Custom timetable project is provide functional for creating custom timetable for NSU students which want to delete unused lessons and add used one.

## Installation

1. Clone this repository.

2. You will need following dependencies to build project:
   1. python3+
   2. python-pip3
   3. pip3 install beautifulsoup4
   4. pip3 install lxml

3. Download your timetable from "https://table.nsu.ru/group/your_group_number" in project directory(with chrome you should use save as).
You need it to have all files to see your timetable in original style

## Usage
1. Change config.json file:
   1. Put your group number
   2. Put name of downloaded html file
   3. Change itemsToAdd and itemsToDelete whatever you want
   4. Put all groups from your stream

2. Run python script:
   python3 parser.py [ path/to/your/config/file ]
3. Open html file.
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
		],
		"groups":
		[
			17201,
			17202,
			17203,
			17204,
			17205,
			17206,
			17207,
			17208,
			17209,
			17210
		]
	}
