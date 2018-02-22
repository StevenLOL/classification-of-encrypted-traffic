import time
from random import randint
from selenium import webdriver

def expand_shadow_element(browser, element):
  shadow_root = browser.execute_script('return arguments[0].shadowRoot', element)
  return shadow_root

def enable_flash(browser, page):
    browser.get("chrome://settings/content/flash")
    time.sleep(2)
    settings = browser.find_elements_by_tag_name("settings-ui")[0]
    shadow_settings = expand_shadow_element(browser, settings)
    settings_main = shadow_settings.find_elements_by_css_selector("settings-main")[0]
    shadow_settings_main = expand_shadow_element(browser, settings_main)
    settings_basic_page = shadow_settings_main.find_elements_by_css_selector("settings-basic-page")[0]
    shadow_settings_basic_page = expand_shadow_element(browser, settings_basic_page)
    advancedPage = shadow_settings_basic_page.find_elements_by_css_selector("div[id='advancedPage']")[0]
    settingsSection = advancedPage.find_elements_by_css_selector("settings-section[section='privacy']")[0]
    settings_privacy_page = settingsSection.find_elements_by_css_selector("settings-privacy-page")[0]
    shadow_settings_privacy_page = expand_shadow_element(browser, settings_privacy_page)
    settings_subpage = shadow_settings_privacy_page.find_elements_by_css_selector("settings-subpage")[0]
    category_setting_exceptions = settings_subpage.find_elements_by_css_selector("category-setting-exceptions")[0]
    shadow_category_setting_exceptions = expand_shadow_element(browser, category_setting_exceptions)
    site_list = shadow_category_setting_exceptions.find_elements_by_css_selector("site-list[category-header='Tillad']")[
        0]
    shadow_site_list = expand_shadow_element(browser, site_list)
    addSite = shadow_site_list.find_element_by_id('addSite')
    addSite.click()
    dialog = shadow_site_list.find_elements_by_css_selector("add-site-dialog")[0]
    shadow_dialog = expand_shadow_element(browser, dialog)
    dialog_window = shadow_dialog.find_element_by_id("dialog")
    input_box = dialog_window.find_element_by_id("site")
    input_box.send_keys(page)  # INSERT EXCEPTION HERE
    add_button = dialog_window.find_element_by_id("add")
    add_button.click()


def login(browser, username, password):
    browser.get("https://dk.hbonordic.com/sign-in")
    # LOGIN
    time.sleep(3)
    emailField = browser.find_element_by_id("email")
    passwordField = browser.find_element_by_css_selector("input[data-automation='sign-in-password-input-input']")
    emailField.send_keys(username)
    passwordField.send_keys(password)

    submit = browser.find_element_by_css_selector("button[data-automation='sign-in-submit-button']")

    submit.click()

    time.sleep(3)

    browser.get("https://dk.hbonordic.com/home")
    time.sleep(3)

def streamVideo(browser, duration, username, password):
    enable_flash(browser, page="https://dk.hbonordic.com:443")
    login(browser, username, password)
    videos = browser.find_elements_by_css_selector("a[data-automation='play-button']")
    video = videos[randint(0, len(videos))]
    videoURL = video.get_attribute("href")
    browser.get(videoURL)
    time.sleep(duration)