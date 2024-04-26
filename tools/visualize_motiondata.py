from matplotlib import pyplot

def show(mouse_data):
    x = [data[0] for data in mouse_data]
    y = [data[1] for data in mouse_data]

    fig, ax = pyplot.subplots()
    ax.plot(x, y)

    # Reverse the y-axis limits
    ax.set_ylim(ax.get_ylim()[::-1])

    pyplot.xlabel('X position')
    pyplot.ylabel('Y position')
    pyplot.title('')

    pyplot.show()

show()