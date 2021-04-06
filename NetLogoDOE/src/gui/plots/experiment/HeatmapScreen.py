import PySimpleGUI as sg
import plotly.express as px
from src.util.data_processing.merge_experiment_data import merge_data
from src.gui.custom_components import title, metric4_radio_buttons, question_mark


class HeatmapScreen:

    def __init__(self):
        question_mark_padding = ((0, 0), (0, 0))
        self.layout = [[title('Heatmap')],
                       [sg.Text('Graph Title:'), sg.Input(key='heatmap_title_input')],
                       [sg.Text('Color scale:'), sg.Input('viridis', key='heatmap_color_input')],
                       [sg.Text('Metric:'), question_mark('Help', padding=question_mark_padding)],
                       metric4_radio_buttons('heatmap'),
                       [sg.Button('Generate', key='heatmap_generate_button')],
                       [sg.Button('Back', key='heatmap_back_button')]]
        self.results = None

    def check_events(self, event, values, window):
        if event == 'experiment_write_results_event':
            self.results = values['experiment_write_results_event']
        if event == 'heatmap_generate_button':
            self.generate_heatmap(values, window)
        if event == 'heatmap_back_button':
            window['heatmap_panel'].update(visible=False)
            window['experiment_result_panel'].update(visible=True)

    def generate_heatmap(self, values, window):
        exp = self.results[0]
        outcomes = self.results[1]

        repetitions = len(self.results[1][list(self.results[1].keys())[0]][0])
        metric = self.get_selected_radio_button(values)
        merged_data = merge_data(exp, outcomes, repetitions, metric)

        try:
            fig = px.imshow(merged_data.corr(), title=values['heatmap_title_input'],
                        color_continuous_scale=values['heatmap_color_input'])
        except ValueError:
            window.write_event_value('show_error_window', 'Error in input: Invalid color value for color scale.\n'
                                                          'Please make sure the input is a valid plotly color scale.')
            return
        fig.update_layout(title_x=0.5)
        fig.show()

    def get_selected_radio_button(self, values):
        for i in range(4):
            if values[f'heatmap_metric_{i + 1}']:
                return i + 1
        return 1
