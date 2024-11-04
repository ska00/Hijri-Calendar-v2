'''
Author: Salama Algaz
Date: 10/11/2024

This code tries to make the Hijri months as consistent as possible except for Dhul Hijjah which 
occassionally has an extra day. This month is called the Kabs month because it is where an extra day is added.
The month Muharram will sometimes appear at the end of the year, or at the start depending
on where the the large gap between seasons (i.e. the solar year) and the hijri (lunar) year occurs.
I looked for the months in which two full moons occur and depending on that decided where to put
the Muharram month. An alternative would be to calculate the deviation of the lunar year (typically
having 354 or 355 days) from the solar year(365.24 days) and once the gap exceeds a certain amount
the extra month is placed again depending on where this gap exceeded it's limit.

I've tried to look for a pattern for the placement of Muharram and the Kabs days but could not find
one. Instead I look for deviations from solar calendar and adjusted if needed.


Note: 
The data on Astropixels.com has one error where the year 3869 has two januarys. I manually had to change
the year of the second January to 3870. Keep this in mind when using the data_scraper_with_eclipses.py file

Note:
The data used is in UTC/UT timezone, however the output displays 
the dates in AST timezone which is the timezone of Mecca, Saudi Arabia. 

Credits:
Some tables retrieved from https://www.somacon.com/p570.php
Moon Phases Table courtesy of Fred Espenak, www.Astropixels.com. Thanks to Fred for this treasure of data.
'''


'''	--------- PACKAGES ------------ '''
import csv
import math
import pytz
import sys
from datetime import datetime, timedelta


print("Packages imported successfully")


'''	--------- UTILITIES ------------ '''
def get_number_of_days_in_month():
	d = {}
	for month_number in range(1, 12 + 1):
		d[month_number] = 30 if month_number % 2 == 1 else 29
	return d

def is_fullmoon(row):
	return row["phase"] == "Full Moon"


'''	--------- CONSTANTS ------------ '''

AVG_SYNODIC_MONTH = 29 + 12 / 24 + (44/60 / 24)	# 29 days, 12 hours, 44 minutes -> 29.530594 days

DATEFORMAT = "%Y-%m-%d %H:%M:%S"

FILES = [ 
		{"start_year":  601, "end_year": 2100, "filename": "moon-phases-601-to-2100-UTC.csv"},
		{"start_year": 1900, "end_year": 2100, "filename": "moon-phases-1900-to-2100-UTC.csv"},
		{"start_year": 1902, "end_year": 1998, "filename": "moon-phases-1902-to-1998-UTC.csv"},
		{"start_year": 1980, "end_year": 2077, "filename": "moon-phases-1980-to-2077-UTC.csv"},
		{"start_year": 2023, "end_year": 2024, "filename": "moon-phases-2023-to-2024-UTC.csv"},
		{"start_year": 2024, "end_year": 2027, "filename": "moon-phases-2024-to-2027-UTC.csv"},
		{"start_year": 2024, "end_year": 2040, "filename": "moon-phases-2024-to-2040-UTC.csv"},
		{"start_year": 2024, "end_year": 2044, "filename": "moon-phases-2024-to-2044-UTC.csv"},
		{"start_year": 2024, "end_year": 2055, "filename": "moon-phases-2024-to-2055-UTC.csv"},
		]

FILES_W_ECLIPSES = [
		{"start_year":  601, "end_year": 700, "filename": "moon-phases-601-to-700-with-eclipses-UTC.csv"},
		{"start_year":  601, "end_year": 2100, "filename": "moon-phases-601-to-2100-with-eclipses-UTC.csv"},
		{"start_year":  601, "end_year": 4000, "filename": "moon-phases-601-to-4000-with-eclipses-UTC.csv"},
		]

# This is the month that occassionally has an extra day, so Dhul Hijjah sometimes has 29 or 30 days
KABS_MONTH = 12

HIJRI_MONTHS = {
		1: "Safar I", 2: "Safar II", 3: "Rabi I\t", 
		4: "Rabi II", 5: "Jumada I", 6: "Jumada II",
		7: "Rajab\t", 8: "Sha'ban", 9: "Ramadan", 
		10: "Shawwal", 11: "Dhul Qadah", 12: "Dhul Hij."
		}

HIJRI_MONTHS_DAYCOUNT = get_number_of_days_in_month()

HIRJI_START_YEAR = 622 # AD

# Add the 13th month: Muharram
HIJRI_MONTHS[13] = "Muharram"  		# Muharram is placed at end of year
HIJRI_MONTHS_DAYCOUNT[13] = 30
HIJRI_MONTHS[0] = "Muharram"  		# Muharram is placed at start of year
HIJRI_MONTHS_DAYCOUNT[0] = 30

MECCA_TIMEZONE = pytz.timezone('Asia/Riyadh')

