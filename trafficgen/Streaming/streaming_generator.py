import sys
sys.path.insert(0, "/home/mclrn/dlproject/")
import datetime
from threading import Thread
from selenium import webdriver
from slackclient import SlackClient
import traceback
import os
from selenium.webdriver.support.ui import WebDriverWait


# import trafficgen.Streaming.win_capture as cap
# import trafficgen.Streaming.streaming_types as stream

import unix_capture as cap
import streaming_types as stream
from constants import SLACK_TOKEN

def notifySlack(message):
    sc = SlackClient(SLACK_TOKEN)
    try:
        sc.api_call("chat.postMessage", channel="#server", text=message)
    except:
        sc.api_call("chat.postMessage", channel="#server", text="Could not send stacktrace")


def generate_streaming(duration, dir, total_iterations, chrome_options=None):
    iterations = 0
    while iterations < total_iterations:
        print("Iteration:", iterations)
        if iterations % 25 == 0:
            notifySlack("Starting iteration: " + str(iterations))
        browsers, capture_thread, file, streaming_threads, = [], [], [], []
        file =''
        try:
            if iterations % 2 == 0:
                browsers, capture_thread, file, streaming_threads = generate_threaded_streaming(stream.Youtube, "youtube", dir, duration, chrome_options, num_threads=10)
            else:
                browsers, capture_thread, file, streaming_threads = generate_threaded_streaming(stream.Twitch, "twitch", dir, duration, chrome_options, num_threads=10)
        except Exception as ex:
            notifySlack("Something went wrong when setting up the threads \n %s" % traceback.format_exc())

        try:
            capture_thread.start()
            for thread in streaming_threads:
                # Start streaming threads
                thread.start()
            print("streaming started")
            capture_thread.join() # Stream until the capture thread joins
            print("capture done - thread has joined")
            # for browser in browsers:
            # #    clear_cache(browser)
            #     browser.close()

        except Exception as e:
            notifySlack("Something went wrong %s" % traceback.format_exc())
            # Wait for capture thread
            capture_thread.join()
            # Do a cleanup since somthing went wrong
            cap.cleanup(file)
            # for browser in browsers:
            #     browser.close()
        try:
            for browser in browsers:
                browser.quit()
        except Exception as e:
            notifySlack("Something went wrong %s" % traceback.format_exc())
            os.system("killall chrome")
            os.system("killall chromedriver")
        iterations += 1


def generate_threaded_streaming(obj: stream.Streaming, stream_name, dir, duration, chrome_options=None, num_threads=5):
    #### STREAMING ####
    # Create filename
    now = datetime.datetime.now()
    file = dir + "/%s-%.2d%.2d_%.2d%.2d%.2d.pcap" % (stream_name, now.day, now.month, now.hour, now.minute, now.second)
    # Instantiate thread
    capture_thread = Thread(target=cap.captureTraffic, args=(1, duration, dir, file))
    # Create five threads for streaming
    streaming_threads = []
    browsers = []
    for i in range(num_threads):
        browser = webdriver.Chrome(options=chrome_options)
        browser.implicitly_wait(10)
        browsers.append(browser)
        t = Thread(target=obj.stream_video, args=(obj, browser))
        streaming_threads.append(t)

    return browsers, capture_thread, file, streaming_threads


def get_clear_browsing_button(driver):
    """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page. /deep/ to go past shadow roots"""
    return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


def clear_cache(driver, timeout=60):
    """Clear the cookies and cache for the ChromeDriver instance."""
    # navigate to the settings page
    driver.get('chrome://settings/clearBrowserData')

    # wait for the button to appear
    wait = WebDriverWait(driver, timeout)
    wait.until(get_clear_browsing_button)

    # click the button to clear the cache
    get_clear_browsing_button(driver).click()

    # wait for the button to be gone before returning
    wait.until_not(get_clear_browsing_button)


if __name__ == "__main__":
    #netflixuser = os.environ["netflixuser"]
    #netflixpassword = os.environ["netflixpassword"]
    #hbouser = os.environ["hbouser"]
    #hbopassword = os.environ["hbopassword"]
    # slack_token = os.environ['slack_token']
    # Specify duration in seconds
    duration = 60 * 1
    total_iterations = 1000
    save_dir = '/home/mclrn/Data'
    chrome_profile_dir = "/home/mclrn/.config/google-chrome/"
    options = webdriver.ChromeOptions()
    #options.add_argument('user-data-dir=' + chrome_profile_dir)
    options.add_argument("--enable-quic")
    # options.add_argument('headless')
    generate_streaming(duration, save_dir, total_iterations, options)
    print("something")