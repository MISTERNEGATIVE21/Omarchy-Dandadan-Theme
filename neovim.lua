-- DANDADAN Neovim — Wallpaper 41: Thunder God Battle Scarlet
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
            vim.api.nvim_set_hl(0, "Visual",        { bg = "#CB1F2E44" })
            vim.api.nvim_set_hl(0, "Search",        { bg = "#CB1F2E55", fg = "#FFFFFF" })
            vim.api.nvim_set_hl(0, "CursorLine",    { bg = "#1A1C26" })
            vim.api.nvim_set_hl(0, "StatusLine",    { bg = "#CB1F2E",    fg = "#FFFFFF" })
            vim.api.nvim_set_hl(0, "StatusLineNC",  { bg = "#1A1C26",    fg = "#616367" })
            vim.api.nvim_set_hl(0, "TabLineSel",    { bg = "#CB1F2E",    fg = "#FFFFFF" })
            vim.api.nvim_set_hl(0, "TabLine",       { bg = "#14161E",        fg = "#616367" })
            vim.api.nvim_set_hl(0, "WinSeparator",  { fg = "#CB1F2E66" })
            vim.api.nvim_set_hl(0, "FloatBorder",   { fg = "#CB1F2E" })
            vim.api.nvim_set_hl(0, "DiagnosticError",   { fg = "#CB1F2E"    })
            vim.api.nvim_set_hl(0, "DiagnosticWarn",    { fg = "#CB651F"      })
            vim.api.nvim_set_hl(0, "DiagnosticInfo",    { fg = "#1FCBBB" })
            vim.api.nvim_set_hl(0, "DiagnosticHint",    { fg = "#D4A823" })
            vim.api.nvim_set_hl(0, "TelescopeSelection", { bg = "#CB1F2E33", fg = "#F0F4FC" })
            vim.api.nvim_set_hl(0, "TelescopeBorder",    { fg = "#CB1F2E" })
            vim.api.nvim_set_hl(0, "TelescopePromptBorder", { fg = "#CB1F2E" })
        end,
    },
}
