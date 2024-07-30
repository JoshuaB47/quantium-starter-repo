# eww, got regrets on how I labeled the file
from app import app

# I'm too much of a fool to figure out how to use
# chromedriver/selenium, but it oughta be fine and
# this should work perfectly first try :-)
def test_header_existing(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element_by_id("header", timeout=4)

def test_visualization_existing(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element_by_id("visualization", timeout=4)

def test_region_picker_existing(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element_by_id("region", timeout=4)