"""
***************** PLEASE READ ************:
This limit is somewhat arbitrary. Change this as you see fit. I recommend a value from 0 to 0.5.

If the hirji calendar day is behind the full moon (gregorian) date by 0.1 days, the code will add an 
extra day in dhul hijjah. You'll notice, though, that I do not add an extra day even if the value 
falls under the limit if the year includes the Muharram month. This is because Muharram typically 
readjusts the hijri calendar to the Gregorian calendar in which adding the day actually overshoots 
the Hijri calendar.
"""
LIMIT_LUNAR_DAYS_OFF = 0.1 

SOLARYEAR_DAYS = 365.24219	# days


'''	-------- FUNCTIONS ------------ '''
def get_filename(start_year, end_year, contains_eclipse = False):
	""" Returns filename of the csv file with the given starting and ending year """
	
	_files = FILES_W_ECLIPSES if contains_eclipse else FILES

	for file in _files:
		if file["start_year"] == start_year and file["end_year"] == end_year:
			return file["filename"]

	raise FileNotFoundError

def parse_file(start_year, end_year):
	""" Reads file, recording entries only when it's a full moon """

	filename = "Moon phases CSV files/" + get_filename(start_year, end_year)

	entries = []
	with open(filename, "r") as csvfile:
		reader = csv.DictReader(csvfile)
		entries = list(filter(is_fullmoon, reader))

	print("\nFile parsed successfully\n")
	return entries

def parse_file_with_eclipses(start_year, end_year):
	""" Reads file, recording entries only when it's a full moon """

	filename = "Moon phases CSV files w eclipses/" + get_filename(start_year, end_year, True)

	entries = []
	eclipses = []

	with open(filename, "r") as csvfile:
		
		reader = csv.DictReader(csvfile)
		for row in reader:
			
			if row["phase"] != "Full Moon":
				if eclipse := row["eclipse"]:
					eclipses.append(eclipse)
				continue

			if eclipses != []:
				if entries[-1]["eclipse"] == "":
					entries[-1]["eclipse"] = ", ".join(eclipses)
				else:
					entries[-1]["eclipse"] = entries[-1]["eclipse"] + ", " + ", ".join(eclipses)
				eclipses = []
			
			entries.append(row)

			
	print("\nFile parsed successfully\n")
	return entries


'''	----------- MAIN -------------- '''

