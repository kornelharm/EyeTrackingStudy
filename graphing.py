from functools import partial
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import colorline as cl

def save_graph(image_file_name, x_line_sets, y_line_sets, c, cmaps, x_point_sets, y_point_sets, lims, title, x_label, y_label):
	fig, axes = plt.subplots()
	axes.set(title=title, xlabel=x_label, ylabel=y_label)
	axes.set_xlim([0, lims[0]])
	axes.set_ylim([0, lims[1]])
	for (x_line_set, y_line_set) in zip(x_line_sets, y_line_sets):
		cl.colorline(x_line_set, y_line_set, cmap=cmaps)
	for (x_point_set, y_point_set) in zip(x_point_sets, y_point_sets):
		plt.scatter(x_point_set, y_point_set, c=c, cmap=cmaps, s=15, marker="P", edgecolors=(0,0,0,0.3), linewidths=1.0)
	plt.savefig(image_file_name)
	plt.close(fig)

def show_graph(x_line_sets, y_line_sets, c, cmaps, x_point_sets, y_point_sets, lims, title, x_label, y_label):
	fig, axes = plt.subplots()
	axes.set(title=title, xlabel=x_label, ylabel=y_label)
	axes.set_xlim([0, lims[0]])
	axes.set_ylim([0, lims[1]])
	for (x_line_set, y_line_set) in zip(x_line_sets, y_line_sets):
		cl.colorline(x_line_set, y_line_set, cmap=cmaps)
	for (x_point_set, y_point_set) in zip(x_point_sets, y_point_sets):
		plt.scatter(x_point_set, y_point_set, c=c, cmap=cmaps, s=15, marker="P", edgecolors=(0,0,0,0.3), linewidths=1.0)
	plt.show()

def save_animation(animation_file_name, x_line_sets, y_line_sets, c, cmaps, x_point_sets, y_point_sets, lims, total_frames, frame_duration, loop_animation, title, xlabel, ylabel):
	fig, axes = plt.subplots()
	animation_func = partial(
		animate_n_datasets, 
		axes=axes,
		x_line_sets=x_line_sets, 
		y_line_sets=y_line_sets,
		c=c,
		cmaps=cmaps,
		x_point_sets = x_point_sets,
		y_point_sets = y_point_sets,
		lims = lims,
		xlabel=xlabel,
		ylabel=ylabel,
		title=title 
	)
	animation = ani.FuncAnimation(fig, animation_func, frames=total_frames, interval=frame_duration, repeat=loop_animation)
	writer = ani.PillowWriter(fps=30)
	animation.save(animation_file_name, writer=writer)
	plt.close(fig)

def show_animation(x_line_sets, y_line_sets, c, cmaps, x_point_sets, y_point_sets, lims, total_frames, frame_duration, loop_animation):
	fig, axes = plt.subplots()
	animation_func = partial(
		animate_n_datasets, 
		axes=axes, 
		x_line_sets=x_line_sets, 
		y_line_sets=y_line_sets,
		c=c,
		cmaps=cmaps,
		x_point_sets = x_point_sets,
		y_point_sets = y_point_sets,
		lims = lims
		)
	animation = ani.FuncAnimation(fig, animation_func, frames=total_frames, interval=frame_duration, repeat=loop_animation, blit=True)
	plt.show()

def animate_n_datasets(frame, axes, x_line_sets, y_line_sets, c, cmaps, x_point_sets, y_point_sets, lims, xlabel, ylabel, title):
	axes.clear()
	axes.set_xlim([0, lims[0]])
	axes.set_ylim([0, lims[1]])
	axes.set_title(title)
	axes.set_xlabel(xlabel)
	axes.set_ylabel(ylabel)
	for (x_line_set, y_line_set, cmap) in zip(x_line_sets, y_line_sets, cmaps):
		cl.colorline(x_line_set[:frame], y_line_set[:frame], cmap=cmaps)
	for (x_point_set, y_point_set) in zip(x_point_sets, y_point_sets):
		plt.scatter(x_point_set[:frame], y_point_set[:frame], c=c[:frame], cmap=cmaps, s=15, marker="P", edgecolors=(0,0,0,0.3), linewidths=1.0)