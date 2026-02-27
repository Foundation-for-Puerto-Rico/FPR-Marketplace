# FPR Tools Marketplace

Plugin marketplace for Foundation for Puerto Rico editorial tools.

## Installation

### Add the marketplace

```
/plugin marketplace add Foundation-for-Puerto-Rico/FPR-Marketplace
```

### Install a plugin

```
/plugin install fpr-editorial-agent@fpr-tools
```

### Install Brand Voice

```
/plugin install brand-voice@fpr-tools
```

## Available Plugins

| Plugin | Description |
|--------|-------------|
| `fpr-editorial-agent` | Applies FPR style guide to DOCX documents with track changes |
| `brand-voice` | Enforces FPR brand voice across proposals, briefs, public comms, and community materials |

## Auto-provisioning

Add to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "fpr-tools": {
      "source": { "source": "github", "repo": "Foundation-for-Puerto-Rico/FPR-Marketplace" }
    }
  },
  "enabledPlugins": {
    "fpr-editorial-agent@fpr-tools": true,
    "brand-voice@fpr-tools": true
  }
}
```
