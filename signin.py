import unittest
from random import randint
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from mimesis import Person
from mimesis import Address
from mimesis import Text
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

en = Address('en')
person = Person('en')
text = Text('en')

class SignIn(unittest.TestCase):


    @classmethod
    def setUpClass(inst):
        inst.driver = webdriver.Chrome()
        inst.driver.get('http://automationpractice.com/index.php')

    @classmethod
    def tearDownClass(inst):

        inst.driver.quit()

    def test_a_Enter_email(self):

        driver = self.driver
        driver.find_element_by_class_name('login').click()
        assert 'Login' in self.driver.title

# invalid email
        driver.find_element_by_name('email_create').send_keys('email@')
        driver.find_element_by_id('SubmitCreate').click()
        assert driver.find_element_by_id('create_account_error').is_enabled()

# valid email
        enter_email = driver.find_element_by_name('email_create')
        enter_email.clear()
        global random_email
        random_email = person.email()
        enter_email.send_keys(random_email)
        driver.find_element_by_id('SubmitCreate').click()
        transition = WebDriverWait(self.driver, 10).until(EC.url_contains('#account-creation'))
        assert transition

# try to register without required fields

    def test_b_Required_fields(self):

        driver = self.driver
        driver.find_element_by_id('submitAccount').click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')
        assert alert

# sequential tests all required fields
# make sure that corresponding errors disappear

    def test_c_First_Name(self):

        driver = self.driver
        driver.find_element_by_id('id_gender1').click()
        first_name = driver.find_element_by_id('customer_firstname')
        first_name.clear()
        global first
        first = person.name()
        first_name.send_keys(first)
        driver.find_element_by_id('submitAccount').click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')
        assert 'firstname' not in alert.text

    def test_d_Last_Name(self):

        driver = self.driver
        last_name = driver.find_element_by_id('customer_lastname')
        last_name.clear()
        global last
        last = person.surname()
        last_name.send_keys(last)
        driver.find_element_by_id('submitAccount').click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')
        assert 'lastname' not in alert.text

    def test_e_Prefilled_Email(self):

        driver = self.driver
        email = driver.find_element_by_id('email')
        assert email.get_attribute('value') == random_email

    def test_f_Prefilled_Address_Name(self):

        driver = self.driver
        address_first_name = driver.find_element_by_id('firstname')
        assert address_first_name.get_attribute('value') == first

        address_last_name = driver.find_element_by_id('lastname')
        assert address_last_name.get_attribute('value') == last

    def test_g_Address(self):

        driver = self.driver
        driver.find_element_by_id('address1').send_keys(en.address())
        driver.find_element_by_id('submitAccount').click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')
        assert 'address1 is required' not in alert.text

    def test_h_City_and_State(self):

        driver = self.driver
        driver.find_element_by_id('city').send_keys(en.city())
        driver.find_element_by_id('submitAccount').click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')
        assert 'city' not in alert.text

        states_dropdown = driver.find_element_by_id('id_state')
        state = Select(states_dropdown)
        state.select_by_index(randint(0,52))
        driver.find_element_by_id('submitAccount').click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')
        assert 'State' not in alert.text

    def test_i_ZIP(self):

        driver = self.driver
        driver.find_element_by_id('postcode').send_keys(en.zip_code())
        driver.find_element_by_id('submitAccount').click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')
        assert 'Zip/Postal' not in alert.text

    def test_j_Mobile_Phone(self):

        driver = self.driver
        driver.find_element_by_id('phone_mobile').send_keys(person.telephone())
        driver.find_element_by_id('submitAccount').click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')
        assert 'phone number' not in alert.text

    def test_k_Change_Alias(self):
        driver = self.driver
        address_alias = driver.find_element_by_id('alias')
        address_alias.clear()
        address_alias.send_keys('Default')

# fill optional fields

    def test_l_Day_of_Birth(self):

        driver = self.driver
        days_dropdown = driver.find_element_by_id('days')
        Select(days_dropdown).select_by_index(randint(0,29))
        driver.find_element_by_id('submitAccount').click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')
        assert 'Invalid date of birth' in alert.text

        month_dropdown = driver.find_element_by_id('months')
        Select(month_dropdown).select_by_index(randint(0,11))
        driver.find_element_by_id('submitAccount').click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')
        assert 'Invalid date of birth' in alert.text

        years_dropdown = driver.find_element_by_id('years')
        Select(years_dropdown).select_by_value(str(randint(1900, 2019)))
        driver.find_element_by_id('submitAccount').click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')
        assert 'Invalid date of birth' not in alert.text

    def test_m_Other_fields(self):
        driver = self.driver
        driver.find_element_by_id('other').send_keys(text.text(quantity=3))
        driver.find_element_by_id('phone').send_keys(person.telephone())
        # need to come up with some assert

    def test_n_Password_And_Finish_Account_Creation(self):

        driver = self.driver
        password = driver.find_element_by_id('passwd')
        password.clear()
        password.send_keys(person.password(4))
        driver.find_element_by_id('submitAccount').click()
        alert = driver.find_element_by_css_selector('.alert.alert-danger')
        assert 'passwd is invalid' in alert.text

        password = driver.find_element_by_id('passwd')
        password.clear()
        password.send_keys(person.password(5))
        driver.find_element_by_id('submitAccount').click()

        WebDriverWait(driver, 10).until(EC.url_contains('controller=my-account'))

        assert driver.title == 'My account - My Store'


if __name__ == "__main__":
    unittest.main()
