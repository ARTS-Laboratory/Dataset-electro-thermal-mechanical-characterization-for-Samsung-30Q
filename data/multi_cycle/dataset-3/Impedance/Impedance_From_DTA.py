# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:49:10 2026
Modified last on Tues June 2 11:50 2026

Creates the Bode and Nyquist Plots Automatically
Only needed file. 

Note: 
    - Update the cell count to ensure the code won't fail
    - DTA files must be put into data folder (same capitalization)
    - DTA files must be named like: <TestName>_Cell_1
        - Update the cell number. It must be at the end like shown
    - Have a media folder (same capitalization)
        
@author: Charlie Buren
"""

''' Library Setup '''
import numpy as np
import matplotlib.pyplot as plt
import gamry_parser as parser
from pathlib import Path
from dataclasses import dataclass 
from pathlib import Path

''' Update '''
"Path to the folder. The data folder should be a subdirectory of this folder"
Folder_path = r'C:\School\Navy\Github\dataset-cycling-with-strain-monitoring-for-samsung-30Q-cell\data\Dataset-2\post-test-spectroscopy' #Change this (leave the r outside quotes)

"""
Note that if you change the number of cells you need to update the colors.
Also if you change cell count the Display_Graphs.md will not update.
"""
Cell_Count = 3
colors = ['blue', 'red', 'green'] #[cell 1, cell 2, cell 3]


''' Optional Settings '''
save_type = '.png' #Leave period if you want to change the file save type


''' Relative Paths '''
search_directory = Path(Folder_path)

#relative paths 
save_media_path = f'{search_directory}/media'
DTA_folder_path = f'{search_directory}/data'

#Test Name
Test_Path_Directory = Path(DTA_folder_path)
Test_Path_Cell1 = next(Test_Path_Directory.glob('*Cell_1.DTA'), None)

Test_Name_Extra_ = Test_Path_Cell1.stem.replace(('Cell_1'), '')
Test_Name = Test_Name_Extra_[:-1]


''' Labels '''
Ylabel_Mag = 'Mod (ohm)'
Ylabel_Phase = 'Zphz (deg)'
Xlabel_Phase = 'Frequency (Hz)'
Xlabel_Nyquist = 'Zreal (ohm)'
Ylabel_Nyquist = '-Zimag (ohm)'


''' Data Class '''
@dataclass
class CellBuilder:
    """Creates the class for each cell"""
    path: Path
    test_label: str
    contin: bool
    
    def create_DTA_dict(DTA_folder_path, Test_Name, Cell_Count): 
        """ this creates and returns the dictionary of cell DTA paths """ 
        DTA_dict = {}

        for i in range(1, Cell_Count+1):
            Cell_Num = f'Cell_{i}'
            DTA_dict[Cell_Num] = f'{DTA_folder_path}\\{Test_Name}_{Cell_Num}.DTA'
        return DTA_dict

@dataclass
class GraphBuilderBode:
    """Creates the class to graph each cell"""
    Freq: np.ndarray
    Zmod: np.ndarray
    Zphz: np.ndarray
    MagLabel: str
    PhaseLabel: str
    PlotTitle: str
    Choose_Color: str
    Save_Name: str
    
    def create_graph(self):
        #Graphing
        Bode_Plot = plt.figure(layout="constrained")
        Plot_Array = Bode_Plot.subplots(2,1, squeeze = False)
        
        #Labels
        Bode_Plot.suptitle(self.PlotTitle)
        
        #Mag Graph (Top)
        Bode_Mag_Plot = Plot_Array[0,0]
        Bode_Mag_Plot.semilogx(self.Freq, self.Zmod, color = self.Choose_Color, linestyle = '-', label = self.MagLabel) 
        Bode_Mag_Plot.set_ylabel(Ylabel_Mag)
        Bode_Mag_Plot.legend()
           
        #Phase Graph (Bot)
        Bode_Phase_Plot = Plot_Array[1,0]
        Bode_Phase_Plot.semilogx(self.Freq, self.Zphz, color = self.Choose_Color, linestyle = '-', label = self.PhaseLabel) 
        Bode_Phase_Plot.set_ylabel(Ylabel_Phase)
        Bode_Phase_Plot.set_xlabel(Xlabel_Phase)
        Bode_Phase_Plot.legend()
        
        Bode_Plot.savefig(self.Save_Name)
        plt.show()

@dataclass
class GraphBuilderNyquist:
    """Creates the class to graph each cell"""
    Zreal: np.ndarray
    Zimag: np.ndarray
    NyquistLabel: str
    PlotTitle: str
    Choose_Color: str
    Save_Name: str
    
    def create_nyquist_graph(self):
        #Graphing
        single_fig, single_ax = plt.subplots()
        single_fig.suptitle(self.PlotTitle)
        single_ax.grid(True, alpha = .3)
        
        single_ax.plot(self.Zreal, self.Zimag, color = self.Choose_Color, linestyle = '-', label = self.NyquistLabel)
        single_ax.set_ylabel(Ylabel_Nyquist)
        single_ax.set_xlabel(Xlabel_Nyquist)
        single_ax.legend()
        
        single_fig.savefig(self.Save_Name)
        plt.show()


''' Defs '''
def create_bode(DTA_files, save_media_path, colors, Test_Name, save_type, Cell_Count):
    """ 3 Single Cell Plots """
    # DTA_files = CellBuilder.create_DTA_dict()
    save_data = {}  
    for i, (cell_id, path) in enumerate(DTA_files.items()): #for loop iterating on the dictonary. (cell_id, path) assagins dict values 
        '''for title/labels'''
        cell_id_no_underline = cell_id.replace('_',' ')
    
        gp = parser.GamryParser()
        gp.load(filename=path)
        df = gp.get_curve_data()
        
        #save path
        save_name = f'{save_media_path}/{Test_Name}_{cell_id}_Bode{save_type}'
    
        graph_single = GraphBuilderBode(
            Freq=df['Freq'].values,
            Zmod=df['Zmod'].values,
            Zphz=df['Zphz'].values,
            MagLabel=f'{cell_id_no_underline} Mag',
            PhaseLabel=f'{cell_id_no_underline} Phase',
            PlotTitle=f'Bode Plot: {cell_id_no_underline}',
            Choose_Color=colors[i % len(colors)], # Cycles through colors
            Save_Name=save_name
            )
    
        save_data[cell_id] = graph_single
    
        graph_single.create_graph()
        
    
    ''' Overlay '''
    list_Freq, list_Zmod, list_Zphz = [], [], []
    label_mag, label_phase = [], []

    for i in range (1,(Cell_Count+1)):
        """Create a variable with data_cell# (ex: freq_1)"""
        cell_name = f'Cell_{i}'
        cell_name_title = cell_name.replace('_', ' ')
    
        #add data every pass
        list_Freq.append(save_data[cell_name].Freq)
        list_Zmod.append(save_data[cell_name].Zmod)
        list_Zphz.append(save_data[cell_name].Zphz)
    
        #add labels every pass
        label_mag.append(f'{cell_name_title} Mag')
        label_phase.append(f'{cell_name_title} Phase')
    

    ''' Overlay Graphing '''
    Overlay_Plot = plt.figure(layout="constrained")
    Overlay_Array = Overlay_Plot.subplots(2,1, squeeze = False)
    Overlay_Plot.suptitle('Overlay')

    #Mag Graph (Top)
    Overlay_Plot_Mag = Overlay_Array[0,0]
    Overlay_Plot_Mag.set_ylabel(Ylabel_Mag)

    #Phase Graph (Bot)
    Overlay_Plot_Phase = Overlay_Array[1,0]
    Overlay_Plot_Phase.set_ylabel(Ylabel_Phase)
    Overlay_Plot_Phase.set_xlabel(Xlabel_Phase)

    #Graphing 
    for i in range (Cell_Count):
        """Creates the overlay graph"""
        #Mag Graph (Top)
        Overlay_Plot_Mag.semilogx(list_Freq[i],
                                list_Zmod[i],
                                color = colors[i],
                                linestyle = '-',
                                label = label_mag[i]
                                )
        

        #Phase Graph (Bot)
        Overlay_Plot_Phase.semilogx(list_Freq[i],
                                    list_Zphz[i],
                                    color = colors[i],
                                    linestyle = '-',
                                    label = label_phase[i]
                                    )

    save_name_overlay = f'{save_media_path}/{Test_Name}_Overlay_Bode{save_type}'

    #legend
    Overlay_Plot_Mag.legend()
    Overlay_Plot_Phase.legend()

    Overlay_Plot.savefig(save_name_overlay)
    plt.show()

