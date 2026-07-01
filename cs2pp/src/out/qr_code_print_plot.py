import matplotlib.pyplot as plt
import numpy as np

def print_to_plot(matrix: list[list[bool]], file_path) -> None:
    size = len(matrix)
    data = np.zeros((size, size), dtype=int)
    for r in range(size):
        for c in range(size):
            data[r, c] = 1 if matrix[r][c] else 0

    # format the image
    fig, ax = plt.subplots()
    ax.spines['top'].set_visible(False)  # hide the frame
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.xticks([])  # hide tics and their labels
    plt.yticks([])
    ax.set_aspect(1)  # make the shape square

    # create the image
    plt.imshow(data, cmap='Greys')
    if file_path is None:
        plt.show()
    else:
        plt.savefig(file_path)
    #plt.savefig("out/qr_code.png")

