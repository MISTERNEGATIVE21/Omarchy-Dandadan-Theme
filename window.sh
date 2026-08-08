#!/usr/bin/env bash

MAX_TITLE_LEN=20

print_status() {
    window=$(hyprctl activewindow -j 2>/dev/null)
    address=$(jq -r '.address // empty' <<< "$window")

    # No active window -> show Desktop + Workspace
    if [[ -z "$address" || "$address" == "null" ]]; then
        ws=$(hyprctl activeworkspace -j | jq -r '.id // "1"')

        top_line="Desktop"
        bottom_line="Workspace $ws"

        esc_top=$(sed 's/&/&amp;/g; s/</&lt;/g; s/>/&gt;/g' <<< "$top_line")
        esc_bottom=$(sed 's/&/&amp;/g; s/</&lt;/g; s/>/&gt;/g' <<< "$bottom_line")

        text="<span size='7500' foreground='#a6adc8' rise='-2000'>$esc_top</span>\n<span size='9000' weight='bold' foreground='#ffffff'>$esc_bottom</span>"

        jq -nc \
            --arg text "$text" \
            --arg tooltip "$bottom_line" \
            '{text: $text, tooltip: $tooltip, class: "empty"}'
        return
    fi

    class=$(jq -r '.class // empty' <<< "$window")
    title=$(jq -r '.title // empty' <<< "$window")

    esc_class=$(sed 's/&/&amp;/g; s/</&lt;/g; s/>/&gt;/g' <<< "$class")
    esc_title=$(sed 's/&/&amp;/g; s/</&lt;/g; s/>/&gt;/g' <<< "$title")

    if ((${#esc_title} > MAX_TITLE_LEN)); then
        truncated_title="${esc_title:0:$MAX_TITLE_LEN}…"
    else
        truncated_title="$esc_title"
    fi

    text="<span size='7500' foreground='#E1477A' rise='-2000'>$esc_class</span>\n<span size='9000' weight='bold' foreground='#F0F4FC'>$truncated_title</span>"

    jq -nc \
        --arg text "$text" \
        --arg tooltip "$class — $title" \
        '{text: $text, tooltip: $tooltip, class: "active"}'
}

print_status