def create_nyquist(DTA_files, save_media_path, colors, Test_Name, save_type, Cell_Count):
    """ 3 Single Cell Plots """
    # DTA_files = CellBuilder.create_DTA_dict()
    save_data = {}

    for i, (cell_id, path) in enumerate(DTA_files.items()): #for loop iterating on the dictionary. (cell_id, path) assagins dict values 
        #for title/labels
        cell_id_no_underline = cell_id.replace('_',' ')
        
        gp = parser.GamryParser()
        gp.load(filename=path)
        df = gp.get_curve_data()
            
        #save path
        save_name_nyquist_single = f'{save_media_path}/{Test_Name}_{cell_id}_Nyquist{save_type}'
        
        graph_nyquist_single = GraphBuilderNyquist(
            Zreal=df['Zreal'].values,
            Zimag=-1*(df['Zimag'].values), #negative inverst the graph to be correct
            NyquistLabel=f'{cell_id_no_underline}',
            PlotTitle=f'Nyquist Plot: {cell_id_no_underline}',
            Choose_Color=colors[i % len(colors)], # Cycles through colors
            Save_Name=save_name_nyquist_single
            )
        
        save_data[cell_id] = graph_nyquist_single
        
        graph_nyquist_single.create_nyquist_graph()
        
    ''' Overlay '''
    list_Zreal, list_Zimag= [], []
    label_nyquist = []

    for i in range (1, (Cell_Count+1)):
        """Create a variable with data_cell# (ex: freq_1)"""
        cell_name = f'Cell_{i}'
        cell_name_title = cell_name.replace('_', ' ')
        
        #add data every pass
        list_Zreal.append(save_data[cell_name].Zreal)
        list_Zimag.append(save_data[cell_name].Zimag)
        
        #add labels every pass
        label_nyquist.append(f'{cell_name_title}')
        

    ''' Overlay Graphing '''
    overlay_fig, overlay_ax = plt.subplots()
    overlay_fig.suptitle('Overlay: Nyquist Plot')
    overlay_ax.grid(True, alpha = .3)

    #plot variables
    for i in range (Cell_Count):
        overlay_ax.plot(list_Zreal[i], 
                        list_Zimag[i],
                        color = colors[i], 
                        linestyle = '-', 
                        label = label_nyquist[i]
                        )

    #Saving Graph
    save_name_nyquist_overlay = f'{save_media_path}/{Test_Name}_Overlay_Nyquist{save_type}'
    overlay_fig.savefig(save_name_nyquist_overlay)

    #labels
    overlay_ax.legend()

    plt.show()

