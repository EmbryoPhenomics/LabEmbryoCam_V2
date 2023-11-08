import dash
from dash import dcc
import dash_daq as daq
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc

# Tab styles for ascending in hierarchy

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#6E6E6E',
    'color': 'white',
    'padding': '6px'
}

tab_selected_style_sub_main = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#424242',
    'color': 'white',
    'padding': '6px'
}

tab_selected_style_main = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#848484',
    'color': 'white',
    'padding': '6px'
}

def app_layout():
    return html.Div(children=[

    html.Div(className='row', children=[
        html.Div(className='two columns', children=[
            html.Img(src='./assets/img/embryophenomicslogo.png', style={'display': 'inline-block', 'height': '100px'}),
        ]),
        html.Div(className='eight columns', children=[
            html.Br(), # forces columns to be created
            html.Div(children=[
                html.Div(children=[
                    html.H6('Current timepoint:'),
                    html.Br(),
                    html.H6('Current embryo:')
                ], style={'width': '20%', 'display': 'table-cell'}),
                html.Div(children=[
                    dbc.Progress(id="timepoint-pg", style={'height': '20px'}),
                    html.Br(),
                    html.Br(),
                    dbc.Progress(id="embryo-pg", style={'height': '20px'})
                ], style={'width': '80%', 'display': 'table-cell'}),
            ], style={'width': '100%', 'display': 'table'}),
        ]),
        html.Div(className='two columns', children=[
            html.Br(),
            html.Button('Shutdown', 'close-app'),
            html.Div(id='close-app-div')
        ])
    ]),

    html.Div(className='row', children=[
                html.Div(id='loaded-data-callback'),
                html.Div(id='hiddenFPSdata'),
                html.Div(id='fullROIData'),
                html.Div(id='config-save-callback'),
                html.Div(id='connect-cam-callback'),

                html.Div(className='row', children=[
                    html.Div(className='four columns', children=[

                        dbc.Card([
                            dbc.CardHeader('Experiment Settings'),
                            dbc.CardBody([
                                dcc.Input(
                                    id='config-name-input',
                                    type='text',
                                    placeholder='Please name a config file...'),
                                html.Div(children=[
                                    html.Div(children=[
                                        dcc.Upload(
                                            id='load-config-button', 
                                            multiple=False,
                                            children=html.Button('Load'))
                                    ], style={'width': '10%', 'display': 'table-cell'}),

                                    html.Div(children=[
                                        html.Button('Save', id='save-config-button')
                                    ], style={'width': '10%', 'display': 'table-cell'}),

                                    html.Div(children=[], style={'width': '80%', 'display': 'table-cell'}),
                                ], style={'width': '100%', 'display': 'table'}),
                            ])
                        ], style={'width': '35rem'}, color='dark', outline=True),

                        html.Br(),

                        dbc.Card([
                            dbc.CardHeader('Camera settings'),
                            dbc.CardBody([

                                html.Label('LED brightness', style={'display': 'inline-block'}),

                                dcc.Slider(
                                    id='hardware-brightness',
                                    min=0,
                                    max=100,
                                    value=0,
                                    tooltip={'always_visible': True, 'placement': 'bottom'},
                                    persistence=True),
                                html.Div(id='hardware-brightness-callback'),

                                # html.Br(),

                                html.Div(children=[
                                    html.Div(children=[
                                        html.Label(children='Exposure'),
                                        daq.NumericInput(id='exposure', min=0, max=999999, value=0, size=100, disabled=False, persistence=True),
                                    ], style={'width': '50%', 'display': 'table-cell'}),
                                    html.Div(children=[
                                        html.Label(children='Contrast'),                                        
                                        daq.NumericInput(id='contrast', min=0, max=999999, value=0, size=100, disabled=False, persistence=True),
                                    ], style={'width': '50%', 'display': 'table-cell'}),
                                ], style={'width': '100%', 'display': 'table'}),

                                html.Div(id='exposure-change'),
                                html.Div(id='contrast-change'),

                                html.Br(),

                                html.Div(children=[
                                    html.Div(children=[
                                        html.Label(children='Frame-rate'),
                                        daq.NumericInput(id='fps', min=0, max=999999, value=0, size=75, disabled=False, persistence=True),
                                    ], style={'width': '40%', 'display': 'table-cell'}),
                                    html.Div(children=[
                                        html.Label(children='Resolution'),
                                        dcc.Dropdown(
                                            id='resolution-preset',
                                            placeholder='Please select a resolution...',
                                            options=[
                                                dict(label='640x480', value=640),
                                                dict(label='1024x768', value=768),
                                                dict(label='1280x720', value=1280),
                                                dict(label='1920x1080', value=1920),
                                                dict(label='256x256', value=256),
                                                dict(label='512x512', value=512),
                                                dict(label='1024x1024', value=1024),
                                                dict(label='2048x2048', value=2048)],
                                            disabled=False,
                                            persistence=True,
                                            persistence_type='session'),
                                    ], style={'width': '60%', 'display': 'table-cell'}),
                                ], style={'width': '100%', 'display': 'table'}),

                                html.Div(id='resolution-preset-change'),
                                html.Div(id='fps-change'),

                                html.Br(),

                                html.Button('Update', id='update-camera-settings'),
                                html.Div(id='hidden-update-callback'),
                            ]),
                        ], style={'width': '35rem'}, color='dark', outline=True),

                        html.Br(),
                        
                        dbc.Card([
                            dbc.CardHeader('XYZ controls and settings'),
                            dbc.CardBody([
                                html.Button('Set Origin', id='home-xy-button'),
                                html.Div(id='xyz-homing-callback'),

                                html.Br(),
                                html.Div(id='initial-xy'),

                                html.Div(children=[
                                    html.Div(className='row', children=[
                                        html.Label('Distance:'),
                                        dcc.Dropdown(
                                            id='xyz-magnitude',
                                            options=[
                                                dict(label='0.001mm', value=0.001),
                                                dict(label='0.01mm', value=0.01),
                                                dict(label='0.1mm', value=0.1),
                                                dict(label='1mm', value=1),
                                                dict(label='10mm', value=10)],
                                            value=0.001),
                                        html.Br(),
                                    ]),

                                    html.Br(),

                                    html.Div(className='row', children=[
                                        html.Div(className='eight columns', children=[
                                            html.Div(children=[
                                                html.Div(children=[
                                                    dbc.Button(html.I(className='fa-solid fa-square-arrow-up-right fa-flip-horizontal fa-2xl'), color='dark', size='lg', id='left-diag-xy-up'),
                                                ], style={'width': '33%', 'display': 'table-cell'}),
                                                html.Div(children=[
                                                    dbc.Button(html.I(className='fa-solid fa-arrow-up fa-2xl'), color='dark', size='lg', id='up-xy'),
                                                ], style={'width': '33%', 'display': 'table-cell'}),
                                                html.Div(children=[
                                                    dbc.Button(html.I(className='fa-solid fa-square-arrow-up-right fa-2xl'), color='dark', size='lg', id='right-diag-xy-up'),
                                                ], style={'width': '33%', 'display': 'table-cell'}),
                                            ], style={'width': '100%', 'display': 'table'}),

                                            html.Br(),

                                            html.Div(children=[
                                                html.Div(children=[
                                                    dbc.Button(html.I(className='fa-solid fa-arrow-left fa-2xl'), color='dark', size='lg', id='left-xy')
                                                ], style={'width': '33%', 'display': 'table-cell'}),
                                                html.Div(children=[
                                                    html.Br(),
                                                ], style={'width': '33%', 'display': 'table-cell'}),
                                                html.Div(children=[
                                                    dbc.Button(html.I(className='fa-solid fa-arrow-right fa-2xl'), color='dark', size='lg', id='right-xy')
                                                ], style={'width': '33%', 'display': 'table-cell'}),
                                            ], style={'width': '100%', 'display': 'table'}),
                                            html.Br(),

                                            html.Div(children=[
                                                html.Div(children=[
                                                    dbc.Button(html.I(className='fa-solid fa-square-arrow-up-right fa-rotate-180 fa-2xl'), color='dark', size='lg', id='left-diag-xy-down')
                                                ], style={'width': '33%', 'display': 'table-cell'}),
                                                html.Div(children=[
                                                    dbc.Button(html.I(className='fa-solid fa-arrow-down fa-2xl'), color='dark', size='lg', id='down-xy')
                                                ], style={'width': '33%', 'display': 'table-cell'}),
                                                html.Div(children=[
                                                    dbc.Button(html.I(className='fa-solid fa-square-arrow-up-right fa-rotate-90 fa-2xl'), color='dark', size='lg', id='right-diag-xy-down')
                                                ], style={'width': '33%', 'display': 'table-cell'}),
                                            ], style={'width': '100%', 'display': 'table'}),
                                        ]),
                                        html.Div(className='four columns', children=[
                                            dbc.Button(html.I(className='fa-solid fa-arrow-up fa-2xl'), color='dark', size='lg', id='up-z'),
                                            html.Br(),
                                            html.Br(),
                                            html.Br(),
                                            html.Br(),
                                            dbc.Button(html.I(className='fa-solid fa-arrow-down fa-2xl'), color='dark', size='lg', id='down-z'),
                                        ]),

                                        html.Div(children=[
                                            html.Div(id='left-diag-xy-up-div'),
                                            html.Div(id='up-xy-div'),
                                            html.Div(id='right-diag-xy-up-div'),

                                            html.Div(id='left-xy-div'),
                                            html.Div(id='right-xy-div'),

                                            html.Div(id='left-diag-xy-down-div'),
                                            html.Div(id='down-xy-div'),
                                            html.Div(id='right-diag-xy-down-div'),

                                            html.Div(id='up-z-div'),
                                            html.Div(id='down-z-div'),

                                        ])
                                    ])
                                ])
                            ])
                        ], style={'width': '35rem'}, color='dark', outline=True),

                        html.Br(),

                        dbc.Card([
                            dbc.CardHeader('XYZ Positions'),
                            dbc.CardBody([
                                html.Div(children=[
                                    html.Div(children=[
                                        html.Button('Current', id='grab-xy'),
                                        html.Div(id='grab-xy-callback')
                                    ], style={'width': '40', 'display': 'table-cell'}),

                                    html.Div(children=[
                                        html.Br()
                                    ], style={'width': '20', 'display': 'table-cell'}),

                                    html.Div(children=[
                                        html.Button('Replace', id='replace-xy-button'),
                                        html.Div(id='replace-xy-callback')
                                    ], style={'width': '40%', 'display': 'table-cell'}),

                                    html.Div(children=[], style={'width': '80%', 'display': 'table-cell'}),

                                ], style={'width': '100%', 'display': 'table'}),

                                html.Br(),

                                html.Div(id='remove-xy-callback'),
                                dash_table.DataTable(
                                    id='xy_coords',
                                    columns=[
                                        dict(name='X', id='x'), 
                                        dict(name='Y', id='y'), 
                                        dict(name='Z', id='z'),
                                        dict(name='Label', id='label')],
                                    style_cell={'textAlign': 'left'},
                                    style_cell_conditional=[{'if': {'column_id': col},'width': '20%'} for col in ['x','y','z']],
                                    fixed_rows={'headers': True},
                                    style_table={'height': 300},
                                    row_deletable=True,
                                    row_selectable='single',
                                    editable=True,
                                    page_size=300
                                )
                            ])
                        ], style={'width': '35rem'}, color='dark', outline=True),
                        
                        html.Br(),

                        dbc.Card([
                            dbc.CardHeader('Acquisition'),
                            dbc.CardBody([
                                html.Label(children='Number of positions'),
                                dcc.RadioItems(
                                    id='acquisition-number',
                                    options=[
                                        {'label': 'Single', 'value': 'Single'},
                                        {'label': 'Multiple', 'value': 'Multiple'}],
                                    value='Single',
                                    labelStyle={'display': 'inline-block'}),

                                html.Div(id='acquisition-number-change'),

                                html.Br(),

                                html.Div(children=[
                                    html.Div(children=[
                                        html.Label(children='Number of time-points')
                                    ], style={'width': '70%', 'display': 'table-cell'}),
                                    html.Div(children=[
                                        daq.NumericInput(id='total-time-points', min=1, max=100000, value=1, size=100)
                                    ], style={'width': '30%', 'display': 'table-cell'}),
                                ], style={'width': '100%', 'display': 'table'}),

                                html.Div(id='total-time-points-change'),

                                html.Div(children=[
                                    html.Div(children=[
                                        html.Label(children='Acquisition interval (mins)')
                                    ], style={'width': '70%', 'display': 'table-cell'}),
                                    html.Div(children=[
                                        daq.NumericInput(id='acq-length', min=0, max=100000, value=1, size=100)
                                    ], style={'width': '30%', 'display': 'table-cell'}),
                                ], style={'width': '100%', 'display': 'table'}),

                                html.Div(id='acq-length-change'),

                                html.Div(children=[
                                    html.Div(children=[
                                        html.Label(children='Acquisition length (secs)')
                                    ], style={'width': '70%', 'display': 'table-cell'}),
                                    html.Div(children=[
                                        daq.NumericInput(id='each-time-limit', min=1, max=100000, value=1, size=100)
                                    ], style={'width': '30%', 'display': 'table-cell'}),
                                ], style={'width': '100%', 'display': 'table'}),

                                html.Div(id='each-time-limit-change'),

                                html.Br(),

                                html.Label('Drive and Folder selection:'),

                                html.Div(children=[
                                    html.Div(children=[
                                        dcc.Input(
                                            id='acquire-path-input', 
                                            type='text',
                                            placeholder='Specify a folder to save video for the drive selected...',),
                                    ], style={'width': '70%', 'display': 'table-cell'}),
                                    html.Div(children=[
                                        html.Button('Select', id='path-select'),
                                    ], style={'width': '30%', 'display': 'table-cell'}),
                                ], style={'width': '100%', 'display': 'table'}),

                                html.Div(id='acquire-outpath-check'),
                                html.Div(id='acquire-path-input-change'),

                                html.Br(),

                                # html.Div(children=[
                                #     html.Div(children=[
                                #         html.Label(children='Disk space (available/total)')
                                #     ], style={'width': '50%', 'display': 'table-cell'}),
                                #     html.Div(children=[
                                #         html.Label(id='disk_space_text')
                                #     ], style={'width': '50%', 'display': 'table-cell'}),
                                # ], style={'width': '100%', 'display': 'table'}),

                                # html.Br(),

                                # html.Div(children=[
                                #     html.Div(children=[
                                #         html.Label(children='Projected usage')
                                #     ], style={'width': '50%', 'display': 'table-cell'}),
                                #     html.Div(children=[
                                #         html.Label(id='projected_usage_text')
                                #     ], style={'width': '50%', 'display': 'table-cell'}),
                                # ], style={'width': '100%', 'display': 'table'}),

                                html.Br(),

                                html.Button('Start acquisition', id='acquire-button'),
                                html.Div(id='hiddenAcquire'),
                                html.Button('Cancel acquisition', id='cancel-acquire-button'),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(dbc.ModalTitle("Acquisition Error")),
                                        dbc.ModalBody("Please cancel the live stream before starting an acquisition."),
                                        dbc.ModalFooter(
                                            dbc.Button(
                                                "Close", id="close-stream-popup", className="ms-auto", n_clicks=0
                                            )
                                        ),
                                    ],
                                    id="acquisition-live-stream-popup",
                                    is_open=False,
                                ),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(dbc.ModalTitle("Acquisition Error")),
                                        dbc.ModalBody("Folder already exists, please change it to not overwrite existing data."),
                                        dbc.ModalFooter(
                                            dbc.Button(
                                                "Close", id="close-folder-popup", className="ms-auto", n_clicks=0
                                            )
                                        ),
                                    ],
                                    id="acquisition-folder-popup",
                                    is_open=False,
                                ),
                            ])
                        ], style={'width': '35rem'}, color='dark', outline=True),

                        html.Br(),
                    ]),
                    
                    #html.Div(className='one column', children=[]),

                    html.Div(className='seven columns', children=[

                        dbc.Card([
                            dbc.CardHeader('Camera View'),
                            dbc.CardBody([

                                html.Div(children=[
                                    html.Div(children=[
                                        html.Br(),
                                    ], style={'width': '24%', 'display': 'table-cell'}),

                                    html.Div(children=[
                                        html.Br(),
                                    ], style={'width': '40%', 'display': 'table-cell'}),
                                    html.Div(children=[
                                        html.Label('Camera streaming mode')
                                    ], style={'width': '36%', 'display': 'table-cell'})
                                ], style={'width': '100%', 'display': 'table'}),

                                html.Div(children=[
                                    html.Div(children=[
                                        html.Button('Snap', id='test-frame-button')
                                    ], style={'width': '10%', 'display': 'table-cell'}),

                                    html.Div(children=[
                                        html.Button('Start/Stop Stream', id='camera-live-stream'),
                                    ], style={'width': '40%', 'display': 'table-cell'}),
                                    html.Div(children=[
                                        daq.ToggleSwitch(
                                            id='camera-streaming-mode',
                                            value=False,
                                            label=['Browser', 'Desktop'])
                                    ], style={'width': '50%', 'display': 'table-cell'})
                                ], style={'width': '100%', 'display': 'table'}),

                                html.Br(),

                                html.Div(children=[], id='camera-state-live-view'),
                                html.Div(children=[], id='camera-state-snapshot'),

                                dcc.Tabs(
                                    id='image-capture-tabs',
                                    value='still-tab',
                                    children=[
                                        dcc.Tab(label='Still Image', value='still-tab', style=tab_style, selected_style=tab_selected_style_main, children=[
                                            html.Div(id='still-image', children=[])
                                        ]),
                                        dcc.Tab(label='Live Stream', value='stream-tab', style=tab_style, selected_style=tab_selected_style_main, children=[
                                            html.Br(),
                                            html.Img(src="/video_feed")
                                        ])
                                    ]
                                ),
                                html.Div(id='image-capture-tab-state-still', children=[]),
                                html.Div(id='image-capture-tab-state-stream', children=[])
                            ])
                        ], style={'width': '80rem'}, color='dark', outline=True),

                        html.Br(),

                        dbc.Card([
                            dbc.CardHeader('XYZ View'),
                            dbc.CardBody([
                                html.Div(children=[
                                    html.Div(children=[
                                        html.Div(children=[
                                            html.Div(children=[
                                                html.Label('Activate graph')
                                            ], style={'width': '50%', 'display': 'table-cell'}),

                                            html.Div(children=[
                                                daq.BooleanSwitch(
                                                    id='activate-graph-switch',
                                                    on=False)
                                            ], style={'width': '50%', 'display': 'table-cell'})
                                        ], style={'width': '100%', 'display': 'table'}),

                                        html.Div(children=[
                                            html.Div(children=[
                                                html.Label('Dimensions')
                                            ], style={'width': '50%', 'display': 'table-cell'}),

                                            html.Div(children=[
                                                daq.ToggleSwitch(
                                                    id='dimensions-switch',
                                                    value=False,
                                                    label=['2D', '3D'])
                                            ], style={'width': '50%', 'display': 'table-cell'})
                                        ], style={'width': '100%', 'display': 'table'}),
                                    ], style={'width': '45%', 'display': 'table-cell'}),
                                    html.Div(children=[], style={'width': '10%', 'display': 'table-cell'}),
                                    html.Div(children=[
                                        html.Div(children=[
                                            html.Div(children=[
                                                html.Button('Generate xy', id='generate-xy-button', disabled=True)
                                            ], style={'width': '40%', 'display': 'table-cell'}),
                                            html.Div(children=[
                                                dcc.Dropdown(
                                                    id='plate-size',
                                                    placeholder='Please select a plate size...',
                                                    options=[
                                                        dict(label='24 wells', value=24),
                                                        dict(label='48 wells', value=48),
                                                        dict(label='96 wells', value=96),
                                                        dict(label='384 wells', value=384)],
                                                    disabled=True)
                                            ], style={'width': '60%', 'display': 'table-cell'})
                                        ], style={'width': '100%', 'display': 'table'}),
                                        html.P('Note that you need position A1 to generate positions.'),
                                    ], style={'width': '45%', 'display': 'table-cell'}),
                                ], style={'width': '100%', 'display': 'table'}),

                                html.Div(id='generate-xy-callback'),
                                html.Div(id='load-xy-callback'),

                                html.Div(id='coord-graph-div', children=[]),      
                                html.Div(id='graph-xy-move'),
                            ])
                        ], style={'width': '80rem'}, color='dark', outline=True),

                    ]),
                ]),
            ])
        ])
