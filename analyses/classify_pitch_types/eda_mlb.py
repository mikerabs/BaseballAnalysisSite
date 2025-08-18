import psycopg2
from config import config
import pandas as pd
import numpy
import matplotlib.pyplot as plt

def connect_return_data():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # create a cursor
        cur = conn.cursor()
        
    # execute a statement
        print('PostgreSQL database version:')
        cur.execute("SELECT ps.pitcher, ps.player_name, ps.pitch_type, ps.pitch_name,ps.release_speed, ps.release_pos_x, ps.release_pos_y, ps.release_pos_z, ps.description, ps.zone, ps.p_throws, ps.pfx_x, ps.pfx_z, ps.plate_x, ps.plate_z, ps.vx0, ps.vy0, ps.vz0,ps.ax, ps.ay, ps.az, ps.effective_speed, ps.release_spin_rate, ps.release_extension, ps.spin_axis from pitches_statcast ps where (pitch_type = 'SI' OR pitch_type = 'FS') AND game_year < 2021;")

        rows = cur.fetchall()

        colnames = [desc[0] for desc in cur.description]

        print("Query executed successfully.")
        return pd.DataFrame(rows, columns=colnames)
       
    # close the communication with the PostgreSQL
        cur.close()
        return query
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def create_scatter_pitch(df, x, y, color):
    # Map pitch_type categories to colors
    color_map = {
        "SI": "blue",
        "FS": "red"
    }
    colors = df[color].map(color_map)

    fig, ax = plt.subplots()
    scatter = ax.scatter(df[x], df[y], c=colors, label=df[color])

    # Add labels and legend
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title("Pitch Movement (pfx_x vs pfx_z)")

    # custom legend
    handles = [plt.Line2D([0], [0], marker='o', color='w', 
                          markerfacecolor=c, markersize=8, label=pt)
               for pt, c in color_map.items()]
    ax.legend(handles=handles, title="Pitch Type")

    plt.show()
    plt.savefig("scatter_pitch.png", dpi=300, bbox_inches="tight")

if __name__ == '__main__':
    data = connect_return_data()
    create_scatter_pitch(data, "pfx_x", "pfx_z", "pitch_type")




