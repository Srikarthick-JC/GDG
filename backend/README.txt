Create a GEMINI_API_KEY

Open POWERSHELL  in the BACKEND

Use this code to add your API KEY

--------------------------------
setx GEMINI_API_KEY "YOUR_API_KEY_HERE"
--------------------------------

And run the python file app.py [BACKEND]

Then run the index.html page

Working of app.py :
    i]To simulate real time scenario , we have used the python to generate two metrics :
        1]Latency
        2]Output Size
    ii]We have specified a Baseline

    iii]Each time the python code generate a random Latency and Output Size

    iv]If they cross the baseline , the details are prompted to Gemini which displays the suggestion and reason .

