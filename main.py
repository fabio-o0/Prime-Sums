import random
import math

class Graph:
    def __init__(self):
        self.graph = {}
        self.previous = {}
        self.hamiltonian_path = []

    def add(self, val):
        self.previous = self.copy()
        self.graph[val] = []
        if len(self.graph) == 1:
            return
        for node in self.graph:  # O(|V|)
            if node != val:
                if is_prime(node + val):
                    if val not in self.graph[node]:
                        self.graph[node].append(val)
                    if node not in self.graph[val]:
                        self.graph[val].append(node)

        curr_path = self.get_difference(val)
        if val < 26:
            self.hamiltonian_path = self.hamiltonian([], False)
        else:
            if len(curr_path) > 0:
                self.hamiltonian_path = self.hamiltonian(curr_path, True)
            else:
                self.hamiltonian_path = self.hamiltonian([], False)

    def get_difference(self, val):
        if isinstance(self.hamiltonian_path, bool):
            return []
        same = []
        different = []
        found = False
        for node in self.hamiltonian_path:
            if self.previous[node] != self.graph[node] and not found:
                found = True
            if not found:
                same.append(node)
            else:
                different.append(node)
        return same

    def copy(self):
        new = {}
        for k in self.graph:
            new[k] = self.graph[k].copy()
        return new

    def hamiltonian(self, path=[], given_start=False):
        size = len(self.graph)
        sub_graph = self.copy()
        if len(path) > 0:
            for node in list(sub_graph):  # O(|E|)
                if node in path and node != path[-1]:
                    for connection in sub_graph[node]:
                        sub_graph[connection].remove(node)
                    del sub_graph[node]

        def search(routes, start=given_start):
            if len(path) == size:
                return path
            routes = sorted(routes, key=lambda routes: len(sub_graph[routes]))
            if start:
                routes.remove(path[-1])
                routes.insert(0, path[-1])
                path.pop()
            for route in routes:
                if route not in path:
                    path.append(route)
                for vertex in sub_graph[route]:
                    sub_graph[vertex].remove(route)
                if search(sub_graph[route], False):
                    return path
                path.pop()
                for vertex in sub_graph[route]:
                    sub_graph[vertex].append(route)
            return False

        return search([k for k in sub_graph])

def fermat(a, n, p):
    res = 1
    a = a % p
    while n > 0:
        if n & 1:
            res = (res * a) % p
        n = n >> 1
        a = (a * a) % p
    return res
    
def is_prime(n, k = 4):
    if n <= 1 or n == 4: return False
    if n <= 3: return True
    while k > 0:
        a = random.randint(2, n - 1)
        if math.gcd(n, a) != 1:
            return False
        if fermat(a, n - 1, n) != 1:
            return False
        k -= 1
    return True

def validate(sol):
    for i in range(len(sol) - 1):
        if not is_prime(sol[i] + sol[i + 1]):
            return False
    return True


def main():
    import sys
    from timeit import default_timer as timer
    sys.setrecursionlimit(1000000)
    graph = Graph()
    start = timer()
    for i in range(1, 50):
        beg = timer()
        graph.add(i)
        end = timer()
        if graph.hamiltonian_path:
            print(f"{i}: {graph.hamiltonian_path}, took {(end - beg) * 1000} milliseconds, result is {validate(graph.hamiltonian_path)}")
        else:
            print(f"{i} has no path, took {(end - beg) * 1000} milliseconds")
    finish = timer()
    print(f"Total time was {(finish - start) * 1000} milliseconds")


if __name__ == "__main__":
    main()
