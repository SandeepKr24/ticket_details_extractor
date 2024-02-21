Ticket Details Extractor

Here is a demo-

https://github.com/SandeepKr24/ticket_details_extractor/assets/94790806/dc7c995a-8bff-40bb-b322-08dda098f9b8

For some reason, my screen recorder did not capture the chrome tab that the script opened to extract the station names and codes :(

Steps to run-
1) Install Python
2) Install the required dependencies and libraries (refer requirements.txt) ~use this command if you have pip installed - pip install requirements.txt
3) Edit the 'pdf_path' variable in the file 'fetch_details.py' with the actual path to your ticket pdf
4) Run the file 'to_json.py', this will create a new file 'output.json' which will contain all the key details.

PS- I encourage you to extract the text from the pdfs and then experiment with it on regex101.com by writing different expressions yourself.
Feel free to reach out to me: sandeep.workmail24@gmail.com with any suggestions on how I can further improve this.

Also, I am currently working on extending this functionality to flight boarding pass and bus tickets aswell. (stay connected here for further updates)
