# Hockey Brain

The hockey brain is made up of the following parts

## Event Log Importer

This module takes care of downloading, storing, and parsing NHL event logs. It has a collection of
parsing functions to convert the various event type descriptions into meaningful, structured data.

Uses BeautifulSoup for DOM operations, and Requests for retrieving event logs.

## Data Persistance Layer

Stores game events in a queryable data store

## Event Query DSL

A DSL for querying NHL games in hockey terms.

## Statistics Calculation

- a variety of corsi statistics
- integration with quality of competition and line/team stats

## Leagues and teams

An API for creating teams and assigning players to them,
and retrieving any related statistics

## Web interface

A web interface for all systems
- User creations
- Users teams
- Statistics query system
- Prebuilt statistics queries and views (team, pool team, line, etc)
- Ad-hoc query builder

## Game Prediction

Uses trending data combined with quality of competition scores to predict game outcomes

## General Manager

- Identifies cold players on a team and finds suitable replacements
- Suggests trades when players are peaking

## Related links

[http://predictionmachine.com/](http://predictionmachine.com/)

[http://www.cs.toronto.edu/~lilien/lilien_projCH.html](http://www.cs.toronto.edu/~lilien/lilien_projCH.html)
