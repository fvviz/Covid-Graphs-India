from matplotlib.animation import writers

api_url = "https://api.covid19india.org/csv/latest/states.csv"

month_dict = {
    "01": "Jan",
    "02": "Feb",
    "03": "March",
    "04": "Apr",
    "05": "May",
    "06": "Jun",
    "07": "Jul",
    "08": "Aug",
    "09": "Sept",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec"

}


def save_video(animation, name):
    writer_ = writers["ffmpeg"]
    writer = writer_(fps=15, metadata={'artist': 'Me'}, bitrate=1800)
    animation.save(name, writer)