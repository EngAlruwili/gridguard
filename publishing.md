# Publish the repository and demonstration

## GitHub

Install Git, sign in to GitHub, and create an empty repository named `gridguard`.
Do not initialize that remote with a README or license. Replace YOUR_USERNAME below.
Run these commands inside the delivered `gridguard` folder, not its parent workspace.

```bash
git init
git branch -M main
git add .
git status
git diff --cached --stat
git commit -m "Build GridGuard educational transformer monitor"
git remote add origin https://github.com/YOUR_USERNAME/gridguard.git
git push -u origin main
```

If Git requests an identity, configure your own name and email locally before
committing. Authenticate with your usual GitHub credential method; never commit
tokens or passwords. Review staged files before the commit. Add the description
and topics from `docs/github.md`. GitHub Actions will run only after the workflow
is pushed; a local passing test run is not a claim that remote CI passed.

## Record the actual dashboard

1. Install dependencies, run tests, and launch Streamlit using the README commands.
2. In a screen recorder such as OBS Studio, record the browser window with the
   synthetic-data banner visible. Use a clean browser profile and hide private tabs.
3. Capture the default combined-stress case, a replay progression, the typical day,
   both voltage disturbance cases, and the fixed-demand rating comparison.
4. Use a vertical 1080 x 1920, 30 fps project in a video editor you already have.
   Crop individual charts and metrics instead of shrinking an entire desktop screen.
5. Follow the nine scenes in `docs/video.md`. Record the English narration at a
   natural pace, then align each scene to the voice. The target length is 72 seconds.
6. Import `media/subtitles_ar.srt` as UTF-8. It is timed for the supplied scripted
   demo. If you re-record or edit the narration, retime every cue to the new audio.
7. Use Noto Sans Arabic or IBM Plex Sans Arabic if available, enable RTL shaping,
   and inspect mixed punctuation and numerals. Use white text on a dark backing,
   around 48-58 px at 1080-pixel width, maximum two lines. Keep subtitles around
   y=1510-1710 and leave the bottom 180 pixels clear of essential information.
   Reserve that area in the composition so subtitles do not cover charts.
8. Export H.264 MP4 with AAC audio, 1080 x 1920, 9:16. Check the full video on a
   phone, including text readability, cropping, audio level, and subtitle timing.

## Supplied demonstration video

The separate delivery MP4 uses rendered cards and charts calculated by GridGuard,
with a synthetic English Windows voice and burned-in Arabic subtitles. It is an
animation, not a screen recording of Streamlit. The SRT remains editable. It does
not show a real asset or claim actual deployment. Replace it with your own voice
and dashboard footage if you prefer a more personal student presentation.
The rendered video uses Noto Sans Arabic with right-to-left text shaping.
Noto Sans Arabic or IBM Plex Sans Arabic are the preferred editing options.
Fonts are not redistributed in the repository.

## LinkedIn

After publishing the repository, update its real URL in `docs/linkedin.md`.
Upload the video manually, paste the reviewed post, and preview it before publishing.
The supplied video already has visible Arabic subtitles; avoid adding a second
overlapping visible subtitle layer. Keep the editable SRT for future revisions.
Add a thumbnail that says "GridGuard | Synthetic-data demo" and check that the
post makes the project's educational scope clear. No actual upload or publication
has been performed as part of this delivery.
