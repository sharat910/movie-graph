from schema import PlotResponse
from pyvis.network import Network
import networkx as nx

def generate_graph(plot_data: PlotResponse, filename: str):
    net = Network(notebook=True, height='600px', width='100%', cdn_resources='in_line')
    G = nx.DiGraph()

    for character in plot_data.characters:
        G.add_node(character.name, title=character.role)

    for relation in plot_data.relations:
        G.add_edge(relation.character1_name, relation.character2_name, label=relation.relationship_summary)

    net.from_nx(G)

    for node in net.nodes:
        try:
            node['label'] = node['id']
            node['title'] = G.nodes[node['id']]['title']
        except Exception as e:
            print(e)
            print(node)
            print(G.nodes[node['id']])

    net.set_options("""
        var options = {
            "physics": {
            "forceAtlas2Based": {
                "gravitationalConstant": -50,
                "centralGravity": 0.005,
                "springLength": 230,
                "springConstant": 0.18
            },
            "maxVelocity": 146,
            "solver": "forceAtlas2Based",
            "timestep": 0.35,
            "stabilization": {
                "iterations": 150
            }
            },
            "edges": {
            "arrows": {
                "to": { "enabled": true, "scaleFactor": 1 }
            },
            "arrowStrikethrough": false
            }
        }
    """)

    # Save and display the graph
    net.save_graph(filename)