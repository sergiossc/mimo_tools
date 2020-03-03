import pandas as pd
import sqlite3
import numpy as np
"""
Le os resultados de ensaios realizados no Wireless Insite a partir do arquivo SQLite e retorna um array de raios (ray object) com as informacoes acessiveis atraves de propriedades de um objeto ray.

"""

class ray():
    def __init__(self, path_id, channel_id, departure_phi, departure_theta, arrival_phi, arrival_theta, received_power):
        self.path_id = path_id
        self.channel_id = channel_id
        self.departure_phi = np.deg2rad(departure_phi)
        self.departure_theta = np.deg2rad(departure_theta)
        self.arrival_phi = np.deg2rad(arrival_phi)
        self.arrival_theta = np.deg2rad(arrival_theta)
        self.received_power = received_power
	

def read_data(chn_id):
    """
    As informacoes obtidas podem ser selecionadas a partir da edicao dastring sql.
    #sql = "SELECT P.path_id, channel_id, received_power, time_of_arrival, departure_phi, departure_theta, arrival_phi, arrival_theta, cmp_e_x_r, cmp_e_x_i, cmp_e_y_r, cmp_e_y_i, cmp_e_z_r, cmp_e_z_i, cmp_h_x_r, cmp_h_x_i, cmp_h_y_r, cmp_h_y_i, cmp_h_z_r, cmp_h_z_i, freespace_path_loss, freespace_path_loss_woa, e_theta_r, e_theta_i, e_phi_r, e_phi_i, cir_phs, cmp_volt_r, cmp_volt_i FROM [path] AS P JOIN path_utd ON P.path_id = path_utd.path_id"
    
    Existem outras tabelas com outras informacoes dos resultados dos ensaios. Pode-se usar o DB Browser for SQLite pra visualizar o banco de dados completo.
    """

    conn = sqlite3.connect("/home/snow/github/land/lib/mimo_tools/data/urban_land.urban_land_x3d.sqlite")
    
    sql = "SELECT P.path_id, channel_id, departure_phi, departure_theta, arrival_phi, arrival_theta, received_power FROM [path] AS P JOIN path_utd ON P.path_id = path_utd.path_id WHERE channel_id="+str(chn_id)
    
    df = pd.read_sql_query(sql, conn)
    conn.close()

    data_dict = df.to_dict()
    
    num_paths = len(data_dict['path_id'])
    #print ("num_paths: ", num_paths)
    #num_paths = 10
    rays = []
    for n in range(num_paths):
        path_id = data_dict['path_id'][n] 
        channel_id = data_dict['channel_id'][n] 
        departure_phi = data_dict['departure_phi'][n] 
        departure_theta = data_dict['departure_theta'][n] 
        arrival_phi = data_dict['arrival_phi'][n]
        arrival_theta = data_dict['arrival_theta'][n] 
        received_power = data_dict['received_power'][n] 
        #if chn_id == channel_id:
        r = ray(path_id, channel_id, departure_phi, departure_theta, arrival_phi, arrival_theta, received_power)
        rays.append(r) 
    #print ("len of rays of this channel: ", len(rays))

    #rays = [ray for ray in rays if (ray.arrival_phi >= -np.pi/2 ) and (ray.arrival_phi <= np.pi/2)]
    #rays = [ray for ray in rays if (ray.arrival_theta < np.pi/2 ) and (ray.arrival_theta > -np.pi/2)]
    #rays = [ray for ray in rays if (ray.departure_theta < np.pi/2 ) and (ray.departure_theta > -np.pi/2)]
    #rays = [ray for ray in rays if (ray.departure_phi >= 0 ) and (ray.departure_phi <= np.pi/2)]
    #rays = [ray for ray in rays if (ray.departure_phi >= -np.pi/2 ) and (ray.departure_phi <= np.pi/2)]
    #rays = [ray for ray in rays if (ray.departure_theta >= -np.pi/2 ) and (ray.departure_theta <= np.pi/2)]
 
    #sum_pwer = np.sum([ray.received_power for ray in rays])
    #print ("------------------>>>>> ", sum_pwer)
    rays = pwr_normalize(rays)
    #rays = [rays[ np.random.randint(1,len(rays))]]
    return rays

def pwr_normalize(rays):
    #rays = read_data(chn_id)
    pwr = np.array([ray.received_power for ray in rays ])
    magnitude = np.sqrt(np.sum(pwr ** 2))
    #pwr_min = pwr[0]
    for ray in rays:
        ray.received_power =  ray.received_power / magnitude
    return rays