def main():

	'''	--------- GLOBALS* (*not really..) ------------ '''
	start_year = 601
	end_year = 4000
	# entries = parse_file(start_year, end_year)
	entries = parse_file_with_eclipses(start_year, end_year)
	entries_length = len(entries)


	def get_muharram_position(index, year):
		"""
			This checks if the given year contains a blue moon (or 13 full moons) and returns
			the position (1) if the blue moon occurs in the months 1 - 6 inclusive, 13 if in the 
			months 7 - 12 inclusive. Otherwise, if there is no Muharram month it will return -1.

			Note: This is defined within main so that it can access the variable 'entries'.
				It is not ideal to nest this function within main but it is less ideal to pass in the 
				large list 'entries'. It significantly slows down the program.
		"""
		_month_count = 1
		_index = index

		while(_month_count < 14):
			try:
				_start_month = datetime.strptime(entries[_index]["datetime"], DATEFORMAT).month
				_end_month = datetime.strptime(entries[_index + 1]["datetime"], DATEFORMAT).month
				_year = datetime.strptime(entries[_index]["datetime"], DATEFORMAT).year
			except:
				return -1

			if _year > year:
				return -1

			if _start_month == _end_month:
				return 1 if _month_count <= 6 else 13

			_month_count += 1
			_index += 1

		return -1	


	'''	--------- VARIABLES ------------ '''

	end_month = -1   		# Placeholder for the date of the end of the month
	hirji_year = 1  		# Hirji year
	lunar_days = 0   		# Number of days in the Hirji Calendar
	lunar_days_off = 0  	# Number of days difference between Hirji calendar and true full moon observations
	month_count = 0 		# Which month we're in, look at 'HIJRI_MONTHS'
	muharram_position = -1  # The position the month 'Muharram' falls into


	for i in range(entries_length):

		# If loop just started set start of month to Gregorian full moon date.
		if end_month == -1:
			start_month = datetime.strptime(entries[i]["datetime"], DATEFORMAT) + timedelta(days = 1)


		# Get start and end of calendar month from Gregorian (True i.e. observed Full Moon)
		gregorian_start_month = datetime.strptime(entries[i]["datetime"], DATEFORMAT)
		gregorian_end_month = datetime.strptime(entries[i + 1]["datetime"], DATEFORMAT)


		# Hijri Calendar only exists at and after 622 AD
		if gregorian_start_month.year < HIRJI_START_YEAR:
			continue;

		# Add month count
		month_count += 1
		# Get end of calendar month
		end_month = start_month + timedelta(days = HIJRI_MONTHS_DAYCOUNT[month_count])

		
		# -------------------------------- TIMEZONE ------------------------------------
		# Assign UTC to naive datetime objects
		start_month.replace(tzinfo=pytz.utc).astimezone(MECCA_TIMEZONE)
		end_month.replace(tzinfo=pytz.utc).astimezone(MECCA_TIMEZONE)
		gregorian_start_month.replace(tzinfo=pytz.utc).astimezone(MECCA_TIMEZONE)
		gregorian_end_month.replace(tzinfo=pytz.utc)

		# Convert to MECCA time zone
		start_month = start_month.astimezone(MECCA_TIMEZONE)
		end_month = end_month.astimezone(MECCA_TIMEZONE)
		gregorian_start_month = gregorian_start_month.astimezone(MECCA_TIMEZONE)
		gregorian_end_month = gregorian_end_month.astimezone(MECCA_TIMEZONE)

		
		"""
			Calculate the difference of the true full moon (Gregorian) from the (Hirji) calendar full moon
			You can either calculate deviation in the start of the month or the end of the month.
		"""
		# lunar_days_off = (end_month - gregorian_end_month).total_seconds() /(24 * 3600)
		lunar_days_off = (start_month - gregorian_start_month).total_seconds() /(24 * 3600)
			

		"""
			If it's kabs month (Dhul Hijjah) and its off by more than a day (note: we want to be off by 1 day because
			calendar month starts AFTER a full moon is observed barring occassional deviations) add an extra day. 
			This ensures no difference more than THREE whole days happens.
		"""
		# Adjust length of the month accordingly if it's KABS month
		if lunar_days_off <= LIMIT_LUNAR_DAYS_OFF and month_count == KABS_MONTH and muharram_position == -1:
			end_month += timedelta(days = 1)			# Add a day to the end of the month
			HIJRI_MONTHS_DAYCOUNT[KABS_MONTH] = 30  	# This is for printing purposes
		
		else:
			HIJRI_MONTHS_DAYCOUNT[KABS_MONTH] = 29


		if lunar_days_off > 3 or lunar_days < -3:
			print("\nTERMINATING PROGRAM: LUNAR DAYS MORE THAN THREE WHOLE DAYS OFF")
			print(f"\nLUNAR DAYS OFF: {lunar_days_off}")
			print("\n[FAILURE] Computing Hijri Calendar\n")
			sys.exit(1)

		# Keep track of lunar days
		lunar_days += HIJRI_MONTHS_DAYCOUNT[month_count]

		# Print Hijri Month
		print(f"{HIJRI_MONTHS[month_count]} {HIJRI_MONTHS_DAYCOUNT[month_count]} \t\t\t\t\t\t\t\t\t\t\t\t\t\t{entries[i]['eclipse']}")

		# Print the Gregorian date
		print(f"\tFull Moon Observed: "+ 
			f"{gregorian_start_month.strftime('%B %d, %Y')} - {(gregorian_end_month - timedelta(days=1)).strftime('%B %d, %Y')}")

		# Print the Hirji Calendar in Gregorian
		print(f"\tHijri (Gregorian) \t{start_month.strftime('%B %d, %Y')} - {(end_month - timedelta(days=1)).strftime('%B %d, %Y')}")

		# Print Hijri calendar Natural
		print(f"\tHijri (Natural): \t{HIJRI_MONTHS[month_count]} {1}, {hirji_year} - "
				+ f"{HIJRI_MONTHS[month_count]} {HIJRI_MONTHS_DAYCOUNT[month_count]}, {hirji_year}")
		
		# print("\t\t\t\t\t\tDays off:", lunar_days_off)
		print()


		# -------- END OF YEAR ---------
		if end_month.month == 1 and start_month.month != 1:

			# Check deviation of Hijri year (in days) from solar year
			if abs(SOLARYEAR_DAYS - lunar_days) > 30:
				print("\nTERMINATING PROGRAM: HIRJI YEAR IS OFF FROM SOLAR YEAR BY MORE THAN 30 DAYS")
				print("\n[FAILURE] Computing Hijri Calendar\n")

				sys.exit(2)

			upcoming_year = end_month.year

			# Exit if last year
			if upcoming_year == end_year: 	
				break;

			print(f"\n------------------------------- THE YEAR IS {upcoming_year} ------------------------------\n")
				

			hirji_year += 1
			lunar_days  = 0
			month_count = 0
			muharram_position = get_muharram_position(i, upcoming_year)

			# If Muharram is beginning of year shift all the months down
			if muharram_position == 1:
				month_count = -1

			# For debugging purposes
			print(f"Muharram position:", muharram_position); print()

		# Go the next month
		start_month = end_month


	print("\n[SUCCESS] Computing Hijri Calendar\n")



'''	------- EXECUTE MAIN ---------- '''
if __name__ == "__main__":
	main()