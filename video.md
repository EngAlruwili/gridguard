# Vertical video production plan

Format: 1080 x 1920 pixels, 9:16, 30 fps, H.264 MP4 with AAC audio.
Duration: 72 seconds. Narration: approximately 160 English words, natural student tone.
Use no background music, or add only music you have permission to use at a low level.

## Storyboard

| Time | What appears | Short English on-screen text | Transition |
|---|---|---|---|
| 00:00-00:08 | Transformer diagram; three monitored indicators | GridGuard / Read the warning signs | Fade in |
| 00:08-00:16 | Inputs, model, and dashboard cards | Open source. Explainable. Local. | Cut |
| 00:16-00:24 | Fictional load and ambient curves | Synthetic inputs / One fictional hot day | Cut |
| 00:24-00:32 | Loading and voltage plots with thresholds | Loading + voltage / Visible thresholds | Cut |
| 00:32-00:40 | Current comparison at 400 V and 380 V, fixed 500 kVA | Same kVA. Lower voltage. Higher current. | Cut |
| 00:40-00:48 | Ambient and temperature proxy curves | Thermal lag / Calculated proxy | Cut |
| 00:48-00:56 | Severity cards and explicit alert reasons | Every alert has a reason | Cut |
| 00:56-01:04 | Replay controls and rating sensitivity comparison | Replay. Compare. Test. | Cut |
| 01:04-01:12 | Source tree and invitation to review | Explore GridGuard / Repository link in the post | Fade out |

Full voice-over: `media/narration.txt`. Machine-readable scene timings and narration
parts: `media/storyboard.json`. Arabic translations appear only in
`media/subtitles_ar.srt`, kept as UTF-8. Each four-second cue corresponds to one
voice part; each scene contains two parts. The delivery renderer pads each voice
part into its four-second slot and only accelerates a clip if needed to fit.
For a fresh human recording, retime cues to the actual speech.

## Layout and caption direction

Use a dark navy background, white main text, teal chart lines, amber WATCH markers,
and red CRITICAL markers. Include text labels so color is not the only signal.
Keep a visible "SYNTHETIC DATA" label throughout the video. Label the thermal
output "proxy" and the asset "fictional".

Reserve the lower portion for Arabic captions: roughly y=1510-1710 at 1080 x 1920.
Leave at least 180 pixels at the bottom for platform overlays. Keep charts above
y=1450 and preserve side margins of at least 70 pixels.
Recommended fonts: **Noto Sans Arabic** or **IBM Plex Sans Arabic**, with proper
right-to-left shaping, white text on dark backing, and approximately 48-58 px text.
Use no more than two caption lines, and inspect Arabic punctuation visually.
Use English everywhere else, including the chart labels and title cards.

## Honest presentation

The supplied MP4 is a scripted animation of model outputs, not a browser screen
recording. It uses a synthetic English voice. No real asset, measured dataset,
accuracy result, university endorsement, or industrial deployment is implied.
The closing card points to the repository link in the post so no invented URL is
burned into the video. Insert the real repository URL in the post before publishing.
