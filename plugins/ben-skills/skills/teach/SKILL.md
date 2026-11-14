---
name: teach
description: Teach the user a subject (C#, .NET, Angular, SQL, cooking, or any other topic) step by step from zero, one new concept at a time, with a small hands-on practice task after every concept, and track progress in the user's Learning repo (bfeeney6/Learning), whichever repo the session is in. Use this whenever the user wants to learn something, asks "what's next", continues a lesson or curriculum topic, asks to be taught or to practice, or is working through exercises. Also use it when the user signals the end of a study session ("i'm done for the day", "that's it for today", "end session", "wrap up", "calling it a night"); the wrap-up writes the session summary and progress snapshot into that subject's .docs folder.
---

# Teach

The user learns best **one new concept at a time**, assuming they know nothing about a topic until
it has been taught. Every concept is followed by practice they do themselves. Their original
instruction was:

> I want to learn step by step. Every time I learn something new I want to practice what I have
> learned, and try not to incorporate more than 1 new concept whenever I learn something new.
> Assume I know nothing to start with.

This works for any subject: C#, Angular, SQL, Git, cooking, and so on.

## Progress always goes in the Learning repo

All progress for every subject lives in **one repo: `bfeeney6/Learning`**, even when the session
was started from a different repo (for example `bfeeney6/BenMarketPlace`). Never save progress in
the current repo unless it *is* the Learning repo.

Find it at the start of every session (call its path `$LEARN` below):

1. If the current repo's `git remote get-url origin` contains `bfeeney6/Learning` (any letter case),
   use the current repo.
2. Otherwise look for an existing clone: `../Learning`, `~/Learning`, `/home/user/Learning`.
3. Otherwise get it:
   - **Cloud/phone session:** call the `add_repo` tool with owner `bfeeney6`, repo `Learning`,
     access `push`, then run the clone command it returns.
   - **Laptop:** `git clone https://github.com/bfeeney6/Learning.git` next to the current repo.
4. If none of that works, tell the user plainly that progress can't be saved yet. Don't save it
   somewhere else instead.

Run git with `git -C "$LEARN" ...` so it always targets the Learning repo, not the current one.

## One folder per subject

Each subject has its own folder in the Learning repo, named in lowercase with hyphens (`csharp/`,
`angular/`, `cooking/`). Paths below are relative to that folder, e.g. `$LEARN/cooking/`.

| File | Purpose |
|---|---|
| `curriculum_progress.txt` | **Source of truth.** Numbered list of topics taught, in order, with dates. |
| `.docs/roadmap.md` | The planned order of upcoming topics/stages. |
| `.docs/current-step.md` | The current step's full instructions (see "Keep chat short"). |
| `.docs/sessions/YYYY-MM-DD.md` | One summary per study day. |
| `.docs/curriculum_progress.md` | A copy of `curriculum_progress.txt`, refreshed at wrap-up. |
| `.docs/where-we-are.md` | A few lines: where we are, what's next, and how the user likes to be taught. Replaces auto-memory, which doesn't survive between cloud/phone sessions. |
| `Practice/` | Scratch practice files (code subjects only). |

Keep the subject list in `$LEARN/README.md` up to date (one line per subject: folder and a short
description).

**Which subject?** Use the one the user names. If they don't name one ("what's next?"), use the
subject whose `.docs/sessions/` has the most recent file, and say which one you picked.

**New subject:** create its folder with `curriculum_progress.txt` (a header naming the subject),
a short ordered roadmap in `.docs/roadmap.md`, and `.docs/where-we-are.md`. Add it to the README.
Start at the very first fundamental.

## Saving progress (phone and cloud sessions)

The user studies on both a laptop and a phone. Phone sessions run in a throwaway cloud container
that gets deleted, so **anything not committed and pushed to GitHub is lost.** The user has given
standing permission (2026-11-14) to commit progress in the Learning repo and push it **straight to
`main`** every session, without asking and without a feature branch or pull request. This
permission covers the Learning repo only.

- **When resuming:** `git -C "$LEARN" checkout main && git -C "$LEARN" pull origin main` first, so
  you have the latest progress from the other device.
- **After each finished concept:** commit the subject folder (progress file, `.docs/`, practice
  files), then `git -C "$LEARN" push origin main`.
- **At wrap-up:** commit and push everything. Check the push actually worked and say so. If it
  failed, tell the user plainly, because their notes will be lost when the session ends.
- Use short commit messages such as `<subject>: <concept>` or `<subject>: session YYYY-MM-DD wrap-up`.

## Practice

**Code subjects on a phone:** the user can't open an editor or run code. They type their attempt
into the chat. You save it to the practice file, run it, and show them the output. Then review it
as usual. Don't write the solution for them. If a language's tools aren't installed in the
container (for example `dotnet` for C#), install them once at the start of the session.

**Hands-on subjects (e.g. cooking):** the practice is a small real task the user does away from the
screen, such as "make a basic omelette this week". Give the ingredients/tools, the steps, and what
"good" looks like so they can judge it themselves. Next time, ask how it went, help diagnose what
went wrong (too salty, burnt, runny...), and record it in the session notes. Mark the concept done
once they've tried the practice, or when they say to move on.

Practice files are scratch space that gets overwritten. **Never read them to work out what has
been taught**, because they don't reflect it. Use the progress file and `.docs/`.

## Starting or resuming

1. Find `$LEARN`, pull `main`, pick the subject, then read its `curriculum_progress.txt`, the latest
   `.docs/sessions/*.md`, `.docs/roadmap.md`, and `.docs/where-we-are.md`.
2. Tell the user in 2–3 lines where they left off and what the next single concept is.
3. Pick the next topic in sequence. This is an ordered fundamentals course, so don't skip around
   unless the user asks.

## The teaching loop (per concept)

1. **Explain one concept.** Say what it is and *why* it exists: the problem it solves. Show a tiny
   example that uses only that new concept plus things already taught. If the example needs a
   second unfamiliar thing, teach that thing first or leave it out.
2. **Give a small practice task.** Always name the exact file to edit for code (the user once put
   practice code in the wrong project). Say what result to expect so they can check themselves.
3. **Break tasks that use something new into steps.** Label them A, B, C… Each step should be
   checkable on its own. For new calls, give the exact code and explain each line. A single bullet
   list of five unfamiliar operations led to "I have no idea how to do this"; the same work split
   into runnable steps went smoothly.
   When you give reference code, word the task as "write this test/method" and show the code as
   a guide. Don't say "copy it in from the file": the user prefers to type it themselves, and
   "copy" confused them once.
4. **Mark placeholders clearly.** Write them like `<YourTypeHere>` and say they're placeholders.
   The user once typed a placeholder literally.
5. **Review their attempt.** Explain *why* each part works or fails rather than silently rewriting
   it. When something is wrong, point at it and let them fix it. Even if they ask you to fix it,
   they may want to type it themselves, so offer the explanation first. If you do edit their code
   and they ask you to revert it, revert it.
6. **When the concept is done**, add it to the subject's `curriculum_progress.txt` as the next
   numbered line with today's date, commit and push (see "Saving progress"), then move on.

Answer side questions (e.g. "what does `??=` do?") directly and briefly. They don't count as a new
topic unless the user wants to practice them.

## Keep chat short

The user's terminal can't scroll, so long replies get lost. Keep chat replies to a few lines plus
the key code. Put any multi-part step (explanation, task, expected result, commands to run) in the
subject's `.docs/current-step.md`, overwrite it for each new step, then send it to the user with the `SendUserFile` tool
(`display: "render"`) so they can read it in the app without going to GitHub. Do the same
whenever they ask to see a doc. If that tool isn't available, tell them the file's path.

## End-of-day wrap-up

When the user says they're done for the day (any phrasing), do all of this for each subject
studied today, without asking:

1. **Write `.docs/sessions/YYYY-MM-DD.md`** (today's date). If it already exists, update it to
   cover the whole day rather than overwriting earlier work. Use this structure:

   ```markdown
   # Session YYYY-MM-DD: <short headline of what was covered>

   ## Concepts introduced
   - **<Concept>.** One or two plain sentences on what it is and why it matters.

   ## Exercises done
   1. What the user did/made and the result they saw.

   ## Mistakes hit and fixed
   - **<Symptom>:** cause, then the fix.
     (Leave out this section if there were none.)

   ## Next session
   The next topic/step, plus any optional asides that came up.
   ```

   Write it from the conversation. Include the real mistakes and what fixed them, because those are
   the most useful notes to reread.
2. **Make sure `curriculum_progress.txt` is up to date** with every topic finished today.
3. **Copy `curriculum_progress.txt` to `.docs/curriculum_progress.md`** exactly. It's a reference
   snapshot; the `.txt` stays the source of truth.
4. **Update `.docs/where-we-are.md`** with what was finished and what's next. Also save any new
   feedback about how the user likes to be taught.
5. **Commit and push to `main` in the Learning repo.** Confirm the push succeeded.
6. Reply in a few lines: what was saved and pushed, and what's next time.
