from ant_algorithm import get_data_graphic, set_probabilities_on
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def draw_diagram(ax_diagram):
    set_probabilities_on(True)
    data_graphic = get_data_graphic()

    if data_graphic:
        transitions = {}
        for ant_data in data_graphic:
            for k, v in list(ant_data.values())[0]:
                if k not in transitions:
                    transitions[k] = []
                transitions[k].append(v)

        averages = {k: np.mean(v) for k, v in transitions.items()}

        ax_diagram.clear()
        ax_diagram.bar(averages.keys(), averages.values(), color='skyblue')
        ax_diagram.set_xlabel("Переходы", fontsize=12, fontweight='bold', color='blue')
        ax_diagram.set_ylabel("Среднее значение", fontsize=12, fontweight='bold', color='blue')

        for label in ax_diagram.get_xticklabels():
            label.set_rotation(45)
            label.set_horizontalalignment("right")
            label.set_fontsize(10)
            label.set_color('purple')

        ax_diagram.grid(axis='y', linestyle='--', alpha=0.7)  # Add dashed grid lines for the y-axis

        plt.tight_layout()
        plt.subplots_adjust(hspace=0.5)
        plt.draw()
        plt.pause(0.1)


def draw_graph(graph, edge_labels, pos, node_colors):
    labels = {node: str(node) for node in graph.nodes()}

    node_images = {}
    for node in graph.nodes(data=True):
        node_id = node[0]
        if "image" in node[1] and "pos" in node[1]:
            node_images[node_id] = node[1]["image"]

    nx.draw_networkx_labels(graph, pos, labels=labels, font_color='black', font_weight='bold')

    nx.draw_networkx_nodes(graph, pos, node_color=[node_colors[node] for node in graph.nodes()])

    for node_id, image in node_images.items():
        image_data = plt.imread(image)
        extent = [pos[node_id][0] - 0.05, pos[node_id][0] + 0.05, pos[node_id][1] - 0.05, pos[node_id][1] + 0.05]
        plt.imshow(image_data, extent=extent, zorder=2)

    nx.draw_networkx_edges(graph, pos, width=1, edge_color='gray', arrows=True)

    edge_weight_labels = {(u, v): f'P: {round(edge_labels[(u, v)], 2)}\nW: {graph[u][v]["weight"]}' for u, v in
                          graph.edges()}
    nx.draw_networkx_edge_labels(graph, pos, edge_weight_labels, font_color='black', font_weight='bold', font_size=8)


def display_info(ax, edge_pheromone, G):
    ax.clear()
    ax.axis('tight')
    ax.axis('off')
    data = [(u, v, G[u][v]['weight'], round(edge_pheromone[(u, v)], 2)) for u, v in G.edges()]
    table = ax.table(cellText=data, colLabels=["U", "V", "Расстояние", "Феромон"], cellLoc='center', loc='upper right')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(0.9, 1)

    for cell in table._cells:
        if cell[0] == 0:
            table._cells[cell].set_text_props(fontsize=10, weight='bold', color='blue')
            table._cells[cell].set_facecolor("yellow")
        else:
            table._cells[cell].set_text_props(fontsize=10, color='black')


    plt.tight_layout()
    plt.subplots_adjust(hspace=0.5)
    plt.draw()
    plt.pause(0.1)


def draw_ant_probability(probability_data):
    transitions = {}
    for ant_data in probability_data:
        for k, v in list(ant_data.values())[0]:
            if k not in transitions:
                transitions[k] = []
            transitions[k].append(v)

    averages = {k: np.mean(v) for k, v in transitions.items()}

    fig, ax = plt.subplots()
    ax.bar(averages.keys(), averages.values(), color='skyblue')
    ax.set_xlabel("Переходы", fontsize=12, fontweight='bold', color='blue')
    ax.set_ylabel("Среднее время", fontsize=12, fontweight='bold', color='blue')

    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_horizontalalignment("right")
        label.set_fontsize(10)
        label.set_color('purple')

    plt.draw()
    plt.pause(0.1)
