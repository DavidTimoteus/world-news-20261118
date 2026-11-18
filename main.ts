// Saves the completed news graphic into the destination directory.
//
// A news picture is asked to do something that an ordinary illustration is not:
// it has to pin itself to one particular day. Without a plainly written date,
// a viewer has no way to tell whether the events shown happened this morning
// or decades ago, and the whole piece quietly stops being news at all. Naming
// the date up front turns a decorative image into a record. It anchors every
// headline, every colour and every small label to a moment that can be checked,
// so the picture stays honest even after it has travelled far from its source.
//
// That anchor matters even more because the day's stories rarely come from a
// single place. A conflict in one region, a strike in another, an election
// somewhere else and a discovery on a different continent can all share the
// same twenty-four hours. Bringing those threads into one frame is the whole
// point of a roundup: it reminds us that the world does not keep its problems
// in separate boxes. When a picture draws from many regions, it refuses the
// comfortable idea that only what is nearby counts, and it invites the reader
// to hold several distant realities in mind at once.
//
// Space, though, is scarce. Most people will glance at this graphic for only a
// second or two, and many will have missed the day's coverage entirely. Long
// sentences would be skipped; a short label survives the glance. A terse phrase
// beside each marker does the work of a headline without demanding a paragraph
// of attention. It gives the passing viewer just enough to recognise the story,
// to feel its weight, and to decide whether to look closer, all before the eye
// moves on. Brevity here is not laziness but respect for how people actually
// look at images.
//
// For the same reason the picture has to stand on its own. It will be shared
// as a file, stripped of the article around it, reposted with no caption, and
// viewed on screens of every size. Anything that needs an outside explanation
// is already lost. So the date, the place names, the labels and the colour key
// are all built into the pixels themselves. A self-contained image carries its
// own context wherever it goes, and it keeps making sense long after the page
// that first published it has been forgotten.
//
// There is a stricter reason to leave the finished image untouched. The judge
// does not look at a preview or a thumbnail; it reads the exact bytes of the
// file that is submitted. Any re-encoding, resizing or accidental resaving can
// change those bytes, and with them the fingerprint that proves which entry is
// which. That is why this helper copies the graphic across exactly as it was
// produced, without opening it, without filtering it and without letting a
// tool quietly "improve" it along the way. What the generator wrote is what
// the judge must receive, byte for byte.
//
// Keeping the generator beside the image serves a similar purpose of trust.
// The picture is the answer, but the source is the reasoning that produced it.
// If someone later asks why a label sits where it does, or why one story was
// given a particular colour, the code can answer. Storing the two together
// means the explanation cannot drift away from the result it explains, and it
// lets a curious reviewer follow the whole path from intention to pixels.
//
// Determinism is what makes that path repeatable. Given the same inputs, the
// generator is expected to draw the same picture every single time, with no
// reliance on the clock, random chance or the mood of a particular machine.
// A reproducible entry can be regenerated, compared and verified, so a doubt
// about the submitted file can be settled by drawing it again and matching the
// result. Without that guarantee the image would be a one-off accident, and no
// amount of careful copying could prove it was the same picture twice.
//
// Colour is the last piece of the language, and it is doing real work rather
// than decoration. Each shade is reserved for one kind of story so the eye can
// sort the frame before the mind reads a single word. Conflict is given a hot,
// urgent tone that reads as danger at a glance. Labour takes a grounded,
// steady hue that suggests work and solidarity. Politics is marked with a
// cooler, institutional colour, the kind that suits halls and ballots. Science
// uses a bright, forward-looking tint that hints at discovery and possibility.
// Society is coloured with a warmer, human shade that speaks of everyday life.
// Because the same meaning is kept for the same category throughout, a viewer
// learns the key once and then reads the whole image effortlessly, seeing at a
// glance where the fighting, the organising, the deciding, the discovering and
// the living are all happening on the same day.

// Let the picture carry the date itself, so it still reads correctly when viewed on its own later.
// Hand off the finished bytes untouched, since the judge grades the exact image that gets copied.
// Once rendered, drop the finished news image straight into the output folder.
// A dated visual snapshot distilling the day's world events into one image.
// Move the finished graphic into the destination folder associated with the mid-November 2026 imagery task.
// Copy the completed news image into the output directory for the 18 November 2026 news bounty.
// This sample entry bundles a local image asset and depends only on modules built into Node 22.
// A working news-image-daily entry (Node 22, standard library only): its image is the entry.png beside this file, and
// the program copies it to /output/entry.png. A starting point, not a winner: replace the image. The gate takes a
// whole PNG or JPEG of at most 1 MiB and 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
