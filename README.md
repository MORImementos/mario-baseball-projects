# Project-Rio-Scripts
This set of scripts all pertains to the Project Rio client, which is a client made for Mario Superstar Baseball (MSSB). The developers of the client added features such as stat tracking by reading the game's memory, outputted via JSON file. Recently, they created a RESTful API to upload statfiles to so that users could readily access their information. 

## project-rio-discord-bot
This is a bot for the MSSB discord that has a variety of commands. I helped create a cog (discord bot analog to a python class) that generates random teams, as well as other randomization features. The game's RNG seeding makes generating truly random teams problematic so I helped write scripts to do so.

## dme_reading
These files are scripts used to access and manipulate Dolphin Memory Engine, a tool used to read the game's memory and read and/or write to it. I created a GUI that displays certain values in real time, as well as a script that updates the team array in game with random values (done before the discord bot removed the need for it).

## local_statfile_scripts
These files are various local statfile scripts, used to parse json statfiles stored locally from the game. The files consolidate the information and present it in a more "baseball stat"-like format. Several of the scripts are able to iterate over all the json files in a directory, with various parameters.

## obsolete
These are files I once worked on but later files I wrote removed the need for them. 

## rioweb_api_scripts
This set of files is similar to local_statfile_scripts, in that it reads json data, consolidates it, and displays it in a user-friendly format, but instead of local files, it accesses the rioweb RESTful API where they have the data stored in a database. 

## statfile_validator
At the request of one of the Rio devs, I made a file that validates the statfiles produced by the client. At one point there were problems with the statfiles, so these scripts look for errors and indicate them. Additionally the files are compared against a json schema so for further validation. The error information can be printed either to the console or exported to a txt file.

## utils
This folder contains various helper functions or scripts. A couple of them are from other individuals (who I have credited at the top of the files).

## WIP
This just includes files I am still working on, at various stages of completion.