from matplotlib.animation import writers, PillowWriter

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
state_options = ['Andaman and Nicobar Islands',
          'Andhra Pradesh',
          'Arunachal Pradesh',
          'Assam',
          'Bihar',
          'Chandigarh',
          'Chhattisgarh',
          'Dadra and Nagar Haveli and Daman and Diu',
          'Delhi',
          'Goa',
          'Gujarat',
          'Haryana',
          'Himachal Pradesh',
          'All states',
          'Jammu and Kashmir',
          'Jharkhand',
          'Karnataka',
          'Kerala',
          'Ladakh',
          'Lakshadweep',
          'Madhya Pradesh',
          'Maharashtra',
          'Manipur',
          'Meghalaya',
          'Mizoram',
          'Nagaland',
          'Odisha',
          'Puducherry',
          'Punjab',
          'Rajasthan',
          'Sikkim',
          'State Unassigned',
          'Tamil Nadu',
          'Telangana',
          'Tripura',
          'Uttar Pradesh',
          'Uttarakhand',
          'West Bengal']

year_options = ["2021", "2020", "2020-21"]



def save_graph(animation, name):
    if name.endswith(".mp4"):
        writer_ = writers["ffmpeg"]
        writer = writer_(fps=15, metadata={'artist': 'Me'}, bitrate=1800)
        animation.save(name, writer)
    elif name.endswith(".gif"):
        writergif = PillowWriter(fps=10)
        animation.save(name, writer=writergif)