from doreah.control import mainfunction

from . import filenames, duplicates

actions = {
	"n":filenames.main,
	"d":duplicates.main
}

@mainfunction({},flags=["dryrun","save_log"],shield=True)
def main(action,*args,**kwargs):
	if action in actions:
		actions[action](*args,**kwargs)
	else:
		print("Valid actions are:",*actions.keys())
