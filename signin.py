import unittest
from random import randint
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from mimesis import Person
person = Person('en')

class SignIn(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_Sign_in(self):    \

        driver = self.driver
        driver.get('http://automationpractice.com/index.php')

        sign_button = driver.find_element_by_class_name('login')
        sign_button.click()

        assert 'Login' in driver.title

# invalid email
        enter_email = driver.find_element_by_name('email_create')
        enter_email.send_keys('email@')
        create_button = driver.find_element_by_id('SubmitCreate')
        create_button.click()
        assert driver.find_element_by_id('create_account_error').is_enabled()

# valid email
        enter_email.clear()
        random_email = person.email()
        enter_email.send_keys(random_email)
        create_button.click()
        time.sleep(5)

        assert '#account-creation' in driver.current_url

# try to register without required fields
        register_button = driver.find_element_by_id('submitAccount')
        register_button.click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')
        assert alert

        driver.find_element_by_id('id_gender1').click()

# sequential data entry
# make sure that corresponding errors disappear

        first_name = driver.find_element_by_id('customer_firstname')
        first_name.clear()
        first = person.name()
        first_name.send_keys(first)
        register_button = driver.find_element_by_id('submitAccount')
        register_button.click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')

        assert 'firstname' not in alert.text

        last_name = driver.find_element_by_id('customer_lastname')
        last_name.clear()
        last = person.surname()
        last_name.send_keys(last)
        register_button = driver.find_element_by_id('submitAccount')
        register_button.click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')

        assert 'lastname' not in alert.text

        email = driver.find_element_by_id('email')
        assert email.get_attribute('value') == random_email

        password = driver.find_element_by_id('passwd')
        password.clear()
        password.send_keys(person.password(4))
        register_button = driver.find_element_by_id('submitAccount')
        register_button.click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')

        assert 'passwd is invalid' in alert.text

        password = driver.find_element_by_id('passwd')
        password.clear()
        password.send_keys(person.password(5))
        register_button = driver.find_element_by_id('submitAccount')
        register_button.click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')

        assert 'passwd' not in alert.text

        days_dropdown = driver.find_element_by_id('days')
        Select(days_dropdown).select_by_index(randint(0,30))
        register_button = driver.find_element_by_id('submitAccount')
        register_button.click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')

        assert 'Invalid date of birth' in alert.text


        month_dropdown = driver.find_element_by_id('months')
        Select(month_dropdown).select_by_index(randint(0,11))
        register_button = driver.find_element_by_id('submitAccount')
        register_button.click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')

        assert 'Invalid date of birth' in alert.text

        years_dropdown = driver.find_element_by_id('years')
        Select(years_dropdown).select_by_value(str(randint(1900, 2019)))
        register_button = driver.find_element_by_id('submitAccount')
        register_button.click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')

        assert 'Invalid date of birth' not in alert.text


        address_first_name = driver.find_element_by_id('firstname')
        assert address_first_name.get_attribute('value') == first

        address_last_name = driver.find_element_by_id('lastname')
        assert address_last_name.get_attribute('value') == last

        address = driver.find_element_by_id('address1')
        address.send_keys(person.)

        city = driver.find_element_by_id('city')
        city.send_keys('Samara')

        states_dropdown = driver.find_element_by_id('id_state')
        state = Select(states_dropdown)
        state.select_by_index(randint(0,52))

        zip = driver.find_element_by_id('postcode')
        zip.send_keys(randint(11111, 99999))

        mobile = driver.find_element_by_id('phone_mobile')
        mobile.send_keys('79876543210')

        address_alias = driver.find_element_by_id('alias')
        address_alias.clear()
        address_alias.send_keys('Default')

        register_button = driver.find_element_by_id('submitAccount')
        register_button.click()

        time.sleep(3)

        assert 'controller=my-account' in driver.current_url


    def tearDown(self):
        self.driver.close()
