import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

df = pd.read_excel('AtividadeExtencionista.xlsx')

df.columns = df.columns.str.strip()

geolocator = Nominatim(user_agent="survey_analysis_florianopolis", timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.5)

df['endereco_completo'] = df['Cidade'].astype(str) + ', ' + \
                          df['Bairro'].astype(str) + ', ' + \
                          df['Estado'].astype(str) + ', Brazil'

print("Iniciando geolocalização... Isso pode demorar alguns minutos.")

locais_unicos = pd.DataFrame(df['endereco_completo'].unique(), columns=['endereco_completo'])
locais_unicos['location'] = locais_unicos['endereco_completo'].apply(geocode)
locais_unicos['lat'] = locais_unicos['location'].apply(lambda loc: loc.latitude if loc else None)
locais_unicos['lon'] = locais_unicos['location'].apply(lambda loc: loc.longitude if loc else None)

df = df.merge(locais_unicos[['endereco_completo', 'lat', 'lon']], on='endereco_completo', how='left')

df.to_excel('Atividade_com_Coordenadas.xlsx', index=False)

#GRÁFICO DE BARRAS (ESTADOS)
df_estados = df.groupby('Estado').size().reset_index(name='Total_Respostas')
df_estados = df_estados.sort_values(by='Total_Respostas', ascending=False)

fig_barras = px.bar(
    df_estados,
    x='Estado',
    y='Total_Respostas',
    text='Total_Respostas',
    title='Total de Respostas por Estado',
    color='Total_Respostas',
    color_continuous_scale='Bluered',
    labels={'Total_Respostas': 'Número de Respostas', 'Estado': 'Estado (UF)'}
)

fig_barras.update_traces(textposition='outside',
                         marker_line_color='rgb(8,48,107)',
                        marker_line_width=1.5)
fig_barras.update_layout(
    bargap=0.6, 
    xaxis_tickangle=0,
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(showgrid=True, gridcolor='LightGray'),
    height=500
)

#MAPA 2: FLORIANÓPOLIS (CALOR)
df_floripa = df[df['Cidade'].str.contains('Florianópolis', case=False, na=False)].copy()
df_floripa = df_floripa.dropna(subset=['lat', 'lon'])

df_floripa_mapa = df_floripa.groupby(['lat', 'lon', 'Bairro']).size().reset_index(name='Respostas')
max_respostas_floripa = df_floripa_mapa['Respostas'].max()

fig_floripa = px.density_mapbox(
    df_floripa_mapa,
    lat='lat',
    lon='lon',
    z='Respostas', 
    radius=18,
    center={"lat": -27.5945, "lon": -48.5477},
    zoom=10,
    mapbox_style="carto-positron",
    title="Mapa de Calor: Intensidade de Respostas por Bairro em Florianópolis",
    color_continuous_scale=[
        [0.0, 'rgba(0,0,0,0)'],
        [0.01, '#0d0887'],
        [0.5, "#f8a859"], 
        [0.8, "#f8d341"], 
        [1.0, '#f0f921']
    ],
    range_color=[0, max_respostas_floripa]
)
fig_floripa.update_layout(
    margin={"r":0,"t":40,"l":0,"b":0},
    coloraxis_colorbar=dict(
        title="Nº de Respostas",
        tickvals=list(range(0, int(max_respostas_floripa) + 1, 2)),
        tickmode="array"
    )
)

#MAPA: DETALHAMENTO SANTA CATARINA
df_sc = df[df['Estado'].str.contains('SC', case=False, na=False)].copy()
df_sc = df_sc.dropna(subset=['lat', 'lon'])

df_sc_mapa = df_sc.groupby(['lat', 'lon', 'Cidade', 'Bairro']).size().reset_index(name='Respostas')

max_respostas = df_sc_mapa['Respostas'].max()

fig_sc = px.density_mapbox(
    df_sc_mapa,
    lat='lat',
    lon='lon',
    z='Respostas',
    radius=30,
    center={"lat": -27.2423, "lon": -50.2189},
    zoom=7,
    mapbox_style="carto-positron",
    title="Distribuição Geográfica: Todas as Cidades com Resposta",
    color_continuous_scale=[
        [0, 'rgba(0,0,0,0)'],
        [0.0001, '#67001f'],
        [0.2, '#d6604d'],
        [0.4, '#c51b7d'],
        [0.6, '#762a83'],
        [0.8, '#4393c3'],
        [1.0, '#053061']
    ],
    range_color=[0, max_respostas]
)

fig_sc.update_layout(
    margin={"r":0,"t":40,"l":0,"b":0},
    coloraxis_colorbar=dict(
        title="Nº de Respostas",
        tickvals=[1, 5, 10, max_respostas],
        tickmode="array"
    )
)

fig_sc.write_html("mapa_calor_sc.html")
fig_barras.write_html("grafico_barras_estados.html")
fig_floripa.write_html("mapa_floripa.html")

fig_barras.show()
fig_floripa.show()
fig_sc.show()

print("Processo concluído! Verifique os arquivos 'grafico_barras_estados.html', 'mapa_calor_sc.html' e 'mapa_floripa.html'.")