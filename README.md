# FPR Tools Marketplace

Plugin marketplace for Foundation for Puerto Rico editorial tools.

## Installation

### Add the marketplace

```
/plugin marketplace add FulanoXpr/FPR-Marketplace
```

### Install a plugin

```
/plugin install fpr-editorial-agent@fpr-tools
```

## Available Plugins

| Plugin | Description |
|--------|-------------|
| `fpr-editorial-agent` | Applies FPR style guide to DOCX documents with track changes |

## Auto-provisioning

Add to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "fpr-tools": {
      "source": { "source": "github", "repo": "FulanoXpr/FPR-Marketplace" }
    }
  },
  "enabledPlugins": {
    "fpr-editorial-agent@fpr-tools": true
  }
}
```
