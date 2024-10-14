import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import Menu, messagebox, filedialog, StringVar
from tkinter import ttk
import re
import numpy as np
from datetime import datetime
import os
from plom import parse_input, initialize, run, save_dict, load_dict
import sys
import threading
from scipy.stats import gaussian_kde


def launch_gui():
    
    # Global variable to keep track of the "About" window
    global about_window
    about_window = None
    
    # Global switch for save on exit
    save_on_exit = False
    
    def click_event(event):
        x,y = root.winfo_pointerxy()                   # get the mouse position on screen
        widget = root.winfo_containing(x,y)            # identify the widget at this location
        # print(widget)
        widget.focus()
        displayMessage__createjob()
    
    # Function to handle the close event
    def on_close():
        if save_on_exit:
            response = messagebox.askyesnocancel("Save current session?", "Do you want to save the current session before closing?")
        
            if response is None:  # Cancel was selected
                return
        
            if response:  # Save was selected
                # Placeholder for the save logic
                print("Saving current session...")
        
        # Close the application
        sys.stdout = original_stdout
        root.destroy()
    
    # Function to bind Ctrl+W to the close event
    def bind_shortcuts():
        root.bind('<Control-w>', lambda event: on_close())
        
        if about_window:
            about_window.bind('<Control-w>', lambda event: close_about_window())
            about_window.bind('<Escape>', lambda event: close_about_window())
    
    # Function to open the "About" window
    def show_about():
        global about_window
        if about_window:
            about_window.lift()  # Bring to front if already open
            return
    
        about_window = tk.Toplevel(root)
        about_window.title("About")
        about_window.geometry("400x200")  # Set the size of the About window
    
        # Add the text information, with the first two lines split into two each
        about_label1 = tk.Label(about_window, text="GUI for the PLoM algorithm\nPhilippe Hawi (USC)\nRoger Ghanem (USC)\nVenkat Aitharaju (General Motors)")
        about_label1.pack(pady=10)
    
        about_label2 = tk.Label(about_window, text="Functionalities based on the Python codebase \ndeveloped by Philippe Hawi")
        about_label2.pack(pady=10)
    
        # Add the clickable link
        link = tk.Label(about_window, text="https://github.com/philippehawi/PLoM", fg="blue", cursor="hand2")
        link.pack(pady=10)
        link.bind("<Button-1>", lambda e: open_github_link())
    
        # Bind Escape and Ctrl+W to close the About window
        about_window.bind('<Control-w>', lambda event: close_about_window())
        about_window.bind('<Escape>', lambda event: close_about_window())
    
        # Set the close function for the About window
        about_window.protocol("WM_DELETE_WINDOW", close_about_window)
    
        # Set focus to the About window
        about_window.focus_set()
    
    # Function to close the About window
    def close_about_window():
        global about_window
        if about_window:
            about_window.destroy()
            about_window = None
            bind_shortcuts()  # Restore Ctrl+W to close the main window
    
    # Function to open the GitHub link in a web browser
    def open_github_link():
        import webbrowser
        webbrowser.open("https://github.com/philippehawi/PLoM")
    
    # Function to open a file dialog and set the path in the entry field
    def browse_folder(entry_widget):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, folder_selected)
    
    def browse_file(entry_widget):
        file_selected = filedialog.askopenfilename()
        if file_selected:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_selected)
    
    def datetimeStr():
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def clear_log():
        log_text.delete(1.0, tk.END)
    
    def reset_gui():
        root.destroy()  # Close the existing root window
        launch_gui()  # Relaunch the GUI

    
    
    def get_plom_gui_input():
        job_name               = opt_save__plom_job_name.get()
        job_path               = opt_save__plom_job_path.get()
        diagnostics_criteria   = opt_save__plom_diag_criteria.get()
        diagnostics_inputType  = opt_save__plom_diag_inputType.get()
        diagnostics_inputValue = opt_save__plom_diag_inputValue.get()
        data_path              = opt_save__plom_data_path.get()
        data_columnsAre        = opt_save__plom_data_columnsAre.get()
        data_hasLabels         = opt_save__plom_data_hasLabels.get()
        data_hasIndices        = opt_save__plom_data_hasIndices.get()
        data_colIgnore         = opt_save__plom_data_colIgnore.get()
        data_rowIgnore         = opt_save__plom_data_rowIgnore.get()
        scaling_yesNo          = opt_save__plom_scaling_yesNo.get()
        scaling_method         = opt_save__plom_scaling_method.get()
        pca_yesNo              = opt_save__plom_pca_yesNo.get()
        pca_method             = opt_save__plom_pca_method.get()
        pca_criteria           = opt_save__plom_pca_criteria.get()
        pca_scaleEvecs         = opt_save__plom_pca_scaleEvecs.get()
        dmaps_yesNo            = opt_save__plom_dmaps_yesNo.get()
        dmaps_epsilon          = opt_save__plom_dmaps_epsilon.get()
        dmaps_kappa            = opt_save__plom_dmaps_kappa.get()
        dmaps_L                = opt_save__plom_dmaps_L.get()
        dmaps_firstEigvec      = opt_save__plom_dmaps_firstEigvec.get()
        dmaps_dim              = opt_save__plom_dmaps_dim.get()
        projection_yesNo       = opt_save__plom_projection_yesNo.get()
        projection_source      = opt_save__plom_projection_source.get()
        projection_target      = opt_save__plom_projection_target.get()
        sampling_yesNo         = opt_save__plom_sampling_yesNo.get()
        sampling_NSamples      = opt_save__plom_sampling_NSamples.get()
        sampling_f0            = opt_save__plom_sampling_f0.get()
        sampling_dr            = opt_save__plom_sampling_dr.get()
        sampling_itoSteps      = opt_save__plom_sampling_itoSteps.get()
        sampling_potMethod     = opt_save__plom_sampling_potMethod.get()
        sampling_kdeBW         = opt_save__plom_sampling_kdeBW.get()
        sampling_saveSamples   = opt_save__plom_sampling_saveSamples.get()
        sampling_samplesFType  = opt_save__plom_sampling_samplesFType.get()
        sampling_parallel      = opt_save__plom_sampling_parallel.get()
        sampling_njobs         = opt_save__plom_sampling_njobs.get()
        results_dict           = opt_save__plom_results_dict.get()
        results_plots          = opt_save__plom_results_plots.get()
        
        return [job_name, job_path, diagnostics_criteria, diagnostics_inputType, 
                diagnostics_inputValue, data_path, data_columnsAre, data_hasLabels, 
                data_hasIndices, data_colIgnore, data_rowIgnore, scaling_yesNo, 
                scaling_method, pca_yesNo, pca_method, pca_criteria, pca_scaleEvecs,
                dmaps_yesNo, dmaps_epsilon, dmaps_kappa, dmaps_L, dmaps_firstEigvec, 
                dmaps_dim, projection_yesNo, projection_source, projection_target, 
                sampling_yesNo, sampling_NSamples, sampling_f0, sampling_dr, 
                sampling_itoSteps, sampling_potMethod, sampling_kdeBW, 
                sampling_saveSamples, sampling_samplesFType, sampling_parallel, 
                sampling_njobs, results_dict, results_plots]
    
    def save_session(file_path=None):
        plom_gui_input = get_plom_gui_input()
        
        if file_path == None:
            file_path = filedialog.asksaveasfilename(
                title="Save session file",
                defaultextension=".txt",  # Default file extension
                filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
            )
        
        if file_path:
            with open(file_path, 'w') as f:
                for line in plom_gui_input:
                    f.write(f"{line}\n")
                print(f"Session saved to {file_path}\n")
    
    def load_session():
        file_path = filedialog.askopenfilename(
            title="Select session file", 
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    [job_name, job_path, diagnostics_criteria, diagnostics_inputType, 
                     diagnostics_inputValue, data_path, data_columnsAre, data_hasLabels, 
                     data_hasIndices, data_colIgnore, data_rowIgnore, scaling_yesNo, 
                     scaling_method, pca_yesNo, pca_method, pca_criteria, pca_scaleEvecs,
                     dmaps_yesNo, dmaps_epsilon, dmaps_kappa, dmaps_L, dmaps_firstEigvec, 
                     dmaps_dim, projection_yesNo, projection_source, projection_target, 
                     sampling_yesNo, sampling_NSamples, sampling_f0, sampling_dr, 
                     sampling_itoSteps, sampling_potMethod, sampling_kdeBW, 
                     sampling_saveSamples, sampling_samplesFType, sampling_parallel, 
                     sampling_njobs, results_dict, results_plots] = f.read().splitlines()
            
                    opt_save__plom_job_name.set(job_name)
                    opt_save__plom_job_path.set(job_path)
                    opt_save__plom_diag_criteria.set(diagnostics_criteria)
                    opt_save__plom_diag_inputType.set(diagnostics_inputType)
                    opt_save__plom_diag_inputValue.set(diagnostics_inputValue)
                    opt_save__plom_data_path.set(data_path)
                    opt_save__plom_data_columnsAre.set(data_columnsAre)
                    opt_save__plom_data_hasLabels.set(data_hasLabels)
                    opt_save__plom_data_hasIndices.set(data_hasIndices)
                    opt_save__plom_data_colIgnore.set(data_colIgnore)
                    opt_save__plom_data_rowIgnore.set(data_rowIgnore)
                    opt_save__plom_scaling_yesNo.set(scaling_yesNo)
                    opt_save__plom_scaling_method.set(scaling_method)
                    opt_save__plom_pca_yesNo.set(pca_yesNo)
                    opt_save__plom_pca_method.set(pca_method)
                    opt_save__plom_pca_criteria.set(pca_criteria)
                    opt_save__plom_pca_scaleEvecs.set(pca_scaleEvecs)
                    opt_save__plom_dmaps_yesNo.set(dmaps_yesNo)
                    opt_save__plom_dmaps_epsilon.set(dmaps_epsilon)
                    opt_save__plom_dmaps_kappa.set(dmaps_kappa)
                    opt_save__plom_dmaps_L.set(dmaps_L)
                    opt_save__plom_dmaps_firstEigvec.set(dmaps_firstEigvec)
                    opt_save__plom_dmaps_dim.set(dmaps_dim)
                    opt_save__plom_projection_yesNo.set(projection_yesNo)
                    opt_save__plom_projection_source.set(projection_source)
                    opt_save__plom_projection_target.set(projection_target)
                    opt_save__plom_sampling_yesNo.set(sampling_yesNo)
                    opt_save__plom_sampling_NSamples.set(sampling_NSamples)
                    opt_save__plom_sampling_f0.set(sampling_f0)
                    opt_save__plom_sampling_dr.set(sampling_dr)
                    opt_save__plom_sampling_itoSteps.set(sampling_itoSteps)
                    opt_save__plom_sampling_potMethod.set(sampling_potMethod)
                    opt_save__plom_sampling_kdeBW.set(sampling_kdeBW)
                    opt_save__plom_sampling_saveSamples.set(sampling_saveSamples)
                    opt_save__plom_sampling_samplesFType.set(sampling_samplesFType)
                    opt_save__plom_sampling_parallel.set(sampling_parallel)
                    opt_save__plom_sampling_njobs.set(sampling_njobs)
                    opt_save__plom_results_dict.set(results_dict)
                    opt_save__plom_results_plots.set(results_plots)
                print(f'Session file loaded: "{file_path}"\n')
            except:
                pass
    
    
    def load_training(data_path, data_columnsAre, data_hasLabels, data_hasIndices, 
                      data_colIgnore, data_rowIgnore):
        
        if data_hasLabels:
            skiprows = 1
        else:
            skiprows = 0
            
        if data_path.endswith(".txt"):
            data = np.loadtxt(data_path, skiprows=skiprows)
        elif data_path.endswith(".npy"):
            data = np.load(data_path)
        
        if len(data_colIgnore) > 0:
            data_colIgnore = np.array([x for x in data_colIgnore.replace(' ', '').split(',') if x], dtype=int)
            data = np.delete(data, data_colIgnore, axis=1)
        
        if len(data_rowIgnore) > 0:
            data_rowIgnore = np.array([x for x in data_rowIgnore.replace(' ', '').split(',') if x], dtype=int)
            data = np.delete(data, data_rowIgnore, axis=0)
        
        if data_columnsAre.strip() == 'Samples':
            data = data.T
        
        if data_hasIndices:
            data = data[:, 1:]
        
        return data
    
    
    def displayMessage__createjob(message='', color='black'):  
        job_message['text'] = message  
        job_message['foreground'] = color 
    
    
    def make_input_deck(plom_gui_input):
        
        plom_gui_input = ['True' if str(x).strip() == 'Yes' else x for x in plom_gui_input]
        plom_gui_input = ['False' if str(x).strip() == 'No' else x for x in plom_gui_input]
        
        [job_name, job_path, diagnostics_criteria, diagnostics_inputType, 
         diagnostics_inputValue, data_path, data_columnsAre, data_hasLabels, 
         data_hasIndices, data_colIgnore, data_rowIgnore, scaling_yesNo, 
         scaling_method, pca_yesNo, pca_method, pca_criteria, pca_scaleEvecs,
         dmaps_yesNo, dmaps_epsilon, dmaps_kappa, dmaps_L, dmaps_firstEigvec, 
         dmaps_dim, projection_yesNo, projection_source, projection_target, 
         sampling_yesNo, sampling_NSamples, sampling_f0, sampling_dr, 
         sampling_itoSteps, sampling_potMethod, sampling_kdeBW, 
         sampling_saveSamples, sampling_samplesFType, sampling_parallel, 
         sampling_njobs, results_dict, results_plots] = plom_gui_input
        
        if pca_method == "Cumulative Energy":
            pca_method = "cum_energy"
            pca_criteriaName = "pca_cum_energy    "
        elif pca_method == "Eigenvalue Cutoff":
            pca_method = "eigv_cutoff"
            pca_criteriaName = "pca_eigv_cutoff "
        elif pca_method == "PCA Dimension":
            pca_method = "pca_dim"
            pca_criteriaName = "pca_dim         "
        
        if projection_source == "PCA space":
            projection_source = "pca"
        elif projection_source == "Scaled space":
            projection_source = "scaling"
        elif projection_source == "Original space":
            projection_source = "data"
        
        if projection_target == "PCA space":
            projection_target = "pca"
        elif projection_target == "DMAPs space":
            projection_target = "dmaps"
        
        job_path_full = f'{job_path}/{job_name}'
        os.makedirs(job_path_full, exist_ok=True)
        os.chdir(job_path_full)
        
        lines = [
         '# this is an input file for PLoM;\n',
         "# lines starting with '#' or '*' are ignored;\n",
         "# leading ' ', '\\t', '\\n' are ignored;\n",
         '# option and value should be separated by whitespace(s) or TAB(s);\n',
         "# inline comments begin with '#'\n",
         '#########################################################################\n',
         '\n',
         '\n',
         
         '*** PATH OF TRAINING (INPUT) DATA ***\n',
         'training           training.txt\n',
         '\n',
         '\n',
         
         '*** SCALING PARAMETERS ***\n',
         f'scaling            {scaling_yesNo}\n',
         f'scaling_method     {scaling_method}\n',
         '\n',
         '\n',
         
         '*** PCA PARAMETERS ***\n',
         f'pca                {pca_yesNo}\n',
         f'pca_scale_evecs    {pca_scaleEvecs}\n',
         f'pca_method         {pca_method}\n',
         f'{pca_criteriaName} {pca_criteria}\n',
         '\n',
         '\n',
         
         '*** DMAPS PARAMETERS ***\n',
         f'dmaps              {dmaps_yesNo}\n',
         f'dmaps_epsilon      {dmaps_epsilon} # <float> or auto\n',
         f'dmaps_kappa        {dmaps_kappa}\n',
         f'dmaps_L            {dmaps_L}\n',
         f'dmaps_first_evec   {dmaps_firstEigvec}\n',
         f'dmaps_m_override   {dmaps_dim}\n',
         'dmaps_dist_method  standard\n',
         '\n',
         '\n',
         
         '*** SAMPLING PARAMETERS ***\n',
         f'sampling           {sampling_yesNo}\n',
         f'num_samples        {sampling_NSamples}\n',
         f'parallel           {sampling_parallel}\n',
         f'n_jobs             {sampling_njobs}\n',
         f'save_samples       {sampling_saveSamples}\n',
         f'samples_fname      output/samples.{sampling_samplesFType} # if None, file will be named using job_desc and save time\n',
         #f'samples_fmt        {sampling_samplesFType} # npy or txt\n',
         '\n',
         '\n',
         
         '*** ITO PARAMETERS ***\n',
         f'projection         {projection_yesNo}\n',
         f'projection_source  {projection_source} # pca, scaling, or data\n',
         f'projection_target  {projection_target} # dmaps or pca\n',
         f'ito_f0             {sampling_f0}\n',
         f'ito_dr             {sampling_dr}\n',
         f'ito_steps          {sampling_itoSteps} # <int> or auto\n',
         f'ito_pot_method     {sampling_potMethod}\n',
         f'ito_kde_bw_factor  {sampling_kdeBW}\n',
        
         '\n',
         '\n',
         '*** JOB PARAMETERS ***\n',
         f'job_desc           {job_name}\n',
         'verbose            True\n'
         ]
        
        with open('input.txt', 'w') as f:
            f.writelines(lines)
    
    
    def create_job():
        plom_gui_input = get_plom_gui_input()
        
        [job_name, job_path, diagnostics_criteria, diagnostics_inputType, 
         diagnostics_inputValue, data_path, data_columnsAre, data_hasLabels, 
         data_hasIndices, data_colIgnore, data_rowIgnore, scaling_yesNo, 
         scaling_method, pca_yesNo, pca_method, pca_criteria, pca_scaleEvecs,
         dmaps_yesNo, dmaps_epsilon, dmaps_kappa, dmaps_L, dmaps_firstEigvec, 
         dmaps_dim, projection_yesNo, projection_source, projection_target, 
         sampling_yesNo, sampling_NSamples, sampling_f0, sampling_dr, 
         sampling_itoSteps, sampling_potMethod, sampling_kdeBW, 
         sampling_saveSamples, sampling_samplesFType, sampling_parallel, 
         sampling_njobs, results_dict, results_plots] = plom_gui_input
        
        if not job_name:
            displayMessage__createjob('Enter valid job name', 'red')
            return
        
        if not job_path:
            displayMessage__createjob('Enter valid job path', 'red')
            return
        
        if not data_path:
            displayMessage__createjob('Enter valid data path', 'red')
            return
        
        job_path_full = f'{job_path}/{job_name}'
        os.makedirs(job_path_full, exist_ok=True)
        os.makedirs(f'{job_path_full}/output', exist_ok=True)
        os.chdir(job_path_full)
        
        save_session(f"{job_path_full}/session.txt")
        
        training_data = load_training(data_path, data_columnsAre, data_hasLabels, 
                                      data_hasIndices, data_colIgnore, data_rowIgnore)
        np.savetxt("training.txt", training_data)
        print(f"Training data loaded: {training_data.shape[0]} samples, {training_data.shape[1]} features")
        print(f'Training data saved: "{job_path_full}/training.txt"\n')
        
        make_input_deck(plom_gui_input)
        print("Input deck created")
        print(f'Input deck saved: "{job_path_full}/input.txt"\n')
        
        displayMessage__createjob('Job created successfully', 'blue')
    
    
    def run_job():
        create_job()
        
        plom_gui_input = get_plom_gui_input()
        
        [job_name, job_path, diagnostics_criteria, diagnostics_inputType, 
         diagnostics_inputValue, data_path, data_columnsAre, data_hasLabels, 
         data_hasIndices, data_colIgnore, data_rowIgnore, scaling_yesNo, 
         scaling_method, pca_yesNo, pca_method, pca_criteria, pca_scaleEvecs,
         dmaps_yesNo, dmaps_epsilon, dmaps_kappa, dmaps_L, dmaps_firstEigvec, 
         dmaps_dim, projection_yesNo, projection_source, projection_target, 
         sampling_yesNo, sampling_NSamples, sampling_f0, sampling_dr, 
         sampling_itoSteps, sampling_potMethod, sampling_kdeBW, 
         sampling_saveSamples, sampling_samplesFType, sampling_parallel, 
         sampling_njobs, results_dict, results_plots] = plom_gui_input
        
        job_path_full = f'{job_path}/{job_name}'
        os.makedirs(job_path_full, exist_ok=True)
        os.makedirs(f'{job_path_full}/output', exist_ok=True)
        os.chdir(job_path_full)
        
        input_deck_fname = "input.txt"
        
        if not os.path.exists(input_deck_fname):
            displayMessage__createjob('Job input deck not found', 'red')
            return
        
        try:
            args = parse_input(input_deck_fname)
        except:
            displayMessage__createjob('Unable to parse job input deck', 'red')
            return
        
        print("\n\n*** JOB STARTING ***\n\n")
        solution_dict = initialize(**args)
        run(solution_dict)
        
        dict_path = f'{job_path_full}/output/result.dict'
        save_dict(solution_dict, dict_path)
        print(f'\n\nResults dictionary saved: "{dict_path}"\n')
        
        displayMessage__createjob('Job completed successfully', 'blue')
        
        print("\n\n*** JOB COMPLETED SUCCESSFULLY ***\n\n")
        
        os.replace(f'{job_name}_plom_summary.txt', 'output/summary.txt')
    
    
    def run_job_thread():
        task_thread = threading.Thread(target=run_job)
        task_thread.start()
    
    
    class TextRedirector:
        def __init__(self, text_widget):
            self.text_widget = text_widget
    
        def write(self, message):
            self.text_widget.insert(tk.END, message)
            self.text_widget.see(tk.END)
            self.text_widget.update_idletasks()  # Force GUI to update
    
        def flush(self):
            pass
    
    
    def load_data(path, dtype=None, empty_ok=False):
        if path == "" and empty_ok:
            return None
        if path.endswith('.txt'):
            if dtype == "text":
                with open(path, 'r') as f:
                    lines = f.readlines()  # Read all lines from the file
                    lines = [line.strip() for line in lines]
                    return lines
            else:
                return np.loadtxt(path)
        if path.endswith('.npy'):
            return np.load(path)
        raise ValueError("Invalid filetype")
        
    
    #****************************   MAIN WINDOW   ********************************#
    
    # Create the main window
    root = tk.Tk()
    root.title("PLoM GUI (USC-GM)")
    root.geometry("1600x820")  # Set window size
    
    # Create a style
    style = ttk.Style()
    
    # Configure the style for TCombobox
    # style.configure('TCombobox', fieldbackground='orange', background='grey')
    # style.theme_use('clam')
    # style.map('custom.TCombobox', fieldbackground=[('readonly','light grey')])
    
    # Create a menu bar
    menu_bar = Menu(root)
    
    # Add File menu with "New session", "Load session", "Save session"
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New session", command=reset_gui)
    file_menu.add_command(label="Load session", command=load_session)
    file_menu.add_command(label="Save session", command=save_session)
    file_menu.add_separator()  # Add a separator line
    file_menu.add_command(label="Exit", command=on_close)
    menu_bar.add_cascade(label="File", menu=file_menu)
    
    # Add Edit menu
    edit_menu = Menu(menu_bar, tearoff=0)
    edit_menu.add_command(label="Undo")
    edit_menu.add_command(label="Redo")
    menu_bar.add_cascade(label="Edit", menu=edit_menu)
    
    # Add Help menu
    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About", command=show_about)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    
    # Set the menu bar on the root window
    root.config(menu=menu_bar)
    
    # Create a main frame for the tabs
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    #*****************************************************************************#
    
    #********************************   TABS   ***********************************#
    
    # Create a Notebook widget (tabs)
    tab_control = ttk.Notebook(main_frame)
    
    # Create the "PLoM Sampling" tab
    data_augmentation_tab = tk.Frame(tab_control)
    tab_control.add(data_augmentation_tab, text="PLoM Sampling")
    
    # Create the "PLoM Results" tab
    jobResults_tab = tk.Frame(tab_control)
    tab_control.add(jobResults_tab, text="PLoM Results")
    
    # Create the "Diagnostics Results" tab
    diagResults_tab = tk.Frame(tab_control)
    tab_control.add(diagResults_tab, text="Diagnostics Results")
    
    # Create the "Feature Ranking" tab
    featureRanking_tab = tk.Frame(tab_control)
    tab_control.add(featureRanking_tab, text="Feature Ranking")
    
    # Create the "Conditioning" tab
    conditioning_tab = tk.Frame(tab_control)
    tab_control.add(conditioning_tab, text="Conditioning")
    
    # Create the "Create Forward Models" tab
    createModels_tab = tk.Frame(tab_control)
    tab_control.add(createModels_tab, text="Create Forward Models")
    
    # Create the "Run Forward Models" tab
    runModels_tab = tk.Frame(tab_control)
    tab_control.add(runModels_tab, text="Run Forward Models")
    
    # Pack the notebook widget into the main frame
    tab_control.pack(fill=tk.BOTH, expand=True)
    
    #*****************************************************************************#
    
    #*************************   DATA AUGMENTATION TAB   *************************#
    
    # Create frames for layout in the "Data augmentation" tab
    plom_settings_frame = tk.Frame(data_augmentation_tab, width=400)
    plom_settings_frame.grid(row=0, column=0, sticky='ns')
    
    plom_settings_frame2 = tk.Frame(data_augmentation_tab, width=400)
    plom_settings_frame2.grid(row=0, column=1, sticky='ns')
    
    log_frame = tk.Frame(data_augmentation_tab)
    log_frame.grid(row=0, column=2, sticky='nsew', pady=(0, 10), padx=(0, 10))
    
    # Configure column weights for the frames
    data_augmentation_tab.grid_columnconfigure(0, weight=0, minsize=400)  # Fixed width column with minsize
    data_augmentation_tab.grid_columnconfigure(1, weight=0, minsize=400)
    data_augmentation_tab.grid_columnconfigure(2, weight=1)  # Expanding column
    
    # Configure row weight (optional if you want the row to expand)
    data_augmentation_tab.grid_rowconfigure(0, weight=1)
    
    # Configure plom_settings_frame to have a fixed width of 400 pixels
    plom_settings_frame.grid_propagate(False)  # Prevent the frame from resizing
    
    # Set row index for frames
    current_row = 0
    
    # Add "Settings" label to the left frame
    # settings_label = tk.Label(plom_settings_frame, text="Settings", anchor='w', font=("Arial", 12, "bold"))
    # settings_label.grid(row=current_row, column=0, columnspan=2, sticky='w', padx=10, pady=(5, 5))
    
    # settings_label2 = tk.Label(plom_settings_frame2, text="", anchor='w', font=("Arial", 12, "bold"))
    # settings_label2.grid(row=current_row, column=0, columnspan=2, sticky='w', padx=10, pady=(5, 5))
    
    
    
    # Group 1: PLoM job-related options
    current_row += 1
    frame__plom_job = tk.LabelFrame(plom_settings_frame, text="Job", padx=10, pady=10, font=("Arial", 10, "bold"))
    frame__plom_job.grid(row=current_row, column=0, columnspan=3, sticky='ew', padx=10, pady=(10, 5))
    
    opt_save__plom_job_name = tk.StringVar(frame__plom_job)
    opt_save__plom_job_name.set(f'job_{datetimeStr()}')
    opt_label__plom_job_name = tk.Label(frame__plom_job, text="Job name", anchor='w')
    opt_label__plom_job_name.grid(row=0, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_job_name = tk.Entry(frame__plom_job, textvariable=opt_save__plom_job_name)
    opt_value__plom_job_name.grid(row=0, column=1, sticky='ew')
    
    opt_save__plom_job_path = tk.StringVar(frame__plom_job)
    opt_save__plom_job_path.set(os.path.expanduser("~"))
    
    opt_label__plom_job_path = tk.Label(frame__plom_job, text="Job path", anchor='w', fg='blue')
    opt_label__plom_job_path.grid(row=1, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_job_path = tk.Entry(frame__plom_job, textvariable=opt_save__plom_job_path)
    opt_value__plom_job_path.grid(row=1, column=1, sticky='ew')
    
    browse_button__plom_job_path = tk.Button(frame__plom_job, text="Browse", command=lambda: browse_folder(opt_value__plom_job_path))
    browse_button__plom_job_path.grid(row=1, column=2, sticky='ew', padx=(5, 0))
    
    # Configure the frame__plom_job grid columns to ensure proper alignment and expandability
    frame__plom_job.grid_columnconfigure(0, weight=0)  # Label column (fixed size)
    frame__plom_job.grid_columnconfigure(1, weight=1)  # Entry column (expandable)
    frame__plom_job.grid_columnconfigure(2, weight=0)  # Button column (fixed size)
    
    ################################################################################
    ################################################################################
    
    # PLoM diagnostics-related options
    group_row = 0
    current_row += 1
    frame__plom_diag = tk.LabelFrame(plom_settings_frame, text="Diagnostics", padx=10, pady=10, font=("Arial", 10, "bold"))
    frame__plom_diag.grid(row=current_row, column=0, columnspan=2, sticky='ew', padx=10, pady=(10, 5))
    
    diag_criteria_options = [" (None)", " Sample size (N)", " DMaps kernel bandwidth (epsilon)"]
    opt_save__plom_diag_criteria = tk.StringVar(frame__plom_diag)
    opt_label__plom_diag_criteria = tk.Label(frame__plom_diag, text="Convergence citeria", anchor='w')
    opt_label__plom_diag_criteria.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_diag_criteria = ttk.Combobox(frame__plom_diag, values=diag_criteria_options, state='readonly', textvariable=opt_save__plom_diag_criteria)
    opt_value__plom_diag_criteria.current(0)
    opt_value__plom_diag_criteria.grid(row=group_row, column=1, sticky='ew')
    
    def update_diagnostics_label(event):
        print("updating label")
        selected_option = opt_save__plom_diag_criteria.get()
        # input_type  = opt_save__plom_diag_inputType.get().strip()
        if selected_option == diag_criteria_options[0]:
            opt_label__plom_diag_inputValue.config(text="Criteria values")
            opt_value__plom_diag_inputType.config(state="disabled")
            opt_value__plom_diag_inputValue.config(state="disabled")  # Disable the entry field
            displayMessage__plom_diag_inputValue()
        elif selected_option == diag_criteria_options[1]:
            opt_value__plom_diag_inputType.config(state="readonly")
            opt_label__plom_diag_inputValue.config(text="Sample size values")
            opt_value__plom_diag_inputValue.config(state="normal", validate="all", validatecommand=(reg_val__validate__plom_diag_inputValue, '%P', '%d', '%i', '%S', '%V'))  # Enable the entry field
        elif selected_option == diag_criteria_options[2]:
            opt_value__plom_diag_inputType.config(state="readonly")
            opt_label__plom_diag_inputValue.config(text="Epsilon values")
            opt_value__plom_diag_inputValue.config(state="normal", validate="all", validatecommand=(reg_val__validate__plom_diag_inputValue, '%P', '%d', '%i', '%S', '%V'))  # Enable the entry field
    
    opt_value__plom_diag_criteria.bind("<<ComboboxSelected>>", update_diagnostics_label)
    
    
    group_row += 1
    diag_criteria_input_types = [" Min, Max, Step", " Min, Max, Num cases", " List of values"]
    opt_save__plom_diag_inputType = tk.StringVar(frame__plom_diag)
    opt_label__plom_diag_inputType = tk.Label(frame__plom_diag, text="Input type", anchor='w')
    opt_label__plom_diag_inputType.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_diag_inputType = ttk.Combobox(frame__plom_diag, values=diag_criteria_input_types, state='disabled', textvariable=opt_save__plom_diag_inputType)
    opt_value__plom_diag_inputType.current(0)
    opt_value__plom_diag_inputType.grid(row=group_row, column=1, sticky='ew')
    opt_value__plom_diag_inputType.bind("<<ComboboxSelected>>", update_diagnostics_label)
    
    group_row += 1
    opt_save__plom_diag_inputValue = tk.StringVar(frame__plom_diag)
    opt_label__plom_diag_inputValue = tk.Label(frame__plom_diag, text="Criteria values", anchor='w')
    opt_label__plom_diag_inputValue.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_diag_inputValue = tk.Entry(frame__plom_diag, state="disabled", textvariable=opt_save__plom_diag_inputValue)
    opt_value__plom_diag_inputValue.grid(row=group_row, column=1, sticky='ew')
    
    def validate__plom_diag_inputValue(P, d, i, S, V):
        input_str = P
        why = d # action code: 0 for deletion, 1 for insertion, or -1 for focus in, focus out, or a change to the textvariable
        idx = i # index of insertion, or -1
        what = S # inserted character
        reason = V # reason for this callback: one of 'focusin', 'focusout', 'key', or 'forced' if the textvariable was changed
        print(reason)
        
        if opt_save__plom_diag_criteria.get() == diag_criteria_options[1]: # SAMPLE SIZE CONVERGENCE
            if opt_save__plom_diag_inputType.get() in diag_criteria_input_types[0:2]:
                pattern = r"^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*$"
            elif opt_save__plom_diag_inputType.get() == diag_criteria_input_types[2]:
                pattern = r"^\s*\d+(\s*,\s*\d+)*\s*$"
            match = re.match(pattern, input_str)
        
            if reason == "focusin" or reason == "focusout":
                if len(input_str) == 0:
                    displayMessage__plom_diag_inputValue()
                    return True
                if match:
                    if opt_save__plom_diag_inputType.get() in diag_criteria_input_types[0:2]:
                        a, b, c = map(int, match.groups())
                        if b < a:
                            displayMessage__plom_diag_inputValue(error="Max should be >= Min", color='red')
                            return False
                        if c == 0:
                            if opt_save__plom_diag_inputType.get() == diag_criteria_input_types[0]:
                                displayMessage__plom_diag_inputValue(error="Step should be > 0", color='red')
                            else:
                                displayMessage__plom_diag_inputValue(error="Num cases should be > 0", color='red')
                            return False
                        displayMessage__plom_diag_inputValue()
                        return True
                    elif opt_save__plom_diag_inputType.get() == diag_criteria_input_types[2]:
                        integers = list(map(int, re.findall(r"\d+", input_str)))
                        if min(integers) == 0:
                            displayMessage__plom_diag_inputValue(error="All values should be > 0", color='red')
                            return False
                        displayMessage__plom_diag_inputValue()
                        return True
                else:
                    if opt_save__plom_diag_inputType.get() in diag_criteria_input_types[0:2]:
                        displayMessage__plom_diag_inputValue(error = 'Input should follow the pattern: integer1, integer2, integer3', color = 'red')
                    elif  opt_save__plom_diag_inputType.get() == diag_criteria_input_types[2]:
                        displayMessage__plom_diag_inputValue(error = 'Input should follow the pattern: integer1, integer2, ...', color = 'red')
                    return False
            
            if why == "1": # insertion
                if what.isdigit() or what == " " or what == ",":
                    displayMessage__plom_diag_inputValue()
                    return True
                else:
                    return False
            
            if why == "0":
                displayMessage__plom_diag_inputValue()
                return True
        
        elif opt_save__plom_diag_criteria.get() == diag_criteria_options[2]: # EPSILON CONVERGENCE
            if why == "1": # insertion
                if what.isdigit() or what in [" ", ",", "."]:
                    displayMessage__plom_diag_inputValue()
                    return True
                else:
                    return False
            
            if why == "0":
                displayMessage__plom_diag_inputValue()
                return True
            
            if opt_save__plom_diag_inputType.get() == diag_criteria_input_types[0]:
                pattern = r"^\s*\d+(\.\d+)?\s*,\s*\d+(\.\d+)?\s*,\s*\d+(\.\d+)?\s*$"
            elif opt_save__plom_diag_inputType.get() == diag_criteria_input_types[1]:
                pattern = r"^\s*\d+(\.\d+)?\s*,\s*\d+(\.\d+)?\s*,\s*\d+\s*$"
            match = re.match(pattern, input_str)
            
            if reason == "focusin" or reason == "focusout":
                if len(input_str) == 0:
                    displayMessage__plom_diag_inputValue()
                    return True
                if match:
                    if opt_save__plom_diag_inputType.get() in diag_criteria_input_types[0:2]:
                        a, b, c = map(float, re.findall(r"\d+\.\d+|\d+", input_str))
                        if b < a:
                            displayMessage__plom_diag_inputValue(error="Max should be >= Min", color='red')
                            return False
                        if c == 0:
                            if opt_save__plom_diag_inputType.get() == diag_criteria_input_types[0]:
                                displayMessage__plom_diag_inputValue(error="Step should be > 0", color='red')
                            else:
                                displayMessage__plom_diag_inputValue(error="Num cases should be > 0", color='red')
                            return False
                        displayMessage__plom_diag_inputValue()
                        return True
                    elif opt_save__plom_diag_inputType.get() == diag_criteria_input_types[2]:
                        floats = list(map(float, re.findall(r"\d+", input_str)))
                        if min(floats) == 0:
                            displayMessage__plom_diag_inputValue(error="All values should be > 0", color='red')
                            return False
                        displayMessage__plom_diag_inputValue()
                        return True
                else:
                    if opt_save__plom_diag_inputType.get() == diag_criteria_input_types[0]:
                        displayMessage__plom_diag_inputValue(error = 'Input should follow the pattern: value1, value2, value3', color = 'red')
                    if opt_save__plom_diag_inputType.get() == diag_criteria_input_types[1]:
                        displayMessage__plom_diag_inputValue(error = 'Input should follow the pattern: value1, value2, integer', color = 'red')
                    elif  opt_save__plom_diag_inputType.get() == diag_criteria_input_types[2]:
                        displayMessage__plom_diag_inputValue(error = 'Input should follow the pattern: value1, value2, ...', color = 'red')
                    return False
    
    def displayMessage__plom_diag_inputValue(error = '', color = 'black'):  
        error_label__plom_diag_inputValue['text'] = error  
        opt_value__plom_diag_inputValue['foreground'] = color  
    
    reg_val__validate__plom_diag_inputValue = root.register(validate__plom_diag_inputValue)
    opt_value__plom_diag_inputValue.config(validate="all", validatecommand=(reg_val__validate__plom_diag_inputValue, '%P', '%d', '%i', '%S', '%V'))
    
    
    #-# error label
    group_row += 1
    error_label__plom_diag_inputValue = ttk.Label(frame__plom_diag, foreground = 'red')  
    error_label__plom_diag_inputValue.grid(row = group_row, column = 0, columnspan=2, sticky = 'w')
    
    
    frame__plom_diag.grid_columnconfigure(0, weight=0)  # Label column (fixed size)
    frame__plom_diag.grid_columnconfigure(1, weight=1)  # Entry column (expandable)
    
    ################################################################################
    ################################################################################
    
    # Group 2: PLoM data-related options
    group_row = 0
    current_row += 1
    frame__plom_data = tk.LabelFrame(plom_settings_frame, text="Data", padx=10, pady=10, font=("Arial", 10, "bold"))
    frame__plom_data.grid(row=current_row, column=0, columnspan=3, sticky='ew', padx=10, pady=(10, 5))
    
    opt_save__plom_data_path = tk.StringVar(frame__plom_data)
    opt_label__plom_data_path = tk.Label(frame__plom_data, text="Data path", anchor='w', fg='blue')
    opt_label__plom_data_path.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_data_path = tk.Entry(frame__plom_data, textvariable=opt_save__plom_data_path)
    opt_value__plom_data_path.grid(row=group_row, column=1, sticky='ew')
    opt_button__plom_data_path = tk.Button(frame__plom_data, text="Browse", command=lambda: browse_file(opt_value__plom_data_path))
    opt_button__plom_data_path.grid(row=group_row, column=2, sticky='ew', padx=(5, 0))
    
    group_row += 1
    columnsAre_options = [" Features", " Samples"]
    opt_save__plom_data_columnsAre = tk.StringVar(frame__plom_data)
    opt_label__plom_data_columnsAre = tk.Label(frame__plom_data, text="Columns are", anchor='w')
    opt_label__plom_data_columnsAre.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value_plom_data_columnsAre = ttk.Combobox(frame__plom_data, values=columnsAre_options, state='readonly', textvariable=opt_save__plom_data_columnsAre)
    opt_value_plom_data_columnsAre.current(0)
    opt_value_plom_data_columnsAre.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__plom_data_hasLabels = tk.IntVar()
    opt_label__plom_data_hasLabels = tk.Label(frame__plom_data, text="Features have labels", anchor='w')
    opt_label__plom_data_hasLabels.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value_plom_data_hasLabels = tk.Checkbutton(frame__plom_data, variable=opt_save__plom_data_hasLabels, onvalue = 1, offvalue = 0, anchor='w')
    opt_value_plom_data_hasLabels.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__plom_data_hasIndices = tk.IntVar()
    opt_label__plom_data_hasIndices = tk.Label(frame__plom_data, text="Samples have indices", anchor='w')
    opt_label__plom_data_hasIndices.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value_plom_data_hasIndices = tk.Checkbutton(frame__plom_data, variable=opt_save__plom_data_hasIndices, onvalue = 1, offvalue = 0, anchor='w')
    opt_value_plom_data_hasIndices.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__plom_data_colIgnore = tk.StringVar(frame__plom_data)
    opt_label__plom_data_colIgnore = tk.Label(frame__plom_data, text="Column indices to ignore", anchor='w')
    opt_label__plom_data_colIgnore.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_data_colIgnore = tk.Entry(frame__plom_data, textvariable=opt_save__plom_data_colIgnore)
    opt_value__plom_data_colIgnore.grid(row=group_row, column=1, sticky='ew')
    
    def displayMessage__plom_data_colIndicesIgnore(error = '', color = 'black'):
            error_label__plom_data_colIgnore['text'] = error  
            opt_value__plom_data_colIgnore['foreground'] = color 
    
    def validate__plom_data_colIndicesIgnore(P, d, i, S, V):
        input_str = P
        why = d # action code: 0 for deletion, 1 for insertion, or -1 for focus in, focus out, or a change to the textvariable
        idx = i # index of insertion, or -1
        what = S # inserted character
        reason = V # reason for this callback: one of 'focusin', 'focusout', 'key', or 'forced' if the textvariable was changed
        
        pattern = r"^\s*\d+(\s*,\s*\d+)*\s*$"
        match = re.match(pattern, input_str)
        
        if reason == "focusin" or reason == "focusout":
            if len(input_str) == 0:
                displayMessage__plom_data_colIndicesIgnore()
                return True
            if match:
                displayMessage__plom_data_colIndicesIgnore()
                return True
            else:
                displayMessage__plom_data_colIndicesIgnore(error = 'Input should follow the pattern: integer1, integer2, ...', color = 'red')
                return False
        
        if why == "1": # insertion
            if what.isdigit() or what == " " or what == ",":
                displayMessage__plom_data_colIndicesIgnore()
                return True
            else:
                return False
        
        if why == "0":
            displayMessage__plom_data_colIndicesIgnore()
            return True
    
    reg_val__validate__plom_data_colIndicesIgnore = root.register(validate__plom_data_colIndicesIgnore)
    opt_value__plom_data_colIgnore.config(validate="all", validatecommand=(reg_val__validate__plom_data_colIndicesIgnore, '%P', '%d', '%i', '%S', '%V'))
    group_row += 1
    error_label__plom_data_colIgnore = ttk.Label(frame__plom_data, foreground = 'red')  
    error_label__plom_data_colIgnore.grid(row = group_row, column = 0, columnspan=2, sticky = 'w')
    
    group_row += 1
    opt_save__plom_data_rowIgnore = tk.StringVar(frame__plom_data)
    opt_label__plom_data_rowIgnore = tk.Label(frame__plom_data, text="Row indices to ignore", anchor='w')
    opt_label__plom_data_rowIgnore.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_data_rowIgnore = tk.Entry(frame__plom_data, textvariable=opt_save__plom_data_rowIgnore)
    opt_value__plom_data_rowIgnore.grid(row=group_row, column=1, sticky='ew')
    
    def displayMessage__plom_data_rowIndicesIgnore(error = '', color = 'black'):
            error_label__plom_data_rowIgnore['text'] = error  
            opt_value__plom_data_rowIgnore['foreground'] = color 
    
    def validate__plom_data_rowIndicesIgnore(P, d, i, S, V):
        input_str = P
        why = d # action code: 0 for deletion, 1 for insertion, or -1 for focus in, focus out, or a change to the textvariable
        idx = i # index of insertion, or -1
        what = S # inserted character
        reason = V # reason for this callback: one of 'focusin', 'focusout', 'key', or 'forced' if the textvariable was changed
        
        pattern = r"^\s*\d+(\s*,\s*\d+)*\s*$"
        match = re.match(pattern, input_str)
        
        if reason == "focusin" or reason == "focusout":
            if len(input_str) == 0:
                displayMessage__plom_data_rowIndicesIgnore()
                return True
            if match:
                displayMessage__plom_data_rowIndicesIgnore()
                return True
            else:
                displayMessage__plom_data_rowIndicesIgnore(error = 'Input should follow the pattern: integer1, integer2, ...', color = 'red')
                return False
        
        if why == "1": # insertion
            if what.isdigit() or what == " " or what == ",":
                displayMessage__plom_data_rowIndicesIgnore()
                return True
            else:
                return False
        
        if why == "0":
            displayMessage__plom_data_rowIndicesIgnore()
            return True
    
    reg_val__validate__plom_data_rowIndicesIgnore = root.register(validate__plom_data_rowIndicesIgnore)
    opt_value__plom_data_rowIgnore.config(validate="all", validatecommand=(reg_val__validate__plom_data_rowIndicesIgnore, '%P', '%d', '%i', '%S', '%V'))
    group_row += 1
    error_label__plom_data_rowIgnore = ttk.Label(frame__plom_data, foreground = 'red')  
    error_label__plom_data_rowIgnore.grid(row = group_row, column = 0, columnspan=2, sticky = 'w')
    
    
    # Configure the data_group_plom_frame grid columns to ensure proper alignment and expandability
    frame__plom_data.grid_columnconfigure(0, weight=0)  # Label column (fixed size)
    frame__plom_data.grid_columnconfigure(1, weight=1)  # Entry column (expandable)
    
    ################################################################################
    ################################################################################
    
    # Group 3: PLoM scaling-related options
    group_row = 0
    current_row += 1
    
    frame__plom_scaling = tk.LabelFrame(plom_settings_frame, text="Scaling", padx=10, pady=10, font=("Arial", 10, "bold"))
    frame__plom_scaling.grid(row=current_row, column=0, columnspan=2, sticky='ew', padx=10, pady=(10, 5))
    
    # Example settings for Group 2
    scaling_options = [" Yes", " No"]
    opt_save__plom_scaling_yesNo = tk.StringVar(frame__plom_scaling)
    opt_label__plom_scaling_yesNo = tk.Label(frame__plom_scaling, text="Scale data", anchor='w')
    opt_label__plom_scaling_yesNo.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_scaling_yesNo = ttk.Combobox(frame__plom_scaling, values=scaling_options, state='readonly', textvariable=opt_save__plom_scaling_yesNo)
    opt_value__plom_scaling_yesNo.current(0)
    opt_value__plom_scaling_yesNo.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    scaling_methods = ["Normalization", "MinMax"]
    opt_save__plom_scaling_method = tk.StringVar(frame__plom_scaling)
    opt_label__plom_scaling_method = tk.Label(frame__plom_scaling, text="Scaling method", anchor='w')
    opt_label__plom_scaling_method.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_scaling_method = ttk.Combobox(frame__plom_scaling, values=scaling_methods, state='readonly', textvariable=opt_save__plom_scaling_method)
    opt_value__plom_scaling_method.current(0)
    opt_value__plom_scaling_method.grid(row=group_row, column=1, sticky='ew')
    
    def update_scaling_method_label(event):
        selected_option = opt_save__plom_scaling_yesNo.get()
        if selected_option == " No":
            opt_value__plom_scaling_method.config(state="disabled")
        else:
            opt_value__plom_scaling_method.config(state="readonly")
            
    opt_value__plom_scaling_yesNo.bind("<<ComboboxSelected>>", update_scaling_method_label)
    
    
    # Configure the frame__plom_scaling grid columns to ensure proper alignment and expandability
    frame__plom_scaling.grid_columnconfigure(0, weight=0)  # Label column (fixed size)
    frame__plom_scaling.grid_columnconfigure(1, weight=0)  # Entry column (expandable)
    
    ################################################################################
    ################################################################################
    
    # Group: PLoM PCA-related options
    group_row = 0
    current_row += 1
    
    frame__plom_pca = tk.LabelFrame(plom_settings_frame, text="PCA", padx=10, pady=10, font=("Arial", 10, "bold"))
    frame__plom_pca.grid(row=current_row, column=0, columnspan=2, sticky='ew', padx=10, pady=(10, 5))
    
    pca_options = [" Yes", " No"]
    opt_save__plom_pca_yesNo = tk.StringVar(frame__plom_pca)
    opt_label__plom_pca_yesNo = tk.Label(frame__plom_pca, text="Run PCA", anchor='w')
    opt_label__plom_pca_yesNo.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_pca_yesNo = ttk.Combobox(frame__plom_pca, values=pca_options, state='readonly', textvariable=opt_save__plom_pca_yesNo)
    opt_value__plom_pca_yesNo.current(0)
    opt_value__plom_pca_yesNo.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    pca_methods = ["Cumulative Energy", "Eigenvalue Cutoff", "PCA Dimension"]
    opt_save__plom_pca_method = tk.StringVar(frame__plom_pca)
    opt_label__plom_pca_method = tk.Label(frame__plom_pca, text="PCA reduction method", anchor='w')
    opt_label__plom_pca_method.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_pca_method = ttk.Combobox(frame__plom_pca, values=pca_methods, state='readonly', textvariable=opt_save__plom_pca_method)
    opt_value__plom_pca_method.current(0)
    opt_value__plom_pca_method.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    pca_criteria = ["Target Cumulative Energy", "Eigenvalue Cutoff Value", "Desired PCA Dimension"]
    opt_save__plom_pca_criteria = tk.StringVar(frame__plom_pca)
    opt_save__plom_pca_criteria.set("0.999")
    opt_label__plom_pca_criteria = tk.Label(frame__plom_pca, text=pca_criteria[0], anchor='w')
    opt_label__plom_pca_criteria.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_pca_criteria = tk.Entry(frame__plom_pca, textvariable=opt_save__plom_pca_criteria)
    opt_value__plom_pca_criteria.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    pca_scaleEvecs = [" Yes", " No"]
    opt_save__plom_pca_scaleEvecs = tk.StringVar(frame__plom_pca)
    opt_label__plom_pca_scaleEvecs = tk.Label(frame__plom_pca, text="Scale Eigenvectors", anchor='w')
    opt_label__plom_pca_scaleEvecs.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_pca_scaleEvecs = ttk.Combobox(frame__plom_pca, values=pca_scaleEvecs, state='readonly', textvariable=opt_save__plom_pca_scaleEvecs)
    opt_value__plom_pca_scaleEvecs.current(0)
    opt_value__plom_pca_scaleEvecs.grid(row=group_row, column=1, sticky='ew')
    
    def update_pca_criteria_label(event):
        selected_option = opt_save__plom_pca_method.get()
        if selected_option != opt_save__plom_pca_method_OLD.get():
            opt_save__plom_pca_method_OLD.set(selected_option)
            if selected_option == pca_methods[0]:
                opt_label__plom_pca_criteria.config(text=pca_criteria[0])
                opt_save__plom_pca_criteria.set("0.999")
            elif selected_option == pca_methods[1]:
                opt_label__plom_pca_criteria.config(text=pca_criteria[1])
                opt_save__plom_pca_criteria.set("1e-3")
            elif selected_option == pca_methods[2]:
                opt_label__plom_pca_criteria.config(text=pca_criteria[2])
                opt_save__plom_pca_criteria.set("2")
    
    opt_save__plom_pca_method_OLD = tk.StringVar(frame__plom_pca)
    opt_save__plom_pca_method_OLD.set(opt_save__plom_pca_method.get())
    opt_value__plom_pca_method.bind("<<ComboboxSelected>>", update_pca_criteria_label)
    
    def update_pca_options(event):
        selected_option = opt_save__plom_pca_yesNo.get()
        if selected_option == pca_options[1]:
            opt_value__plom_pca_method.config(state='disabled')
            opt_value__plom_pca_criteria.config(state='disabled')
            opt_value__plom_pca_scaleEvecs.config(state='disabled')
        else:
            opt_value__plom_pca_method.config(state='readonly')
            opt_value__plom_pca_criteria.config(state='normal')
            opt_value__plom_pca_scaleEvecs.config(state='readonly')
    
     
    opt_value__plom_pca_yesNo.bind("<<ComboboxSelected>>", update_pca_options)
    
    
    # Configure the frame__plom_scaling grid columns to ensure proper alignment and expandability
    frame__plom_pca.grid_columnconfigure(0, weight=0)  # Label column (fixed size)
    frame__plom_pca.grid_columnconfigure(1, weight=0)  # Entry column (expandable)
    
    
    ################################################################################
    ################################################################################
    
    # Add Submit button
    current_row += 1
    button_createJob = tk.Button(plom_settings_frame, text="Create job", command=create_job)
    button_createJob.grid(row=current_row, column=0, sticky='w', padx=10, pady=(20, 0))
    
    button_runJob = tk.Button(plom_settings_frame, text="Run job", command=run_job_thread)
    button_runJob.grid(row=current_row, column=1, sticky='w', padx=10, pady=(20, 0))
    
    current_row += 1
    job_message = tk.Label(plom_settings_frame, foreground = 'black', padx=10, pady=10)
    job_message.grid(row=current_row, column = 0, columnspan=2, sticky = 'w')
    
    
    ################################################################################
    ################################################################################
    
    current_row = -1
    
    ################################################################################
    ################################################################################
    
    # Group: PLoM DMAPS-related options
    group_row = 0
    current_row += 1
    
    frame__plom_dmaps = tk.LabelFrame(plom_settings_frame2, text="DMAPs", padx=10, pady=10, font=("Arial", 10, "bold"))
    frame__plom_dmaps.grid(row=current_row, column=0, columnspan=2, sticky='ew', padx=10, pady=(10, 5))
    
    dmaps_options = ["Yes", "No"]
    opt_save__plom_dmaps_yesNo = tk.StringVar(frame__plom_dmaps)
    opt_label__plom_dmaps_yesNo = tk.Label(frame__plom_dmaps, text="Run DMAPs", anchor='w')
    opt_label__plom_dmaps_yesNo.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_dmaps_yesNo = ttk.Combobox(frame__plom_dmaps, values=dmaps_options, state='readonly', textvariable=opt_save__plom_dmaps_yesNo)
    opt_value__plom_dmaps_yesNo.current(0)
    opt_value__plom_dmaps_yesNo.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__plom_dmaps_epsilon = tk.StringVar(frame__plom_dmaps)
    opt_save__plom_dmaps_epsilon.set('auto')
    opt_label__plom_dmaps_epsilon = tk.Label(frame__plom_dmaps, text="Epsilon", anchor='w')
    opt_label__plom_dmaps_epsilon.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_dmaps_epsilon = tk.Entry(frame__plom_dmaps, textvariable=opt_save__plom_dmaps_epsilon)
    opt_value__plom_dmaps_epsilon.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__plom_dmaps_kappa = tk.StringVar(frame__plom_dmaps)
    opt_save__plom_dmaps_kappa.set('1')
    opt_label__plom_dmaps_kappa = tk.Label(frame__plom_dmaps, text="Kappa", anchor='w')
    opt_label__plom_dmaps_kappa.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_dmaps_kappa = tk.Entry(frame__plom_dmaps, textvariable=opt_save__plom_dmaps_kappa)
    opt_value__plom_dmaps_kappa.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__plom_dmaps_L = tk.StringVar(frame__plom_dmaps)
    opt_save__plom_dmaps_L.set('0.1')
    opt_label__plom_dmaps_L = tk.Label(frame__plom_dmaps, text="L (eigval drop factor)", anchor='w')
    opt_label__plom_dmaps_L.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_dmaps_L = tk.Entry(frame__plom_dmaps, textvariable=opt_save__plom_dmaps_L)
    opt_value__plom_dmaps_L.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__plom_dmaps_firstEigvec = tk.StringVar(frame__plom_dmaps)
    opt_label__plom_dmaps_firstEigvec = tk.Label(frame__plom_dmaps, text="Include first eigenvector", anchor='w')
    opt_label__plom_dmaps_firstEigvec.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_dmaps_firstEigvec = ttk.Combobox(frame__plom_dmaps, values=["Yes", "No"], state='readonly', textvariable=opt_label__plom_dmaps_firstEigvec)
    opt_value__plom_dmaps_firstEigvec.current(1)
    opt_value__plom_dmaps_firstEigvec.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__plom_dmaps_dim = tk.StringVar(frame__plom_dmaps)
    opt_save__plom_dmaps_dim.set('0')
    opt_label__plom_dmaps_dim = tk.Label(frame__plom_dmaps, text="Dimension override", anchor='w')
    opt_label__plom_dmaps_dim.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_dmaps_dim = tk.Entry(frame__plom_dmaps, textvariable=opt_save__plom_dmaps_dim)
    opt_value__plom_dmaps_dim.grid(row=group_row, column=1, sticky='ew')
    
    frame__plom_dmaps.grid_columnconfigure(0, weight=0)  # Label column (fixed size)
    frame__plom_dmaps.grid_columnconfigure(1, weight=1)  # Entry column (expandable)
    
    
    ################################################################################
    ################################################################################
    
    # Group: PLoM Projection-related options
    group_row = 0
    current_row += 1
    
    frame__plom_projection = tk.LabelFrame(plom_settings_frame2, text="Projection", padx=10, pady=10, font=("Arial", 10, "bold"))
    frame__plom_projection.grid(row=current_row, column=0, columnspan=2, sticky='ew', padx=10, pady=(10, 5))
    
    projection_options = ["Yes", "No"]
    opt_save__plom_projection_yesNo = tk.StringVar(frame__plom_projection)
    opt_label__plom_projection_yesNo = tk.Label(frame__plom_projection, text="Project data", anchor='w')
    opt_label__plom_projection_yesNo.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_projection_yesNo = ttk.Combobox(frame__plom_projection, values=projection_options, state='readonly', textvariable=opt_save__plom_projection_yesNo)
    opt_value__plom_projection_yesNo.current(0)
    opt_value__plom_projection_yesNo.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    projection_source_options = ["PCA space", "Scaled space", "Original space"]
    opt_save__plom_projection_source = tk.StringVar(frame__plom_projection)
    opt_label__plom_projection_source = tk.Label(frame__plom_projection, text="Projection source", anchor='w')
    opt_label__plom_projection_source.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_projection_source = ttk.Combobox(frame__plom_projection, values=projection_source_options, state='readonly', textvariable=opt_save__plom_projection_source)
    opt_value__plom_projection_source.current(0)
    opt_value__plom_projection_source.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    projection_target_options = ["DMAPs space", "PCA space"]
    opt_save__plom_projection_target = tk.StringVar(frame__plom_projection)
    opt_label__plom_projection_target = tk.Label(frame__plom_projection, text="Projection target", anchor='w')
    opt_label__plom_projection_target.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_projection_target = ttk.Combobox(frame__plom_projection, values=projection_target_options, state='readonly', textvariable=opt_save__plom_projection_target)
    opt_value__plom_projection_target.current(0)
    opt_value__plom_projection_target.grid(row=group_row, column=1, sticky='ew')
    
    frame__plom_projection.grid_columnconfigure(0, weight=0)  # Label column (fixed size)
    frame__plom_projection.grid_columnconfigure(1, weight=1)  # Entry column (expandable)
    
    
    ################################################################################
    ################################################################################
    
    # Group: PLoM Sampling-related options
    group_row = 0
    current_row += 1
    
    frame__plom_sampling = tk.LabelFrame(plom_settings_frame2, text="Sampling", padx=10, pady=10, font=("Arial", 10, "bold"))
    frame__plom_sampling.grid(row=current_row, column=0, columnspan=2, sticky='ew', padx=10, pady=(10, 5))
    
    sampling_options = ["Yes", "No"]
    opt_save__plom_sampling_yesNo = tk.StringVar(frame__plom_sampling)
    opt_label__plom_sampling_yesNo = tk.Label(frame__plom_sampling, text="Run sampling", anchor='w')
    opt_label__plom_sampling_yesNo.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_sampling_yesNo = ttk.Combobox(frame__plom_sampling, values=sampling_options, state='readonly', textvariable=opt_save__plom_sampling_yesNo)
    opt_value__plom_sampling_yesNo.current(0)
    opt_value__plom_sampling_yesNo.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__plom_sampling_NSamples = tk.StringVar(frame__plom_sampling)
    opt_save__plom_sampling_NSamples.set('1')
    opt_label__plom_sampling_NSamples = tk.Label(frame__plom_sampling, text="Number of samples", anchor='w', fg='blue')
    opt_label__plom_sampling_NSamples.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_sampling_NSamples = tk.Entry(frame__plom_sampling, textvariable=opt_save__plom_sampling_NSamples)
    opt_value__plom_sampling_NSamples.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__plom_sampling_f0 = tk.StringVar(frame__plom_sampling)
    opt_save__plom_sampling_f0.set('1.0')
    opt_label__plom_sampling_f0 = tk.Label(frame__plom_sampling, text="f0", anchor='w')
    opt_label__plom_sampling_f0.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_sampling_f0 = tk.Entry(frame__plom_sampling, textvariable=opt_save__plom_sampling_f0)
    opt_value__plom_sampling_f0.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__plom_sampling_dr = tk.StringVar(frame__plom_sampling)
    opt_save__plom_sampling_dr.set('0.1')
    opt_label__plom_sampling_dr = tk.Label(frame__plom_sampling, text="dr", anchor='w')
    opt_label__plom_sampling_dr.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_sampling_dr = tk.Entry(frame__plom_sampling, textvariable=opt_save__plom_sampling_dr)
    opt_value__plom_sampling_dr.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__plom_sampling_itoSteps = tk.StringVar(frame__plom_sampling)
    opt_save__plom_sampling_itoSteps.set('auto')
    opt_label__plom_sampling_itoSteps = tk.Label(frame__plom_sampling, text="Num. of Ito steps", anchor='w')
    opt_label__plom_sampling_itoSteps.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_sampling_itoSteps = tk.Entry(frame__plom_sampling, textvariable=opt_save__plom_sampling_itoSteps)
    opt_value__plom_sampling_itoSteps.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    sampling_potMethod_options = ["1", "2", "3", "4", "5", "6", "7"]
    opt_save__plom_sampling_potMethod = tk.StringVar(frame__plom_sampling)
    opt_label__plom_sampling_potMethod = tk.Label(frame__plom_sampling, text="Potential method", anchor='w')
    opt_label__plom_sampling_potMethod.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_sampling_potMethod = ttk.Combobox(frame__plom_sampling, values=sampling_potMethod_options, state='readonly', textvariable=opt_save__plom_sampling_potMethod)
    opt_value__plom_sampling_potMethod.current(2)
    opt_value__plom_sampling_potMethod.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__plom_sampling_kdeBW = tk.StringVar(frame__plom_sampling)
    opt_save__plom_sampling_kdeBW.set('1.0')
    opt_label__plom_sampling_kdeBW = tk.Label(frame__plom_sampling, text="KDE bandwidth factor", anchor='w')
    opt_label__plom_sampling_kdeBW.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_sampling_kdeBW = tk.Entry(frame__plom_sampling, textvariable=opt_save__plom_sampling_kdeBW)
    opt_value__plom_sampling_kdeBW.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    sampling_saveSamples_options = ["Yes", "No"]
    opt_save__plom_sampling_saveSamples = tk.StringVar(frame__plom_sampling)
    opt_label__plom_sampling_saveSamples = tk.Label(frame__plom_sampling, text="Save samples", anchor='w')
    opt_label__plom_sampling_saveSamples.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_sampling_saveSamples = ttk.Combobox(frame__plom_sampling, values=sampling_saveSamples_options, state='readonly', textvariable=opt_save__plom_sampling_saveSamples)
    opt_value__plom_sampling_saveSamples.current(0)
    opt_value__plom_sampling_saveSamples.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    sampling_samplesFType_options = ["txt", "npy"]
    opt_save__plom_sampling_samplesFType = tk.StringVar(frame__plom_sampling)
    opt_label__plom_sampling_samplesFType = tk.Label(frame__plom_sampling, text="Samples filetype", anchor='w')
    opt_label__plom_sampling_samplesFType.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_sampling_samplesFType = ttk.Combobox(frame__plom_sampling, values=sampling_samplesFType_options, state='readonly', textvariable=opt_save__plom_sampling_samplesFType)
    opt_value__plom_sampling_samplesFType.current(0)
    opt_value__plom_sampling_samplesFType.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    sampling_parallel_options = ["Yes", "No"]
    opt_save__plom_sampling_parallel = tk.StringVar(frame__plom_sampling)
    opt_label__plom_sampling_parallel = tk.Label(frame__plom_sampling, text="Parallel sampling", anchor='w')
    opt_label__plom_sampling_parallel.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_sampling_parallel = ttk.Combobox(frame__plom_sampling, values=sampling_parallel_options, state='readonly', textvariable=opt_save__plom_sampling_parallel)
    opt_value__plom_sampling_parallel.current(1)
    opt_value__plom_sampling_parallel.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__plom_sampling_njobs = tk.StringVar(frame__plom_sampling)
    opt_save__plom_sampling_njobs.set('-1')
    opt_label__plom_sampling_njobs = tk.Label(frame__plom_sampling, text="Number of jobs", anchor='w')
    opt_label__plom_sampling_njobs.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_sampling_njobs = tk.Entry(frame__plom_sampling, textvariable=opt_save__plom_sampling_njobs)
    opt_value__plom_sampling_njobs.grid(row=group_row, column=1, sticky='ew')
    
    frame__plom_sampling.grid_columnconfigure(0, weight=0)  # Label column (fixed size)
    frame__plom_sampling.grid_columnconfigure(1, weight=1)  # Entry column (expandable)
    
    ################################################################################
    ################################################################################
    
    # Group: PLoM Results-related options
    group_row = 0
    current_row += 1
    
    frame__plom_results = tk.LabelFrame(plom_settings_frame2, text="Results", padx=10, pady=10, font=("Arial", 10, "bold"))
    frame__plom_results.grid(row=current_row, column=0, columnspan=2, sticky='ew', padx=10, pady=(10, 5))
    
    group_row += 1
    results_save_options = ["Yes", "No"]
    opt_save__plom_results_dict = tk.StringVar(frame__plom_results)
    opt_label__plom_results_dict = tk.Label(frame__plom_results, text="Save results dictionary", anchor='w')
    opt_label__plom_results_dict.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_results_dict = ttk.Combobox(frame__plom_results, values=results_save_options, state='readonly', textvariable=opt_save__plom_results_dict)
    opt_value__plom_results_dict.current(0)
    opt_value__plom_results_dict.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__plom_results_plots = tk.StringVar(frame__plom_results)
    opt_label__plom_results_plots = tk.Label(frame__plom_results, text="Save plots", anchor='w')
    opt_label__plom_results_plots.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__plom_results_plots = ttk.Combobox(frame__plom_results, values=results_save_options, state='readonly', textvariable=opt_save__plom_results_plots)
    opt_value__plom_results_plots.current(0)
    opt_value__plom_results_plots.grid(row=group_row, column=1, sticky='ew')
    
    
    frame__plom_results.grid_columnconfigure(0, weight=0)  # Label column (fixed size)
    frame__plom_results.grid_columnconfigure(1, weight=1)  # Entry column (expandable)
    
    ################################################################################
    ################################################################################
    
    # Configure the left frame grid columns to ensure proper alignment and expandability
    plom_settings_frame.grid_columnconfigure(0, weight=0)  # Label column (fixed size)
    plom_settings_frame.grid_columnconfigure(1, weight=1)  # Entry column (expandable)
    
    plom_settings_frame2.grid_columnconfigure(0, weight=0)  # Label column (fixed size)
    plom_settings_frame2.grid_columnconfigure(1, weight=1)  # Entry column (expandable)
    
    # Add a label for the log frame
    log_label = tk.Label(log_frame, text="Log", font=("Arial", 12, "bold"))
    log_label.pack(side=tk.TOP, anchor='w', pady=(5, 0))  # Add top padding
    
    ################################################################################
    ################################################################################
    
    # Create the 'Clear Log' button and pack it above the log box
    clear_button = tk.Button(log_frame, text="Clear Log", command=clear_log)
    clear_button.pack(side=tk.TOP, anchor='w', pady=5)  # Adjust padding as needed
    
    # Add a text widget for the log with padding to control its start position
    log_text = tk.Text(log_frame, wrap='word', bg='white')
    log_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 5))  # Add right padding
    
    original_stdout = sys.stdout
    sys.stdout = TextRedirector(log_text)
    # sys.stdout = original_stdout
    
    
    
    #*****************************************************************************#
    
    #******************************   JOB RESULTS TAB ****************************#
    
    
    # Add sample content to other tabs
    # tk.Label(jobResults_tab, text="Job Results Tab Content", font=("Arial", 12)).pack(pady=20)
    
    global job_dict
    job_dict = None
    
    
    def browse_results_file():
        # Open a file dialog to choose the results dictionary file
        file_path = filedialog.askopenfilename()
        results_entry.delete(0, tk.END)  # Clear the entry box
        results_entry.insert(0, file_path)  # Insert selected path into the entry box
    
    
    def load_results_file():
        global job_dict
        # Function to load the results file from the path entered
        file_path = results_entry.get()
        try:
            job_dict = load_dict(file_path)
            status_label.config(text="Results dictionary loaded successfully", fg="green")
            print(job_dict.keys())
        except:
            status_label.config(text="Cannot load results dictionary", fg="red")
    
    
    def generate_plot(plot_type):
        # Clear the existing plot (if any)
        for widget in plot_area.winfo_children():
            widget.destroy()
    
        # Generate random data for the plot (you can replace this with your actual data)
        x = np.linspace(0, 10, 100)
        if plot_type == "Plot 1":
            y = np.sin(x)
        elif plot_type == "Plot 2":
            y = np.cos(x)
        else:
            y = np.tan(x)
    
        # Create a Matplotlib figure and plot
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_title(plot_type)
    
        # Embed the plot in the Tkinter GUI
        canvas = FigureCanvasTkAgg(fig, master=plot_area)  # Create canvas from the figure
        canvas.draw()  # Draw the plot onto the canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Prevent matplotlib from opening a new window
        # plt.close(fig)
    
    
    def plot2D_training(plom_dict, i=0, j=1, size=9, pt_size=10, 
                                      color='blue'):
        if plom_dict is None:
            print("no dict")
            return
        
        for widget in plot_area.winfo_children():
            widget.destroy()
            
        training = plom_dict['data']['training'].T
        
        fig, ax = plt.subplots(figsize=(size, size))
        plt.scatter(training[i], training[j], s=pt_size, c=color)
        plt.gca().set_aspect('equal')
        plt.title(f'Training, n={training.shape[1]}')
        
        canvas = FigureCanvasTkAgg(fig, master=plot_area)  # Create canvas from the figure
        canvas.draw()  # Draw the plot onto the canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    
    def plot2D_reconstructed_training(plom_dict, i=0, j=1, size=9, pt_size=10, 
                                      color=['cmap','cmap']):
        if plom_dict is None:
            print("no dict")
            return
        
        for widget in plot_area.winfo_children():
            widget.destroy()
            
        training = plom_dict['data']['training'].T
        reconst_training = plom_dict['data']['reconst_training'].T
        [c1, c2] = color
        if c1 == 'cmap': c1 = range(training.shape[1])
        if c2 == 'cmap': c2 = range(training.shape[1])
        # plt.figure(figsize=(size, size))
        fig, ax = plt.subplots(figsize=(size, size))
        t_plot = plt.scatter(training[i], training[j], s=pt_size, c=c1)
        t_r_plot = plt.scatter(reconst_training[i], reconst_training[j], 
                               s=pt_size, c=c2)
        plt.legend((t_plot, t_r_plot), ('Training', 'Reconstructed training'), 
                   loc='best')
        plt.gca().set_aspect('equal')
        plt.title(f'Training vs reconstructed training, n={training.shape[1]}')
        
        canvas = FigureCanvasTkAgg(fig, master=plot_area)  # Create canvas from the figure
        canvas.draw()  # Draw the plot onto the canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    
    def plot2d_samples(plom_dict, i=0, j=1, size=9, pt_size=10):
        if plom_dict is None:
            print("no dict")
            return
        
        for widget in plot_area.winfo_children():
            widget.destroy()
        
        training = plom_dict['data']['training'].T
        samples = plom_dict['data']['augmented'].T
        N = training.shape[1]
        num_sample = plom_dict['input']['ito_num_samples']
        fig, ax = plt.subplots(figsize=(size, size))
        plt.scatter(training[i], training[j], color='b', s=pt_size, 
                    label='Training', marker="+")
        for k in range(num_sample):
            plt.scatter(samples[i, k*N:(k+1)*N], samples[j, k*N:(k+1)*N], 
                        color=np.random.rand(3), s=pt_size)
        plt.legend(loc='best')
        plt.gca().set_aspect('equal')
        plt.title('Training + New samples')
        
        canvas = FigureCanvasTkAgg(fig, master=plot_area)  # Create canvas from the figure
        canvas.draw()  # Draw the plot onto the canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    
    def plot_dmaps_eigenvalues(plom_dict, n=0, size=8, pt_size=10, save=False):
        if plom_dict is None:
            print("no dict")
            return
        
        for widget in plot_area.winfo_children():
            widget.destroy()
        
        evals = plom_dict['dmaps']['eigenvalues'][1:]
        m = plom_dict['dmaps']['dimension']
        if n == 0:
            n = max(min(2*m, evals.size), 10)
        elif n=='all':
            n = evals.size
        
        fig, ax = plt.subplots(figsize=(size, size/2))
        plt.plot(range(m), evals[:m], c='r')
        plt.scatter(range(m), evals[:m], c='r', s=pt_size)
        plt.plot(range(m-1, n), evals[m-1:n], c='b', alpha=0.25)
        plt.scatter(range(m, n), evals[m:n], c='b', s=pt_size)
        plt.yscale("log")
        plt.title(f"DMAPS Eigenvalues (m={m})")
        
        canvas = FigureCanvasTkAgg(fig, master=plot_area)  # Create canvas from the figure
        canvas.draw()  # Draw the plot onto the canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    
    def plot2D_dmaps_basis(plom_dict, vecs=[1,2], size=9, pt_size=10):
        if plom_dict is None:
            print("no dict")
            return
        
        for widget in plot_area.winfo_children():
            widget.destroy()
        
        evecs = plom_dict['dmaps']['basis'][:, vecs].T
        c = range(evecs.shape[1])

        fig, ax = plt.subplots(figsize=(size, size))
        plt.scatter(evecs[0], evecs[1], s=pt_size, c=c)
        plt.gca().set_aspect('equal')
        plt.title(f'DMAPS basi vectors {vecs[0]} (x) vs {vecs[1]} (y)')
        
        canvas = FigureCanvasTkAgg(fig, master=plot_area)  # Create canvas from the figure
        canvas.draw()  # Draw the plot onto the canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    
    def plot_pca_eigenvalues(plom_dict, log=True, save=False):
        if plom_dict is None:
            print("no dict")
            return
        
        for widget in plot_area.winfo_children():
            widget.destroy()
        
        evals = np.flip(plom_dict['pca']['eigvals'])
        evals = evals[evals > 1e-15]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        if log:
            plt.yscale('log')
            plt.ylim(evals.min()*0.9, evals.max()*1.1)
        plt.scatter(range(len(evals)), evals, s=7)
        plt.title("PCA Eigenvalues")
        plt.xticks(np.arange(0, len(evals), 5))
        plt.xlabel("Eigenvalue Index")
        plt.ylabel("Eigenvalue")
        plt.grid()
        
        canvas = FigureCanvasTkAgg(fig, master=plot_area)  # Create canvas from the figure
        canvas.draw()  # Draw the plot onto the canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    
    def plot_training_pdf(plom_dict, i=0, size=9):
        if plom_dict is None:
            print("no dict")
            return
        
        for widget in plot_area.winfo_children():
            widget.destroy()
        
        training  = plom_dict['data']['training'][:, i]
        
        xmin = min(0.8*min(training), 1.2*min(training))
        xmax = max(0.8*max(training), 1.2*max(training))
        
        xx = np.linspace(xmin, xmax, 100)
        
        kde = gaussian_kde(training)
        pdf_values = kde(xx)
        
        fig, ax = plt.subplots(figsize=(size, size/2))
        plt.plot(xx, pdf_values)
        plt.title("PDF (training)")
        plt.xlabel(f"Feature {i}")
        plt.ylabel("PDF")
        plt.grid()
        
        canvas = FigureCanvasTkAgg(fig, master=plot_area)  # Create canvas from the figure
        canvas.draw()  # Draw the plot onto the canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    
    def plot_augmented_pdf(plom_dict, i=0, size=9):
        if plom_dict is None:
            print("no dict")
            return
        
        for widget in plot_area.winfo_children():
            widget.destroy()
        
        augmented  = plom_dict['data']['augmented'][:, i]
        
        xmin = min(0.8*min(augmented), 1.2*min(augmented))
        xmax = max(0.8*max(augmented), 1.2*max(augmented))
        
        xx = np.linspace(xmin, xmax, 100)
        
        kde = gaussian_kde(augmented)
        pdf_values = kde(xx)
        
        fig, ax = plt.subplots(figsize=(size, size/2))
        plt.plot(xx, pdf_values)
        plt.title("PDF (augmented)")
        plt.xlabel(f"Feature {i}")
        plt.ylabel("PDF")
        plt.grid()
        
        canvas = FigureCanvasTkAgg(fig, master=plot_area)  # Create canvas from the figure
        canvas.draw()  # Draw the plot onto the canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    
    def plot_train_vs_aug_pdf(plom_dict, i=0, size=9):
        if plom_dict is None:
            print("no dict")
            return
        
        for widget in plot_area.winfo_children():
            widget.destroy()
        
        training  = plom_dict['data']['training'][:, i]
        augmented  = plom_dict['data']['augmented'][:, i]
        
        xmin = min(0.8*min(training), 1.2*min(training), 0.8*min(augmented), 1.2*min(augmented))
        xmax = max(0.8*max(training), 1.2*max(training), 0.8*max(augmented), 1.2*max(augmented))
        
        xx = np.linspace(xmin, xmax, 100)
        
        kde_train = gaussian_kde(training)
        kde_aug = gaussian_kde(augmented)
        pdf_values_train = kde_train(xx)
        pdf_values_aug = kde_aug(xx)
        
        fig, ax = plt.subplots(figsize=(size, size/2))
        plt.plot(xx, pdf_values_aug, label="Augmented")
        plt.plot(xx, pdf_values_train, '--', color='black', alpha=0.5)
        plt.title("PDF (training vs. augmented)")
        plt.xlabel(f"Feature {i}")
        plt.ylabel("PDF")
        plt.legend()
        plt.grid()
        
        canvas = FigureCanvasTkAgg(fig, master=plot_area)  # Create canvas from the figure
        canvas.draw()  # Draw the plot onto the canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    
    def plot_training_jointPDF(plom_dict, i=0, j=1, size=9, surface=True):
        if plom_dict is None:
            print("no dict")
            return
        
        for widget in plot_area.winfo_children():
            widget.destroy()
        
        training  = plom_dict['data']['training'][:, [i, j]]
        
        xmin = min(0.9*min(training[:, 0]), 1.1*min(training[:, 0]))
        xmax = max(0.9*max(training[:, 0]), 1.1*max(training[:, 0]))
        ymin = min(0.9*min(training[:, 1]), 1.1*min(training[:, 1]))
        ymax = max(0.9*max(training[:, 1]), 1.1*max(training[:, 1]))
        xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        positions = np.vstack([xx.ravel(), yy.ravel()])
        
        kde = gaussian_kde(training.T)
        pdf_values = kde(positions)
        pdf_values = pdf_values.reshape(xx.shape)
        
        fig = plt.figure(figsize=(size, size))
        fig, ax = plt.subplots(figsize=(size, size))
        contour = ax.contourf(xx, yy, pdf_values, cmap='Blues')
        plt.scatter(training[:, 0], training[:, 1], s=5, c='red', label='Sample Points')

        plt.xlabel(f'Feature {i}')
        plt.ylabel(f'Feature {j}')
        plt.gca().set_aspect('equal')
        plt.title("Joint PDF (training)")
        plt.colorbar(contour, label='Density')
        plt.legend()
        
        canvas = FigureCanvasTkAgg(fig, master=plot_area)  # Create canvas from the figure
        canvas.draw()  # Draw the plot onto the canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    
    def plot_augmented_jointPDF(plom_dict, i=0, j=1, size=9, surface=True):
        if plom_dict is None:
            print("no dict")
            return
        
        for widget in plot_area.winfo_children():
            widget.destroy()
        
        training  = plom_dict['data']['training'][:, [i, j]]
        augmented = plom_dict['data']['augmented'][:, [i, j]]
        
        xmin = min(0.9*min(augmented[:, 0]), 1.1*min(augmented[:, 0]), 0.9*min(training[:, 0]), 1.1*min(training[:, 0]))
        xmax = max(0.9*max(augmented[:, 0]), 1.1*max(augmented[:, 0]), 0.9*max(training[:, 0]), 1.1*max(training[:, 0]))
        ymin = min(0.9*min(augmented[:, 1]), 1.1*min(augmented[:, 1]), 0.9*min(training[:, 1]), 1.1*min(training[:, 1]))
        ymax = max(0.9*max(augmented[:, 1]), 1.1*max(augmented[:, 1]), 0.9*max(training[:, 1]), 1.1*max(training[:, 1]))
        xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        positions = np.vstack([xx.ravel(), yy.ravel()])
        
        kde = gaussian_kde(augmented.T)
        pdf_values = kde(positions)
        pdf_values = pdf_values.reshape(xx.shape)
        
        fig, ax = plt.subplots(figsize=(size, size))
        contour = ax.contourf(xx, yy, pdf_values, cmap='Blues')
        plt.scatter(augmented[:, 0], augmented[:, 1], s=5, c='red', label='Augmented Sample Points')
        plt.scatter(training[:, 0], training[:, 1], s=5, c='yellow', label='Training Sample Points')

        plt.xlabel(f'Feature {i}')
        plt.ylabel(f'Feature {j}')
        plt.gca().set_aspect('equal')
        plt.title("Joint PDF (augmented)")
        plt.colorbar(contour, label='Density')
        plt.legend()
        
        canvas = FigureCanvasTkAgg(fig, master=plot_area)  # Create canvas from the figure
        canvas.draw()  # Draw the plot onto the canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    


    # Configure the grid layout for the Job Results tab
    jobResults_tab.grid_columnconfigure(1, weight=1)  # Make the right column expandable
    
    # Left column: options and buttons
    left_frame = tk.Frame(jobResults_tab, width=310)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    left_frame.grid_propagate(False)
    
    # Right column: plot area (which resizes with the window)
    plot_area = tk.Frame(jobResults_tab, bg="white", relief="sunken")
    plot_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    
    
    # Add elements to the left column
    # Section 1: Results dictionary
    results_section = tk.LabelFrame(left_frame, text="Results dictionary", padx=10, pady=10)
    results_section.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
    
    results_label = tk.Label(results_section, text="Results dictionary path")
    results_label.grid(row=0, column=0, sticky="w")
    
    results_entry = tk.Entry(results_section, width=32)
    results_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    
    browse_button = tk.Button(results_section, text="Browse", command=browse_results_file)
    browse_button.grid(row=1, column=1, padx=(5, 0), pady=5)
    
    # "Load" button below the entry field and browse button
    load_button = tk.Button(results_section, text="Load", command=load_results_file)
    load_button.grid(row=2, column=0, sticky="w", pady=5)
    
    status_label = tk.Label(results_section, text="", fg="green", anchor="w")
    status_label.grid(row=3, column=0, sticky="w", pady=5)
    
    # Section 2: Plots
    plots_section = tk.LabelFrame(left_frame, text="Plots", padx=10, pady=10)
    plots_section.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
    
    # Add buttons for generating different plots
    current_row = -1
    
    current_row += 1
    plot1_button = tk.Button(plots_section, text="Training data (2D)", command=lambda: plot2D_training(job_dict, int(plot1_var1_save.get()), int(plot1_var2_save.get())))
    plot1_button.grid(row=current_row, column=0, sticky="ew", pady=5)
    plot1_var1_save = tk.StringVar(plots_section)
    plot1_var1_save.set('0')
    plot1_var2_save = tk.StringVar(plots_section)
    plot1_var2_save.set('1')
    plot1_var1 = tk.Entry(plots_section, width=4, textvariable=plot1_var1_save, justify='center')
    plot1_var1.grid(row=current_row, column=1, sticky="ew", pady=5, padx=(10, 5))
    plot1_label = tk.Label(plots_section, text="vs", anchor='w')
    plot1_label.grid(row=current_row, column=2, sticky='w', padx=(0, 0))
    plot1_var2 = tk.Entry(plots_section, width=4, textvariable=plot1_var2_save, justify='center')
    plot1_var2.grid(row=current_row, column=3, sticky="ew", pady=5, padx=5)
    
    current_row += 1
    plot2_button = tk.Button(plots_section, text="Reconstructed training data (2D)", command=lambda: plot2D_reconstructed_training(job_dict, int(plot2_var1_save.get()), int(plot2_var2_save.get())))
    plot2_button.grid(row=current_row, column=0, sticky="ew", pady=5)
    plot2_var1_save = tk.StringVar(plots_section)
    plot2_var1_save.set('0')
    plot2_var2_save = tk.StringVar(plots_section)
    plot2_var2_save.set('1')
    plot2_var1 = tk.Entry(plots_section, width=4, textvariable=plot2_var1_save, justify='center')
    plot2_var1.grid(row=current_row, column=1, sticky="ew", pady=5, padx=(10, 5))
    plot2_label = tk.Label(plots_section, text="vs", anchor='w')
    plot2_label.grid(row=current_row, column=2, sticky='w', padx=(0, 0))
    plot2_var2 = tk.Entry(plots_section, width=4, textvariable=plot2_var2_save, justify='center')
    plot2_var2.grid(row=current_row, column=3, sticky="ew", pady=5, padx=5)
    
    current_row += 1
    plot3_button = tk.Button(plots_section, text="Samples", command=lambda: plot2d_samples(job_dict, int(plot3_var1_save.get()), int(plot3_var2_save.get())))
    plot3_button.grid(row=current_row, column=0, sticky="ew", pady=5)
    plot3_var1_save = tk.StringVar(plots_section)
    plot3_var1_save.set('0')
    plot3_var2_save = tk.StringVar(plots_section)
    plot3_var2_save.set('1')
    plot3_var1 = tk.Entry(plots_section, width=4, textvariable=plot3_var1_save, justify='center')
    plot3_var1.grid(row=current_row, column=1, sticky="ew", pady=5, padx=(10, 5))
    plot3_label = tk.Label(plots_section, text="vs", anchor='w')
    plot3_label.grid(row=current_row, column=2, sticky='w', padx=(0, 0))
    plot3_var2 = tk.Entry(plots_section, width=4, textvariable=plot3_var2_save, justify='center')
    plot3_var2.grid(row=current_row, column=3, sticky="ew", pady=5, padx=5)
    
    current_row += 1
    plot4_button = tk.Button(plots_section, text="DMAPs Eigenvalues", command=lambda: plot_dmaps_eigenvalues(job_dict))
    plot4_button.grid(row=current_row, column=0, sticky="ew", pady=5)
    
    current_row += 1
    plot5_button = tk.Button(plots_section, text="DMAPs Basis", command=lambda: plot2D_dmaps_basis(job_dict, int(plot5_var1_save.get()), int(plot5_var2_save.get())))
    plot5_button.grid(row=current_row, column=0, sticky="ew", pady=5)
    plot5_var1_save = tk.StringVar(plots_section)
    plot5_var1_save.set('0')
    plot5_var2_save = tk.StringVar(plots_section)
    plot5_var2_save.set('1')
    plot5_var1 = tk.Entry(plots_section, width=4, textvariable=plot5_var1_save, justify='center')
    plot5_var1.grid(row=current_row, column=1, sticky="ew", pady=5, padx=(10, 5))
    plot5_label = tk.Label(plots_section, text="vs", anchor='w')
    plot5_label.grid(row=current_row, column=2, sticky='w', padx=(0, 0))
    plot5_var2 = tk.Entry(plots_section, width=4, textvariable=plot5_var2_save, justify='center')
    plot5_var2.grid(row=current_row, column=3, sticky="ew", pady=5, padx=5)
    
    current_row += 1
    plot6_button = tk.Button(plots_section, text="PCA Eigenvalues", command=lambda: plot_pca_eigenvalues(job_dict))
    plot6_button.grid(row=current_row, column=0, sticky="ew", pady=5)
    
    current_row += 1
    plot7_button = tk.Button(plots_section, text="1-D PDF (training)", command=lambda: plot_training_pdf(job_dict, int(plot7_var1_save.get())))
    plot7_button.grid(row=current_row, column=0, sticky="ew", pady=5)
    plot7_var1_save = tk.StringVar(plots_section)
    plot7_var1_save.set('0')
    plot7_var1 = tk.Entry(plots_section, width=4, textvariable=plot7_var1_save, justify='center')
    plot7_var1.grid(row=current_row, column=1, sticky="ew", pady=5, padx=(10, 5))
    
    current_row += 1
    plot8_button = tk.Button(plots_section, text="1-D PDF (augmented)", command=lambda: plot_augmented_pdf(job_dict, int(plot8_var1_save.get())))
    plot8_button.grid(row=current_row, column=0, sticky="ew", pady=5)
    plot8_var1_save = tk.StringVar(plots_section)
    plot8_var1_save.set('0')
    plot8_var1 = tk.Entry(plots_section, width=4, textvariable=plot8_var1_save, justify='center')
    plot8_var1.grid(row=current_row, column=1, sticky="ew", pady=5, padx=(10, 5))
    
    current_row += 1
    plot9_button = tk.Button(plots_section, text="1-D PDF (training vs augmented)", command=lambda: plot_train_vs_aug_pdf(job_dict, int(plot9_var1_save.get())))
    plot9_button.grid(row=current_row, column=0, sticky="ew", pady=5)
    plot9_var1_save = tk.StringVar(plots_section)
    plot9_var1_save.set('0')
    plot9_var1 = tk.Entry(plots_section, width=4, textvariable=plot9_var1_save, justify='center')
    plot9_var1.grid(row=current_row, column=1, sticky="ew", pady=5, padx=(10, 5))
    
    current_row += 1
    plot10_button = tk.Button(plots_section, text="2-D PDF (training)", command=lambda: plot_training_jointPDF(job_dict, int(plot10_var1_save.get()), int(plot10_var2_save.get())))
    plot10_button.grid(row=current_row, column=0, sticky="ew", pady=5)
    plot10_var1_save = tk.StringVar(plots_section)
    plot10_var1_save.set('0')
    plot10_var2_save = tk.StringVar(plots_section)
    plot10_var2_save.set('1')
    plot10_var1 = tk.Entry(plots_section, width=4, textvariable=plot10_var1_save, justify='center')
    plot10_var1.grid(row=current_row, column=1, sticky="ew", pady=5, padx=(10, 5))
    plot10_label = tk.Label(plots_section, text="vs", anchor='w')
    plot10_label.grid(row=current_row, column=2, sticky='w', padx=(0, 0))
    plot10_var2 = tk.Entry(plots_section, width=4, textvariable=plot10_var2_save, justify='center')
    plot10_var2.grid(row=current_row, column=3, sticky="ew", pady=5, padx=5)
    
    current_row += 1
    plot11_button = tk.Button(plots_section, text="2-D PDF (augmented)", command=lambda: plot_augmented_jointPDF(job_dict, int(plot11_var1_save.get()), int(plot11_var2_save.get())))
    plot11_button.grid(row=current_row, column=0, sticky="ew", pady=5)
    plot11_var1_save = tk.StringVar(plots_section)
    plot11_var1_save.set('0')
    plot11_var2_save = tk.StringVar(plots_section)
    plot11_var2_save.set('1')
    plot11_var1 = tk.Entry(plots_section, width=4, textvariable=plot11_var1_save, justify='center')
    plot11_var1.grid(row=current_row, column=1, sticky="ew", pady=5, padx=(10, 5))
    plot11_label = tk.Label(plots_section, text="vs", anchor='w')
    plot11_label.grid(row=current_row, column=2, sticky='w', padx=(0, 0))
    plot11_var2 = tk.Entry(plots_section, width=4, textvariable=plot11_var2_save, justify='center')
    plot11_var2.grid(row=current_row, column=3, sticky="ew", pady=5, padx=5)
    
    # Make sure the plot area resizes with the window
    jobResults_tab.grid_rowconfigure(0, weight=1)
    jobResults_tab.grid_columnconfigure(1, weight=1)
    
    

    
    
    #*****************************************************************************#
    
    #**************************   DIAGNOSTICS RESULTS TAB ************************#
    
    tk.Label(diagResults_tab, text="Diagnostics Results Tab Content", font=("Arial", 12)).pack(pady=20)
    
    
    
    #*****************************************************************************#
    
    #*****************************   CONDITIONING TAB ****************************#
    
    # Configure grid layout for the conditioning_tab
    conditioning_tab.grid_columnconfigure(0, weight=0, minsize=400)
    conditioning_tab.grid_columnconfigure(1, weight=1)  # Make right column expandable
    conditioning_tab.grid_rowconfigure(0, weight=1)     # Make rows fill the window
    conditioning_tab.grid_rowconfigure(1, weight=1)     # Ensure the right column is dynamic
    
    # Left column frame (fixed width)
    cond_left_frame = tk.Frame(conditioning_tab, width=400)
    cond_left_frame.grid(row=0, column=0, rowspan=2, sticky='ns', padx=10, pady=10)
    cond_left_frame.grid_propagate(False)  # Prevent frame from resizing
    
    # Right column frame (expandable)
    cond_right_frame = tk.Frame(conditioning_tab)
    cond_right_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=10, pady=10)
    
    
    # Add "Settings" label above the text box in the left column
    settings_label = tk.Label(cond_left_frame, text="Settings", font=("Arial", 12, "bold"))
    settings_label.grid(row=0, column=0, sticky='w')  # Align the label to the left
    
    # Add "Log" label above the text box in the right column
    log_label = tk.Label(cond_right_frame, text="Log", font=("Arial", 12, "bold"))
    log_label.grid(row=0, column=0, sticky='w')  # Align the label to the left
    
    # Right column text box for output (under "Log" label)
    output_text = tk.Text(cond_right_frame, wrap='word', height=10, bg='white')
    output_text.grid(row=1, column=0, sticky="nsew", pady=(16, 5))  # Use upper half for text output
    
    # Add "Plots" label above the plot area
    plots_label = tk.Label(cond_right_frame, text="Plots", font=("Arial", 12, "bold"))
    plots_label.grid(row=2, column=0, sticky='w')  # Align the label to the left
    
    # Right column frame for the plot (bottom half, under "Plots" label)
    plot_area = tk.Frame(cond_right_frame, bg='white', height=200)
    plot_area.grid(row=3, column=0, sticky="nsew")  # Fill remaining space for plot area
    
    # Configure the grid for the right column to expand properly
    cond_right_frame.grid_rowconfigure(1, weight=1)  # Output text box expands vertically
    cond_right_frame.grid_rowconfigure(3, weight=1)  # Plot area expands vertically
    cond_right_frame.grid_columnconfigure(0, weight=1)  # Both sections expand horizontally
    
    ################################################################################
    ################################################################################
    
    # Set row index for frames
    current_row = 0
    
    ################################################################################
    ################################################################################
    
    # Frame for Data loading in the left column
    group_row = 0
    current_row += 1
    frame__data_loading = tk.LabelFrame(cond_left_frame, text="Data loading", padx=10, pady=10, font=("Arial", 10, "bold"))
    frame__data_loading.grid(row=current_row, column=0, columnspan=3, sticky="ew", padx=10, pady=(10, 5))  # Top with spacing
    
    opt_save__cond_data_path = tk.StringVar(frame__data_loading)
    opt_label__cond_data_path = tk.Label(frame__data_loading, text="Data path", anchor='w')
    opt_label__cond_data_path.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__cond_data_path = tk.Entry(frame__data_loading, textvariable=opt_save__cond_data_path)
    opt_value__cond_data_path.grid(row=group_row, column=1, sticky='ew')
    opt_button__cond_data_path = tk.Button(frame__data_loading, text="Browse", command=lambda: browse_file(opt_value__cond_data_path))
    opt_button__cond_data_path.grid(row=group_row, column=2, sticky='ew', padx=(5, 0))
    
    group_row += 1
    opt_save__cond_dataBW_path = tk.StringVar(frame__data_loading)
    opt_label__cond_dataBW_path = tk.Label(frame__data_loading, text="Data (BW optimization) path", anchor='w')
    opt_label__cond_dataBW_path.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__cond_dataBW_path = tk.Entry(frame__data_loading, textvariable=opt_save__cond_dataBW_path)
    opt_value__cond_dataBW_path.grid(row=group_row, column=1, sticky='ew')
    opt_button__cond_dataBW_path = tk.Button(frame__data_loading, text="Browse", command=lambda: browse_file(opt_value__cond_dataBW_path))
    opt_button__cond_dataBW_path.grid(row=group_row, column=2, sticky='ew', padx=(5, 0))
    
    group_row += 1
    opt_save__cond_dataLabels_path = tk.StringVar(frame__data_loading)
    opt_label__cond_dataLabels_path = tk.Label(frame__data_loading, text="Data labels path", anchor='w')
    opt_label__cond_dataLabels_path.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__cond_dataLabels_path = tk.Entry(frame__data_loading, textvariable=opt_save__cond_dataLabels_path)
    opt_value__cond_dataLabels_path.grid(row=group_row, column=1, sticky='ew')
    opt_button__cond_dataLabels_path = tk.Button(frame__data_loading, text="Browse", command=lambda: browse_file(opt_value__cond_dataLabels_path))
    opt_button__cond_dataLabels_path.grid(row=group_row, column=2, sticky='ew', padx=(5, 0))
    
    group_row += 1
    opt_save__cond_x_path = tk.StringVar(frame__data_loading)
    opt_label__cond_x_path = tk.Label(frame__data_loading, text="Conditioning values path", anchor='w')
    opt_label__cond_x_path.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__cond_x_path = tk.Entry(frame__data_loading, textvariable=opt_save__cond_x_path)
    opt_value__cond_x_path.grid(row=group_row, column=1, sticky='ew')
    opt_button__cond_x_path = tk.Button(frame__data_loading, text="Browse", command=lambda: browse_file(opt_value__cond_x_path))
    opt_button__cond_x_path.grid(row=group_row, column=2, sticky='ew', padx=(5, 0))
    
    group_row += 1
    opt_save__cond_yTrue_path = tk.StringVar(frame__data_loading)
    opt_label__cond_yTrue_path = tk.Label(frame__data_loading, text="Data labels path", anchor='w')
    opt_label__cond_yTrue_path.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__cond_yTrue_path = tk.Entry(frame__data_loading, textvariable=opt_save__cond_yTrue_path)
    opt_value__cond_yTrue_path.grid(row=group_row, column=1, sticky='ew')
    opt_button__cond_yTrue_path = tk.Button(frame__data_loading, text="Browse", command=lambda: browse_file(opt_value__cond_yTrue_path))
    opt_button__cond_yTrue_path.grid(row=group_row, column=2, sticky='ew', padx=(5, 0))
    
    group_row += 1
    opt_save__cond_weights_path = tk.StringVar(frame__data_loading)
    opt_label__cond_weights_path = tk.Label(frame__data_loading, text="Weights path", anchor='w')
    opt_label__cond_weights_path.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__cond_weights_path = tk.Entry(frame__data_loading, textvariable=opt_save__cond_weights_path)
    opt_value__cond_weights_path.grid(row=group_row, column=1, sticky='ew')
    opt_button__cond_weights_path = tk.Button(frame__data_loading, text="Browse", command=lambda: browse_file(opt_value__cond_weights_path))
    opt_button__cond_weights_path.grid(row=group_row, column=2, sticky='ew', padx=(5, 0))
    
    group_row += 1
    opt_save__cond_bw_path = tk.StringVar(frame__data_loading)
    opt_label__cond_bw_path = tk.Label(frame__data_loading, text="Bandwidths path", anchor='w')
    opt_label__cond_bw_path.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__cond_bw_path = tk.Entry(frame__data_loading, textvariable=opt_save__cond_bw_path)
    opt_value__cond_bw_path.grid(row=group_row, column=1, sticky='ew')
    opt_button__cond_bw_path = tk.Button(frame__data_loading, text="Browse", command=lambda: browse_file(opt_value__cond_bw_path))
    opt_button__cond_bw_path.grid(row=group_row, column=2, sticky='ew', padx=(5, 0))
    
    global cond__data
    global cond__data_labels
    global cond__x
    global cond__y_true
    
    def load_cond_data():
        global cond__data
        global cond__data_labels
        global cond__x
        global cond__y_true
        # Function to load the files from the paths entered
        path__data        = opt_value__cond_data_path.get()
        print("path", path__data)
        path__data_labels = opt_value__cond_dataLabels_path.get()
        path__x           = opt_value__cond_x_path.get()
        path__y_true      = opt_value__cond_yTrue_path.get()
        try:
            cond__data        = load_data(path__data)
            cond__data_labels = load_data(path__data_labels)
            cond__x           = load_data(path__x)
            cond__y_true      = load_data(path__y_true, dtype='text', empty_ok=True)
            label__cond_data_load_status.config(text="Data loaded successfully", fg="green")
        except:
            label__cond_data_load_status.config(text="Cannot load data", fg="red")
    
    group_row += 1
    button__cond_data_load = tk.Button(frame__data_loading, text="Load", command=load_cond_data)
    button__cond_data_load.grid(row=group_row, column=0, sticky="w", pady=5)
    
    group_row += 1
    label__cond_data_load_status = tk.Label(frame__data_loading, text="", fg="green", anchor="w")
    label__cond_data_load_status.grid(row=group_row, column=0, sticky="w", pady=5)
    
    
    ################################################################################
    ################################################################################
    
    # Frame for Conditioning settings in the left column
    group_row = 0
    current_row += 1
    frame__cond_settings = tk.LabelFrame(cond_left_frame, text="Conditioning settings", padx=10, pady=10, font=("Arial", 10, "bold"))
    frame__cond_settings.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 5))  # Below data_loading_frame
    
    cond_types = ["Expectation", "PDF"]
    opt_save__cond_type = tk.StringVar(frame__cond_settings)
    opt_label__cond_type = tk.Label(frame__cond_settings, text="Conditioning type", anchor='w')
    opt_label__cond_type.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__cond_type = ttk.Combobox(frame__cond_settings, values=cond_types, state='readonly', textvariable=opt_save__cond_type)
    opt_value__cond_type.current(0)
    opt_value__cond_type.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__cond_qoi_cols = tk.StringVar(frame__cond_settings)
    opt_label__cond_qoi_cols = tk.Label(frame__cond_settings, text="QoI column indices", anchor='w')
    opt_label__cond_qoi_cols.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__cond_qoi_cols = tk.Entry(frame__cond_settings, textvariable=opt_save__cond_qoi_cols)
    opt_value__cond_qoi_cols.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    opt_save__cond_cond_cols = tk.StringVar(frame__cond_settings)
    opt_label__cond_cond_cols = tk.Label(frame__cond_settings, text="Conditional column indices", anchor='w')
    opt_label__cond_cond_cols.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__cond_cond_cols = tk.Entry(frame__cond_settings, textvariable=opt_save__cond_cond_cols)
    opt_value__cond_cond_cols.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    weights_types = ["Computed", "User specified"]
    opt_save__weights_type = tk.StringVar(frame__cond_settings)
    opt_label__weights_type = tk.Label(frame__cond_settings, text="Conditioning weights", anchor='w')
    opt_label__weights_type.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__weights_type = ttk.Combobox(frame__cond_settings, values=weights_types, state='readonly', textvariable=opt_save__weights_type)
    opt_value__weights_type.current(0)
    opt_value__weights_type.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    bw_types = ["Computed (optimal)", "Computed (Silverman)", "User specified"]
    opt_save__bw_type = tk.StringVar(frame__cond_settings)
    opt_label__bw_type = tk.Label(frame__cond_settings, text="Conditioning bandwidths", anchor='w')
    opt_label__bw_type.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__bw_type = ttk.Combobox(frame__cond_settings, values=bw_types, state='readonly', textvariable=opt_save__bw_type)
    opt_value__bw_type.current(0)
    opt_value__bw_type.grid(row=group_row, column=1, sticky='ew')
    
    group_row += 1
    parallel_options = ["False", "True"]
    opt_save__parallel = tk.StringVar(frame__cond_settings)
    opt_label__parallel = tk.Label(frame__cond_settings, text="Parallel", anchor='w')
    opt_label__parallel.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__parallel = ttk.Combobox(frame__cond_settings, values=parallel_options, state='readonly', textvariable=opt_save__parallel)
    opt_value__parallel.current(0)
    opt_value__parallel.grid(row=group_row, column=1, sticky='ew')
    
    
    ################################################################################
    ################################################################################
    
    # Frame for Optimization settings in the left column
    group_row = 0
    current_row += 1
    frame__bwOpt_settings = tk.LabelFrame(cond_left_frame, text="Bandwidth optimization settings", padx=10, pady=10, font=("Arial", 10, "bold"))
    frame__bwOpt_settings.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 5))  # Below data_loading_frame
    
    bwOpt_types = ["Genetic Algorithm", "Minimize"]
    opt_save__bwOpt_type = tk.StringVar(frame__bwOpt_settings)
    opt_label__bwOpt_type = tk.Label(frame__bwOpt_settings, text="Optimization method", anchor='w')
    opt_label__bwOpt_type.grid(row=group_row, column=0, sticky='w', padx=(0, 5))
    opt_value__bwOpt_type = ttk.Combobox(frame__bwOpt_settings, values=bwOpt_types, state='readonly', textvariable=opt_save__bwOpt_type)
    opt_value__bwOpt_type.current(0)
    opt_value__bwOpt_type.grid(row=group_row, column=1, sticky='ew')
    
    ################################################################################
    ################################################################################
    
    
    ################################################################################
    ################################################################################
    
    
    #*****************************************************************************#
    
    #**************************   RUN FORWARD MODEL TAB **************************#
    
    # Configure grid layout for the runModels_tab
    runModels_tab.grid_columnconfigure(0, weight=0, minsize=400)
    runModels_tab.grid_columnconfigure(1, weight=1)  # Make right column expandable
    runModels_tab.grid_rowconfigure(0, weight=1)     # Make rows fill the window
    runModels_tab.grid_rowconfigure(1, weight=1)
    
    # Left column frame (fixed width)
    runModels_left_frame = tk.Frame(runModels_tab, width=400)
    runModels_left_frame.grid(row=0, column=0, rowspan=2, sticky='ns', padx=10, pady=10)
    runModels_left_frame.grid_propagate(False)  # Prevent frame from resizing
    
    # Right column frame (expandable)
    runModels_right_frame = tk.Frame(runModels_tab)
    runModels_right_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=10, pady=10)
    
    
    
    
    
    
    # Function to clear text in output_text box
    def clear_output_text():
        output_text.delete(1.0, tk.END)


    
    ################################################################################
    ################################################################################
    ################################################################################
    ################################################################################
    ################################################################################
    ################################################################################
    
    # Bind button click to widget detection
    root.bind("<Button-1>", click_event)
    
    # Bind the shortcuts for closing the app
    bind_shortcuts()
    
    # Set the close function for the main window
    root.protocol("WM_DELETE_WINDOW", on_close)
    
    # Run the application
    root.mainloop()

if __name__ == '__main__':
    launch_gui()

## convergence with N, other diagnostics, plots