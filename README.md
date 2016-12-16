# hop_suisse
Repository for ADA project

The project is run by a new team, obtained by merging two ADA teams 


- [Ondine Chanon](https://github.com/ochanon)
- [Maxime Peschard](https://github.com/maximepeschard)
- [Stefano Savarè](https://github.com/deatinor)
- [Gianrocco Lazzari](https://github.com/ggrrll)
- [Antonio Iubatti](https://github.com/antonioiubatti93)


## Working steps

Each step, described chronologically, corresponds to a folder. 
* [Project_proposal](https://github.com/maximepeschard/hop_suisse/blob/master/project_proposal/project_proposal_hop_suisse.md):
Describes guideline, goals and objectives of the project.
* Global_parsing: From datasport main page, make requests to extract all the names, dates and places of every running competition from, and the url links where to find the results.
    Done in the file: global_parsing.ipynb
    Dataset created: links2runs.csv
* Ranking_parsing: From every url link, get all the information about every specific race, that is all the information about every runner: name, age, category, ranking, pace, etc.
    Done in the file: parsing_datasport.ipynb
    Dataset created: temporarily [here](https://www.dropbox.com/s/tt9z5bik6uqndbz/full_database.csv?dl=0)
* Weather: From links2runs.csv consider every date and place and find the corresponding weather and temperature in order to do performance analysis with respect to the weather/temperature.
    Done in the files: weather.py and weather_utilis.py
    Dataset created, adding weather information to links2runs.csv: races-information-complete.csv
* Data_analysis: As the name says, this is where data analysis can be found!
