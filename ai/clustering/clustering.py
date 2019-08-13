'''
Clustering
'''

from tkinter import *
import random
import math


def read_data():
    file = open("data.txt", "r")
    data = []
    for line in file.readlines():
        info = line.split(',')
        try:
            model = info[0]
            carbon = float(info[1])
            millage = float(info[2])
            data.append([model, carbon, millage])
        except ValueError:
            pass
    file.close()
    return data


class Cluster:
    def __init__(self, data, classes):
        self.data = data
        self.classes = classes

        self.matrix_x = []
        self.matrix_y = []
        self.centroids = []
        self.map = []

        self.create_data_matrix()
        self.generate_centroids2(self.classes)

    def create_data_matrix(self):
        for line in self.data:
            self.matrix_x.append(line[1])
            self.matrix_y.append(line[2])

    def generate_centroids(self, k):
        range_x = (min(self.matrix_x), max(self.matrix_x))
        range_y = (min(self.matrix_y), max(self.matrix_y))

        for i in range(0, k):
            self.centroids.append([random.uniform(range_x[0], range_x[1]), random.uniform(range_y[0], range_y[1])])

    def generate_centroids2(self, k):
        for i in range(0, k):
            index = random.randint(0, len(self.matrix_x) - 1)
            self.centroids.append([self.matrix_x[index], self.matrix_y[index]])

    def classification(self):
        self.map = []
        for i in range(0, len(self.matrix_y)):
            minimum = math.sqrt((self.matrix_x[i] - self.centroids[0][0]) ** 2 + (self.matrix_y[i] - self.centroids[0][1]) ** 2)
            minimum_index = 0
            for k in range(1, len(self.centroids)):
                current = math.sqrt((self.matrix_x[i] - self.centroids[k][0]) ** 2 + (self.matrix_y[i] - self.centroids[k][1]) ** 2)
                if minimum > current:
                    minimum = current
                    minimum_index = k
            self.map.append(minimum_index)

    def get_cost(self):
        total_cost = 0
        for i in range(0, len(self.matrix_y)):
            centroid_cost = 0
            for k in range(0, len(self.centroids)):
                if self.map[i] == k:
                    distance = math.sqrt(
                        (self.matrix_x[i] - self.centroids[k][0]) ** 2 + (self.matrix_y[i] - self.centroids[k][1]) ** 2)
                    centroid_cost += distance
            total_cost += centroid_cost
        return total_cost

    def print_result(self):
        # Distance between centroid and origin
        for i in range(0, len(self.centroids)):
            distance = math.sqrt(self.centroids[i][0] ** 2 + self.centroids[i][1] ** 2)
            self.centroids[i] = [distance] + self.centroids[i]
            self.centroids[i].append(i)

        self.centroids.sort()
        self.centroids.reverse()

        class_counter = 65
        for centroid in self.centroids:
            for d in range(0, len(self.matrix_x)):
                if self.map[d] == centroid[3]:
                    print("Classe %s: %s"%(chr(class_counter), self.data[d][0]))

            class_counter += 1

    def update_centroids(self):
        for i in range(0, self.classes):
            avg_x = 0
            avg_y = 0
            length = 0

            for m in range(0, len(self.matrix_x)):
                if self.map[m] == i:
                    avg_x += self.matrix_x[m]
                    avg_y += self.matrix_y[m]

                    length += 1

            if length != 0:
                avg_x /= length
                avg_y /= length

            self.centroids[i][0] = avg_x
            self.centroids[i][1] = avg_y


