# dashboard/dashboard.py

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from django.conf import settings
from dashboard.views import task_completion_rate, overdue_tasks, task_priority_distribution, tasks_created_vs_completed, productivity_trends, category_wise_task_completion

# Define your Dash app
app = DjangoDash(name='dashboard', serve_locally=False)  # serve_locally=False for production

# Define the layout of your Dash app
app.layout = html.Div(
    [
        html.H1('Your Dashboard Title'),
        
        # Example of a bar chart
        dcc.Graph(id='task-completion-bar'),
        
        # Example of a pie chart
        dcc.Graph(id='task-priority-pie'),

        # Example of a line chart
        dcc.Graph(id='productivity-trends-line'),
        
        # Example of a table
        html.H2('Category-wise Task Completion'),
        html.Table(id='category-task-completion-table'),
        
        # Example of refreshing data button
        html.Button('Refresh Data', id='refresh-button'),
        
        # Example of a hidden div to store data
        html.Div(id='hidden-div', style={'display': 'none'})
    ]
)

# Example callback for task completion bar chart
@app.callback(
    Output('task-completion-bar', 'figure'),
    [Input('refresh-button', 'n_clicks')]  # Example input (could be a button to refresh data)
)
def update_task_completion_bar(n_clicks):
    # Fetch data using your existing Django views functions
    completion_rate_response = task_completion_rate(None)  # Pass None for request parameter

    # Construct a bar chart
    figure = {
        'data': [
            {'x': ['Completion Rate'], 'y': [completion_rate_response.data['completion_rate']], 'type': 'bar', 'name': 'Completion Rate'}
        ],
        'layout': {
            'title': 'Task Completion Rate',
            'yaxis': {'title': 'Percentage'}
        }
    }

    return figure

# Example callback for task priority pie chart
@app.callback(
    Output('task-priority-pie', 'figure'),
    [Input('refresh-button', 'n_clicks')]  # Example input (could be a button to refresh data)
)
def update_task_priority_pie(n_clicks):
    # Fetch data using your existing Django views functions
    priority_distribution_response = task_priority_distribution(None)

    # Construct a pie chart
    labels = [item['priority'] for item in priority_distribution_response.data]
    values = [item['count'] for item in priority_distribution_response.data]

    figure = {
        'data': [
            go.Pie(labels=labels, values=values, hole=0.3)
        ],
        'layout': {
            'title': 'Task Priority Distribution'
        }
    }

    return figure

# Example callback for productivity trends line chart
@app.callback(
    Output('productivity-trends-line', 'figure'),
    [Input('refresh-button', 'n_clicks')]  # Example input (could be a button to refresh data)
)
def update_productivity_trends_line(n_clicks):
    # Fetch data using your existing Django views functions
    productivity_trends_response = productivity_trends(None)

    # Construct a line chart
    x_data = [item['created_at__date'] for item in productivity_trends_response.data]
    y_data = [item['count'] for item in productivity_trends_response.data]

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

# Example callback for category-wise task completion table
@app.callback(
    Output('category-task-completion-table', 'children'),
    [Input('refresh-button', 'n_clicks')]  # Example input (could be a button to refresh data)
)
def update_category_task_completion_table(n_clicks):
    # Fetch data using your existing Django views functions
    category_wise_task_completion_response = category_wise_task_completion(None)

    # Construct an HTML table
    table_rows = []
    for item in category_wise_task_completion_response.data:
        table_rows.append(
            html.Tr([
                html.Td(item['category']),
                html.Td(f"{item['completed_tasks']} / {item['total_tasks']}"),
                html.Td(f"{item['completion_rate']:.2f}%")
            ])
        )

    return table_rows