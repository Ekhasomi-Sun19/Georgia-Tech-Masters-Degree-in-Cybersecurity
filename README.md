# Georgia-Tech-Masters-Degree-in-Cybersecurity
This repo contains folders and file of tasks, projects, assignment, and coding exercise for the different courses completed throughout this program 

# Claude + Dataverse Setup

Connect Claude in VS Code to a Microsoft Dataverse environment on Windows.

Before you start

- Claude is already installed in VS Code.
- Open VS Code with right-click → **Run as administrator**.
- Use a **PowerShell** terminal (Terminal → New Terminal).
- Type only the command. Don't paste the `PS C:\...>` prompt text.

Use npm.cmd and npx.cmd

On most work machines PowerShell blocks plain `npm` and `npx` with the error "running scripts is disabled on this system." Adding `.cmd` avoids it. This guide uses `.cmd` throughout.

1. ## Install the Power Platform CLI

   ```
   winget install Microsoft.PowerAppsCLI
   ```

   Close VS Code and reopen it as administrator.
2. ## Install Node.js

   ```
   winget install OpenJS.NodeJS.LTS
   ```

   Close and reopen VS Code, then check that each command prints a version number:

   ```
   node -v
   npm.cmd -v
   npx.cmd -v
   ```
3. ## Install the Dataverse skills

   ```
   npx.cmd skills add microsoft/Dataverse-skills -s "*"
   ```

   Answer the prompts exactly like this:
   - Additional agentsType `claude`, press Space on Claude Code (○ becomes ●), then Enter
   - Installation scopeGlobal
   - Installation methodCopy to all agents

   Pressing Enter on the agent list without first pressing Space selects nothing, and the skills won't reach Claude.
4. ## Install the Power Platform skills

   ```
   npx.cmd skills add microsoft/power-platform-skills -s "*"
   ```

   Same answers: Claude Code, Global, Copy to all agents.
5. ## Confirm the skills are installed

   ```
   Get-ChildItem $HOME\.claude\skills
   ```

   You should see the `dv-...` folders plus the Power Platform skills. Then close and reopen VS Code.
6. ## Sign in to Power Platform

   ```
   pac auth create
   ```

   A browser opens. Sign in with your work account. Check the profile was created:

   ```
   pac auth list
   ```
7. ## Select your environment

   ```
   pac env list
   ```

   Find your environment and copy its URL, then select it:

   ```
   pac env select --environment https://yourorg.crm.dynamics.com/
   ```

   Confirm with `pac env list` (the `*` marks the active environment) or `pac org who`.
8. ## Test it

   Open Claude in VS Code and ask: *"List the tables in my Dataverse environment."*

## Troubleshooting

| Problem | Fix |
| --- | --- |
| "Running scripts is disabled on this system" | Use `npm.cmd` / `npx.cmd` instead of `npm` / `npx`. |
| `pac` or `node` "not recognized" | Close and reopen VS Code. If that doesn't work, restart the computer. |
| `.claude\skills` is missing or empty | Rerun the install. Make sure Claude Code is selected with Space and choose Copy to all agents. |
| "Get-Process: A positional parameter cannot be found" | The `PS C:\...>` prompt was pasted with the command. Type only the command. |
| Your environment isn't in `pac env list` | Your account doesn't have access. Ask your manager or Power Platform admin. |
