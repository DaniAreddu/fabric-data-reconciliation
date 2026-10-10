# Talk scripts and timing

The session exists in two English editions. Both follow the same 40 slides, with four chapter dividers, nine Messina content slides and six questions to the audience. They differ in how much is said on each slide.

| Edition | Speech | Timing | Words before Q&A | Speech at 110 words/min | Estimated session |
|---|---|---|---:|---:|---:|
| 50-minute slot | [Speech](50min/Sofia_2026_English_50min_Speech.md) | [Timing](50min/Sofia_2026_English_50min_Timing.md) | 3,678 | 33:26 | 49:52 |
| Extended | [Speech](extended/Sofia_2026_English_Extended_Speech.md) | [Timing](extended/Sofia_2026_English_Extended_Timing.md) | 4,484 | 40:46 | 57:12 |

The estimated session adds, to the speech before Q&A: 2:51 of extra time on visuals, 0:39 for 39 slide changes, 2:30 for six short audience exchanges, 8:00 of Q&A including its invitation, 0:26 for the closing contacts and a 2:00 margin. These are estimates from word counts, not a timed rehearsal. The Extended edition needs a slot of about an hour; it does not fit 50 minutes.

The word counts and timings are recomputed from the speech files by `tests/test_materials.py`.

## How the scripts are written

Each speech is continuous prose, one paragraph per thought, with no slide headings and no sources in the spoken text. Sources appear once, in the bibliography at the end of each file. The Extended speech is the same text as the speaker notes in `presentations/Sofia_2026_English_Extended_Final.pptx`; a test compares them.

These Markdown files are the only editable copies of the speeches. If a speech changes, update the deck notes and the timing file with it.

The closing paragraphs were written before this repository was published. They say the pack is not yet at a public link and that the QR code opens LinkedIn. They are kept unchanged so the scripts stay identical to the speaker notes. The QR code on slide 40 does open the speaker's LinkedIn profile, not this repository.
