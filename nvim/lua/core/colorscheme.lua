local status, _ = pcall(vim.cmd, "colorscheme gruvbox")
if not status then
	print("F no funciona")
	return
end
