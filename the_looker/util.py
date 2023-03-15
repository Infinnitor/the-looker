import os


def get_all_files(p, add_path="", v=None):
	v = [] if v is None else v
	d = os.listdir(p)

	for x in d:
		x = os.path.join(p, x)
		if os.path.isdir(x):
			get_all_files(x, v=v)
		else:
			v.append(trim_path(x))

	return v


def trim_path(p):
	if p.startswith("./"):
		p = p[2:]
	return p

