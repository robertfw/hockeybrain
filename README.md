# Hockey Brain

The hockey brain is made up of the following parts

## Event Log Importer

Imports statistics from NHL event logs. Uses BeautifulSoup for initial parsing

## Data Persistance Layer

## Event Query DSL

A DSL for querying NHL games in hockey terms.

## Standard Statistics Calculation

- corsi
- quality of competition
- tieing the above into line & team stats

## Pool Team API

An API for creating teams and assigning players to them,
and retrieving any related statistics

## Web interface

A web interface for all systems
- User creations
- Users teams
- Statistics query system
- Prebuilt statistics queries and views (team, pool team, line, etc)
- Ad-hoc query builder

## Extensions to DSL to support trending

Extend reports to identify players who are hot, cold, and changing

## Basic Game Prediction

Combine statistics and trends in a mathetmatical model for game prediction

## Future extensions

- Trade Analyser - suggests viable trades
- Automatic team management
- Social media parsing with NLP for sentiment analysis
- Parrallel, genetically driven, neural network game prediction

## Related links

[http://predictionmachine.com/](http://predictionmachine.com/)

[http://www.cs.toronto.edu/~lilien/lilien_projCH.html](http://www.cs.toronto.edu/~lilien/lilien_projCH.html)
