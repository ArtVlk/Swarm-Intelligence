import random
from matplotlib.widgets import TextBox, Button

from matplotlib.gridspec import GridSpec
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from ant_algorithm import ant_colony_iteration, get_probabilities_button_value, set_probabilities_button
from graph import draw_graph, display_info, draw_diagram
from help import get_const, get_var, print_path, generate_random_parameters, calculate_trust_scores

ALPHA, BETA, EVAPORATION_RATE, INITIAL_PHEROMONE, ITERATIONS, ANTS_COUNT, EDGES, START_NODE, END_NODE = get_const()
edge_labels, hacked_nodes = get_var()


def main():
    G = nx.DiGraph()

    random_weights = [random.randint(1, 9) for _ in range(len(EDGES))]
    print(random_weights)
    G.add_weighted_edges_from(zip([u for u, v in EDGES], [v for u, v in EDGES], random_weights))

    G.add_node(1, image="computer0.png", pos=(0, 0), size=100)
    G.add_node(16, image="computer1.png", pos=(5, 0), size=100)

    edge_pheromone = {(u, v): float(INITIAL_PHEROMONE) for u, v in G.edges()}

    def update_parameters_and_scores_graph(frame):
        update_parameters_and_scores()

    def update(frame):
        edge_labels = {(u, v): round(edge_pheromone[(u, v)], 2) for u, v in G.edges()}
        plt.sca(ax_graph)
        plt.cla()
        draw_graph(G, edge_labels, pos, node_colors)
        draw_diagram(ax_diagram)
        display_info(ax_info, edge_pheromone, G)
        plt.draw()

        ant_colony_iteration(G, ANTS_COUNT, ALPHA, BETA, EVAPORATION_RATE, edge_pheromone, START_NODE, END_NODE, ITERATIONS,
                             trust_scores)
        print_path(START_NODE, END_NODE, edge_pheromone, G, ALPHA, BETA)

    def update_parameters_and_scores():
        global parameters, trust_scores
        parameters = generate_random_parameters(G.number_of_nodes(), hacked_nodes)
        trust_scores = calculate_trust_scores(parameters, G.number_of_nodes())

    update_parameters_and_scores()

    pos = nx.spring_layout(G)

    plt.ion()

    gs = GridSpec(nrows=2, ncols=2, height_ratios=[1, 1])

    fig = plt.figure(figsize=(20, 10))

    ax_graph = fig.add_subplot(gs[:, 0])
    ax_info = fig.add_subplot(gs[0, 1])
    ax_diagram = fig.add_subplot(gs[1, 1])

    node_colors = {node: 'orange' for node in G.nodes()}

    print_prohabilities_ax = plt.axes([0, 0.96, 0.16, 0.03])
    print_prohabilities = Button(print_prohabilities_ax, 'Вывести в консоль пути и вероятности', color='green',
                                 hovercolor='lightcoral')

    def print_probabilities_button(event):
        global value
        value = get_probabilities_button_value()
        set_probabilities_button(not value)

    print_prohabilities.on_clicked(print_probabilities_button)

    ani = FuncAnimation(fig, update_parameters_and_scores_graph, interval=2000)
    ant_ani = FuncAnimation(fig, update, interval=2000)

    plt.ioff()
    plt.subplots_adjust(top=1)
    plt.show()


if __name__ == "__main__":
    main()
