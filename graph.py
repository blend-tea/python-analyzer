import networkx as nx
import os

# [[filename, [module name or path, [import func]], [module name or path, [import func]], ...], ...]
inp = [
    ['test/test.py', [
        ['test/test1/t.py', ['test']], 
        ['test/test1/test1.py', ['x']], 
        ['test/test1/test1.py', ['y']]]], 
    ['test/test2/test2.py', []], 
    ['test/test2/t/t.py', [
        ['test/test2/test2.py', ['x']]]], 
    ['test/test1/test1.py', [[
        'test/test1/t.py', ['test']], 
        ['test/test2/t/t.py', ['t']]]], 
    ['test/test1/t.py', [
        ['os', ['path']], 
        ['sys', ['argv']]]]]



def main(inp=inp):
    Graph = nx.DiGraph()
    nodes = create_node_list(inp)
    for node in nodes:
        Graph.add_node(node)
    edges = create_edge_list(inp)
    for edge in edges:
        Graph.add_edge(*edge)
    g = nx.nx_agraph.to_agraph(Graph)
    g.node_attr["style"] = "filled"

    node_colors = []
    num_nodes = len(Graph.nodes())
    for node in Graph.nodes():
        num_edges = len(list(Graph.in_edges(node)))
        red_value = max(0.01, num_edges / num_nodes)
        node_colors.append(f"#ff{int((1 - red_value)*255):02x}{int((1 - red_value)*255):02x}")
        
    for node, color in zip(g.nodes(), node_colors):
        g.get_node(node).attr["color"] = color
    if not os.path.isdir("out"):
        try:
            os.mkdir("out")
        except:
            print("mkdir error.")
            exit()
    g.draw('out/dot.pdf',prog='dot')
    g.draw('out/neato.pdf',prog='neato')
    g.draw('out/fdp.pdf',prog='fdp')
    g.draw('out/sfdp.pdf',prog='sfdp')
    g.draw('out/twopi.pdf',prog='twopi')
    g.draw('out/circo.pdf',prog='circo')
    g.draw('out/osage.pdf',prog='osage')



def create_node_list(inp:list) -> set:
    node = set()
    for i in inp:
        node.add(i[0])
        for imp in i[1]:
            node.add(imp[0])
    return node



def create_edge_list(inp:list) -> list:
    edges = []
    for i in inp:
        for imp in i[1]:
            edges.append([imp[0],i[0]])
    return edges



if __name__ == "__main__":
    main()
