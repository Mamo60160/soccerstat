import pandas as pd
import streamlit as st
import plotly.express as px

st.title("Dashboard d'Analyse des Statistiques des Joueurs de Football")

df = pd.read_csv('data/top5-players-cleans.csv')

df['Gls_per_MP'] = df['Gls'] / df['MP']
df['Ast_per_MP'] = df['Ast'] / df['MP']
df['Min_per_MP'] = df['Min'] / df['MP']

df = df[df['MP'] > 0]

st.sidebar.header("Filtres")

positions = df['Pos'].unique()
selected_pos = st.sidebar.multiselect("Sélectionnez les positions à afficher", positions, default=positions)

players = df['Player'].unique()
selected_players = st.sidebar.multiselect("Sélectionnez les joueurs à analyser", players, default=players[:10])

filtered_df = df[(df['Pos'].isin(selected_pos)) & (df['Player'].isin(selected_players))]

sort_by = st.sidebar.selectbox("Trier par", ['Gls_per_MP', 'Ast_per_MP', 'Min_per_MP'], index=0)
ascending = st.sidebar.checkbox("Tri ascendant", value=False)

filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)

st.subheader("Buts par match")
fig1 = px.bar(filtered_df, x='Player', y='Gls_per_MP', color='Pos',
              title="Buts par match (Gls/MP)", labels={'Gls_per_MP': 'Buts par match', 'Player': 'Joueur'},
              hover_data=['MP', 'Pos'])
st.plotly_chart(fig1)

st.subheader("Assists par match")
fig2 = px.bar(filtered_df, x='Player', y='Ast_per_MP', color='Pos',
              title="Assists par match (Ast/MP)", labels={'Ast_per_MP': 'Assists par match', 'Player': 'Joueur'},
              hover_data=['MP', 'Pos'])
st.plotly_chart(fig2)

st.subheader("Minutes jouées par match")
fig3 = px.bar(filtered_df, x='Player', y='Min_per_MP', color='Pos',
              title="Minutes jouées par match (Min/MP)", labels={'Min_per_MP': 'Minutes par match', 'Player': 'Joueur'},
              hover_data=['MP', 'Pos'])
st.plotly_chart(fig3)

st.subheader("Tableau des statistiques sélectionnées")
st.dataframe(filtered_df[['Player', 'Pos', 'MP', 'Gls', 'Ast', 'Min', 'Gls_per_MP', 'Ast_per_MP', 'Min_per_MP']])
