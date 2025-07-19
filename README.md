# AI
I made an ai chatbot and its talking to me via an lcd connected to an arduino. This is for Windows.
I added python and ngrok to my path. 
Essentially, here is what i do to start my project:
  1: plug in arduino to the laptop. ensure it is at the port COM9 (code is configured to COM9. You can change this in: device manager-> Ports -> Arduino Uno -> (right click) properties -> port settings -> advanced -> COM port number (9).)
  2: open windows powershell. (i have python as a PATH variable.) type in "cd Desktop\ChatbotLCD". I have a folder on my desktop called "ChatbotLCD".
  3: type "python serial_bridge.py". I have the serial bridge saved in the folder on my desktop. It is saved as "serial_bridge.py". i used VS Code to save the python file. You can use the notepad app.
  4: open a new tab in powershell. type "ngrok http 5000". (I have ngrok as a PATH variable). You should see something like "https://32b643aa110a.ngrok-free.app/". This is used later.
  5. Now, go to Render.com. click on "Deploy your app for free". sign in using whichever method you please. I used github. Click on "New Web Service" and click on "Existing Image". Open a new tab and do not alter this tab.
  6: In the new tab go to "n8n.io". Click on "Get started for free". On the sign in page, scroll down and click "Open installation docs". Click "Docker Installation Guide". Scroll down and copy "docker.n8n.io/n8nio/n8n". Do NOT just copy it from this page. it will still work just fine, i just think itd be funny for someone to go through all that trouble despite the link being right here.
  7: On render, under "Image URL", paste "docker.n8n.io/n8nio/n8n". Again, make sure you still visit n8n.io. It is funny to me. Now, press "connect". Scroll down and click on the free instance. Im broke so im using the free version. Scroll down and deploy the web service.
  8: Give it a few minutes and you should see a link that looks something like "https://n8n-jpa3.onrender.com". click on this link. If it doesnt work, you were too impatient, and you need to wait longer. 
  9: Now, sign in using whatever email you want. this isnt important because the web service will reset after inactivity. Click on "create workflow". 
  10: click on "Add first step". search for "chat trigger". Now, click on the "+" to the right of the chat trigger and search for "AI". hit "Ai Agent". Click on the "chat model" udder. type in "groq". Note: this isnt the same as "grok" which is the funny ai model on X.
  11: now, open a new tab. search "groq api keys". you should be on "https://console.groq.com/keys". Keep moving forward until you get an api key. Copy this key and store it on a random discord server that has noone else but you in it. Thats what i did.
  12: Now that you have a groq api key, go back to n8n, hit the "groq chat model" node under the ai agent cow, press "select credential", hit "create new credential", and paste the api key.
  13: Click on the Memory node under the Ai Agent and select simple memory.
  14: now, to the right of Ai Agent, click on the "+" sign. search for http request. Under method, change it to POST. For the URL, go back to your windows powershell, or whereever you used ngrok, and look for that link i mentioned earlier. It should look something like "https://32b643aa110a.ngrok-free.app/". DO NOT use mine. im actually serious this time; each link is different. copy this link and paste it into the URL section on n8n. after the link you should type /display. you should have something like "https://e42cae760d76.ngrok-free.app/display" as your URL.
  15: scroll down and turn on "Send Body". for "Body Content Type" select "JSON". for "Specify Body" select "Using Fields Below". for "Name" type in "message". for Value type in "{{ $node["AI Agent"].json["output"] }}"
  16: now, go back to "AI Agent". press "Add Option". choose "system message". type in "You are a helpful assistant. Keep message under 32 characters for lcd display.". 
You should be all set!!
  
