import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Flujo Máximo", layout="centered")
st.title("🔁 Calculadora de Flujo Máximo")

st.write("Formato: nodo_origen,nodo_destino,capacidad")
st.write("Ejemplo: S,A,10")

edges_input = st.text_area("Aristas (una por línea)", height=200)

source = st.text_input("Nodo fuente", "S")
sink = st.text_input("Nodo sumidero", "T")

if st.button("Calcular flujo máximo"):
    try:
        G = nx.DiGraph()

        for i, line in enumerate(edges_input.splitlines(), start=1):
            line = line.strip()
            if not line:
                continue  # ignora líneas vacías

            parts = [x.strip() for x in line.split(",")]
            if len(parts) != 3:
                st.error(f"Línea {i} mal escrita: {line}")
                st.stop()

            u, v, c = parts
            G.add_edge(u, v, capacity=int(c))

        if source not in G or sink not in G:
            st.error("La fuente o el sumidero no existen en el grafo")
            st.stop()

        flujo, flow_dict = nx.maximum_flow(G, source, sink)
        st.success(f"✅ Flujo máximo = {flujo}")

        # limpiar figura
        plt.clf()

        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_size=2000)

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels={(u, v): d["capacity"] for u, v, d in G.edges(data=True)}
        )

        st.pyplot(plt)

    except Exception as e:
        st.error(f"Error: {e}")
