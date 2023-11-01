fix:
	git add .
	git commit -m "$$(git status --porcelain)"
