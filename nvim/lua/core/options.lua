local opt = vim.opt

-- numero de lineas
opt.relativenumber = true
opt.number = true

-- tabs e identacion
opt.tabstop = 2
opt.shiftwidth = 2
opt.expandtab = true
opt.autoindent = true

-- line wrap
opt.wrap = false

-- opciones de busqueda
opt.ignorecase = true
opt.smartcase = true

-- cursor line
opt.cursorline = false

-- backspace
opt.backspace = "indent,eol,start"
opt.background = "dark"

-- clipboard
opt.clipboard:append("unnamedplus")

-- split windows
opt.splitright = true
opt.splitbelow = true

opt.iskeyword:append("-")
