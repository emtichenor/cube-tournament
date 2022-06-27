.. _intro-overview:

==================
Cube Tournament Basics
==================

This program simulates tournaments where players compete against each other trying to set faster times solving a Rubik's Cube. 
Each match consists of two players completing 5 solves to create an "`average of 5 <https://www.speedsolving.com/wiki/index.php/Average>`_". 
These tournaments use the `double elimination format <https://en.wikipedia.org/wiki/Double-elimination_tournament>`_ where the general idea is that if
you lose twice you are eliminated from the tournament. To qualify for a tournament, each player completes 5 solves and then they are seeded into the tournament based on their average of 5.


Roster Creation
=================================

A roster needs to be generated for either mode. When creating a roster the program will ask you for basic info (name, age, save file name), roster size, and then
ask you how you want to generate the times for each player in the roster. However it is important to understand how a players times are generated:

Individual Player's Times
-----------------------
Each player has two variables, their expected score and their consistency. Times are generated using a `Normal Distribution <https://en.wikipedia.org/wiki/Normal_distribution>`_
Where their expected score is the mean or the midpoint of the curve and the consistency is the standard deviation. In simpler terms the expected score will
determine the average times and the consistency will determine how close or far away from the average each time is.

.. image:: images/Standard_deviation_diagram.png


Custom
-------------------
Choosing custom gives you the ability to set the variables for the roster. There are 4 variables to set:
*Expected score -  This is the 
Auto
-------------------

