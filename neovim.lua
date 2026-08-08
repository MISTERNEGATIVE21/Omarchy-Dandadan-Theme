-- DANDADAN Neovim — Wallpaper 48: Final Form Crimson & Cyber Teal
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
            vim.api.nvim_set_hl(0, "Visual",        { bg = "#E6282844" })
            vim.api.nvim_set_hl(0, "Search",        { bg = "#E6282855", fg = "#FFFFFF" })
            vim.api.nvim_set_hl(0, "CursorLine",    { bg = "#1A1C26" })
            vim.api.nvim_set_hl(0, "StatusLine",    { bg = "#E62828",    fg = "#FFFFFF" })
            vim.api.nvim_set_hl(0, "StatusLineNC",  { bg = "#1A1C26",    fg = "#616367" })
            vim.api.nvim_set_hl(0, "TabLineSel",    { bg = "#E62828",    fg = "#FFFFFF" })
            vim.api.nvim_set_hl(0, "TabLine",       { bg = "#14161E",        fg = "#616367" })
            vim.api.nvim_set_hl(0, "WinSeparator",  { fg = "#E6282866" })
            vim.api.nvim_set_hl(0, "FloatBorder",   { fg = "#E62828" })
            vim.api.nvim_set_hl(0, "DiagnosticError",   { fg = "#E62828"    })
            vim.api.nvim_set_hl(0, "DiagnosticWarn",    { fg = "#E68628"      })
            vim.api.nvim_set_hl(0, "DiagnosticInfo",    { fg = "#28E6E6" })
            vim.api.nvim_set_hl(0, "DiagnosticHint",    { fg = "#28C4E6" })
            vim.api.nvim_set_hl(0, "TelescopeSelection", { bg = "#E6282833", fg = "#F0F4FC" })
            vim.api.nvim_set_hl(0, "TelescopeBorder",    { fg = "#E62828" })
            vim.api.nvim_set_hl(0, "TelescopePromptBorder", { fg = "#E62828" })
        end,
    },
}
