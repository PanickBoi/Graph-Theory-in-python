import os
import json
import networkx as nx
import matplotlib.pyplot as plt

'''
Rendering Engine (not as complicated as it sounds)
'''

class Renderer:
    def __init__(self, graph_list=None, update_type="", fps=1):
        self.graph_list = graph_list
        self.update_type = update_type
        self.fps = fps
        self.running = False
        self.event = False


    def insert_graph(self,G):
        self.graph_list.append(G)

    def render(self):
        for G in self.graph_list:
            fig = plt.figure(G.name,dpi=125)
            ax = plt.gca()
            xlim = ax.get_xlim()  # save zoom state
            ylim = ax.get_ylim()
            ax.cla()
            G.update()
            n_i = G.node_info
            e_i = G.edge_info
            nx.draw_networkx(G.graph, G.pos, ax=ax, node_color=n_i["node_colors"], node_size=n_i["node_sizes"],edge_color=e_i["edge_colors"], width=e_i["edge_widths"])
            if xlim != (0.0, 1.0):  # only restore if user has actually zoomed
                ax.set_xlim(xlim)
                ax.set_ylim(ylim)
            fig.canvas.draw()
            fig.canvas.flush_events()

        plt.pause(1 / self.fps)
    def start_render(self):
        plt.ion()
        self.running = True
        while self.running:
            if self.update_type == "event" and not self.event:
                pass
            else:
                self.render()

    def stop_render(self):
        self.running = False
        plt.ioff()
        plt.show()