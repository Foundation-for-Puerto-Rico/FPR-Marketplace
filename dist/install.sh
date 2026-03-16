#!/bin/bash
# FPR Skills — Manual Installer
# Usage: ./install.sh [skill-name]    Install one skill
#        ./install.sh --all           Install all skills
#        ./install.sh --list          List available skills

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

mkdir -p "$SKILLS_DIR"

list_skills() {
    echo "Available FPR skills:"
    echo ""
    for f in "$SCRIPT_DIR"/*.skill; do
        [ -f "$f" ] || continue
        name=$(basename "$f" .skill)
        size=$(du -h "$f" | cut -f1)
        installed=""
        [ -d "$SKILLS_DIR/$name" ] && installed=" [installed]"
        echo "  $name ($size)$installed"
    done
    echo ""
    echo "Usage:"
    echo "  ./install.sh <skill-name>   Install one skill"
    echo "  ./install.sh --all          Install all skills"
}

install_skill() {
    local name="$1"
    local file="$SCRIPT_DIR/${name}.skill"

    if [ ! -f "$file" ]; then
        echo "Error: skill '$name' not found in $SCRIPT_DIR"
        exit 1
    fi

    if [ -d "$SKILLS_DIR/$name" ]; then
        echo "Updating $name..."
        rm -rf "$SKILLS_DIR/$name"
    else
        echo "Installing $name..."
    fi

    mkdir -p "$SKILLS_DIR/$name"
    tar xzf "$file" -C "$SKILLS_DIR/$name" --strip-components=1
    echo "  ✓ $name → $SKILLS_DIR/$name"
}

case "${1:-}" in
    --list|-l|"")
        list_skills
        ;;
    --all|-a)
        echo "Installing all FPR skills..."
        echo ""
        for f in "$SCRIPT_DIR"/*.skill; do
            [ -f "$f" ] || continue
            install_skill "$(basename "$f" .skill)"
        done
        echo ""
        echo "Done! Restart Claude Code to activate."
        ;;
    --help|-h)
        list_skills
        ;;
    *)
        install_skill "$1"
        echo ""
        echo "Done! Restart Claude Code to activate."
        ;;
esac
