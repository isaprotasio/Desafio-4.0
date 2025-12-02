import streamlit as st
import heapq
import pandas as pd
from collections import defaultdict
import sys
import os

import warnings
warnings.filterwarnings("ignore", message=".*missing ScriptRunContext.*")
warnings.filterwarnings("ignore", category=UserWarning)

if 'streamlit' in sys.modules:
    st.set_page_config(
        page_title="Roteirizador de Metrô", 
        page_icon="🚇", 
        layout="wide",
        initial_sidebar_state="expanded"
    )

st.title("🚇 Planejador de Rotas de Metrô - Algoritmo de Dijkstra")
st.markdown("### Encontre o caminho mais rápido entre estações de metrô")

estacoes_metro = {
    "Linha Azul": {
        "Centro": {"Museu": 3, "Parque": 4},
        "Museu": {"Centro": 3, "Jardim": 5},
        "Jardim": {"Museu": 5, "Universidade": 4},
        "Universidade": {"Jardim": 4}
    },
    "Linha Vermelha": {
        "Parque": {"Centro": 4, "Shopping": 6},
        "Shopping": {"Parque": 6, "Estádio": 5},
        "Estádio": {"Shopping": 5}
    },
    "Linha Verde": {
        "Jardim": {"Museu": 5, "Aeroporto": 7},
        "Aeroporto": {"Jardim": 7}
    }
}

def criar_grafo_completo(dados_estacoes):
    grafo = {}
    
    for linha, estacoes in dados_estacoes.items():
        for estacao, conexoes in estacoes.items():
            if estacao not in grafo:
                grafo[estacao] = {}
            
            for vizinho, tempo in conexoes.items():
                grafo[estacao][vizinho] = tempo
                if vizinho not in grafo:
                    grafo[vizinho] = {}
                grafo[vizinho][estacao] = tempo
    
    return grafo

def dijkstra(grafo, inicio, fim):
    if inicio not in grafo or fim not in grafo:
        return None, None
        
    distancias = {estacao: float('inf') for estacao in grafo}
    distancias[inicio] = 0
    predecessores = {estacao: None for estacao in grafo}
    fila_prioridade = [(0, inicio)]
    
    while fila_prioridade:
        distancia_atual, estacao_atual = heapq.heappop(fila_prioridade)
        
        if distancia_atual > distancias[estacao_atual]:
            continue
        
        if estacao_atual == fim:
            break
        
        for vizinho, peso in grafo[estacao_atual].items():
            nova_distancia = distancia_atual + peso
            
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                predecessores[vizinho] = estacao_atual
                heapq.heappush(fila_prioridade, (nova_distancia, vizinho))
    
    if distancias[fim] == float('inf'):
        return None, None
    
    caminho = []
    estacao_atual = fim
    while estacao_atual is not None:
        caminho.insert(0, estacao_atual)
        estacao_atual = predecessores[estacao_atual]
    
    return caminho, distancias[fim]

grafo_completo = criar_grafo_completo(estacoes_metro)
todas_estacoes = sorted(list(grafo_completo.keys()))

st.sidebar.header("⚙️ Configurações")
origem = st.sidebar.selectbox("Estação de Origem", todas_estacoes)
destino = st.sidebar.selectbox("Estação de Destino", todas_estacoes)
calcular = st.sidebar.button("📍 Calcular Rota", type="primary")

# Área principal
if calcular:
    if origem == destino:
        st.warning("Selecione estações diferentes!")
    else:
        caminho, tempo_total = dijkstra(grafo_completo, origem, destino)
        
        if caminho:
            st.success(f"✅ **Rota encontrada em {tempo_total} minutos**")

            st.subheader("🗺️ Trajeto:")
            for i in range(len(caminho) - 1):
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    st.markdown(f"**{caminho[i]}**")
                with col2:
                    tempo_trecho = grafo_completo[caminho[i]][caminho[i+1]]
                    st.markdown(f"→ *{tempo_trecho} min* →")
                with col3:
                    if i == len(caminho) - 2:
                        st.markdown(f"**{caminho[i+1]}**")
            
            st.subheader("📊 Resumo")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Origem", origem)
            with col2:
                st.metric("Destino", destino)
            with col3:
                st.metric("Tempo Total", f"{tempo_total} min")
            
            with st.expander("📋 Detalhes do Caminho"):
                for i in range(len(caminho) - 1):
                    st.write(f"**{caminho[i]}** → **{caminho[i+1]}** ({grafo_completo[caminho[i]][caminho[i+1]]} minutos)")
        else:
            st.error("❌ Rota não encontrada!")

st.sidebar.markdown("---")
st.sidebar.info("""
**Sistema de Metrô:**
- 3 Linhas ativas
- 8 Estações
- Algoritmo de Dijkstra
""")

st.markdown("---")
st.subheader("🗺️ Mapa do Sistema")

conexoes_data = []
conexoes_vistas = set()

for estacao, conexoes in grafo_completo.items():
    for vizinho, tempo in conexoes.items():
        par = tuple(sorted([estacao, vizinho]))
        if par not in conexoes_vistas:
            conexoes_vistas.add(par)
            conexoes_data.append({
                "Estação A": estacao,
                "Estação B": vizinho,
                "Tempo (min)": tempo
            })

if conexoes_data:
    df = pd.DataFrame(conexoes_data)
    st.dataframe(df, use_container_width=True)

st.markdown("---")
st.caption("Desenvolvido com Streamlit | Algoritmo de Dijkstra | © 2025")