def display_graph_markdown_write(MD_Path,Cell_Count, Test_Name):
    with open(MD_Path, 'w') as f:
        #Single Cell Show
        for i in range(1, Cell_Count+1):
            f.write(f'## Cell {i} Graphs:\n\n')
            f.write(f'<img src="./media/{Test_Name}_Cell_{i}_Bode.png" width="500" height="333.33" alt="Cell {i} Bode Plot">\n')
            f.write(f'<img src="./media/{Test_Name}_Cell_{i}_Nyquist.png" width="500" height="333.33" alt="Cell {i} Nyquist Plot">\n\n')
        
        #Overlay
        f.write(f'## Overlay Graphs:\n\n')
        f.write(f'<img src="./media/{Test_Name}_Overlay_Bode.png" width="500" height="333.33" alt="Overlay Bode Plot">\n')
        f.write(f'<img src="./media/{Test_Name}_Overlay_Nyquist.png" width="500" height="333.33" alt="Overlay Nyquist Plot">\n\n')


''' Variable Setup '''
DTA_files_bode = CellBuilder.create_DTA_dict(DTA_folder_path=DTA_folder_path,
                                             Test_Name=Test_Name, 
                                             Cell_Count=Cell_Count)

DTA_files_nyquist = CellBuilder.create_DTA_dict(DTA_folder_path=DTA_folder_path,
                                                Test_Name=Test_Name,
                                                Cell_Count=Cell_Count)

''' Graphing '''
create_bode(DTA_files=DTA_files_bode,
            save_media_path=save_media_path,
            colors=colors,
            Test_Name=Test_Name,
            save_type=save_type,
            Cell_Count=Cell_Count)

create_nyquist(DTA_files=DTA_files_nyquist,
               save_media_path=save_media_path,
               colors=colors,
               Test_Name=Test_Name,
               save_type=save_type,
               Cell_Count=Cell_Count)


''' Write to MD '''
display_graphs_path = fr'{search_directory}\Display_Graphs.md'

display_graph_markdown_write(MD_Path=display_graphs_path, Cell_Count=Cell_Count, Test_Name=Test_Name)


''' Testing '''
# print(search_directory)
# print(save_media_path)
# print(DTA_folder_path)
# print(display_graphs_path)