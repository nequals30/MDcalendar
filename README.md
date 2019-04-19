# MDcalendar
This is a Python script to parse a Markdown agenda into an HTML calendar.

## The Rules

### Dates
Anything that starts with `### ` is considered a date entry. Some Examples:

```
### June 1
* Lunch with Steve
```

```
### 7/1/2019
- [ ] pay rent
* Dancing
```

Anything before the first `###` is displayed on top above the calendar. I use this for my todo list:

```
-[ ] todo 1
-[ ] todo 2

### mar 31
* task 1
...
```


