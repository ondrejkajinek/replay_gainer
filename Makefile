pylint:
	pylint gainer.py lock.py mpd_gainer.py gainers/ utils/

pylintOrDie:
	pylint gainer.py lock.py mpd_gainer.py gainers/ utils/ || (echo "Pylint failed, 'git commit' aborted" && exit 1)

gitHooksPreCommitEnable:
	# -r relative to link location
	ln -srf git/hooks/pre-commit .git/hooks/

gitHooksPreCommitDisable:
	rm -f .git/hooks/pre-commit
