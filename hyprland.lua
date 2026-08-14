local active_border_color = { colors = { "rgb(08F503)", "rgb(EF02F5)" }, angle = 45 }
local inactive_border_color = "rgba(61636780)"
local active_shadow_color = "rgba(08F50366)"
local inactive_shadow_color = "rgba(00000044)"


hl.config({
  general = {
    col = {
      active_border = active_border_color,
      inactive_border = inactive_border_color,
    },
  },
  group = {
    col = {
      border_active = active_border_color,
      border_inactive = inactive_border_color,
    },
  },
  decoration = {
    shadow = {
      enabled = true,
      range = 10,
      render_power = 4,
      color = active_shadow_color,
      color_inactive = inactive_shadow_color,
    },
  },
})
