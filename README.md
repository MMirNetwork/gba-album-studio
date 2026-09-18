# GBA Album Studio

### An open-source project by MMirNetwork

**Turn your music into a Game Boy Advance album — right in your browser.**

GBA Album Studio lets you choose songs, add cover artwork, arrange a tracklist, and create a single `.gba` file containing your album and its music player. It is made for people who enjoy music, retro handhelds, and making something personal. You do not need to know how to code to use the published website.

MMirNetwork creates this browser-based project edition. It builds on the work of the original GSM Player developers, whose credits and license notices are preserved below and in the application.

[Open the website](https://mmirnetwork.github.io/gba-album-studio/)

> **Deployment note:** This link is the intended project address. It will work once the project's build and deployment have completed successfully. Downloading the source files alone does not enable ROM export: the website must first be built using the included workflow.

## What can I make?

Create a personal mixtape, an album of your own music, or a collection of recordings for a Game Boy Advance music player.

You can:

- Add multiple **WAV, MP3 or FLAC** files.
- Set an **album name and artist name**.
- Add your own **JPG, PNG or WebP cover**.
- Choose a **240-color cover** or a **16-color retro look**.
- Rename tracks and put them in the order you want.
- Download the player and your music together as **one `.gba` file**.

Your music and pictures stay on your device. The application does not upload them to a conversion server.

## What is a `.gba` file?

A `.gba` file, often called a **ROM**, is a program a Game Boy Advance can run. In this project, it contains a music player, your cover, and your songs — not a commercial game.

You can open it in a compatible GBA **emulator**, such as [mGBA](https://mgba.io/). An emulator is an application that runs Game Boy Advance software on your computer.

To use it on an actual GBA, you need a compatible **flash cartridge**: a reusable cartridge that can load your own files. A normal retail game cartridge cannot simply be overwritten with this album.

## Make your first album

1. **Open the website** in a recent version of Chrome, Edge or Firefox.
2. **Name your album.** Enter an album name and an artist name.
3. **Choose a cover**, or keep the default artwork. Your picture is cropped from the center into a square.
4. **Add your music.** Click the file picker or drag WAV, MP3 or FLAC files into the track area.
5. **Arrange your tracks.** Edit their names and use the up/down arrows to change their order.
6. Click **Create GBA** and wait for processing to finish. Keep the page open.
7. Click **Download GBA** to save your finished album.
8. **Test it in mGBA first.** If you want to use real hardware, then follow your flash cartridge's instructions to copy the file onto it.

No account, command line or programming tools are needed to use the published application. Creating the album does not require a GBA BIOS file.

## Player controls

| Button | What it does |
| --- | --- |
| A or B | Pause or resume playback |
| Left / Right | Previous or next track |
| L / R | Seek backward or forward |
| SELECT | Lock or unlock the playback controls |
| Hold START | Show project information, album details and credits |

The information screen introduces **MMirNetwork's open-source project first**, followed by the album details and the original developers' credits. Release START to return to the player.

## What will it sound and look like?

This is a retro music player, not a high-fidelity audio format. Music is converted to **mono at 18157 Hz** using the lossy GSM codec. Expect a noticeable change in sound compared with the original files.

Cover images are reduced to **128 × 128 pixels** and a limited color palette. The same cover is used for the whole album.

The website's handheld display is an **illustrative preview**, not a running emulator. Check the exported file in an emulator to see and hear the actual result.

## Limits to keep in mind

| Item | Limit |
| --- | --- |
| Tracks per album | 99 |
| Finished ROM | 32 MiB |
| Each source audio file | 150 MiB and 15 minutes |
| Cover file | 20 MiB; decoded images are checked against a 50-megapixel limit |
| Album and artist names | 27 ASCII characters each |
| Track names | 59 ASCII characters before the internal file extension |

**ASCII** means the basic English letters, numbers and punctuation supported by the player. Accented letters are simplified where possible, German umlauts are written out, and unsupported characters are replaced. Periods in track names become hyphens. The website shows the exact exported title below each editable name.

A file's extension does not guarantee that your browser can decode every variant of its format. If an MP3 or FLAC file fails, try a current browser or convert it to a standard PCM WAV file.

Long files can require significant memory, especially on phones. The browser may allocate memory before the duration or image-dimension check can reject an oversized file. Start with a small album if you are unsure.

## Privacy and your files

- Music and covers are processed locally in your browser's memory.
- The application does not upload your media, use analytics, or require a login.
- The application does not save your album project in browser storage.
- **Reloading or closing the page clears your current setup.** Download your ROM before leaving.
- Loading the website still involves normal requests to its hosting provider. That is separate from uploading your music.
- The published application embeds its player and encoder; it does not need third-party browser scripts to convert your album.

Only use music and artwork you own or have permission to use. Making a ROM does not give you permission to distribute someone else's recordings or images.

## Common questions

### Do I need to install anything?

Not to create an album on the published website. You will need an emulator or suitable GBA hardware to play the downloaded file.

### Does this modify my original songs?

No. The application reads the files you select and creates a separate download.

### Why is “Create GBA” disabled?

Add at least one track first. If the page says **“One-time website build required,”** you are looking at the source preview rather than a fully built website. The person hosting it must complete the setup below.

### Why do I see a 404 page?

The project website may not have been deployed yet, or the wrong files may have been published. The maintainer should check that **Build GBA Album Studio and deploy Pages** completed successfully. A green run named only **pages-build-deployment** is not proof that the GBA player and encoder were built.

### Can I change the order without adding numbers to the titles?

Yes. The exported track order matches the order in the website.

### Can I give each song a different cover?

Not in this version. One cover is shared by the album.

### Can I stop a conversion?

Yes, use **Cancel**. Encoding can be stopped immediately. If the browser is currently decoding a file, cancellation takes effect when that operation returns. Your tracklist is kept.

### Does updating the website change ROMs I already downloaded?

No. A downloaded ROM is a standalone file. Create and download a new one to get updated player features or credits.

## Host your own copy — no local development tools required

This section is for people who want their own website, not people who only want to make an album.

GitHub can host the static website and perform its one-time build. **GitHub Actions** is GitHub's automation service: it runs the build instructions for you. **GitHub Pages** publishes the result as a website. There is no music-conversion server to maintain.

1. Create a GitHub repository, or use an existing copy of this project.
2. Upload the **extracted project files**, keeping their folders intact. Do not upload only the ZIP.
3. Make sure the hidden `.github` folder is included, especially `.github/workflows/pages.yml`.
4. Keep the website source at `web/index.html`, not just in the repository's top-level directory.
5. Open **Settings → Pages**. Under **Build and deployment → Source**, choose **GitHub Actions**. Do not select a Jekyll or Static HTML starter workflow; this project already provides its own.
6. Commit the files to `main`, `new-ui` or `web-ui`. The included workflow supports all three names. For another branch, add its name to the workflow's `branches` list.
7. Open **Actions → Build GBA Album Studio and deploy Pages** and wait for both the build and deployment to finish. The first build downloads and compiles tools, so it can take several minutes.
8. Find your website link under **Settings → Pages** or in the successful deployment job.

If you need to start a run manually, open the workflow and choose **Run workflow**. GitHub requires the workflow file to be present on the repository's default branch for that manual trigger to be available.

You do not need to provide a personal API key. Actions and Pages must be enabled for your repository; availability and any charges depend on your GitHub plan and usage.

### Updating an existing copy

Replace the matching files from the updated project package, keeping their paths. Commit them to your supported branch and let the workflow rebuild and redeploy. The scripts and tests matter too: copying only the English HTML will not change the GBA information screen.

Existing ROMs keep their old information screens. Export a new album after the updated website has been built.

### If the build fails

Open the failed run in **Actions**, open the red job, and expand the failed step. Include its actual error message when reporting a problem. Do not delete the tests or license checks just to obtain a green checkmark.

The complete compiled site is produced in `dist/`. Publishing the unbuilt `web/` directory will leave export disabled.

## Contribute

You do not have to be a programmer to help. Useful contributions include:

- Clear bug reports with your browser, operating system, steps to reproduce, and error message.
- Testing a small album in an emulator or on real hardware.
- Accessibility feedback and improvements to this guide.
- Suggestions for a simpler album-creation experience.
- Code improvements submitted through a pull request.

Do not attach copyrighted songs or private recordings to a public issue. Use a short recording or test tone you are allowed to share.

## For developers

The website is a single HTML file with inline styling and JavaScript. During the website build, the workflow:

1. Fetches the upstream player at commit `b159d5d415fd49efca50ff6d539d9b55487f0cce`.
2. Applies the cartridge, metadata, title-safety and project-info patches.
3. Compiles the GBA template with devkitARM/libgba.
4. Builds libgsm 1.0.24 as a single-file WebAssembly encoder using Emscripten 3.1.64.
5. Finds patch regions from the ELF symbols and validates their sizes and offsets.
6. Embeds the template, encoder and license notices in the website.
7. Runs the build-time tests and publishes the result to Pages.

For each album, WebAudio decodes and resamples the audio, a Web Worker performs GSM encoding, and JavaScript combines the patched template with a GBFS64 archive. Cover conversion uses RGB555 colors and 8 × 8 tiles, reserving palette entries 0–15 for the player.

Tracks are stored in the requested order. The GBFS directory is intentionally not alphabetically sorted because playback uses index-based access; generic binary-search lookup by filename is not suitable for these archives.

| Path | Purpose |
| --- | --- |
| `web/index.html` | Complete browser interface and album builder |
| `scripts/prepare-player.py` | Patches the pinned upstream player, including the START information screen |
| `scripts/build-player.sh` | Compiles the player inside the devkitPro container |
| `scripts/build-encoder.sh` | Compiles the WebAssembly encoder |
| `scripts/package-site.py` | Validates and embeds runtime assets and license notices |
| `tests/` | Packing, encoder, build and browser tests |
| `.github/workflows/pages.yml` | Automated build, tests and deployment |

Run the dependency-free source tests with:

```sh
node tests/test-web.cjs
```

Other tests need the compiled assets; the workflow installs its browser-test dependencies. The Chromium end-to-end test exercises WAV import, track ordering and ROM export. It is not a compatibility guarantee for every codec variant, browser or flash cartridge.

**Validation status:** Source-level and packaging checks have been run during preparation. A successful complete GitHub build and emulator/hardware playback have not been verified here. Confirm those before treating a release as tested. The devkitPro image currently uses `latest`; pin a verified image digest for reproducible releases.

## Credits and licenses

**GBA Album Studio — an open-source project by MMirNetwork.** This credit refers to the project edition and browser experience, not authorship of the underlying player or codec.

This project would not be possible without:

- **Damian Yerrick** — the original GSM Player for Game Boy Advance and its GBA-specific work.
- **Ben Wiley** — the [album-art and revised-interface fork](https://github.com/benwiley4000/gsmplayer-gba) used as the player base.
- **Jutta Degener and Carsten Bormann** — the [GSM codec implementation](https://www.quut.com/gsm/).
- **The Toast contributors** and other contributors acknowledged in the upstream source and notices.

Original copyright statements and license conditions are preserved. The built website includes the full collected upstream notices under **Third-party licenses & notices** and in `THIRD-PARTY-NOTICES.txt`. The GBA information screen displays the MMirNetwork project introduction first, with upstream credits beneath it.

**License status of the new project code:** This update does not choose or grant a new license for MMirNetwork's additions. The maintainer should add an explicit `LICENSE` for those additions before presenting their reuse terms as settled. Calling a project open source or publishing it on GitHub does not, by itself, grant redistribution or modification rights. Upstream components continue to be governed by their own licenses; a new project license must not replace those notices.

This project is not affiliated with or endorsed by Nintendo. Game Boy Advance is a Nintendo trademark.

This Readme was automatically generated.
