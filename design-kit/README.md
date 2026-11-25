# Setup

Copy everything in this folder to the root of your website repo (keep `.github/` as is).

1. Edit the `TODO` in `AGENTS.md` to point at your real token/style files and component folders.
2. Settings > Branches > add a rule for `main`: require a pull request and one human approval.
3. Optional: add `.github/CODEOWNERS` so design-critical files need an owner's approval:
   ```
   /DESIGN_PRINCIPLES.md   @your-handle
   /AGENTS.md              @your-handle
   /src/styles/            @your-handle
   /src/components/        @your-handle
   ```

## How the AI check works (no CI needed)

AI coding tools read `AGENTS.md` / `CLAUDE.md` automatically, so they follow the rules
while building and must report their design decisions at the end.

To have AI review a change before pushing, tell your tool:
"Review my changes against DESIGN_PRINCIPLES.md and tell me what to simplify."

The PR template makes the author answer the design questions and attach screenshots.
The human reviewer then uses the same checklist.