class Plot:
    def __init__(self, window, cluster):
        self.window = window
        self.iteration_count = cluster.classes
        self.minimum_cost = -1
        self.cluster = cluster
        self.size = [600, 600]
        self.canvas = Canvas(self.window, width=self.size[0] + 100, height=self.size[1] + 100, bg='#cdcdcd')
        self.canvas.place(x = 0, y = 0)
        self.text = Text()
        self.text.insert(END, "15 (max):\n")
        self.text.place(x = 700, y = 0, width = 300, height = 700)
        self.colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ffffff', '#000000']
        self.iterations = 100
        self.first = True
        self.last_cost = 0

    def dynamic_clustering(self):

        if self.first:
            self.canvas.delete(ALL)
            self.first = False
            self.plot_data(self.cluster.matrix_x, self.cluster.matrix_y)
            self.window.after(1000, self.dynamic_clustering)
            return None

        self.cluster.classification()
        self.cluster.update_centroids()
        self.plot(self.cluster.matrix_x, self.cluster.matrix_y, self.cluster.centroids, self.cluster.map)

        current_cost = self.cluster.get_cost()
        self.iterations -= 1

        if self.iterations > 0 and self.last_cost != current_cost:
            self.last_cost = current_cost
            self.window.after(100, self.dynamic_clustering)

        elif self.iteration_count <= 15:

            self.text.insert(END, "Iteration %d\n" % self.iteration_count)
            self.text.insert(END, "  Cost:  %d\n" % current_cost)

            self.cluster.print_result()

            self.iteration_count += 1

            self.cluster.matrix_x = []
            self.cluster.matrix_y = []
            self.cluster.centroids = []
            self.cluster.map = []

            self.cluster.create_data_matrix()
            self.cluster.generate_centroids2(self.iteration_count)

            self.first = True

            if self.minimum_cost != -1 and self.minimum_cost < current_cost:
                line, column = self.text.index('end').split('.')
                line = int(line) - 2

                self.text.tag_add("smaller", "%d.0" % line, "%d.25" % line)
                self.text.tag_config("smaller", foreground="red")
                self.text.insert(END, "\nBest iteration %d\n" % (self.iteration_count - 2))
                self.text.insert(END, "  Cost:  %d\n" % self.minimum_cost)
                self.text.insert(END, "END.")

                line, column = self.text.index('end').split('.')
                line = int(line) - 2
                self.text.tag_add("best", "%d.0" % line, "%d.25" % line)
                self.text.tag_config("best", foreground="blue")

            else:
                self.minimum_cost = current_cost
                self.window.after(500, self.dynamic_clustering)
        else:
            self.text.insert(END, "\nEND.")

    def plot_data(self, matrix_x, matrix_y):

        range_x = (min(matrix_x), max(matrix_x))
        range_y = (min(matrix_y), max(matrix_y))

        for i in range(0, len(matrix_x)):

            scale_x = matrix_x[i] / range_x[1]
            scale_y = matrix_y[i] / range_y[1]

            x = self.size[0] * scale_x
            y = self.size[1] * scale_y

            self.canvas.create_oval((x - 2, y - 2, x + 4, y + 4), fill="black")

    def plot(self, matrix_x, matrix_y, centroids, map):
        self.canvas.delete(ALL)

        range_x = (min(matrix_x), max(matrix_x))
        range_y = (min(matrix_y), max(matrix_y))

        for k in range(0, len(centroids)):
            if k <= 7:
                fill_color = self.colors[k]
            else:
                fill_color = '#%02x%02x%02x' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            scale_x = centroids[k][0] / range_x[1]
            scale_y = centroids[k][1] / range_y[1]

            x = self.size[0] * scale_x
            y = self.size[1] * scale_y

            #self.canvas.create_rectangle((x - 3, y - 3, x + 6, y + 6), fill=centroids[k][2])

            self.canvas.create_rectangle((x - 3, y - 3, x + 6, y + 6), fill=fill_color)

            for i in range(0, len(matrix_x)):

                if map[i] != k:
                    continue

                scale_x = matrix_x[i] / range_x[1]
                scale_y = matrix_y[i] / range_y[1]

                x = self.size[0] * scale_x
                y = self.size[1] * scale_y
                
                #self.canvas.create_oval((x - 2, y - 2, x + 4, y + 4), fill=centroids[k][2])
                
                self.canvas.create_oval((x - 2, y - 2, x + 4, y + 4), fill=fill_color)


def main():
    window = Tk()
    window.geometry('900x700+500+100')
    window.title('Clustering')
    window.resizable(False, False)

    cluster = Cluster(read_data(), 1)
    plot = Plot(window, cluster)
    plot.dynamic_clustering()

    window.mainloop()


if __name__ == '__main__':
    main()
