from matplotlib import pyplot
import matplotlib.image as mpimg

def show(mouse_data):
    img = mpimg.imread('chrome_AHrwpCdnvIvxc.png')
    dpi = 100
    fig_width = img.shape[1] / dpi
    fig_height = img.shape[0] / dpi
    fig, ax = pyplot.subplots(figsize=(fig_width, fig_height), dpi=dpi)
    ax.imshow(img, extent=[0, img.shape[1], 0, img.shape[0]])

    x_data = [data[0] for data in mouse_data]
    y_data = [data[1] for data in mouse_data]

    x = [(data - min(x_data)) * img.shape[1] / (max(x_data) - min(x_data)) for data in x_data]
    y = [(data - min(y_data)) * img.shape[0] / (max(y_data) - min(y_data)) for data in y_data]

    ax.plot(x, y, color='red')
    pyplot.xlabel('X position')
    pyplot.ylabel('Y position')
    pyplot.title('Motiondata')
    pyplot.show()
