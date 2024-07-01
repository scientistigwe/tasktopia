import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
import requests

# Initialize DjangoDash app with serve_locally=True for local development
app = DjangoDash(name='TasktopiaDashboard', serve_locally=True)

# Define the layout of the dashboard using Dash components
app.layout = html.Div(
    [
        html.H1('Tasktopia | Analytics & Insights'),
        
        # Placeholder graphs that will be populated dynamically
        dcc.Graph(id='task-completion-bar'),
        dcc.Graph(id='task-priority-pie'),
        dcc.Graph(id='productivity-trends-line'),
        
        html.H2('Category-wise Task Completion'),
        
        # Table to display category-wise task completion
        html.Table(id='category-task-completion-table', 
                   children=[
                       html.Tr([
                           html.Th("Category"), 
                           html.Th("Completed Tasks"), 
                           html.Th("Total Tasks"), 
                           html.Th("Completion Rate (%)")
                       ])
                   ]),
        
        # Button to trigger data refresh
        html.Button('Refresh Data', id='refresh-button'),
        
        # Hidden div to store data from callbacks
        html.Div(id='hidden-div', style={'display': 'none'})
    ]
)

# Callback to update the Task Completion Rate bar chart
@app.callback(
    Output('task-completion-bar', 'figure'),
    [Input('refresh-button', 'n_clicks')]
)
def update_task_completion_bar(n_clicks):
    response = requests.get('http://127.0.0.1:8000/dashboard/task-completion-rate/')
    data = response.json()

    figure = {
        'data': [
            {'x': ['Completion Rate'], 'y': [data['completion_rate']], 'type': 'bar', 'name': 'Completion Rate'}
        ],
        'layout': {
            'title': 'Task Completion Rate',
            'yaxis': {'title': 'Percentage'}
        }
    }

    return figure

# Callback to update the Task Priority Distribution pie chart
@app.callback(
    Output('task-priority-pie', 'figure'),
    [Input('refresh-button', 'n_clicks')]
)
def update_task_priority_pie(n_clicks):
    response = requests.get('http://127.0.0.1:8000/dashboard/task-priority-distribution/')
    data = response.json()

    labels = [item['priority'] for item in data]
    values = [item['count'] for item in data]

    figure = {
        'data': [
            go.Pie(labels=labels, values=values, hole=0.3)
        ],
        'layout': {
            'title': 'Task Priority Distribution'
        }
    }

    return figure

# Callback to update the Productivity Trends line chart
@app.callback(
    Output('productivity-trends-line', 'figure'),
    [Input('refresh-button', 'n_clicks')]
)
def update_productivity_trends_line(n_clicks):
    response = requests.get('http://127.0.0.1:8000/dashboard/productivity-trends/')
    data = response.json()

    x_data = [item['created_at__date'] for item in data]
    y_data = [item['count'] for item in data]

    figure = {
        'data': [
            go.Scatter(x=x_data, y=y_data, mode='lines+markers', name='Productivity Trends')
        ],
        'layout': {
            'title': 'Productivity Trends',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Tasks Created'}
        }
    }

    return figure

# Callback to update the Category-wise Task Completion table
@app.callback(
    Output('category-task-completion-table', 'children'),
    [Input('refresh-button', 'n_clicks')]
)
def update_category_task_completion_table(n_clicks):
    response = requests.get('http://127.0.0.1:8000/dashboard/category-wise-task-completion/')
    data = response.json()

    table_rows = [
        html.Tr([
            html.Td(item['category']),
            html.Td(item['completed_tasks']),
            html.Td(item['total_tasks']),
            html.Td(f"{item['completion_rate']:.2f}%")
        ]) for item in data
    ]

    return table_rows
