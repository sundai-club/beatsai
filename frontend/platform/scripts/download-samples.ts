const fs = require("fs");
const path = require("path");
const https = require("https");

const BASS_URL =
  "https://cdn.freesound.org/previews/648/648827_13033405-lq.mp3";
const DEMOS_DIR = path.join(process.cwd(), "public", "demos");

// Create demos directory if it doesn't exist
if (!fs.existsSync(DEMOS_DIR)) {
  fs.mkdirSync(DEMOS_DIR, { recursive: true });
}

// List of instruments that will use the bass sample
const instruments = ["drums", "bass", "keys", "vocals"];

// Download bass sample and copy it for each instrument
https
  .get(BASS_URL, (response) => {
    const bassPath = path.join(DEMOS_DIR, "bass.mp3");
    const fileStream = fs.createWriteStream(bassPath);

    response.pipe(fileStream);

    fileStream.on("finish", () => {
      console.log("Downloaded bass.mp3");
      fileStream.close();

      // Copy the bass file for other instruments
      instruments.forEach((instrument) => {
        if (instrument !== "bass") {
          fs.copyFileSync(bassPath, path.join(DEMOS_DIR, `${instrument}.mp3`));
          console.log(`Created ${instrument}.mp3`);
        }
      });
    });
  })
  .on("error", (err) => {
    console.error("Error downloading bass.mp3:", err.message);
  });
