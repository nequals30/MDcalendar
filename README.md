# MDcalendar
This is a Python script to turn a Markdown "agenda" into an HTML calendar.

## How it Works (Calendar Rules)
These are the "rules" that define how the markdown calendar needs to be laid out. The idea is that there are very few rules. 

Only lines that start with `### ` or `+ ` have any special properties. Everything else will get parsed from markdown to html like normal.

Lines that have `---` (horizontal lines) will be ignored.

### Date Entries
Anything line that starts with `### ` starts a date entry. Anything below that line is consided part of that date entry. Some Examples:

```
### June 1
* Lunch with Steve
```

```
### 7/1/2019
- [ ] pay rent
* Dancing
```
### Recurring Events
Anything starting with a `+ ` is a recurring event. For example you can use it to keep track of birthdays:
```
+ 4/18 - bob's birthday
+ 4/22 - steve's birthday
+ 4/27 - steph's birthday
``` 

### Preface / To-Do List
Anything at the top of the file (before the first `### ` or `+ ` is displayed on top above the calendar. I use this for my todo list:

```
-[ ] todo 1
-[ ] todo 2

### mar 31
* task 1
...
```

## Result
The `mdcalendar.py` script does two things:
* It cleans up and organizes the markdown document and saves it to the location specified by the `mdOutPath` in the `mdCalendarConfig.py` file (which by default overwrites the original markdown file).
* It generates a calendar in HTML that looks like this: 

<img src="images/image_sample.png"></img>