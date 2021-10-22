from flask import Flask, render_template

app_start = Flask(__name__)


@app_start.route('/plot/')
def plot():
    # Imports the required libraries : pandas_datareader, datetime, and bokeh
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure
    from bokeh.embed import components
    from bokeh.resources import CDN  # Content Delivery Network

    # Reading the data
    data_frame = data.DataReader(
        name='GOOG',
        data_source='yahoo',
        start=datetime.datetime(2021, 3, 1),
        end=datetime.datetime(2021, 7, 1)
    )

    # Function to check increase and decrease in stocks, between Open_at and Close_at
    def increase_decrease(close_at, open_at):
        if close_at > open_at:
            value = 'Increase'
        elif close_at < open_at:
            value = 'Decrease'
        else:
            value = 'Equal'
        return value

    # Adding Columns to the data_frame
    data_frame['Status'] = [increase_decrease(close_at, open_at) for close_at, open_at in
                            zip(data_frame.Close, data_frame.Open)]
    data_frame['Middle'] = (data_frame.Open + data_frame.Close) / 2
    data_frame['Height'] = abs(data_frame.Close - data_frame.Open)

    # Plotting the plots on the graphs + Styling the graphs
    fig = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode='scale_width')
    fig.title.text = 'Google Stocks Candlestick Graph'
    fig.grid.grid_line_alpha = 0.3

    # Calculating hours
    twelve_hours = 12 * 60 * 60 * 1000  # hours * minute * second * mili-second

    # For rectangle figure in the graphs
    fig.rect(
        data_frame.index[data_frame.Status == 'Increase'],
        data_frame.Middle[data_frame.Status == 'Increase'],
        twelve_hours,
        data_frame.Height[data_frame.Status == 'Increase'],
        fill_color='#90EE90',
        line_color='#000000'
    )

    fig.rect(
        data_frame.index[data_frame.Status == 'Decrease'],
        data_frame.Middle[data_frame.Status == 'Decrease'],
        twelve_hours,
        data_frame.Height[data_frame.Status == 'Decrease'],
        fill_color='#B22222',
        line_color='#000000'
    )

    # Line Segments for the graph
    fig.segment(data_frame.index, data_frame.High, data_frame.index, data_frame.Low, color='#000000')

    script1, div1 = components(fig)
    cdn_js = CDN.js_files[0]

    return render_template('plot.html',
                           script1=script1,
                           div1=div1,
                           cdn_js=cdn_js)


@app_start.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app_start.run(debug=True)
