import numpy as np
# import PIL.Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm
# lowest = -1.0
lowest = 0.0
highest = 1.0

# --------------------------------------
# Color maps ([-1,1] -> [0,1]^3)
# --------------------------------------


def heatmap(x):

    x = x[..., np.newaxis]

    # positive relevance
    hrp = 0.9 - np.clip(x-0.3, 0, 0.7)/0.7*0.5
    hgp = 0.9 - np.clip(x-0.0, 0, 0.3)/0.3*0.5 - np.clip(x-0.3, 0, 0.7)/0.7*0.4
    hbp = 0.9 - np.clip(x-0.0, 0, 0.3)/0.3*0.5 - np.clip(x-0.3, 0, 0.7)/0.7*0.4

    # negative relevance
    hrn = 0.9 - np.clip(-x-0.0, 0, 0.3)/0.3*0.5 - np.clip(-x-0.3, 0, 0.7)/0.7*0.4
    hgn = 0.9 - np.clip(-x-0.0, 0, 0.3)/0.3*0.5 - np.clip(-x-0.3, 0, 0.7)/0.7*0.4
    hbn = 0.9 - np.clip(-x-0.3, 0, 0.7)/0.7*0.5

    r = hrp*(x >= 0)+hrn*(x < 0)
    g = hgp*(x >= 0)+hgn*(x < 0)
    b = hbp*(x >= 0)+hbn*(x < 0)

    return np.concatenate([r, g, b], axis=-1)


def graymap(x):

    x = x[..., np.newaxis]
    return np.concatenate([x, x, x], axis=-1)*0.5+0.5

# --------------------------------------
# Visualizing data
# --------------------------------------

# def visualize(x,colormap,name):
#
#     N = len(x)
#     assert(N <= 16)
#
#     x = colormap(x/np.abs(x).max())
#
#     # Create a mosaic and upsample
#     x = x.reshape([1, N, 29, 29, 3])
#     x = np.pad(x, ((0, 0), (0, 0), (2, 2), (2, 2), (0, 0)), 'constant', constant_values=1)
#     x = x.transpose([0, 2, 1, 3, 4]).reshape([1*33, N*33, 3])
#     x = np.kron(x, np.ones([2, 2, 1]))
#
#     PIL.Image.fromarray((x*255).astype('byte'), 'RGB').save(name)


def plt_vector(x, colormap, num_headers):
    N = len(x)
    assert (N <= 16)
    len_x = 54
    len_y = num_headers
    # size = int(np.ceil(np.sqrt(len(x[0]))))
    length = len_y*len_x
    data = np.zeros((N, length), dtype=np.float64)
    data[:, :x.shape[1]] = x
    data = colormap(data / np.abs(data).max())
    # data = data.reshape([1, N, size, size, 3])
    data = data.reshape([1, N, len_y, len_x, 3])
    # data = np.pad(data, ((0, 0), (0, 0), (2, 2), (2, 2), (0, 0)), 'constant', constant_values=1)
    data = data.transpose([0, 2, 1, 3, 4]).reshape([1 * (len_y), N * (len_x), 3])
    return data
    # data = np.kron(data, np.ones([2, 2, 1])) # scales


def add_subplot(data, num_plots, plot_index, title, figure):
    fig = figure
    ax = fig.add_subplot(num_plots, 1, plot_index)
    cax = ax.imshow(data, interpolation='nearest', aspect='auto')
    # cbar = fig.colorbar(cax, ticks=[0, 1])
    # cbar.ax.set_yticklabels(['0', '> 1'])  # vertically oriented colorbar
    ax.set_title(title)

def plot_data(data, title):
    plt.figure(figsize=(6.4, 2.5))  # figuresize to make 16 headers plot look good
    # plt.axis('scaled')
    plt.imshow(data, interpolation='nearest', aspect='auto')
    plt.title(title)
    plt.tight_layout()


def plotNNFilter(units):
    filters = units.shape[3]
    plt.figure(1, figsize=(20, 20))
    n_columns = 6
    n_rows = np.ceil(filters / n_columns) + 1
    for i in range(filters):
        plt.subplot(n_rows, n_columns, i+1)
        plt.title('Filter ' + str(i))
        plt.imshow(units[0, :, :, i], interpolation="nearest", cmap="gray")

