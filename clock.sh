#!/usr/bin/env bash

day=$(date +"%A")
time=$(date +"%I:%M %p")

printf '{"text":"󰥔 %s %s"}\n' "$day" "$time"
