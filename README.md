# Mortal Kombat Lookup

### Contributors: Victoria Asencio-Clemens, Isaac Lake, and Ethan Vosburg

## Table of Contents
- **[Introduction](#introduction)**<be>
- **[Goals](#goals)**<br>
- **[Project Planning](#project-planning)**<br>

## External Links
- **[Customer Stories](main/docs/user_stories.md)**

## Introduction

For the group project, we will be building the back-end database for a popular video game, Mortal Kombat! For each player, we will track characters unlocked and xp. The read-and-write operations come into play when leveling up or selecting characters 
to equip.

The goal is to make a way to interface with a database to retrieve certain data about all of the different characters in the game. We would also like to add ways to compare characters and see if one might be better in certain circumstances. It would also be interesting to experiment with AI-driven features that would give us insight into how to interpret the information or clue us into how to act on it. 

> [!NOTE]
> **Mortal Kombat** is a street figher-like game that puts two players against each other with different characters that have different traits. The two players fight each other until one remains using different skills and abilities to defeat the opponent. 


## Goals
- Primary Goals
  - Store stats on characters in the game
  - Compare different characters
  - Section and filter characters
- Stretch Goals
  - Add AI analysis
  - add a front-end interaction element


## Project Planning
```mermaid
gantt
    title Mortal Kombat Lookup
    dateFormat  MM-DD-YYYY
    section Prototyping
    Explore Database Setup Options:a1, 04-08-2024, 2w
    Design Schema of Data:a2, 04-08-2024, 1w
    Explore Software Stack Options: after a2, 1w
    section Development
    Implementation of Code      :a3, after a1, 6w
    Database Design      :a4, after a1, 1w
    Website Development: after a4, 5w
    Website Front End Design: frontEnd, after a4, 2w
    Website Back End Design: backEnd, after frontEnd, 3w
    section Final Push
    Final Testing and Validation: after a3, 4w
    Testing Website: testing, after a3, 2w
    Deployment: after testing, 2w
```
