import PySimpleGUI as sg
import plotly.express as px
from src.util.data_processing.merge_experiment_data import merge_data
from src.gui.custom_components import title, question_mark, metric4_radio_buttons


class ParallelCoordinatesScreen:

    def __init__(self):
        question_mark_padding = ((0, 0), (0, 0))
        self.layout = [[title('Parallel Coordinates')],
                       [sg.Text('Graph Title:'), sg.Input(key='parcoords_title_input')],
                       [sg.Text('Line Color:'), sg.Input('Blue', key='parcoords_line_color_input')],
                       [sg.Text('Background Color:'), sg.Input('White', key='parcoords_background_color_input')],
                       [sg.Text('Metric:'),  question_mark('Help', padding=question_mark_padding)],
                       metric4_radio_buttons('parcoords'),
                       [sg.Button('Generate', key='parcoords_generate_button')],
                       [sg.Button('Back', key='parcoords_back_button')]]
        self.results = None

    def check_events(self, event, values, window):
        if event == 'experiment_write_results_event':
            self.results = values['experiment_write_results_event']
        if event == 'parcoords_generate_button':
            self.generate_parallel_coordinates(values, window)
        if event == 'parcoords_back_button':
            window['parcoords_panel'].update(visible=False)
            window['experiment_result_panel'].update(visible=True)

    def generate_parallel_coordinates(self, values, window):
        exp = self.results[0]
        outcomes = self.results[1]

        repetitions = len(self.results[1][list(self.results[1].keys())[0]][0])
        metric = self.get_selected_radio_button(values)
        merged_data = merge_data(exp, outcomes, repetitions, metric)

        fig = px.parallel_coordinates(merged_data, title=values['parcoords_title_input'])
        try:
            fig = fig.update_layout(
                colorway=[values['parcoords_line_color_input'].lower()],
                plot_bgcolor=values['parcoords_background_color_input'],
                paper_bgcolor=values['parcoords_background_color_input'],
                title_x=0.5,
            )
            fig.show()
        except ValueError:
            window.write_event_value('show_error_window', 'Error in input: Invalid color value for the line or '
                                                          'background.\nPlease make sure the input is a valid CSS '
                                                          'color string (black), hexidecimal (#FFFFFF) or rgb value '
                                                          '(rbg(255, 255, 255))')

    def get_selected_radio_button(self, values):
        for i in range(4):
            if values[f'parcoords_metric_{i + 1}']:
                return i + 1
        return 1
