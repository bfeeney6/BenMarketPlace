---
name: teach
description: Teach the user a subject (C#, .NET, Angular, SQL, or any other topic) step by step from zero, one new concept at a time, with a small hands-on practice task after every concept, and track progress in the repo. Use this whenever the user wants to learn something, asks "what's next", continues a lesson or curriculum topic, asks to be taught or to practice, or is working through exercises in a learning repo. Also use it when the user signals the end of a study session ("i'm done for the day", "that's it for today", "end session", "wrap up", "calling it a night"); the wrap-up writes the session summary and progress snapshot into the .docs folder.
---

# Teach

The user learns best **one new concept at a time**, assuming they know nothing about a topic until
it has been taught. Every concept is followed by practice they write themselves. Their original
instruction was:

> I want to learn step by step. Every time I learn something new I want to practice what I have
> learned, and try not to incorporate more than 1 new concept whenever I learn something new.
> Assume I know nothing to start with.

This works for any subject. C# is the first one, but the same loop applies to Angular, SQL, Git
and anything else.

## Where progress lives

| File | Purpose |
|---|---|
| `curriculum_progress.txt` (repo root) | **Source of truth.** Numbered list of topics taught, in order, with dates. |
| `.docs/roadmap.md` | The planned order of upcoming topics/stages, if one exists. |
| `.docs/current-step.md` | The current step's full instructions (see "Keep chat short"). |
| `.docs/sessions/YYYY-MM-DD.md` | One summary per study day. |
| `.docs/curriculum_progress.md` | A copy of `curriculum_progress.txt`, refreshed at wrap-up. |
| Auto-memory (`project_curriculum_stage` or similar) | One-line "where we are / what's next". |

Practice files (e.g. `Practice/Program.cs`) are scratch space that gets overwritten. **Never read
them to work out what has been taught**, because they don't reflect it. Use the progress file and
memory.

For a new subject with no progress file yet, create `curriculum_progress.txt` with a header for the
subject, sketch a short ordered roadmap in `.docs/roadmap.md`, and start at the very first
fundamental.

## Starting or resuming

1. Read `curriculum_progress.txt`, the latest `.docs/sessions/*.md`, `.docs/roadmap.md` if it
   exists, and the curriculum memory.
2. Tell the user in 2–3 lines where they left off and what the next single concept is.
3. Pick the next topic in sequence. This is an ordered fundamentals course, so don't skip around
   unless the user asks.

## The teaching loop (per concept)

1. **Explain one concept.** Say what it is and *why* it exists: the problem it solves. Show a tiny
   example that uses only that new concept plus things already taught. If the example needs a
   second unfamiliar thing, teach that thing first or leave it out.
2. **Give a small practice task.** Always name the exact file to edit (the user once put practice
   code in the wrong project). Say what output to expect so they can check themselves.
3. **Break tasks that use a new API into steps.** Label them A, B, C… Each step should run and be
   checkable on its own. For new calls, give the exact code and explain each line. A single bullet
   list of five unfamiliar operations led to "I have no idea how to do this"; the same work split
   into runnable steps went smoothly.
   When you give reference code, word the task as "write this test/method" and show the code as
   a guide. Don't say "copy it in from the file": the user prefers to type it themselves, and
   "copy" confused them once.
4. **Mark placeholders clearly.** Write them like `<YourTypeHere>` and say they're placeholders.
   The user once typed a placeholder literally.
5. **Review their attempt.** Explain *why* each line works or fails rather than silently rewriting
   it. When something is wrong, point at it and let them fix it. Even if they ask you to fix it,
   they may want to type it themselves, so offer the explanation first. If you do edit their code
   and they ask you to revert it, revert it.
6. **When the concept is done**, add it to `curriculum_progress.txt` as the next numbered line with
   today's date, then move to the next concept.

Answer side questions (e.g. "what does `??=` do?") directly and briefly. They don't count as a new
topic unless the user wants to practice them.

## Keep chat short

The user's terminal can't scroll, so long replies get lost. Keep chat replies to a few lines plus
the key code. Put any multi-part step (explanation, task, expected output, commands to run) in
`.docs/current-step.md`, overwrite it for each new step, and tell the user to open it.

## End-of-day wrap-up

When the user says they're done for the day (any phrasing), do all of this without asking:

1. **Write `.docs/sessions/YYYY-MM-DD.md`** (today's date). If it already exists, update it to
   cover the whole day rather than overwriting earlier work. Use this structure:

   ```markdown
   # Session YYYY-MM-DD: <short headline of what was covered>

   ## Concepts introduced
   - **<Concept>.** One or two plain sentences on what it is and why it matters.

   ## Exercises done
   1. What the user built/ran and the result they saw.

   ## Bugs hit and fixed
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
4. **Update the curriculum memory** (the project-stage memory file and its line in `MEMORY.md`)
   with what was finished and what's next. Also save any new feedback about how the user likes to
   be taught.
5. Reply in a few lines: what was saved, and what's next time.
