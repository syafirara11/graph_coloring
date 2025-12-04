# coloring_samarinda.py

import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt

# Fungsi untuk membaca shapefile dan menghasilkan graf
def read_shapefile(shapefile_path):
    gdf = gpd.read_file(shapefile_path)
    
    # Menampilkan beberapa baris pertama dari kolom geometry untuk memverifikasi tipe geometri
    print("Geometri dari beberapa kecamatan:\n", gdf['geometry'].head())
    
    G = nx.Graph()
    
    # Menambahkan node dan edges berdasarkan data geometris
    for idx, row in gdf.iterrows():
        G.add_node(row['NAMOBJ'], geometry=row['geometry'])
        
        # Menambahkan edges berdasarkan tetangga geometris
        for neighbor in gdf.loc[gdf.geometry.touches(row['geometry'])].itertuples():
            G.add_edge(row['NAMOBJ'], neighbor.NAMOBJ)
    
    return G, gdf

# Koordinat baru untuk setiap kecamatan
def get_manual_positions():
    return {
        'Palaran': (117.185066, -0.617633),
        'Samarinda Seberang': (117.133914, -0.522369),
        'Samarinda Ulu': (117.115706, -0.455079),
        'Samarinda Ilir': (117.162403, -0.505282),
        'Samarinda Utara': (117.205143, -0.396406),
        'Sungai Kunjang': (117.084171, -0.510035),
        'Sambutan': (117.219138, -0.522674),
        'Sungai Pinang': (117.186166, -0.471624),
        'Samarinda Kota': (117.150685, -0.499714),
        'Loa Janan Ilir': (117.11141, -0.559507)
    }

# Algoritma Welch-Powell untuk pewarnaan graf
def welch_powell_coloring(G):
    sorted_nodes = sorted(G.nodes(), key=lambda x: G.degree(x), reverse=True)
    coloring = {}
    
    for node in sorted_nodes:
        # Ambil warna yang sudah digunakan oleh tetangga
        neighbor_colors = {coloring.get(neighbor) for neighbor in G.neighbors(node) if neighbor in coloring}
        
        # Cari warna yang belum digunakan
        color = 0
        while color in neighbor_colors:
            color += 1
        
        coloring[node] = color
    
    return coloring

# Fungsi untuk memvisualisasikan graf yang diberi warna
def plot_colored_graph(G, coloring, title="Colored Graph"):
    color_map = {0: 'red', 1: 'green', 2: 'blue', 3: 'orange'}
    node_colors = [color_map[coloring[node]] for node in G.nodes()]
    
    # Menggunakan koordinat manual untuk penataan posisi titik
    pos = get_manual_positions()  # Menyusun posisi node secara manual
    
    plt.figure(figsize=(12, 12))
    
    # Mengganti font_color menjadi 'black' untuk warna hitam pada label
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=10, font_color='black', font_weight='bold')
    
    plt.title(title)
    
    # Menyimpan graf
    plt.savefig('D:/project_samarinda/2.output_graf.png')
    plt.show()

# Fungsi untuk memvisualisasikan peta kota Samarinda dengan pewarnaan
def plot_map_with_coloring(gdf, coloring, color_map={0: 'red', 1: 'green', 2: 'blue', 3: 'orange'}):
    gdf['color'] = gdf['NAMOBJ'].map(coloring).map(color_map)
    
    # Plot peta dengan label nama kecamatan
    ax = gdf.plot(color=gdf['color'], figsize=(12, 12), legend=True)
    ax.set_title("Peta Kota Samarinda dengan Pewarnaan")
    
    # Menambahkan label nama kecamatan pada peta
    for x, y, label in zip(gdf.geometry.centroid.x, gdf.geometry.centroid.y, gdf['NAMOBJ']):
        ax.text(x, y, label, fontsize=8, ha='center', color='black', weight='bold')
    
    # Menyimpan peta
    plt.savefig('D:/project_samarinda/1.output_peta.png')
    plt.show()

# Main function untuk menjalankan program
if __name__ == "__main__":
    shapefile_path = "Kecamatan_KotaSamarindat.shp"
    
    # Membaca shapefile dan menghasilkan graf
    G, gdf = read_shapefile(shapefile_path)
    
    # Menjalankan algoritma Welch-Powell untuk pewarnaan
    coloring = welch_powell_coloring(G)
    
    # Menampilkan graf yang telah diberi warna
    plot_colored_graph(G, coloring, title="Graph Coloring Kota Samarinda")
    
    # Menampilkan peta kota Samarinda yang sudah diberi warna
    plot_map_with_coloring(gdf, coloring)
