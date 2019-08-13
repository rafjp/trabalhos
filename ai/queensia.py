'''
    Queens puzzle with genetic algorithm.
'''


import random


class Config:
    __table_size = 8
    __population_size = 128
    __max_iterations = 2000

    def __init__(self):
        pass

    @staticmethod
    def get_table_size():
        return Config.__table_size

    @staticmethod
    def get_population_size():
        return Config.__population_size

    @staticmethod
    def get_max_iterations():
        return Config.__max_iterations


class Queens:
    # Chromosome size
    size = Config.get_table_size()

    def __init__(self):
        pass

    @staticmethod
    def generate_chromosome():
        chromosome = []

        for _ in range(0, Queens.size):
            chromosome.append(random.randint(0, Queens.size - 1))

        return chromosome

    @staticmethod
    def print_chromosome(chromosome):
        for i in range(0, Queens.size):
            line = ''
            for j in range(0, Queens.size):

                type = 0
                if chromosome[j] == i:
                    type = 1

                line += str(type)
                if j != Queens.size - 1:
                    line += '  '

            print(line)

    @staticmethod
    def queen_diagonal_cost(chromosome, queen_index):
        value_down = value_up = cost = 0
        value = chromosome[queen_index]

        for i in range(queen_index + 1, Queens.size):
            value_down -= 1
            value_up += 1

            if (value + value_up) == chromosome[i]:
                cost += 1

            if (value + value_down) == chromosome[i]:
                cost += 1

        return cost

    @staticmethod
    def chromosome_cost(chromosome):
        cost = 0

        # Line cost
        for i in range(0, Queens.size):
            for k in range(i + 1, Queens.size):
                if chromosome[i] == chromosome[k]:
                    cost += 1

        # Diagonal
        for i in range(0, Queens.size):
            cost += Queens.queen_diagonal_cost(chromosome, i)

        return cost


class GeneticChromosome:
    def __init__(self, chromosome, cost):
        self.chromosome = chromosome
        self.cost = cost

    def __lt__(self, other):
        if other.cost < self.cost:
            return False
        return True

    def __le__(self, other):
        if other.cost <= self.cost:
            return False
        return Truee

    def __eq__(self, other):
        if other.cost == self.cost:
            return True
        return False

    def __ne__(self, other):
        if other.cost != self.cost:
            return True
        return False

    def __ge__(self, other):
        if other.cost >= self.cost:
            return False
        return True

    def __gt__(self, other):
        if other.cost > self.cost:
            return False
        return True

    def __str__(self):
        return str(self.chromosome) + ": " + str(self.cost)


class GeneticAlgorithm:
    def __init__(self):
        # List of GeneticChromosome
        self.population = []

    def generate_population(self, size):
        for _ in range(0, size):
            chromosome = Queens.generate_chromosome()
            cost = Queens.chromosome_cost(chromosome)
            genetic_chromosome = GeneticChromosome(chromosome, cost)
            self.population.append(genetic_chromosome)

    def print_population(self):
        for chromosome in self.population:
            print(chromosome)

    def get_population_mid(self):
        mid = len(self.population) // 2

        if mid % 2 != 0:
            mid += 1

        return mid

    def sort_population(self):
        self.population.sort()

    def cut_population(self):
        mid = self.get_population_mid()

        new_population = []
        for i in range(0, mid):
            new_population.append(self.population[i])

        self.population = []
        for chromosome in new_population:
            self.population.append(chromosome)

    @staticmethod
    def merge_chromosome(genetic_chromosome_a, genetic_chromosome_b):
        if Queens.size < 2:
            raise IndexError

        pivot = random.randint(0, Queens.size)
        while pivot == 0 or pivot == Queens.size:
            pivot = random.randint(0, Queens.size)

        merge = []

        for j in range(0, pivot):
            merge.append(genetic_chromosome_a.chromosome[j])

        for j in range(pivot, Queens.size):
            merge.append(genetic_chromosome_b.chromosome[j])

        genetic_chromosome_merge = GeneticChromosome(merge, Queens.chromosome_cost(merge))
        return genetic_chromosome_merge

    def merge_population(self):
        if Queens.size < 2:
            raise IndexError

        for i in range(0, len(self.population) - 1):
            merge = GeneticAlgorithm.merge_chromosome(self.population[i], self.population[i + 1])
            self.population.append(merge)

        merge = GeneticAlgorithm.merge_chromosome(self.population[0], self.population[len(self.population) - 1])
        self.population.append(merge)

    def mutate_population(self):
        mid = self.get_population_mid()
        for i in range(1, mid):
            genetic_chromosome = self.population[i]
            pivot = random.randint(1, Queens.size - 1)
            genetic_chromosome.chromosome[pivot] += random.randint(0, Queens.size - 1)
            if genetic_chromosome.chromosome[pivot] >= Queens.size:
                genetic_chromosome.chromosome[pivot] -= Queens.size
            genetic_chromosome.cost = Queens.chromosome_cost(genetic_chromosome.chromosome)

    def simulation(self, population_size, iterations):
        self.generate_population(population_size)
        self.sort_population()

        print('GeneticAlgorithm for size %d' % Queens.size)
        print('max %d iterations running...' % iterations)

        count = 0
        percent = 0
        for i in range(0, iterations):
            new_percent = i / iterations * 100

            if int(new_percent) != int(percent):
                percent = new_percent
                print("%03d%% iteration: %d" % (percent, i))

            self.mutate_population()
            self.sort_population()
            self.cut_population()
            self.merge_population()
            self.sort_population()

            if self.population[0].cost == 0:
                break

            count += 1

        print("%03d%% finished at %d iterations" % (100, count))
        final_cost = Queens.chromosome_cost(self.population[0].chromosome)

        if final_cost != 0:
            print("Solution not found in %d iterations" % count)
            print("The best chromosome has %d cost" % final_cost)

        self.sort_population()
        print(self.population[0].chromosome)
        Queens.print_chromosome(self.population[0].chromosome)


def main():
    genetic_algorithm = GeneticAlgorithm()
    genetic_algorithm.simulation(Config.get_population_size(), Config.get_max_iterations())


if __name__ == '__main__':
    main()
