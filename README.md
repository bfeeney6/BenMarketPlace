# BenMarketPlace

Personal Claude Code plugin marketplace.

## Install
```
/plugin marketplace add bfeeney6/BenMarketPlace
/plugin install ben-skills@ben-marketplace
```

## Use in a project (incl. Claude Code on web/phone)
Add to the project's `.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": {
    "ben-marketplace": { "source": { "source": "github", "repo": "bfeeney6/BenMarketPlace" } }
  },
  "enabledPlugins": { "ben-skills@ben-marketplace": true }
}
```

## Updating
Edit skills under `plugins/ben-skills/skills/`, bump `version` in `plugins/ben-skills/.claude-plugin/plugin.json`, push, then run `/plugin marketplace update ben-marketplace`.
