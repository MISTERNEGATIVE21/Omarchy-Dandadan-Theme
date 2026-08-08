-- DANDADAN Neovim — Wallpaper 01: Okarun & Turbo Granny Golden Spark
-- Uses sunset-drive as base; overrides accent colors dynamically
return {
    { "tahayvr/sunset-drive.nvim", lazy = false, priority = 1000 },
    {
        "LazyVim/LazyVim",
        opts = {
            colorscheme = "sunsetdrive",
        },
    },
    -- Optional: override highlights for per-wallpaper accent
    {
        "LazyVim/LazyVim",
        opts = function(_, opts)
            vim.api.nvim_set_hl(0, "Normal",        { bg = "#14161E",     fg = "#F0F4FC"  })
            vim.api.nvim_set_hl(0, "Visual",        { bg = "#08F50344" })
            vim.api.nvim_set_hl(0, "Search",        { bg = "#08F50355", fg = "#FFFFFF" })
            vim.api.nvim_set_hl(0, "CursorLine",    { bg = "#1A1C26" })
            vim.api.nvim_set_hl(0, "StatusLine",    { bg = "#08F503",    fg = "#FFFFFF" })
            vim.api.nvim_set_hl(0, "StatusLineNC",  { bg = "#1A1C26",    fg = "#616367" })
            vim.api.nvim_set_hl(0, "TabLineSel",    { bg = "#08F503",    fg = "#FFFFFF" })
            vim.api.nvim_set_hl(0, "TabLine",       { bg = "#14161E",        fg = "#616367" })
            vim.api.nvim_set_hl(0, "WinSeparator",  { fg = "#08F50366" })
            vim.api.nvim_set_hl(0, "FloatBorder",   { fg = "#08F503" })
            vim.api.nvim_set_hl(0, "DiagnosticError",   { fg = "#08F503"    })
            vim.api.nvim_set_hl(0, "DiagnosticWarn",    { fg = "#02F576"      })
            vim.api.nvim_set_hl(0, "DiagnosticInfo",    { fg = "#EF02F5" })
            vim.api.nvim_set_hl(0, "DiagnosticHint",    { fg = "#EA0B08" })
            vim.api.nvim_set_hl(0, "TelescopeSelection", { bg = "#08F50333", fg = "#F0F4FC" })
            vim.api.nvim_set_hl(0, "TelescopeBorder",    { fg = "#08F503" })
            vim.api.nvim_set_hl(0, "TelescopePromptBorder", { fg = "#08F503" })
        end,
    },
}
