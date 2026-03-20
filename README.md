My ESP32 & Flask Security System 🛡️

What is this project?

I built this because I wanted to see if I could make a real-world security system using an ESP32 and a Python backend. Basically, you tap an RFID card, the hardware talks to my laptop over WiFi, and my laptop decides if you're allowed in or if the alarm should go off.

I did all of this on Linux Mint, which was a bit of a challenge with the networking, but I got it working!

🛠️ How it works (The Tech Stuff)

The Hardware: I used an ESP32 and an MFRC522 RFID reader.

The Backend: I wrote a server in Python using Flask.

The Database: I used SQLite and SQLAlchemy to save every single scan so I have a history of who tried to get in.

The Dashboard: I made a web page where I can see the logs in real-time and even turn off the alarm if it gets triggered.

🚀 Cool Features I added

The "Intruder" Logic: I programmed it so that my white Card gives "Access Granted," but my blue Tag is marked as an "Intruder." If the tag is scanned, the server triggers an alarm state.

Database Persistence: Even if I restart the server, all the scan history is saved in security.db.

Network Bridge: Since I’m using a virtual environment and a specific IP setup on my laptop, I had to configure a network bridge (10.112.185.239) so the ESP32 could actually find my Flask app.

Secrets Management: I didn't hardcode my WiFi password! I used a secrets.h file to keep my credentials safe.

📂 What’s in this Repo?

/Firmware: This is the C++ code I wrote in the Arduino IDE for the ESP32.

app.py: This is the brain of the project. It handles the logic, the database, and the web routes.

/templates: This holds the HTML for my security dashboard.

requirements.txt: A list of all the Python tools you need to run this yourself.

💡 What I learned

This project taught me a lot about Full-Stack IoT. I had to handle hardware wiring, C++ coding, Python backend logic, and Linux networking all at once. It wasn't always easy (especially getting the Flask modules to cooperate!), but seeing that "Access Granted" message pop up on my dashboard for the first time was a huge win.

🔧 How to run it

Flash the code in the /Firmware folder to your ESP32.

Make sure your laptop and ESP32 are on the same WiFi.

Run pip install -r requirements.txt.

Start the server with python3 app.py.

Open http://localhost:5000 in your browser to see the dashboard!

### 📺 See it in Action!

I’ve included a quick video and some photos of the hardware setup below so you can see exactly how the ESP32 communicates with the Flask server.

**Check out the demo video:**

https://github.com/user-attachments/assets/ac569322-bb71-480b-b946-78cf281117f5


**Hardware Setup:**


<img width="1366" height="768" alt="rfid terminal" src="https://github.com/user-attachments/assets/824e6428-47e5-482f-915e-994981827022" />

<img width="1366" height="768" alt="rfid denied" src="https://github.com/user-attachments/assets/9e370fdf-925e-4417-aaa9-f5fc1dee7f2d" />

<img width="1920" height="1080" alt="rfid" src="https://github.com/user-attachments/assets/1cba5027-96ae-494f-a2cc-476bc2e2f176" />

<img width="1366" h![rfid access denied pic](https://github.com/user-attachments/assets/abca441f-1645-4dd3-b8f5-df65e3614f9b)

eight="768" alt="rfid vs code terminal" src="https://github.com/user-attachments/assets/fa6d2424-c117-4552-b823-7ef60a8aff1f" />

![rfid access granted pic](https://github.com/user-attachments/assets/89cddbd8-9e06-4182-b793-db5bf4544550)

![rfid old project pic](https://github.com/user-attachments/assets/7cccf633-94c2-421c-a79f-d825eaae08e4)
