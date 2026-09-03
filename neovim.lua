-- DANDADAN Neovim — Wallpaper 01: Okarun & Turbo Granny Golden Spark
return {
    { "tahayvr/sunset-drive.nvim", lazy = false, priority = 1000 },
    {
        "LazyVim/LazyVim",
        opts = {
            colorscheme = "sunsetdrive",
        },
    },
    {
        "LazyVim/LazyVim",
        opts = function(_, opts)
            vim.api.nvim_set_hl(0, "Normal",          { bg = "#14161E", fg = "#F0F4FC" })
            vim.api.nvim_set_hl(0, "Visual",          { bg = "#384166", fg = "#FFFFFF", bold = true })
            vim.api.nvim_set_hl(0, "Search",          { bg = "#F1FA8C", fg = "#090A0F", bold = true })
            vim.api.nvim_set_hl(0, "CurSearch",       { bg = "#E80202", fg = "#FFFFFF", bold = true })
            vim.api.nvim_set_hl(0, "IncSearch",       { bg = "#E80202", fg = "#FFFFFF", bold = true })
            vim.api.nvim_set_hl(0, "CursorLine",      { bg = "#1A1D2A" })
            vim.api.nvim_set_hl(0, "CursorLineNr",    { fg = "#E80202", bold = true })
            vim.api.nvim_set_hl(0, "LineNr",          { fg = "#7E859E" })
            vim.api.nvim_set_hl(0, "Comment",         { fg = "#7E859E", italic = true })
            vim.api.nvim_set_hl(0, "StatusLine",      { bg = "#1A1D2A", fg = "#F0F4FC" })
            vim.api.nvim_set_hl(0, "StatusLineNC",    { bg = "#0E1017", fg = "#7E859E" })
            vim.api.nvim_set_hl(0, "Pmenu",           { bg = "#1A1D2A", fg = "#F0F4FC" })
            vim.api.nvim_set_hl(0, "PmenuSel",        { bg = "#384166", fg = "#FFFFFF", bold = true })
            vim.api.nvim_set_hl(0, "PmenuThumb",      { bg = "#E80202" })
            vim.api.nvim_set_hl(0, "DiagnosticError", { fg = "#E3847B" })
            vim.api.nvim_set_hl(0, "DiagnosticWarn",  { fg = "#F1FA8C" })
            vim.api.nvim_set_hl(0, "DiagnosticInfo",  { fg = "#7AA2F7" })
            vim.api.nvim_set_hl(0, "DiagnosticHint",  { fg = "#00F5D4" })
        end,
    },
}
