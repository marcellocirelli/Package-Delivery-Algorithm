# Package Delivery Optimization

This project implements a package delivery routing simulation focused on **efficient data structures and algorithmic optimization**.

The system models package storage, distance calculation, and delivery sequencing to meet timing and status requirements.

## Overview

The goal of this project is to simulate a delivery service that efficiently routes and delivers packages while tracking delivery status and mileage.  
The solution emphasizes correct algorithmic design, data structure selection, and time complexity awareness rather than UI or mapping visuals.

## Core Components

- **Hash Table**  
  Custom hash table implementation used to store and retrieve package data efficiently.

- **Distance Table**  
  Distance matrix used to calculate mileage between delivery locations.

- **Routing Logic**  
  Greedy-style algorithm used to determine delivery order and minimize total distance traveled.

## Features

- Loads package and distance data from CSV files
- Stores packages in a custom hash table
- Calculates total mileage traveled
- Tracks package delivery status over time
- Supports package lookup by ID at different timestamps
- Simulates real-world delivery constraints

## Technologies Used

- **Python**
- Custom data structures (hash table)
- CSV data parsing
- Algorithmic problem solving
- Time and state-based simulation

## Evaluation Criteria

This project demonstrates:
- Effective use of data structures for performance
- Algorithmic thinking and optimization
- Separation of concerns between data storage and logic
- Understanding of time complexity tradeoffs

## Purpose

The primary objective of this project is to apply core DSA concepts to a realistic logistics problem, emphasizing correctness, efficiency, and clarity of implementation.

## Notes

This project was developed and intended as an academic demonstration of routing and data structure concepts rather than a production logistics system.
