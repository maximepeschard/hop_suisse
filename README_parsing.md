# Parsing

Desctiption of the dataframe obtained from scraping the [Datasport](https://www.datasport.com)
website.

The dataframe is available
[here](https://drive.google.com/file/d/0BypxDaHZHjhfNG9qbHA0NGJpbU0/view?usp=sharing).
We used the Pandas library with the Python 3.5 language.

## Features

### Race
> *dtype* object
>
> Name of the Race
>
> _not null_

### Date
> *dtype* object
>
> Date of the Race as String
>
> _not null_

### RaceYear
> *dtype* int64
>
> Year of the Race as int
>
> _not null_

### RaceMonth
> *dtype* int64
>
> Month of the Race as int
>
> _not null_

### Category
> *dtype* object
>
> Categoty of the Race - directly parsed from the Datasport website
>
> _not null_

### Distance
> *dtype* float64
>
> Distance run by the runner. Obtained as Time/Pace
>
> _not null_

### Name
> *dtype* object
>
> Name of the runner
>
> _not null_

### Sex
> *dtype* object
>
> Sex of the runner
> M or F
>
> _not null_

### Year
> *dtype* float64
>
> Year of birth of the runner
>
> _can be null_

### LivingPlace
> *dtype* object
>
> Living place of the runner
>
> _not null_

### Rank
> *dtype* int64
>
> Placement of the runner in the race
>
> _not null_

### Time
> *dtype* timedelta64
>
> Time taken by the runner. datetime.timedelta format
>
> _not null_

### Pace
> *dtype* timedelta64
>
> Pace of the runner. datetime.timedelta format.
>
> _not null_

### Place
> *dtype* object
>
> Place where the race is set.
>
> _not null_

### MinTemp
> *dtype* float64
>
> Minimum temperature the day of the race
>
> _can be null_

### MaxTemp
> *dtype* float64
>
> Maximum temperature the day of the race
>
> _can be null_

### Weather
> *dtype* object
>
> Description of the weather the day of the race
>
> _can be null_

### RaceID
> *dtype* object
>
> Unique identifier for the race. It is the link to the datasport race page.
>
> _not null_

### UserID
> *dtype* object
>
> Unique identifier for the User. Name + Year
> Not always correct. There can be 2 users with the same ID.
>
> _not null_
