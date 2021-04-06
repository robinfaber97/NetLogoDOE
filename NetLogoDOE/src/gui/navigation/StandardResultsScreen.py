import PySimpleGUI as sg
from NetLogoDOE.src.gui.custom_components import title, question_mark


class StandardResultsScreen:

    def __init__(self):
        button_size = (20, 1)
        button_pad = ((0, 0), (20, 0))
        self.layout = [[title("Standard results")],
                       [sg.Button('Configuration Information', key='standard_results_configtable_button',
                                  size=button_size, pad=button_pad),
                        question_mark('Help')],
                       [sg.Button('Timeseries', key='standard_results_timeseries_button',
                                  size=button_size, pad=button_pad),
                        question_mark('Help')],
                       [sg.Button('Boxplot', key='standard_results_boxplot_button',
                                  size=button_size, pad=button_pad),
                        question_mark('Help')],
                       [sg.Button('Violin plot', key='standard_results_violinplot_button',
                                  size=button_size, pad=button_pad),
                        question_mark('Help')],
                       [sg.Button('Histogram', key='standard_results_histogram_button',
                                  size=button_size, pad=button_pad),
                        question_mark('Help')],
                       [sg.Button('Distribution plot', key='standard_results_distplot_button',
                                  size=button_size, pad=button_pad),
                        question_mark('Help')],
                       [sg.Input(key='standard_results_dummy_export', enable_events=True, visible=False, size=(0, 0)),
                        sg.SaveAs('Save Results', file_types=[("Text Files", "*.txt")],
                                  target='standard_results_dummy_export', key="standard_results_save_button",
                                  size=button_size, pad=button_pad),
                        question_mark('Help')],
                       [sg.Button('Back to main menu', key='standard_results_back_button',
                                  size=button_size, pad=button_pad)]]
        self.results = None

    def check_events(self, event, values, window):
        if event == 'standard_write_results_event':
            self.results = values['standard_write_results_event']

        if event == 'standard_results_configtable_button':
            window['standard_result_panel'].update(visible=False)
            window['standard_configtable_panel'].update(visible=True)
        if event == 'standard_results_timeseries_button':
            window['standard_result_panel'].update(visible=False)
            window['timeseries_panel'].update(visible=True)
        if event == 'standard_results_boxplot_button':
            window['standard_result_panel'].update(visible=False)
            window['boxplot_panel'].update(visible=True)
        if event == 'standard_results_violinplot_button':
            window['standard_result_panel'].update(visible=False)
            window['violinplot_panel'].update(visible=True)
        if event == 'standard_results_histogram_button':
            window['standard_result_panel'].update(visible=False)
            window['histogram_panel'].update(visible=True)
        if event == 'standard_results_distplot_button':
            window['standard_result_panel'].update(visible=False)
            window['distplot_panel'].update(visible=True)

        if event == 'standard_results_dummy_export' and not (values['standard_results_dummy_export'] == ''):
            self.export_standard_results(values, values['standard_results_dummy_export'])
        if event == 'standard_results_back_button':
            window['standard_result_panel'].update(visible=False)
            window['main_panel'].update(visible=True)

    def export_standard_results(self, values, file_path):
        results_dict = {}
        results_dict['Configuration'] = self.results[2]
        results_dict['Parameter settings'] = self.results[0]
        results_dict['Reporter values'] = self.results[1]

        f = open(file_path, "w")
        f.write(str(results_dict))
        f.close()



