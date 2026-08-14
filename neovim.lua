-- DANDADAN Neovim — Wallpaper 02: Turbo Granny Crimson Curse
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
            vim.api.nvim_set_hl(0, "Visual",        { bg = "#69000144" })
            vim.api.nvim_set_hl(0, "Search",        { bg = "#69000155", fg = "#FFFFFF" })
            vim.api.nvim_set_hl(0, "CursorLine",    { bg = "#1A1C26" })
            vim.api.nvim_set_hl(0, "StatusLine",    { bg = "#690001",    fg = "#FFFFFF" })
            vim.api.nvim_set_hl(0, "StatusLineNC",  { bg = "#1A1C26",    fg = "#616367" })
            vim.api.nvim_set_hl(0, "TabLineSel",    { bg = "#690001",    fg = "#FFFFFF" })
            vim.api.nvim_set_hl(0, "TabLine",       { bg = "#14161E",        fg = "#616367" })
            vim.api.nvim_set_hl(0, "WinSeparator",  { fg = "#69000166" })
            vim.api.nvim_set_hl(0, "FloatBorder",   { fg = "#690001" })
            vim.api.nvim_set_hl(0, "DiagnosticError",   { fg = "#690001"    })
            vim.api.nvim_set_hl(0, "DiagnosticWarn",    { fg = "#693300"      })
            vim.api.nvim_set_hl(0, "DiagnosticInfo",    { fg = "#006968" })
            vim.api.nvim_set_hl(0, "DiagnosticHint",    { fg = "#C05F58" })
            vim.api.nvim_set_hl(0, "TelescopeSelection", { bg = "#69000133", fg = "#F0F4FC" })
            vim.api.nvim_set_hl(0, "TelescopeBorder",    { fg = "#690001" })
            vim.api.nvim_set_hl(0, "TelescopePromptBorder", { fg = "#690001" })
        end,
    },
}
