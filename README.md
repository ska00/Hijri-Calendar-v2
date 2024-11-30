# A New (Solar-true) Hijri Calendar

## The New Hijri (Lunisolar) Calendar

This project introduces a new type of Hirji Calendar that remains in sync with the solar year (and therefore the Gregorian year). To achieve this a 13th month must be added every 2 to 3 years.
The Hijri months are (in order): Safar I, Safar II, Rabi I, Rabi II, Jumada I, Jumada II, Rajab, Sha'ban, Ramadan, Shawwal, Dhul Qadah, and Dhul Hijjah. Notice that the month 
Muharram has been removed from the traditional Hijri calendar; instead it has been replaced by Safar II, and Safar has been renamed to Safar I. The 13th month _is_ Muharram, which sometimes appears at the start of the 
year or at the end depending on when the gap between the solar year and lunar year diverge most. This keeps the Hijri months in their relative seasons (see the section below for more information).

Similar to the traditional Hijri (Islamic) calendar, the months officially start on the day after observing the new moon. Except that this new calendar starts on the day after the _full moon_ is observed.This means that the length of each month can vary from 29 to 30. Check out the file [hijri_calendar_observed.py](https://github.com/ska00/Hijri-Calendar-v2/blob/main/hijri_calendar_observed.py)

Look at [Example-Hijri-Calendar-Years-600-to-4000.txt](https://github.com/ska00/Hijri-Calendar-v2/blob/main/Example-Hijri-Calendar-Years-600-to-4000.txt) for an example of this calendar. _The years in filenames are Gregorian years_.

This Hirji Calendar accounts for years before its beginning on 622 A.D. Any year before 622 A.D is denoted with the suffix B.H. (Before Hirji) and any year after is denoted with H. (Hirji). This follows the same system as is used for B.C.E and C.E years. You can take a look of this system here: [Example-Hijri-Calendar-Years-1-to-800.txt](https://github.com/ska00/Hijri-Calendar-v2/blob/main/Example-Hijri-Calendar-Years-1-to-800.txt).

## Background: The Hijri (Islamic) Calendar

The traditional Hijri (also called Islamic) calendar, a lunar calendar, is always ~11 days short of the Gregorian (Solar) calendar. This leads to the Hijri months shifting little by little each year. For example, 
Ramadan would start in summer, then (with time) in spring, then in winter and fall until finally it starts again in summer after about 33 years. The issue is that the
Hijri years no longer represent _true_ years in the sense that years represent the passing of all the seasons and the reset of Earth's position relative to the sun. 
The Hijri (Islamic) calendar right now does not include the solar year in its calculations, something that must be accounted for. Some of the Hijri months are named 
with accordance to the season they appear in. For example, Rabi means spring in English. Take today's date: Rabi II 12, 1446 (October 16, 2024). According to the
Islamic calendar it is the second month of spring, but clearly this is incorrect as it is autumn. The disjunction of the seasons with the Hijri calendar
is what motivated this project.

### When is the 13th month added?

The month Muharram will sometimes appear at the end of the year or at the start depending
on when the gap between the seasons (i.e. the solar year) and the hijri (lunar) year becomes too large. To do this I did the following:
I looked for the Gregorian months in which two full moons occur (meaning a blue moon) and depending on that decided where to put
the Muharram month. If a blue moon happened in the first half of the year, Muharamm is placed at the start of the Hijri year, otherwise it is placed at the end.
An alternative would be to calculate the deviation of the lunar year (typically
having 354 or 355 days) from the solar year (365.24 days) and once the gap exceeds a certain amount (~22 days)
the extra month is placed again depending on whether this gap exceeded it's limit in the first half of the year or the second.

### A More Consistent Hirji Calendar (Experimental)

Look at [hijri_calendar_consistent.py](https://github.com/ska00/Hijri-Calendar-v2/blob/main/hijri_calendar_consistent.py) for an attempt at fixing the number of days of each Hijri month, thus making the calendar somewhat more predictable. However, since they are fixed, an additional day must sometimes be added to Dhul Hijjah (the 12th month). This also means that the beginning of the month does not always coincide with the full moon and might start sooner or later.



