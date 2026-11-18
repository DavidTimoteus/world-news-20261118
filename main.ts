// Saves the completed news graphic into the destination directory.
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
