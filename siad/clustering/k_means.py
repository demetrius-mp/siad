from __future__ import annotations

import random
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
from matplotlib.colors import get_named_colors_mapping


@dataclass(unsafe_hash=True)
class Point:
    x: float
    y: float

    def get_distance(self, other: Point):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def get_closest_point(self, *points: Point) -> Point:
        closest_point = {"point": points[0], "distance": self.get_distance(points[0])}

        for point in points:
            distance = self.get_distance(point)
            if distance < closest_point["distance"]:
                closest_point = {"point": point, "distance": distance}

        return closest_point["point"]


@dataclass
class Cluster:
    centroid: Point
    points: list[Point] = field(default_factory=list)

    def assign_points(self, points: list[Point]) -> None:
        self.points = points

    def update_centroid(self) -> None:
        if len(self.points) == 0:
            return

        x = sum(p.x for p in self.points) / len(self.points)
        y = sum(p.y for p in self.points) / len(self.points)

        self.centroid = Point(x, y)


@dataclass
class KMeans:
    points: list[Point]
    number_of_clusters: int
    clusters: dict[Point, Cluster] = field(default_factory=dict)
    first_centroids: list[Point] = field(default_factory=list)

    def _get_closest_cluster_to_point(self, point: Point) -> Cluster:
        centroids = self.clusters.keys()

        closest_centroid = point.get_closest_point(*centroids)

        return self.clusters[closest_centroid]

    def _reset_clusters(self) -> None:
        for cluster in self.clusters.values():
            cluster.points = list()

    def initialize_centroids(self):
        max_x = int(max(self.points, key=lambda p: p.x).x)
        min_x = int(min(self.points, key=lambda p: p.x).x)

        max_y = int(max(self.points, key=lambda p: p.y).y)
        min_y = int(min(self.points, key=lambda p: p.y).y)

        centroids_x = random.sample(range(min_x, max_x), self.number_of_clusters)
        centroids_y = random.sample(range(min_y, max_y), self.number_of_clusters)

        for x, y in zip(centroids_x, centroids_y):
            centroid = Point(x, y)
            self.first_centroids.append(centroid)
            self.clusters[centroid] = Cluster(centroid)

    def assign_points_to_closest_centroid(self) -> None:
        self._reset_clusters()

        for point in self.points:
            closest_cluster = self._get_closest_cluster_to_point(point)
            closest_cluster.points.append(point)

    def __call__(self, number_of_iterations: int = 3):
        self.initialize_centroids()

        for _ in range(number_of_iterations):
            self.assign_points_to_closest_centroid()

            for cluster in self.clusters.values():
                cluster.update_centroid()

        return [self.clusters[c] for c in self.clusters.keys()]


def plot_clusters(*clusters: Cluster, title: str):
    colors = get_named_colors_mapping().values()

    for cluster, color in zip(clusters, colors):
        x = [p.x for p in cluster.points]
        y = [p.y for p in cluster.points]

        plt.plot(x, y, "o", color=color)

        centroid = cluster.centroid

        plt.plot(centroid.x, centroid.y, "x", color=color)

    plt.title(title)

    plt.show()


def main():
    points: list[Point] = [
        Point(2, 10),
        Point(2, 5),
        Point(8, 4),
        Point(5, 8),
        Point(7, 5),
        Point(6, 4),
        Point(1, 2),
        Point(4, 9),
    ]

    number_of_clusters = 3

    k_means = KMeans(points, number_of_clusters)

    number_of_iterations = 5

    clusters = k_means(number_of_iterations)

    print("--- Initial centroids ---")
    for i, centroid in enumerate(k_means.first_centroids):
        print(f"Cluster {i + 1} centroid: {centroid}")

    print()
    print("--- Final clusters ---")
    for cluster in clusters:
        print(cluster)

    plot_clusters(*clusters, title=f"{number_of_iterations} iterations")


if __name__ == "__main__":
    main()
