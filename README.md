# OpenDataFinder
Chatbot interface to Government open data

Open Data Finder

I developed a working prototype chatbot for the Greater London Authority that extracts information from Government open data sources. The business objective is to enable London Datastore users who are not data specialists to “get straight to the answer” of their question without needing to download, open and investigate a csv or Excel file. The prototype is built using Python, Flask, Rasa and Pandas and demonstrates my experience with these technologies.

I created the prototype over a 6 week period in September and October 2019 on a voluntary basis. I presented the prototype and a final report to the London Datastore team in mid-October. The report will be used to evaluate possible applications of a chatbot approach and to evaluate it against other solutions to the same business problem.

A reference is available from the Senior Manager, City Data at Greater London Authority

The project provided me with an opportunity to create from scratch a chatbot using Python and Rasa, having already created a chatbot using JavaScript and the Microsoft LUIS natural language processing service for my Master’s Degree dissertation. The prototype is built with these technologies:

|      Technology    |     Description     |      Version    |
|--------------------|---------------------|-----------------|
|Rasa                |Chatbot framework    |1.2.8            |
|Python              |with venv virtual environment|3.6.8    |
|Python requests     |HTTP requests library|2.22.0           |
|Pandas              |Data analysis library|0.25.1           |
|Flask               |Web server           |1.1.1            |
|jinja2              |Web template engine  |2.10.1           |

		
The overall system is made up of 4 servers. I commissioned all of these servers in a Windows 10 development environment.

1. Web Server: Flask and jinja2 on port 8080. Based on Rasa webchat FAQ project available under GNU GPL licence  (github.com/yogeshhk/GSTFAQChatbot)

    To start the server in a Windows 10 venv development environment:
    $env:FLASK_ENV = "development"
    python -m flask run --host=0.0.0.0 --port=8080 --debugger

2. Rasa NLU and Rasa Core: standard installation with restaurant booking example template running on port 5005

    To train and start the Rasa servers in a venv development environment:
    rasa train
    rasa run -m models --enable-api --cors '*' --debug

3. Rasa Action Server for the custom actions (creating the Pandas query, extracting the response, and returning this to the user) running on port 5055

    To start the server in a venv development environment:
    rasa run actions --debug

4. Facebook Duckling server. The Duckling server is only used by the Rasa NLU server. This is run as a Docker Container (since the server is written in Haskell) running on port 8000
