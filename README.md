# Counter
## Why?
	> I dont like how most of the counter has some sort of countdown time. 
	> I find that it is a source of distracting.
	> This can even process into a statistic record {keep track of number of distraction}

## What in it?
- All the data file (*.JSON)
- All the class, enum
- A run script

## USE:
	Currently, there will be 2 type of counter.
	a work counter and rest counter.
	when one terminate another one begin
- with the previous two counter time. If this is first call, it will prompt user to enter the value
	> ./count.py 

- Set the counter time using cmd
	> ./count.py WORK_COUNTER REST_COUNTER
	
## INPUT:
after use the call:
- enter 'start' to intitiate the counter.

**Set of input:**
	- *start: start the current counter*
	- *pause: pause the current counter and return the remain time*
	- *end: gracefully exit the process*

### must use end to terminate the session else: next time call start will resume from last pause
