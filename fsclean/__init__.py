from doreah.control import mainfunction

from . import filenames, duplicates

actions = {
	"n":filenames.main,
	"d":duplicates.main
}

@mainfunction({},flags=["dryrun","save_log"],shield=True)
def main(action,*args,**kwargs):
	actions[action](*args,**kwargs)
